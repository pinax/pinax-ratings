.. _installation:

Installation
============

* To install agon_ratings::

    pip install agon_ratings

* Add ``agon_ratings`` to your ``INSTALLED_APPS`` setting::

    INSTALLED_APPS = (
        # other apps
        "agon_ratings",
    )

* See the list of :ref:`settings` to modify agon_ratings's
  default behavior and make adjustments for your website.

* Lastly you will want to add `agon_ratings.urls` to your urls definition::

    ...
    url(r"^ratings/", include("agon_ratings.urls")),
    ...

* Optionally, if want to use the ratings category feature of `agon-ratings`
  then you will need to add the `AGON_RATINGS_CATEGORY_CHOICES` setting
  in your `settings.py`::

    AGON_RATINGS_CATEGORY_CHOICES = {
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
