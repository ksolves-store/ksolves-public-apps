odoo.define('ks_hide_button.ks_hide_buttons', function(require) {
    "use strict";

    var AbstractController = require('web.AbstractController');
    var session = require('web.session');

    AbstractController.include({

        willStart: function() {
            var self = this;
            var def = session.user_has_group("ks_hide_buttons.ks_group_hide_edit_button")
            var def2 = session.user_has_group("ks_hide_buttons.ks_group_hide_create_button")
              var models = this._rpc({
                model: 'res.users',
                method: 'ks_get_all_models',
                args: ['']})
            return Promise.all([def,def2,models, this._super.apply(this, arguments)]).then(function(r) {
                self.ks_group_hide_edit_button = r[0];
                self.ks_group_hide_create_button = r[1];
                self.ks_models= r[2];
            });
        },
        is_action_enabled: function(action) {
            if (action == 'edit' && this.ks_models.edit_list.includes(this.modelName)) {
                var flag = false
                if (!this.ks_group_hide_edit_button) {
                    flag = true
                }
                return flag
            } else if (action == 'create' && this.ks_models.create_list.includes(this.modelName)) {
                var flag = false
                if (!this.ks_group_hide_create_button) {
                    flag = true
                }
                return flag
            } else {
                return this._super.apply(this, arguments)
            }
        },
    });
    return AbstractController
});
