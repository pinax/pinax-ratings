.. _usage:

Usage
=====

Integrating `agon_ratings` into your project is just a matter of using a couple of
template tags and wiring up a bit of javascript. The rating form is intended
to function via AJAX and as such returns JSON.

Firstly, you will want to add the following blocks in your templates where
you want to expose the rating form::

    {% load agon_ratings_tags %}
    
    <div class="rating">
        {% user_rate_form some_object %}
        <div id="user_rating"></div>
        <div class="overall_rating">
            {% overall_rating for some_object as the_overall_rating %}
            <span class="rating-{{ the_overall_rating }}">{{ the_overall_rating }}</span>
        </div>
    </div>


Wiring up the interface is up to you the site developer. One approach that seems to
work nicely is integrating with _raty:Raty: like so::

    <script type="text/javascript" src="{{ STATIC_URL }}js/jquery.raty.js"></script>
    <script type="text/javascript">
        {% user_rating for request.user and post as the_user_rating %}
        $(function () {
            $('.rating form').ajaxForm(function(data) {
                var over_r = parseFloat(data["overall_rating"]);
                var over_class = parseInt(over_r * 10);
                $(".rating .overall_rating span").attr("class", "rating-" + over_class).text(over_r);
            });
            $("#user_rating").raty({
                start: {{ the_user_rating }},
                click: function(score, evt) {
                    if (score == null) {
                        $(".rating form input[name=rating]").val(0);
                    } else {
                        $(".rating form input[name=rating]").val(score);
                    }
                    $(".rating form").submit();
                },
                cancel: true,
                path: "{{ STATIC_URL }}images/"
            });
        });
        </script>
     </script>


_raty:Raty: http://www.wbotelhos.com/raty/
