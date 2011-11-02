.. _changelog:

ChangeLog
=========

0.2.1
-----

- added ability in overall_rating template tag to omit the category
  label and get an average rating without concern for category
  averages.


0.2
---

- added support for ratings to have categories instead of just a single
  rating for an object
- dropped natural language of template tags

Migrations
^^^^^^^^^^

Added a category model and updated the unique index on both models::

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


0.1.2
-----

- added a tag, `user_rating_url`, for getting the POST url for posting a rating
- changed `user_rate_form` and documented javascript wiring to a single
  `user_rating_js` inclusion tag that output all the javascript and removed
  the need for a form.

0.1
---

- initial release
