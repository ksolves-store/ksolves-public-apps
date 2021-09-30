

from odoo import models, fields, api


class KsResUsersInherit(models.Model):
    _inherit = 'res.users'

    ks_hide_edit_button = fields.Many2many(
        comodel_name='ir.model',
        string='Hide Edit Button',relation="res_users_edit_rel")

    ks_hide_create_button = fields.Many2many(
        comodel_name='ir.model',
        string='Hide Create Button',relation="res_users_create_rel")

    def ks_get_all_models(self):
        edit_list=[]
        create_list=[]
        for model in self.env.user.ks_hide_edit_button:
            edit_list.append(model.model)
        for model in self.env.user.ks_hide_create_button:
            create_list.append(model.model)
        return {
            'edit_list':edit_list,
            'create_list':create_list
        }