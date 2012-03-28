.. _settings:

Settings
========

.. _agon_num_of_ratings:

AGON_NUM_OF_RATINGS
^^^^^^^^^^^^^^^^^^^

:Default: 5

Defines the number of different rating choices there will be.


AGON_RATINGS_CATEGORY_CHOICES
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:Default: `None`

Defines the models that have rating enabled. Only models that are defined in this
dict are allowed to be rated.

Additionally, this dictionary defines the choices for different models for the
application of ratings along different dimensions rather than just a single rating
for an object.

    AGON_RATINGS_CATEGORY_CHOICES = {
        # Allow simple voting on the app.Post model
        "app.Post": True,

        # Allow voting on the exposure, framing and saturation of an app.Picture
        "app.Picture": [ "exposure", "framing", "saturation" ],
    }
