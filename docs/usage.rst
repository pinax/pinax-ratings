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


If you want to add a form for allowing a user to set a rating, add the
following in the appropriate location on your page::

    {% user_rating_widget request.user obj %}


And then add these tags in the head of your page, or at the bottom of the HTML 
`<body>` element to emit the JavaScript and CSS files required. Developers are
encouraged to use the provided CSS file as an example and develop their own.::

    {% user_rating_js %}
    {% user_rating_css %}


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

    {% user_rating_widget request.user obj "accuracy" %}
