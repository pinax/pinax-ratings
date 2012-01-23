!function($) {

	var AgonRating = function(form, options) {
		options = this.options = $.extend({}, agon.defaults, options);
		this.$form = $(form);
		this.$buttons = this.$form.find('button');

		this.currentRating = options.currentRating || 0;

		var self = this;

		this.$buttons.each(function(i, button) {
			$(button).hover(function(event) {
				self.showRating(i);
                self.hovering = true;
			}, function(event) {
                self.hovering = false;
				self.showRating(self.currentRating);
			});
		});

		this.$buttons.on('click', function(event) {
			event.preventDefault();

			var $button = $(this);
			var $form = self.$form;
			var rating = parseInt($button.attr('value'));

            var oldRating = self.currentRating;

			var data = $form.serializeArray();
			data.push({name: $button.attr('name'), value: rating});

			$form.addClass(options.processingClass)

            self.currentRating = rating;
			self.showRating(rating);

            $.ajax({
                url: $form.attr('action'),
                type: "POST",
                data: data,

                statusCode: {
                    200: function(data, textStatus, jqXHR) {
						self.currentRating = rating;
						self.showRating(rating);
                        self.$form.triggerHandler('agonratingschange', data);
                    }
                },

                error: function() {
                    self.currentRating = oldRating;
                    self.showRating(oldRating);
                },

				complete: function() {
					$form.removeClass(options.processingClass);
				}

            });

		});
	};

    /**
     * Options for this instance.
     *
     * See:
     * <agon.defaults>
     */
    AgonRating.prototype.options = null;

    /**
     * The form this instance is connected to
     */
    AgonRating.prototype.$form = false;

    /**
     * Buttons on the form
     */
    AgonRating.prototype.$buttons = false;

    /**
     * The current rating of this instance.
     */
    AgonRating.prototype.currentRating = false;

    /**
     * If we are currently hovering over a button. Stying works slightly differently when we are hovering.
     */
    AgonRating.prototype.hovering = false;

	AgonRating.prototype.showRating = function(rating) {
        if (this.hovering) return;

		var classes = this.options.buttonClasses;

        this.$form[rating ? 'removeClass' : 'addClass'](this.options.unratedClass);

		this.$buttons.each(function(i, button) {
			var $button = $(button),
				buttonRating = $button.attr('value');

			$button.removeClass(classes.join(' '));
			$button.addClass(classes[buttonRating < rating ? 0 : buttonRating == rating ? 1 : 2]);
		});
	};

	var agon = $.fn.agon = function(options) {
		$(this).each(function(i, el) {
			$(el).data("agon-ratings", new AgonRating(el, options));
		});
	};

	agon.defaults = {
		processingClass: 'agon-ratings-processing',
        unratedClass: 'agon-ratings-unrated',
		buttonClasses: ['agon-ratings-less', 'agon-ratings-current', 'agon-ratings-more']
	};

}( window.jQuery || window.ender );
