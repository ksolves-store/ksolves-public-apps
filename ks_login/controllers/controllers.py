# -*- coding: utf-8 -*-
# from odoo import http


from datetime import datetime

import werkzeug
import odoo
from odoo import http, _
from werkzeug.urls import iri_to_uri
from odoo.addons.auth_signup.controllers.main import AuthSignupHome
from odoo.exceptions import UserError
from openerp.http import request
from odoo.addons.auth_signup.models.res_users import SignupError
import logging
db_monodb = http.db_monodb
# override
def _get_login_redirect_url(uid, redirect=None):
    """ Decide if user requires a specific post-login redirect, e.g. for 2FA, or if they are
    fully logged and can proceed to the requested URL
    """
    if request.session.uid:  # fully logged
        return redirect or '/web'

    # partial session (MFA)
    url = request.env(user=uid)['res.users'].browse(uid)._mfa_url()
    if not redirect:
        return url

    parsed = werkzeug.urls.url_parse(url)
    qs = parsed.decode_query()
    qs['redirect'] = redirect
    return parsed.replace(query=werkzeug.urls.url_encode(qs)).to_url()


# override
def abort_and_redirect(url):
    r = request.httprequest
    response = werkzeug.utils.redirect(url, 302)
    response = r.app.get_response(r, response, explicit_session=False)
    werkzeug.exceptions.abort(response)


def ensure_db(redirect='/web/database/selector'):
    db = request.params.get('db') and request.params.get('db').strip()

    # Ensure db is legit
    if db and db not in http.db_filter([db]):
        db = None

    if db and not request.session.db:
        # User asked a specific database on a new session.
        # That mean the nodb router has been used to find the route
        # Depending on installed module in the database, the rendering of the page
        # may depend on data injected by the database route dispatcher.
        # Thus, we redirect the user to the same page but with the session cookie set.
        # This will force using the database route dispatcher...
        r = request.httprequest
        url_redirect = werkzeug.urls.url_parse(r.base_url)
        if r.query_string:
            # in P3, request.query_string is bytes, the rest is text, can't mix them
            query_string = iri_to_uri(r.query_string)
            url_redirect = url_redirect.replace(query=query_string)
        request.session.db = db
        abort_and_redirect(url_redirect)

    # if db not provided, use the session one
    if not db and request.session.db and http.db_filter([request.session.db]):
        db = request.session.db

    # if no database provided and no database in session, use monodb
    if not db:
        db = db_monodb(request.httprequest)

    # if no db can be found til here, send to the database selector
    # the database selector will redirect to database manager if needed
    if not db:
        werkzeug.exceptions.abort(werkzeug.utils.redirect(redirect, 303))

    # always switch the session to the computed db
    if db != request.session.db:
        request.session.logout()
        abort_and_redirect(request.httprequest.url)

    request.session.db = db

class KsSignupHomeExt(AuthSignupHome):

    @http.route('/web/login', type='http', auth="none")
    def web_login(self, redirect=None, **kw):
        # ensure_db()
        request.params['login_success'] = False
        if request.httprequest.method == 'GET' and redirect and request.session.uid:
            return http.redirect_with_hash(redirect)

        if not request.uid:
            request.uid = odoo.SUPERUSER_ID

        values = request.params.copy()
        try:
            values['databases'] = http.db_list()
        except odoo.exceptions.AccessDenied:
            values['databases'] = None

        if request.httprequest.method == 'POST':
            old_uid = request.uid
            try:
                uid = request.session.authenticate(request.session.db, request.params['login'],
                                                   request.params['password'])
                request.params['login_success'] = True
                return http.redirect_with_hash(self._login_redirect(uid, redirect=redirect))
            except odoo.exceptions.AccessDenied as e:
                request.uid = old_uid
                if e.args == odoo.exceptions.AccessDenied().args:
                    values['error'] = _("Wrong login/password")
                else:
                    values['error'] = e.args[0]
        else:
            if 'error' in request.params and request.params.get('error') == 'access':
                values['error'] = _('Only employees can access this database. Please contact the administrator.')

        if 'login' not in values and request.session.get('auth_login'):
            values['login'] = request.session.get('auth_login')

        if not odoo.tools.config['list_db']:
            values['disable_database_manager'] = True

        ks_active_website = request.env['ks_login.setting.conf'].search([('ks_is_active','=',True)])
        ks_image_url =""
        if ks_active_website:
            # ks_active_website.ks_update_content()
            ks_get_image_id = str(ks_active_website.id)
            ks_base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
            ks_image_url = ks_image_url + ks_base_url + '/web/image?' + 'model=ks_login.setting.conf&id=' + ks_get_image_id + '&field=ks_backgroud_img'
        values['background_src'] = ks_image_url or ''
        values['str_custome'] = "Hello"

        if ks_active_website.ks_checkbox == 'none':
            response = request.render('web.login', values)
        else:
            response = request.render('ks_login.ks_signin_template', values)
        response.headers['X-Frame-Options'] = 'DENY'
        return response
        # else:
        #     return  request.render('ks_login.ks_signin_template', values)
        # response.headers['X-Frame-Options'] = 'DENY'
        return response


class ksAuthSignupHome(AuthSignupHome):

    @http.route('/web/signup', type='http', auth='public', website=True, sitemap=False)
    def web_auth_signup(self, *args, **kw):
        ks_image_url = ""
        qcontext = self.get_auth_signup_qcontext()

        if not qcontext.get('token') and not qcontext.get('signup_enabled'):
            raise werkzeug.exceptions.NotFound()

        if 'error' not in qcontext and request.httprequest.method == 'POST':
            try:
                self.do_signup(qcontext)
                # Send an account creation confirmation email
                if qcontext.get('token'):
                    User = request.env['res.users']
                    user_sudo = User.sudo().search(
                        User._get_login_domain(qcontext.get('login')), order=User._get_login_order(), limit=1
                    )
                    template = request.env.ref('auth_signup.mail_template_user_signup_account_created',
                                               raise_if_not_found=False)
                    if user_sudo and template:
                        template.sudo().send_mail(user_sudo.id, force_send=True)
                return self.web_login(*args, **kw)
            except UserError as e:
                qcontext['error'] = e.args[0]
            except (SignupError, AssertionError) as e:
                if request.env["res.users"].sudo().search([("login", "=", qcontext.get("login"))]):
                    qcontext["error"] = _("Another user is already registered using this email address.")
                else:
                    _logger.error("%s", e)
                    qcontext['error'] = _("Could not create a new account.")
        try:
            qcontext['background_src'] =''
            ks_active_website = request.env['ks_login.setting.conf'].search([('ks_is_active', '=', True)])
            if ks_active_website:
                ks_active_website.ks_update_template_fields()
                ks_get_image_id = str(ks_active_website.id)
                ks_base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
                ks_image_url = ks_image_url + ks_base_url + '/web/image?' + 'model=ks_login.setting.conf&id=' + ks_get_image_id + '&field=ks_backgroud_img'
                qcontext['background_src'] = ks_image_url or ''
                if qcontext['background_src'] == 'none':
                    response = request.render('ks_login.signup_temp', qcontext)
                else:
                    response = request.render('ks_login.signup_temp', qcontext)
                response.headers['X-Frame-Options'] = 'DENY'
                return response
            else:
                response = request.render('auth_signup.signup', qcontext)
                response.headers['X-Frame-Options'] = 'DENY'
                return response
        except:
            response = request.render('auth_signup.signup', qcontext)
            response.headers['X-Frame-Options'] = 'DENY'
            return response
