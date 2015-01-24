.. _installation:

Installation
============

* To install pinax-ratings::

    pip install pinax-ratings

* Add ``pinax-ratings`` to your ``INSTALLED_APPS`` setting::

    INSTALLED_APPS = (
        # other apps
        "pinax.ratings",
    )

* See the list of :ref:`settings` to modify pinax-ratings's
  default behavior and make adjustments for your website.

* Lastly you will want to add `pinax-ratings.urls` to your urls definition::

    ...
    url(r"^ratings/", include("pinax.ratings.urls")),
    ...

* Optionally, if want to use the ratings category feature of `pinax-ratings`
  then you will need to add the `pinax-RATINGS_CATEGORY_CHOICES` setting
  in your `settings.py`::

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
