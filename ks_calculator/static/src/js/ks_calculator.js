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
            'click .ks_dark_mode': '_ksDarkMode',
            'hide.bs.dropdown': "ksHideDropDown",

        },

        ksHideDropDown : function(event){
            if (!event.clickEvent) {
                return true;
            }
            var target = $(event.clickEvent.target);
            return !(target.hasClass('ks_calculator') || target.parents('.ks_calculator').length);
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
                if(x.length > 1){
                    if(x.match(/[a-z]/i)){
                        alert('You can only use number to compute')
                        return false
                    }
                    if(x.includes(" ")){
                        x= x.split(" ").join("")
                    }
//                    if(x[0] ==='0' && x.includes('.') ){
////                        var int_part = Math.trunc(x); // returns 3
////                         x = Number((x-int_part).toFixed(9))
//
//                    }
                    var ks_lst = ['+','-','/','*',]
                    var ks_alpha = ['!','@','#','$','%','^','&','_','{','}','[',']',':',';','>','<',',','?',"'",'"','=','|']
                    if(ks_lst.includes(x[x.length - 1]) || ks_lst.includes(x[0]) ){
                        return false
                    }
//                    if(x[0] ==='0' ){
//                        var int_part = Math.trunc(x); // returns 3
//                         x = Number((x-int_part).toFixed(2))
//                    }
                    for(var n = 0; n < ks_alpha.length; n++){
                        if (ks_alpha.includes(x[n])){
                            return false
                        }
                    }
                    let y = eval(x)
                    $('#edu').val(y)
                }else if(x.length===1){
                    return false
                }
        },
         //function for key press
        _onKeypress: function(e) {
            var keycode = e.which || e.keyCode;
            var valueEntered = String.fromCharCode(keycode);
            if (e.which == 13) {
                let x = $('#edu').val()
                if(x.length > 1){
                    if(x.match(/[a-z]/i)){
                        alert('You can only use number to compute')
                        return false
                    }
                    if(x.includes(" ")){
                        x= x.split(" ").join("")
                    }

                    var ks_lst = ['+','-','/','*',]
                    var ks_alpha = ['!','@','#','$','%','^','&','_','{','}','[',']',':',';','>','<',',','?',"'",'"','=','|']
                    if(ks_lst.includes(x[x.length - 1]) || ks_lst.includes(x[0]) ){
                        return false
                    }
//                    var ks_val_lngt = x.length
//                    if(x[0]==='0'){
//                    var temp = ks_val_lngt
//                    for(var ks = 0; ks <=temp-2; ks++){
//                        if(x[ks] ==='0'){
//                            x = x.replace(x[ks], '')
//                            temp = x.length
//                        }
//                    }
//                    }

                    for(var n = 0; n < ks_alpha.length; n++){
                        if (ks_alpha.includes(x[n])){
                            return false
                        }
                    }
                    let y = eval(x)
                    $('#edu').val(y)
                }else if(x.length===1){
                    return false
                }


            }

        },
        // function for clear the screen
        _ksClearScreen: function _ksClearScreen() {
            $('#edu').val('')
        },
        // function for  dark mode
        _ksDarkMode: function(event) {
            $("#dark_mode").toggleClass("dark-mode");
        },

    });

    SystrayMenu.Items.push(KsCalculatorItem);

    return {
        KsCalculatorItem: KsCalculatorItem,
    };

});
