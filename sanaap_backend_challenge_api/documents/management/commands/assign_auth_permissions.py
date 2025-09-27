from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType


class Command(BaseCommand):
    help = "Assign permissions"

    def handle(self, *args, **options):
        # Create groups
        admin_group, created = Group.objects.get_or_create(name="Admin")
        editor_group, created = Group.objects.get_or_create(name="Editor")
        viewer_group, created = Group.objects.get_or_create(name="Viewer")

        if created:
            self.stdout.write(self.style.SUCCESS("Created groups"))

        # Get content types
        try:
            user_ct = ContentType.objects.get(app_label="auth", model="user")
            group_ct = ContentType.objects.get(app_label="auth", model="group")

            # Get permissions
            user_permissions = Permission.objects.filter(content_type=user_ct)
            group_permissions = Permission.objects.filter(content_type=group_ct)

            # Assign to admin group
            admin_group.permissions.add(*user_permissions)
            admin_group.permissions.add(*group_permissions)

            self.stdout.write(
                self.style.SUCCESS("Successfully assigned permissions to Admin group")
            )

        except ContentType.DoesNotExist:
            self.stdout.write(
                self.style.ERROR("ContentTypes not found. Run migrations first.")
            )
