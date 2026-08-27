from django.template import Context, Template
from django.test import SimpleTestCase
from django.utils.encoding import force_text
from django.utils.module_loading import import_string


class TextileRenderingTests(SimpleTestCase):
    def render(self, value):
        template = Template("{% load markup %}{{ value|textile }}")
        return template.render(Context({"value": value})).strip()

    def test_template_renders_active_markup(self):
        self.assertEqual(
            self.render(
                "h3. What is new\n\n"
                "* Faster startup\n"
                "* New *Dragon's Lair* sounds"
            ).replace("\t", ""),
            "<h3>What is new</h3>\n\n"
            "<ul>\n"
            "<li>Faster startup</li>\n"
            "<li>New <strong>Dragon&#8217;s Lair</strong> sounds</li>\n"
            "</ul>",
        )

    def test_public_filter_path_renders_unicode_and_links(self):
        textile = import_string("django_markup.templatetags.markup.textile")

        self.assertEqual(
            force_text(textile(
                'Cr\u00e9dits by *Zo\u00eb*. '
                'Visit "Syrinscape":https://syrinscape.com/'
            )).strip(),
            '<p>Cr\u00e9dits by <strong>Zo\u00eb</strong>. Visit '
            '<a href="https://syrinscape.com/">Syrinscape</a></p>',
        )


class MarkdownRenderingTests(SimpleTestCase):
    def test_tilde_extension_renders_subscription_text(self):
        template = Template(
            '{% load markup %}{{ value|markdown:"pymdownx.tilde" }}'
        )

        self.assertEqual(
            template.render(Context({
                "value": "Pay ~~USD 10~~ USD 8",
            })).strip(),
            "<p>Pay <del>USD 10</del> USD 8</p>",
        )
