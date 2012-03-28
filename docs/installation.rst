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

* Next, you will want to add `agon_ratings.urls` to your urls definition::

    ...
    url(r"^ratings/", include("agon_ratings.urls")),
    ...

* Lastly, you need to define which models can be voted on in your `settings.py`
  If want to use the ratings category feature of `agon-ratings`, you will need
  to define valid categories here as well.::

    AGON_RATINGS_CATEGORY_CHOICES = {
        # Allow simple voting on the app.Post model
        "app.Post": True,

        # Allow voting on the exposure, framing and saturation of an app.Picture
        "app.Picture": [ "exposure", "framing", "saturation" ],
    }
