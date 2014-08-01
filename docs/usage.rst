.. _usage:

Usage
=====

Integrating `agon_ratings` into your project is just a matter of using a couple of
template tags and wiring up a bit of javascript. The rating form is intended
to function via AJAX and as such returns JSON.

Firstly, add load the template tags for `agon_ratings`::

    {% load agon_ratings_tags %}


Then, if you want to display an overall rating average for an object you can set
a context variable and display it::

    {% overall_rating obj as the_overall_rating %}

    <div class="overall_rating">{{ the_overall_rating }}</div>


Likewise for displaying a user's rating::

    {% user_rating request.user obj as the_user_rating %}

    <div class="user_rating">{{ the_user_rating }}</div>


If you want to add an AJAX form for allowing a user to set a rating, add the
following in the appropriate location on your page::

    <div id="user_rating"></div>


And then add this near the end of your HTML `<body>` to emit some Javascript
libraries and hook up the ratings UI::

    {% user_rating_js request.user obj %}


If you want to do any rating based on categories of ratings for an object or
objects then you do the same as above but just use an optional argument on
the tags::

    {% overall_rating obj "accuracy" as category_rating %}

    <div class="overall_rating category-accuracy">
        {{ category_rating }}
    </div>

and::

    {% user_rating request.user obj "accuracy" as category_rating %}

    <div class="user_rating category-accuracy">
        {{ category_rating }}
    </div>

and::

    <div id="user_rating" class="category-accuracy"></div>

    {% user_rating_js request.user obj "accuracy" %}
