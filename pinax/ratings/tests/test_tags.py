from django.contrib.contenttypes.models import ContentType
from django.template import Context, Template

from .models import Car
from .test import TestCase


class TemplateTagsTest(TestCase):
    """
    Tests for the template tags
    """

    def setUp(self):
        self.test_user = self.make_user(username="test_user")
        self.another_user = self.make_user(username="another_user")
        self.none_car_object = self.make_user(username="a_user")
        self.benz = Car.objects.create(name="Mercedes c200")
        self.post_a_rating(self.test_user, 2)

    def post_a_rating(self, user, rating):
        """
        Helper function to post a rating for the benz object of
        type Car used in the tests
        :param user: User
        :param rating: int
        :return: http response object
        """
        with self.login(user):
            return self.post(
                "pinax_ratings:rate",
                content_type_id=ContentType.objects.get_for_model(self.benz).pk,
                object_id=self.benz.pk,
                data={
                    "rating": rating,
                    "category": "handling"
                },
            )

    def test_user_rating_tag_with_category(self):
        """
        Ensure the template tag user_rating renders a rating
        as posted by the user on a Car object they are rating
        for a specified category in the context
        """

        template = Template(
            "{% load pinax_ratings_tags %}"
            "{% user_rating user object category as the_rating %}"
        )
        context = Context({
            "user": self.test_user,
            "object": self.benz,
            "category": "handling"
        })
        template.render(context)
        self.assertEqual(context["the_rating"], 2)

    def test_user_rating_tag_no_category(self):
        """
        Ensure the template tag user_rating renders a rating
        as posted by the user on a Car object they are rating.
        in this test, no category is specified
        """

        template = Template(
            "{% load pinax_ratings_tags %}"
            "{% user_rating user object category as the_rating %}"
        )
        context = Context({
            "user": self.test_user,
            "object": self.benz,
            "category": ""
        })
        template.render(context)
        self.assertEqual(context["the_rating"], 2)

    def test_overall_rating_tag_with_category(self):
        """
        Ensure the template tag overall_rating renders an
        overall rating for a specified category in the
        context
        """

        self.post_a_rating(self.another_user, 3)

        template = Template(
            "{% load pinax_ratings_tags %}"
            "{% overall_rating object category as the_overall_rating %}"
        )
        context = Context({
            "object": self.benz,
            "category": "handling"
        })
        template.render(context)
        self.assertEqual(context["the_overall_rating"], 2.5)

    def test_overall_rating_tag_with_no_category(self):
        """
        Ensure the template tag overall_rating renders an
        overall rating. in this test, no category is specified
        """

        template = Template(
            "{% load pinax_ratings_tags %}"
            "{% overall_rating object category as the_overall_rating %}"
        )
        context = Context({
            "object": self.benz,
            "category": ""
        })
        template.render(context)
        self.assertEqual(context["the_overall_rating"], 2.0)

    def test_ratings_tag(self):
        """
        Ensure the template tag ratings_tag renders the rating
        """

        template = Template(
            "{% load pinax_ratings_tags %}"
            "{% ratings object as a_rating %}"
        )
        context = Context({
            "object": self.benz
        })
        template.render(context)
        self.assertEqual(context["a_rating"], [])

    def test_user_rating_url(self):
        """
        Ensure the template tag user_rating_url renders the
        post ratings url with the correct kwargs
        """

        template = Template(
            "{% load pinax_ratings_tags %}"
            "{% user_rating_url user object as url %}"
        )
        context = Context({
            "user": self.test_user,
            "object": self.benz
        })
        template.render(context)
        self.assertEqual(
            context["url"],
            "/{}/{}/rate/".format(
                ContentType.objects.get_for_model(self.benz).pk,
                self.benz.pk
            )
        )

    def test_rating_count_tag(self):
        """
        Ensure the template tag rating_count renders the
        correct count
        """

        template = Template(
            "{% load pinax_ratings_tags %}"
            "{% rating_count object as count %}"
        )
        context = Context({
            "object": self.benz
        })
        template.render(context)
        self.assertEqual(context["count"], 1)

    def test_user_rating_js_tag(self):
        """

        """
        template = Template(
            "{% load pinax_ratings_tags %}"
            "{% user_rating_js user object %}"
        )
        context = Context({
            "user": self.test_user,
            "object": self.benz,
            "category": "handling"
        })
        rendered_template = template.render(context)
        self.assertInHTML(
            """
            <script type="text/javascript">
                $(function () {
                    // Assumptions:
                    // 1. you have a div with the id of "user_rating" where you want the stars to go
                    // 2. you have a container with the class .overall_rating where the new average rating will go
                    $("#user_rating").raty({
                        score: function() {
                            return $(this).attr('data-score');
                        },
                        click: function(score, evt) {
                            var current_rating = 0;
                            if (score != null) {
                                current_rating = score;
                            }
                            console.log("Score", score, "/17/1/rate/");
                            $.ajax({
                                url: "/17/1/rate/",
                                type: "POST",
                                data: {
                                    "rating": current_rating
                                },
                                statusCode: {
                                    403: function(jqXHR, textStatus, errorThrown) {
                                        // Invalid rating was posted or invalid category was sent
                                        console.log(errorThrown);
                                    },
                                    200: function(data, textStatus, jqXHR) {
                                            $(".overall_rating").text(data["overall_rating"]);
                                    }
                                }
                            });
                        },
                        cancel: true,
                        path: "Nonepinax/ratings/img/"
                    });
                });
            </script>
            """, rendered_template)
