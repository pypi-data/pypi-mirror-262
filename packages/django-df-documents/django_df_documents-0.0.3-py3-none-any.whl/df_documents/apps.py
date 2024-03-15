from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DfDocumentsConfig(AppConfig):
    name = "df_documents"
    verbose_name = _("Django DF Documents")
