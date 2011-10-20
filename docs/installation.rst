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
