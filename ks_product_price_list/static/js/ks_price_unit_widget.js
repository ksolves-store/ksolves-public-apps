odoo.define('ks_product_price_list.ks_price_unit_widget', function(require) {
    'use strict';

    var core = require('web.core');
    var QWeb = core.qweb;
    var widget_registry = require('web.widget_registry');
    var QtyAtDateWidget = require('sale_stock.QtyAtDateWidget');
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
            this.$el.on('show.bs.popover', function() {
                 $('.popover').popover('hide');

            })
            $(window).click(function(e) {
                if ($(e.target).parents().length>1 && !$(e.target).hasClass('ks_graph')){
                    $('.popover').popover('hide');
                }

        });
        },

        _ksOnClickButton: function() {
            this.$el.find('.graph').prop('special_click', true);
        },
    });
    QtyAtDateWidget.include({
        _setPopOver() {
            this._super.apply(this, arguments);
            this.$el.on('show.bs.popover', function() {
                $('.popover').popover('hide')
            })
            $(window).click(function(e) {
                if ($(e.target).parents().length>1 && !$(e.target).hasClass('ks_graph')){
                    $('.popover').popover('hide');
                }
        });
        }

    })
    widget_registry.add('ks_price_unit_widget', KsCustomDateWidget);

    return KsCustomDateWidget

})
