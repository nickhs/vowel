/* global Backbone */

window.Vowel = {};

window.Vowel.Loading = Backbone.View.extend({
    className: 'vowel-loading-small vowel-loading',

    initialize: function(cont) {
        this.cont = cont;
    },

    render: function() {
        $(this.cont).append(this.el);
        this.startAnimation();
    },

    startAnimation: function() {
        if (this.animation) return;

        this.$el.toggleClass('vowel-loading-small');

        this.animation = setInterval(function() {
            this.$el.toggleClass('vowel-loading-small');
        }.bind(this), 1000);

    },

    stopAnimation: function() {
        if (!this.animation) return;
        clearInterval(this.animation);
    }
});
