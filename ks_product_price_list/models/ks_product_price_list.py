from odoo import fields, api, models, _
import logging
_logger = logging.getLogger(__name__)
from odoo.tools.misc import get_lang


class ks_product_template_inherit(models.Model):
    _inherit = 'product.template'

    ks_sale_pricelists = fields.One2many('product.pricelist', compute='_compute_get_active_pricelist',string='Sale Pricelist')

    def _compute_get_active_pricelist(self):
        pricelist_ids = self.env['product.pricelist'].search([('display_price_on_product','=',True)])
        self.ks_sale_pricelists = pricelist_ids


class ks_product_product_inherit(models.Model):
    _inherit = 'product.product'

    ks_sale_pricelists = fields.One2many('product.pricelist', compute='_compute_get_active_pricelist',string='Sale Pricelist')

    def _compute_get_active_pricelist(self):
        pricelist_ids = self.env['product.pricelist'].search([('display_price_on_product','=',True)])
        self.ks_sale_pricelists = pricelist_ids

class ks_product_pricelist_inherit(models.Model):

    _inherit = "product.pricelist"

    display_price_on_product = fields.Boolean(string="Display Pricelist Price On Products", default=True)
    product_price = fields.Char(string="Price", compute="_compute_get_product_price")

    def _compute_get_product_price(self):
        for ks_product_pricelist in self:
            if ks_product_pricelist._context.get('product_templ_id',False):
                ks_variant_id = self.env['product.template'].browse(ks_product_pricelist._context.get('product_templ_id')).product_variant_ids[0]
                result =  ks_product_pricelist.price_rule_get(ks_variant_id.id, 1.0)
                ks_product_pricelist.product_price = str(ks_product_pricelist.currency_id.round(result[ks_product_pricelist.id][0]))
                if(ks_product_pricelist.currency_id.position != 'after'):
                    ks_product_pricelist.product_price = ks_product_pricelist.currency_id.symbol + ' ' + ks_product_pricelist.product_price
                else:
                    ks_product_pricelist.product_price = ks_product_pricelist.product_price + ' ' + ks_product_pricelist.currency_id.symbol
            elif ks_product_pricelist._context.get('product_id',False):
                product_id = ks_product_pricelist._context.get('product_id')
                result =  ks_product_pricelist.price_rule_get(product_id, 1.0)
                ks_product_pricelist.product_price = str(ks_product_pricelist.currency_id.round(result[ks_product_pricelist.id][0]))
                if(ks_product_pricelist.currency_id.position != 'after'):
                    ks_product_pricelist.product_price = ks_product_pricelist.currency_id.symbol + ' ' + ks_product_pricelist.product_price
                else:
                    ks_product_pricelist.product_price = ks_product_pricelist.product_price + ' ' + ks_product_pricelist.currency_id.symbol
            else:
                ks_product_pricelist.product_price = 0



class ks_sale_order_line_inherit(models.Model):
    _inherit = "sale.order.line"

    ks_pricelist_id = fields.Char(
        string='Pricelist_id',
        related='order_id.pricelist_id.name')

    ks_discount_price = fields.Float(
        string='Discount price',)

    ks_actual_price = fields.Float(
        string='Ks actual price',
        related='product_id.list_price')

    @api.onchange('product_id')
    def product_id_change(self):
        if not self.product_id:
            return
        valid_values = self.product_id.product_tmpl_id.valid_product_template_attribute_line_ids.product_template_value_ids
        # remove the is_custom values that don't belong to this template
        for pacv in self.product_custom_attribute_value_ids:
            if pacv.custom_product_template_attribute_value_id not in valid_values:
                self.product_custom_attribute_value_ids -= pacv

        # remove the no_variant attributes that don't belong to this template
        for ptav in self.product_no_variant_attribute_value_ids:
            if ptav._origin not in valid_values:
                self.product_no_variant_attribute_value_ids -= ptav

        vals = {}
        if not self.product_uom or (self.product_id.uom_id.id != self.product_uom.id):
            vals['product_uom'] = self.product_id.uom_id
            vals['product_uom_qty'] = self.product_uom_qty or 1.0

        product = self.product_id.with_context(
            lang=get_lang(self.env, self.order_id.partner_id.lang).code,
            partner=self.order_id.partner_id,
            quantity=vals.get('product_uom_qty') or self.product_uom_qty,
            date=self.order_id.date_order,
            pricelist=self.order_id.pricelist_id.id,
            uom=self.product_uom.id
        )
        price = 0.0
        for pricelist in self.product_id.ks_sale_pricelists:
            if pricelist.name == self.ks_pricelist_id:
                result =  pricelist._compute_price_rule_multi([(product, self.product_uom_qty, self.order_id.partner_id)])[product.id][pricelist.id][0]
                price = result if result != '0' else self.product_id.list_price
                break;
        vals.update(name=self.get_sale_order_line_multiline_description_sale(product),ks_pricelist_id=self.order_id.pricelist_id.name,ks_discount_price=price,ks_actual_price=self.product_id.list_price)

        self._compute_tax_id()

        if self.order_id.pricelist_id and self.order_id.partner_id:
            vals['price_unit'] = self.env['account.tax']._fix_tax_included_price_company(
                self._get_display_price(product), product.taxes_id, self.tax_id, self.company_id)
        self.update(vals)

        title = False
        message = False
        result = {}
        warning = {}
        if product.sale_line_warn != 'no-message':
            title = _("Warning for %s", product.name)
            message = product.sale_line_warn_msg
            warning['title'] = title
            warning['message'] = message
            result = {'warning': warning}
            if product.sale_line_warn == 'block':
                self.product_id = False
        return result


class ks_sale_order_inherit(models.Model):
    _inherit = "sale.order"

    def update_prices(self):
        self.ensure_one()
        res= super(ks_sale_order_inherit, self).update_prices()
        for line in self.order_line:
            line.ks_discount_price = self.order_line.price_unit
        return res

