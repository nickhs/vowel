/* global Backbone, Vowel */

var SubmitLink = Backbone.View.extend({
    initialize: function(el) {
        this.$el = el;
        this.form = {};

        this.form.csrf_token = el.find('#csrf_token').val();
        this.form.endpoint = el.find('form').attr('action');
        this.form.method = el.find('form').attr('method');
        // this.$el.empty();

        this.input = el.find('form #url');
        el.addClass('js');
        this.togglePasteURL();

        this.input_state = $('<div class="input-status">></div>');
        this.input.after(this.input_state);
        this.input.hover(
            this.handleInputHoverIn.bind(this),
            this.handleInputHoverOut.bind(this));
    },

    togglePasteURL: function() {
        var el = this.input.parent().find('.paste-url');

        if (this.input.val() !== '') {
            el.remove();
            return;
        }

        if (el.length !== 0) {
            el.remove();
        } else {
            el = $('<div class="paste-url">Paste URL</div>');
            this.input.after(el);
        }
    },

    handleInputHoverIn: function(event) {
        dbg.log('in', event);
        this.togglePasteURL();
        this.input.focus();
    },

    handleInputHoverOut: function(event) {
        dbg.log('out', event);
        this.togglePasteURL();
        this.input.blur();
    }
});

$(document).ready(function() {
    return;
    Vowel.linkSubmit = new SubmitLink($('.link-submit'));
    dbg.log('linkSubmit', Vowel.linkSubmit);
});
