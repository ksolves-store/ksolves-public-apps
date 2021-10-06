from odoo import http
from odoo.http import request


class KsMapCod(http.Controller):

    @http.route('/ks_get_map_cod', type='json', auth='public', website=True)
    def ks_map_details(self, **kwargs):
        ks_co_ordinate = request.env.company
        cod = dict()
        if ks_co_ordinate and ks_co_ordinate.ks_longitude and ks_co_ordinate.ks_latitude:
            cod = {'lon': ks_co_ordinate.ks_longitude,
                   'lan': ks_co_ordinate.ks_latitude,
                   'zoom': ks_co_ordinate.ks_zoom,
                   'token': ks_co_ordinate.ks_token}
        return cod
