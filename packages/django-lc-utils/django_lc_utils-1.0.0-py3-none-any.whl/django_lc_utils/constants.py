from django.db import models
from django.utils.translation import gettext_lazy as _


class PERMISSION_TYPE(models.IntegerChoices):
    DJANGO_DEFAULT = 1, _("Django Default")
    BACK_OFFICE = 2, _("Back Office")
    ADMINISTRATIVE = 3, _("Administrative")
    OTHER = 4, _("Other")


class GROUP_TYPE(models.IntegerChoices):
    BACK_OFFICE = 1, _("Back Office")
    ADMINISTRATIVE = 2, _("Administrative")
    OTHER = 3, _("Other")
    SUPERVISOR = 4, _("Supervisor")
