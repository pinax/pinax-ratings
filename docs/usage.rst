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
        
        <div class="user_rating">
            {% user_rating for request.user and some_object as the_user_rating %}
            <span class="rating-{{ the_user_rating }}">{{ the_user_rating }}</span>
        </div>
        
        <div class="overall_rating">
            {% overall_rating for some_object as the_overall_rating %}
            <span class="rating-{{ the_overall_rating }}">{{ the_overall_rating }}</span>
        </div>
    </div>


And then a bit of jQuery (this assumes use of the jquery.form plugin)::

    $('.rating form').ajaxForm(function(data) {
        var user_r = parseInt(data["user_rating"]);
        var over_r = parseFloat(data["overall_rating"]);
        var over_class = parseInt(over_r * 10);
        var user_class = user_r * 10;
        $(".rating .user_rating span").attr("class", "rating-" + user_class).text(user_r);
        $(".rating .overall_rating span").attr("class", "rating-" + over_class).text(over_r);
    });


Wiring up the interface is up to you the site developer. One approach that seems to
work nicely is integrating with _raty:Raty: like so::

    <div id="user_rating"></div>
    <div id="overall_rating"></div>
    
    <script type="text/javascript" src="jquery.raty.min.js" />
    <script type="text/javascript">
        $("#user_rating").raty({
            start = {{ the_user_rating }},
            click = function(score, evt) {
                $(".rating form input[name]").val(score);
                $(".rating form").submit();
            },
            cancel = true
        })
    </script>


_raty:Raty: http://www.wbotelhos.com/raty/
