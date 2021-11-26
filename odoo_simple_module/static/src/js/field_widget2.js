odoo.define('my_field_widget2', function (require) {
    "use strict";
    var AbstractField = require('web.AbstractField');
    var fieldRegistry = require('web.field_registry');
    var colorField = AbstractField.extend({
        className: 'o_string_colorpicker',
        tagName: 'span',
        supportedFieldTypes: ['string'],
        events: {
            'click .o_color_string_pill': 'clickPill',
            'blur .o_color_string_pill': 'blurPill',
        },
        init: function () {
            this._super.apply(this, arguments);
        },
        _renderEdit: function () {
            this.$el.empty();
            var className = "o_color_string_pill";
            this.$el.append($('<input>', {
                'id': 'exact_color',
                'class': className,
                'type': 'color',
                'style': 'position:relative;top:5px;width:65px;height:35px;',
                'value': this.value,
                'data-val': this.value,
            }));
            
        },
        _renderReadonly: function () {
            var className = "o_color_string_pill readonly";
            this.$el.append($('<div>', {
                'id': 'exact_color',
                'class': className,
                'type': 'color',
                'style': 'position:relative;top:5px;width:65px;height:35px;border:5px ridge silver;border-radius:4px;background-color:'+this.value+';',
                'data-val': this.value,
            }));
        },
        clickPill: function (ev) {
            var $target = $(ev.currentTarget);
            var data = $target.data();
            var exact_color = document.getElementById("exact_color");
            console.log(exact_color.value);
            if (exact_color.value != undefined) {
                this._setValue(exact_color.value);
            }
        },
        blurPill: function (ev) {
            var $target = $(ev.currentTarget);
            var data = $target.data();
            var exact_color = document.getElementById("exact_color");
            console.log("color: " + exact_color.value);
            if (exact_color.value != undefined) {
                this._setValue(exact_color.value);
            }
        }
    }); // closing AbstractField

    fieldRegistry.add('int_color2', colorField);
    return {
        colorField: colorField,
    };
}); // closing 'my_field_widget' namespace