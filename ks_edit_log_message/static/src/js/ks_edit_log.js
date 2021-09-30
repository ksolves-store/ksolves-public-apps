odoo.define('ks_edit_log_messag.editable.js', function (require) {
'use strict';

 const components = {

        Message : require('mail/static/src/models/message/message.js'),

    };
    const {
    registerClassPatchModel,
    registerFieldPatchModel,
    registerInstancePatchModel,
} = require('mail/static/src/model/model_core.js');
const { attr } = require('mail/static/src/model/model_field.js');

registerClassPatchModel('mail.message', 'ks_edit_log_message/static/src/js/editable.js', {

    convertData(data) {
        const data2 = this._super(data);
        if ('is_edit' in data) {
            data2.is_edit = data.is_edit;
        }
        if ('is_delete' in data) {
            data2.is_delete = data.is_delete;
        }
        if ('current_date' in data) {
            data2.current_date = data.current_date;
        }
        if ('current_user' in data) {
            data2.current_user = data.current_user;
        }
        return data2;
    },
});

registerFieldPatchModel('mail.message', 'ks_edit_log_message/static/src/js/editable.js', {
     is_edit: attr({
            default: false,
        }),
      is_delete: attr({
            default: false,
        }),
      current_date: attr({
            default: '',
        }),
      current_user: attr({
            default: '',
        }),
});
});