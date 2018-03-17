![](http://pinaxproject.com/pinax-design/patches/pinax-ratings.svg)

# Pinax Ratings

[![](https://img.shields.io/pypi/v/pinax-ratings.svg)](https://pypi.python.org/pypi/pinax-ratings/)

[![CircleCi](https://img.shields.io/circleci/project/github/pinax/pinax-ratings.svg)](https://circleci.com/gh/pinax/pinax-ratings)
[![Codecov](https://img.shields.io/codecov/c/github/pinax/pinax-ratings.svg)](https://codecov.io/gh/pinax/pinax-ratings)
[![](https://img.shields.io/github/contributors/pinax/pinax-ratings.svg)](https://github.com/pinax/pinax-ratings/graphs/contributors)
[![](https://img.shields.io/github/issues-pr/pinax/pinax-ratings.svg)](https://github.com/pinax/pinax-ratings/pulls)
[![](https://img.shields.io/github/issues-pr-closed/pinax/pinax-ratings.svg)](https://github.com/pinax/pinax-ratings/pulls?q=is%3Apr+is%3Aclosed)

[![](http://slack.pinaxproject.com/badge.svg)](http://slack.pinaxproject.com/)
[![](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)


## Table of Contents

* [About Pinax](#about-pinax)
* [Overview](#overview)
  * [Supported Django and Python versions](#supported-django-and-python-versions)
* [Documentation](#documentation)
  * [Installation](#installation)
  * [Usage](#usage)
  * [Settings](#settings)
  * [Templates](#templates)
* [Change Log](#change-log)
* [Contribute](#contribute)
* [Code of Conduct](#code-of-conduct)
* [Connect with Pinax](#connect-with-pinax)
* [License](#license)


## About Pinax

Pinax is an open-source platform built on the Django Web Framework. It is an ecosystem of reusable
Django apps, themes, and starter project templates. This collection can be found at http://pinaxproject.com.


## pinax-ratings

### Overview

``pinax-ratings`` is a ratings app for Django.

#### Supported Django and Python versions

Django \ Python | 2.7 | 3.4 | 3.5 | 3.6
--------------- | --- | --- | --- | ---
1.11 |  *  |  *  |  *  |  *  
2.0  |     |  *  |  *  |  *


## Documentation

### Installation

To install pinax-ratings:

```shell
    $ pip install pinax-ratings
```

Add `pinax.ratings` to your ``INSTALLED_APPS`` setting:

```python
    INSTALLED_APPS = [
        # other apps
        "pinax.ratings",
    ]
```

Next, add `pinax.ratings.urls` to your project urlpatterns:

```python
    urlpatterns = [
        # other urls
        url(r"^ratings/", include("pinax.ratings.urls", namespace="pinax_ratings")),
    ]
```

Finally, view the list of [settings](#settings) to modify pinax-ratings's default behavior and make adjustments for your website.

Optionally, if want to use the ratings category feature of `pinax-ratings` then you will need to add the `pinax-RATINGS_CATEGORY_CHOICES` setting in your `settings.py`:

```python
    PINAX_RATINGS_CATEGORY_CHOICES = {
        "app.Model": {
            "exposure": "How good is the exposure?",
            "framing": "How well was the photo framed?",
            "saturation": "How would you rate the saturation?"
        },
        "app.Model2": {
            "grammar": "Good grammar?",
            "complete": "Is the story complete?",
            "compelling": "Is the article compelling?"
        }
    }
```

### Usage

Integrating `pinax-ratings` into your project is just a matter of using a couple of
template tags and wiring up a bit of javascript. The rating form is intended
to function via AJAX and as such returns JSON.

Firstly, add load the template tags for `pinax-ratings`:

```django
    {% load pinax_ratings_tags %}
```

Then, if you want to display an overall rating average for an object you can set
a context variable and display it:

```django
    {% overall_rating obj as the_overall_rating %}

    <div class="overall_rating">{{ the_overall_rating }}</div>
```

Likewise for displaying a user's rating:

```django
    {% user_rating request.user obj as the_user_rating %}

    <div class="user_rating">{{ the_user_rating }}</div>
```

If you want to add an AJAX form for allowing a user to set a rating, add the
following in the appropriate location on your page:

```django
    <div id="user_rating"></div>
```

And then add this near the end of your HTML `<body>` to emit some Javascript
libraries and hook up the ratings UI:

```django
    {% user_rating_js request.user obj %}
```

If you want to do any rating based on categories of ratings for an object or
objects then you do the same as above but just use an optional argument on
the tags:

```django
    {% overall_rating obj "accuracy" as category_rating %}

    <div class="overall_rating category-accuracy">
        {{ category_rating }}
    </div>
```

and

```django
    {% user_rating request.user obj "accuracy" as category_rating %}

    <div class="user_rating category-accuracy">
        {{ category_rating }}
    </div>
```

and

```django
    <div id="user_rating" class="category-accuracy"></div>

    {% user_rating_js request.user obj "accuracy" %}
```

### Settings

#### PINAX_RATINGS_NUM_OF_RATINGS

Default: 5

Defines the number of different rating choices there will be.

#### PINAX_RATINGS_CATEGORY_CHOICES

Default: `None`

Defines a dictionary of choices for different models for the application of
ratings along different dimensions rather than just a single rating for an
object.

It should follow the format of a dictionary of dictionaries. For example, think of
the context of a website that allowed ratings of photographs and articles
published by other users:

```python
    PINAX_RATINGS_CATEGORY_CHOICES = {
        "app.Model": {
            "exposure": "How good is the exposure?",
            "framing": "How well was the photo framed?",
            "saturation": "How would you rate the saturation?"
        },
        "app.Model2": {
            "grammar": "Good grammar?",
            "complete": "Is the story complete?",
            "compelling": "Is the article compelling?"
        }
    }
```
    
### Templates

`pinax-ratings` comes with two minimal template snippets rendered
by template tags for displaying the rating form.

Templates are found in "pinax/ratings/" subdirectory for your project.

#### `_rating.html`

#### `_script.html`

This is a snippet that renders the bundled Javascript and a simple AJAX posting and
hooking up of a rating UI. This is optional and overridable by the site developer.


## Change Log

### 3.0.2

* Add templatetag tests, model tests

### 3.0.1

* Import reverse from django.urls

### 3.0.0

* Add Django 2.0 compatibility testing
* Drop Django 1.8, 1.9, 1.10, and Python 3.3 support
* Add URL namespacing (BI: urlname "pinax_ratings_rate" is now "pinax_ratings:rate")
* Move documentation into README and standardize layout
* Convert CI and coverage to CircleCi and CodeCov
* Add PyPi-compatible long description

### 2.0.0

* converted category on ratings.Rating and `ratings.OverallRating` models to be
  a CharField that is the actual category label rather than a runtime generated
  ID. _upgrading will require you manually update the database values_

### 1.0.0

* @@@ write change log

### 0.3

* renamed from agon_ratings to pinax-ratings

### 0.2.1

* added ability in overall_rating template tag to omit the category
  label and get an average rating without concern for category
  averages.
* added ability to get average rating over all categories for a
  particular user and particular object.

### 0.2

* added support for ratings to have categories instead of just a single
  rating for an object
* dropped natural language of template tags

#### Migrations

Added a category model and updated the unique index on both models:

    ALTER TABLE "agon_ratings_overallrating" ADD COLUMN "category" int;
    ALTER TABLE "agon_ratings_rating" ADD COLUMN "category" int;
    CREATE UNIQUE INDEX "agon_ratings_overallrating_unq_object_id_content_type_id_category_idx"
        ON "agon_ratings_overallrating" (object_id, content_type_id, category);
    CREATE UNIQUE INDEX "agon_ratings_rating_unq_object_id_content_type_id_user_id_category_idx"
        ON "agon_ratings_rating" (object_id, content_type_id, user_id, category);
    ALTER TABLE "agon_ratings_rating" DROP CONSTRAINT
        IF EXISTS "agon_ratings_rating_object_id_content_type_id_user_id_key";
    ALTER TABLE "agon_ratings_overallrating" DROP CONSTRAINT
        IF EXISTS "agon_ratings_overallrating_object_id_content_type_id_key";

### 0.1.2

* added a tag, `user_rating_url`, for getting the POST url for posting a rating
* changed `user_rate_form` and documented javascript wiring to a single
  `user_rating_js` inclusion tag that output all the javascript and removed
  the need for a form.

### 0.1

* initial release


## Contribute

For an overview on how contributing to Pinax works read this [blog post](http://blog.pinaxproject.com/2016/02/26/recap-february-pinax-hangout/)
and watch the included video, or read our [How to Contribute](http://pinaxproject.com/pinax/how_to_contribute/) section.
For concrete contribution ideas, please see our
[Ways to Contribute/What We Need Help With](http://pinaxproject.com/pinax/ways_to_contribute/) section.

In case of any questions we recommend you join our [Pinax Slack team](http://slack.pinaxproject.com)
and ping us there instead of creating an issue on GitHub. Creating issues on GitHub is of course
also valid but we are usually able to help you faster if you ping us in Slack.

We also highly recommend reading our blog post on [Open Source and Self-Care](http://blog.pinaxproject.com/2016/01/19/open-source-and-self-care/).


## Code of Conduct

In order to foster a kind, inclusive, and harassment-free community, the Pinax Project
has a [code of conduct](http://pinaxproject.com/pinax/code_of_conduct/).
We ask you to treat everyone as a smart human programmer that shares an interest in Python, Django, and Pinax with you.


## Connect with Pinax

For updates and news regarding the Pinax Project, please follow us on Twitter [@pinaxproject](https://twitter.com/pinaxproject)
and check out our [Pinax Project blog](http://blog.pinaxproject.com).


## License

Copyright (c) 2012-2018 James Tauber and contributors under the [MIT license](https://opensource.org/licenses/MIT).
