# -*- coding: utf-8 -*-

from odoo import models, fields, api
import pytz

class ks_mail_extension(models.Model):
    _inherit = "mail.message"

    ks_last_edited_by = fields.Many2one('res.users', string="Last Edited By",readonly=True)
    ks_last_edited_date = fields.Datetime('Last Edited Date', readonly=True)

    def ks_get_action(self,msgid):
        action = self.env['ir.actions.act_window']._for_xml_id('ks_edit_log_message''.ks_action_mail_message_extension_new')
        ctx = dict(self.env.context)
        ctx.update({
            'ks_is_hide': True,
        })
        action['context'] = ctx
        action['res_id'] = msgid
        ctx.update({
            'mail_id':self.id
        })
        self.env.context = ctx
        return action

    def ks_get_time_acc_to_timezone(self,datetime):
        if datetime:
            date = datetime
            utc_date = date.replace(tzinfo=pytz.UTC)
            return utc_date.astimezone(
                pytz.timezone(self.env.user.tz if self.env.user.tz else 'America/Los_Angeles')).strftime('%Y-%m-%d %H:%M:%S')
        else:
            return ''
    def write(self, vals):
        vals.update({
            'ks_last_edited_by': self.env.user.id,
            'ks_last_edited_date': fields.Datetime.now()
        })
        res = super(ks_mail_extension, self).write(vals)
        return res

    def message_format(self):
        vals_list = super(ks_mail_extension, self).message_format()
        for val in vals_list:
            rec= self.browse(val['id'])
            val.update({
                'is_edit' : rec.env.user.has_group('ks_edit_log_message.ks_group_adminstraton_edit') or (rec.create_uid.id==self.env.user.id),
                'is_delete' : rec.env.user.has_group('ks_edit_log_message.ks_group_adminstraton_delete')or (rec.create_uid.id==self.env.user.id),
                'current_date':rec.ks_get_time_acc_to_timezone(rec.ks_last_edited_date),
                'current_user': rec.ks_last_edited_by.name if rec.ks_last_edited_by.name and len(rec.ks_last_edited_by.name) else '',
            })
        return vals_list
