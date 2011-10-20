.. _usage:

Usage
=====

Integrating `agon_ratings` into your project is just a matter of using a couple of
template tags and wiring up a bit of javascript. The rating form is intended
to function via AJAX and as such returns JSON.

Firstly, you will want to add the following blocks in your templates where
you want to expose the rating form::

    {% load agon_ratings_tags %}
    
    {% overall_rating for some_object as the_overall_rating %}
    
    <div id="user_rating"></div>
    
    <div class="overall_rating">{{ the_overall_rating }}</div>
    
    {% user_rating_js request.user some_object %}
