from odoo import models, fields
from odoo.exceptions import ValidationError

class KsResCompany(models.Model):
    _inherit = 'res.company'

    ks_latitude = fields.Char('Latitude', required=True)
    ks_longitude = fields.Char('Longitude', required=True)
    ks_zoom = fields.Integer('Zoom Level', required=True, help="Zoom level is integer value between 10-18",default=15)

