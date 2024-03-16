from django.conf import settings
from django.db import models


class AbstractAuditableModel(models.Model):
    """
    This will have Basic Fields Required in all Models
    """
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="%(class)s_createdby",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="%(class)s_modifiedby",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True
