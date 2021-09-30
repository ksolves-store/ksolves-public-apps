odoo.define('ks_edit_log_message.ks_custom_mail.js', function (require) {
'use strict';

 const components = {
        Message : require('mail/static/src/components/message/message.js'),

    };
    const { patch } = require('web.utils');
    const { addLink, htmlToTextContentInline, parseAndTransform, timeFromNow } = require('mail.utils');
    patch(components.Message,'ks_edit_log_message/static/src/js/ks_custom_mail.js', {

     async _ksOnClickEditMsg(ev) {
           await this.rpc({
                            model: 'mail.message',
                            method: "ks_get_action",
                            args: ['',this.message.id],
                        }).then((result) => {

                            this.trigger("do-action", {
                            action: result,

                            options: {
                                on_close: () => {
                                    window.location.reload();
                                },
                            }});
                        });
        },

     async _ksOnClickDeleteMsg(ev){
              if (confirm('Are you sure you want to delete this message')) {
                  await this.env.services.rpc({
                  model: 'mail.message',
                  method: 'unlink',
                  args: [[this.message.id]],
                });
                    window.location.reload();
                } else {

                }
        },
    });

});










