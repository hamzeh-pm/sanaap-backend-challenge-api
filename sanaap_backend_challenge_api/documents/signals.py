from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from logging import getLogger

logger = getLogger(__name__)


@receiver(post_migrate)
def assign_document_permissions_to_roles(sender, **kwargs):
    if sender.name != "sanaap_backend_challenge_api.documents":
        return

    document_ct = ContentType.objects.get(app_label="documents", model="document")

    add_permission = Permission.objects.get(
        codename="add_document", content_type=document_ct
    )
    change_permission = Permission.objects.get(
        codename="change_document", content_type=document_ct
    )
    delete_permission = Permission.objects.get(
        codename="delete_document", content_type=document_ct
    )
    view_permission = Permission.objects.get(
        codename="view_document", content_type=document_ct
    )

    admin_group = Group.objects.get(name="Admin")
    editor_group = Group.objects.get(name="Editor")
    viewer_group = Group.objects.get(name="Viewer")

    admin_group.permissions.add(
        add_permission, change_permission, delete_permission, view_permission
    )
    editor_group.permissions.add(add_permission, change_permission, view_permission)
    viewer_group.permissions.add(view_permission)

    logger.info(
        "Signal: assign_document_permissions_to_roles, Success: completed successfully."
    )
