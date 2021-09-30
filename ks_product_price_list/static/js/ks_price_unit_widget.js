odoo.define('ks_product_price_list.ks_price_unit_widget', function(require) {
    'use strict';

    var core = require('web.core');
    var QWeb = core.qweb;
    var widget_registry = require('web.widget_registry');
    var Widget = require('web.Widget');
    var _t = core._t;

    var KsCustomDateWidget = Widget.extend({
        template: 'ks_product_pricelist_widget',
        events: _.extend({}, Widget.prototype.events, {
            'click .ks_graph': '_ksOnClickButton',
        }),
        init: function(parent, params) {
            var res = this._super.apply(this, arguments);
            this.data = params.data;
            this.unit_price = this.data.ks_discount_price;
            return res
        },
        start: function() {
            var res = this._super.apply(this, arguments);
            this._setPopOver();
            return res
        },

        _getContent() {
            const $content = $(QWeb.render('QtyDetailPopOver_1', {
                data: this.data,
            }));
            return $content;
        },
        _setPopOver() {
            const $content = this._getContent();
            if (!$content || !this.unit_price || this.unit_price < 1) {
                return;
            }
            const options = {
                content: $content,
                html: true,
                placement: 'left',
                title: _t('Availability'),
                trigger: 'focus',
                delay: {
                    'show': 0,
                    'hide': 100
                },
            };
            this.$el.popover(options);
        },

        _ksOnClickButton: function() {
            this.$el.find('.graph').prop('special_click', true);
        },
    });
    widget_registry.add('ks_price_unit_widget', KsCustomDateWidget);

    return KsCustomDateWidget

})
