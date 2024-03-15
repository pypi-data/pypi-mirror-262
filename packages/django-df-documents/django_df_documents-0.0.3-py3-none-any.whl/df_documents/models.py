import re

import markdown
from django.contrib.sites.models import Site
from django.db import models
from django.template import Context, Template


class Document(models.Model):
    slug = models.SlugField(unique=True)
    content = models.TextField(
        help_text="Markdown. First line could be {% extends 'xxxxxxx.html' %}"
    )

    def render_to_html(self) -> str:
        content_html = markdown.markdown(self.content.strip())
        content_html = re.sub(r"<p>\{%(.+?)%}</p>", r"{%\1%}", content_html)
        return Template(content_html).render(
            Context(
                {
                    "site": Site.objects.get_current(),
                }
            )
        )

    def __str__(self) -> str:
        return self.slug
