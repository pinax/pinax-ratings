from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.template import Context, Template
from django.urls import reverse

from ..models import Rating
from ..templatetags.pinax_ratings_tags import ratings, user_rating_js
from .models import Car
from .test import TestCase


class TemplateTagsTest(TestCase):
    """
    Tests for the template tags
    """

    def setUp(self):
        self.default_rating = 2
        self.default_category = "handling"
        self.other_category = "color"
        self.test_user = self.make_user(username="test_user")
        self.another_user = self.make_user(username="another_user")
        self.not_rated_object = self.make_user(username="a_user")
        self.benz = Car.objects.create(name="Mercedes c200")
        self.post_a_rating(self.test_user, self.default_rating)

    def post_a_rating(self, user, rating, category="handling"):
        """
        Helper function to post a rating for the benz object of
        type Car used in the tests
        :param user: User
        :param rating: int
        :param category: str
        :return: http response object
        """
        with self.login(user):
            return self.post(
                "pinax_ratings:rate",
                content_type_id=ContentType.objects.get_for_model(self.benz).pk,
                object_id=self.benz.pk,
                data={
                    "rating": rating,
                    "category": category
                },
            )

    def config_template_context(self, ctx=None):
        """
        Helper function that configures the context for the template
        :param ctx: dictionary
        :return: context object
        """
        if ctx is None:
            ctx = {
                "user": self.test_user,
                "object": self.benz,
                "category": self.default_category
            }
        context = Context(ctx)
        return context

    def test_user_rating_tag_with_category(self):
        """
        Ensure the template tag user_rating renders a rating
        as posted by the user on a Car object they are rating
        for a specified category in the context
        """
        template = Template(
            "{% load pinax_ratings_tags %}"
            "{% user_rating user object category %}"
        )

        context = self.config_template_context()

        rendered = template.render(context)
        self.assertIn(str(self.default_rating), rendered)

        self.post_a_rating(
            self.test_user,
            self.default_rating + 1,
            self.other_category
        )

        context = self.config_template_context({
            "user": self.test_user,
            "object": self.benz,
            "category": self.other_category
        })
        rendered = template.render(context)
        self.assertIn(str(self.default_rating + 1), rendered)

    def test_user_rating_tag_with_category_on_not_rated_object(self):
        """
        This test ensures that a rating of zero is returned when you
        rate another object other than the one expected to be rated. In
        this case we are rating a User object instead of a Car object
        """
        template = Template(
            "{% load pinax_ratings_tags %}"
            "{% user_rating user object category %}"
        )
        context = self.config_template_context(
            ctx={
                "user": self.test_user,
                "object": self.not_rated_object,
                "category": self.default_category
            }
        )
        rendered = template.render(context)
        self.assertIn(str(0), rendered)

    def test_user_rating_tag_with_no_category(self):
        """
        Ensure the template tag user_rating renders a rating
        as posted by the user on a Car object they are rating.
        in this test, no category is specified
        """

        template = Template(
            "{% load pinax_ratings_tags %}"
            "{% user_rating user object %}"
        )
        context = self.config_template_context({
            "user": self.test_user,
            "object": self.benz
        })

        rendered = template.render(context)
        self.assertIn(str(self.default_rating), rendered)

        self.post_a_rating(
            self.test_user,
            self.default_rating + 1,
            self.other_category
        )

        rendered = template.render(context)
        # the overall rating should be equal to (2 + 3 /2)
        self.assertIn(str(2.5), rendered)

    def test_overall_rating_tag_with_category(self):
        """
        Ensure the template tag overall_rating renders an
        overall rating for a specified category in the
        context
        """

        template = Template(
            "{% load pinax_ratings_tags %}"
            "{% overall_rating object category %}"
        )

        self.post_a_rating(
            self.test_user,
            self.default_rating + 1,
            self.other_category
        )

        self.post_a_rating(self.another_user, self.default_rating + 1)

        context = self.config_template_context({
            "object": self.benz,
            "category": self.default_category
        })

        rendered = template.render(context)
        # the overall rating should be equal to (2 + 3 /2)
        self.assertIn(str(2.5), rendered)

    def test_overall_rating_tag_with_category_on_not_rated_object(self):
        """
        This test ensures that an overall rating of zero is returned when you
        rate another object other than the one expected to be rated. In
        this case we are rating a User object instead of a Car object
        """
        template = Template(
            "{% load pinax_ratings_tags %}"
            "{% overall_rating object category %}"
        )
        context = self.config_template_context({
            "object": self.not_rated_object,
            "category": self.default_category
        })

        rendered = template.render(context)
        self.assertIn(str(0), rendered)

    def test_overall_rating_tag_with_no_category(self):
        """
        Ensure the template tag overall_rating renders an
        overall rating. in this test, no category is specified
        """

        template = Template(
            "{% load pinax_ratings_tags %}"
            "{% overall_rating object %}"
        )

        self.post_a_rating(
            self.test_user,
            self.default_rating + 1,
            self.other_category
        )

        context = self.config_template_context({
            "object": self.benz
        })

        rendered = template.render(context)
        # the overall rating should be equal to (2 + 3 /2)
        self.assertIn(str(2.5), rendered)

    def test_ratings_tag(self):
        """
        Ensure a query set is returned
        """
        content_type = ContentType.objects.get_for_model(self.benz)
        output = ratings(self.benz)
        expected = Rating.objects.filter(
            content_type=content_type,
            object_id=self.benz.pk
        )
        self.assertSetEqual(set(output), set(expected))

    def test_ratings_tag_with_not_rated_object(self):
        """
        Ensure a query set is returned
        """
        ContentType.objects.get_for_model(self.not_rated_object)
        output = ratings(self.not_rated_object)
        self.assertEqual(len(output), 0)

    def test_user_rating_url_tag(self):
        """
        Ensure the template tag user_rating_url renders the
        post ratings url with the correct kwargs
        """

        template = Template(
            "{% load pinax_ratings_tags %}"
            "{% user_rating_url user object %}"
        )
        context = Context({
            "user": self.test_user,
            "object": self.benz
        })
        rendered = template.render(context)
        self.assertIn(
            reverse(
                "pinax_ratings:rate",
                kwargs={
                    "content_type_id": ContentType.objects.get_for_model(self.benz).pk,
                    "object_id": self.benz.pk
                }),
            rendered
        )

    def test_rating_count_tag(self):
        """
        Ensure the template tag rating_count renders the
        correct count
        """

        template = Template(
            "{% load pinax_ratings_tags %}"
            "{% rating_count object %}"
        )

        self.post_a_rating(
            self.another_user,
            self.default_rating + 1,
            self.other_category
        )

        context = self.config_template_context({
            "object": self.benz
        })

        rendered = template.render(context)
        # ratings count should be 2
        self.assertIn(str(2), rendered)

    def test_user_rating_js_tag(self):
        """
        Ensure the correct context is returned for the
        template
        """

        self.post_a_rating(
            self.another_user,
            self.default_rating + 1,
            self.other_category
        )

        context = user_rating_js(self.another_user, self.benz, self.other_category)

        self.assertEqual(context["obj"], self.benz)
        self.assertEqual(context["category"], "color")
        self.assertEqual(context["the_user_rating"], self.default_rating + 1)
        self.assertEqual(context["STATIC_URL"], settings.STATIC_URL)
        self.assertEqual(
            context["post_url"],
            reverse(
                "pinax_ratings:rate",
                kwargs={
                    "content_type_id": ContentType.objects.get_for_model(self.benz).pk,
                    "object_id": self.benz.pk
                }
            ))
