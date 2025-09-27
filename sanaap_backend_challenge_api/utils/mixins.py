from auditlog.models import LogEntry
from django.utils.timezone import now


class ViewsetAccessLogMixin:
    def _log_access(self, request, instance, action):
        user = request.user if request.user.is_authenticated else None
        LogEntry.objects.log_create(
            instance=instance,
            force_log=True,
            actor=user,
            action=LogEntry.Action.ACCESS,
            timestamp=now(),
        )

    def retrieve(self, request, *args, **kwargs):
        self._log_access(request, self.get_object(), "retrieve")
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        self._log_access(request, self.get_object(), "update")
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        self._log_access(request, self.get_object(), "partial_update")
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        self._log_access(request, self.get_object(), "destroy")
        return super().destroy(request, *args, **kwargs)
