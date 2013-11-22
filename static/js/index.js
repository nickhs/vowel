/* global Backbone, Vowel */

var SubmitLink = Backbone.View.extend({
    initialize: function(el) {
        this.setElement(el);
        this.form = {};
        this.form.data = {};

        this.form.data.csrf_token = el.find('#csrf_token').val();
        this.form.endpoint = el.find('form').attr('action');
        this.form.method = el.find('form').attr('method');
        // this.$el.empty();

        this.input = el.find('form #url');
        el.addClass('js');
        this.input.on('keyup', this.handleKeyPress.bind(this));

        this.input_state = $('<div class="input-status input-status-forward">➡</div>');
        this.input_state_cancel = $('<div class="hidden input-status input-status-cancel">x</div>');
        this.input.after(this.input_state);
        this.input.before(this.input_state_cancel);

        this.input_state.on('click', this.handleForwardClick.bind(this));
        this.input_state_cancel.on('click', this.handleCancelClick.bind(this));
        this.input.hover(
            this.handleInputHoverIn.bind(this),
            this.handleInputHoverOut.bind(this));
    },

    handleKeyPress: function(event) {
        if (this.$el.hasClass('processing')) return;
        if (event.keyCode == 13) {
            this.handleForwardClick();
        } else if (event.keyCode == 27) {
            this.handleCancelClick();
        }
    },

    handleInputHoverIn: function(event) {
        dbg.log('in', event);
        if (this.$el.hasClass('processing')) return;
        this.input.focus();
    },

    handleInputHoverOut: function(event) {
        dbg.log('out', event);
        if (this.$el.hasClass('processing')) return;
        this.input.blur();
    },

    handleForwardClick: function(event) {
        dbg.log('click', event);
        var value = this.input.val();
        if (value === '') return;
        if (this.$el.hasClass('processing')) return;

        if (!this.form.data.url) {
            this.form.data.url = value;
            this.input.val('');
            this.input.attr('placeholder', 'Enter Email');
            this.input_state_cancel.removeClass('hidden');
        } else {
            this.form.data.friend = value;
            this.$el.addClass('processing');
            this.loading = new Vowel.Loading(this.$el.find('form'));
            this.loading.render();

            $.ajax({
                type: this.form.method,
                url: this.form.endpoint,
                data: this.form.data,
                success: this.requestSuccess.bind(this),
                error: this.requestError.bind(this),
                dataType: 'json'
            });
        }
    },

    handleCancelClick: function(event) {
        if (this.$el.hasClass('processing')) return;
        this.form.data = {};
        this.input.val('');
        this.input.attr('placeholder', 'Paste URL');
        this.input_state_cancel.addClass('hidden');
    },

    requestSuccess: function(jqxhr) {
        console.log('success', jqxhr);
        this.requestCleanup();
    },

    requestError: function(jqxhr) {
        console.log('failure', jqxhr);
        this.requestCleanup();
    },

    requestCleanup: function() {
        this.$el.removeClass('processing');
        this.loading.remove();
        this.handleCancelClick();
    }

});

$(document).ready(function() {
    Vowel.linkSubmit = new SubmitLink($('.link-submit'));
    dbg.log('linkSubmit', Vowel.linkSubmit);
});
