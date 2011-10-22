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

Defines a dictionary of choices for different models for the application of
ratings along different dimensions rather than just a single rating for an
object.

It should follow the format of a dictionary of dictionaries. For example, think of
the context of a website that allowed ratings of photographs and articles
published by other users::

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
