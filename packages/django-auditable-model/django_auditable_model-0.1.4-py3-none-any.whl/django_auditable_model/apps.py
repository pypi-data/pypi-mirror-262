from django.apps import AppConfig


class DjangoAuditableModelConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "django_auditable_model"
