from odoo import models, fields


class KsResCompany(models.Model):
    _inherit = 'res.company'

    ks_latitude = fields.Char('Latitude', required=True)
    ks_longitude = fields.Char('Longitude', required=True)
    ks_zoom = fields.Integer('Zoom Level', required=True, help="Zoom level is integer value between 10-18", default=15)
    ks_token = fields.Char('Access Token', required=True,
                           help="Need Access Token? visit- https://account.mapbox.com/auth/signin")