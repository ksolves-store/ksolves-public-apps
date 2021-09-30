odoo.define('ks_calculator.ks_calculator.js', function(require) {
    "use strict";

    var config = require('web.config');
    var core = require('web.core');
    var session = require('web.session');
    var time = require('web.time');
    var utils = require('web.utils');
    var Widget = require('web.Widget');
    var SystrayMenu = require('web.SystrayMenu');

    var _t = core._t;
    var QWeb = core.qweb

    var KsCalculatorItem = Widget.extend({
        template: 'ks_calculator_item',
        events: {
            "click .ks_equal_values": "_ksFetchValues",
            "click .ks_get_values": "_ksGetValues",
            "click .ks_clear_screen": "_ksClearScreen",
            'keypress input': '_onKeypress',
            'click .ks_dark_mode': '_ksDarkMode'

        },
        _ksFetchValues: function(event) {
            if ($(event.target).is('i') === false) {
                this.$el.find('#edu').val(this.$el.find('#edu').val() + event.currentTarget.value)
                event.stopPropagation();
            }
        },
        //function for evaluation
        _ksGetValues: function _ksGetValues() {
            let x = $('#edu').val()
            let y = eval(x)
            $('#edu').val(y)
        },
         //function for key press
        _onKeypress: function(e) {
            var keycode = e.which || e.keyCode;
            var valueEntered = String.fromCharCode(keycode);
            if (e.which == 13) {
                let x = $('#edu').val()
                let y = eval(x)
                $('#edu').val(y)
            }

        },
        // function for clear the screen
        _ksClearScreen: function _ksClearScreen() {
            $('#edu').val('')
        },
        // function for  dark mode
        _ksDarkMode: function(event) {
            event.stopPropagation();
            $("#dark_mode").toggleClass("dark-mode");
            $('.ks_calculator_dropdown').addClass('show');
        },

    });

    SystrayMenu.Items.push(KsCalculatorItem);

    return {
        KsCalculatorItem: KsCalculatorItem,
    };

});
