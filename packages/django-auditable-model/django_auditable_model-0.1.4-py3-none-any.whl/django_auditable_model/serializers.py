from rest_framework import serializers

class AuditableSerializerMixin:
    def save(self, **kwargs):
        request = self.context.get('request')
        if not request or not hasattr(request, 'user') or request.user.is_anonymous:
            return super().save(**kwargs)

        if not self.instance:
            kwargs['created_by'] = request.user
        else:
            kwargs['updated_by'] = request.user
        return super().save(**kwargs)
