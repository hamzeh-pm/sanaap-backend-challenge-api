from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = "Create a superuser"

    def add_arguments(self, parser):
        parser.add_argument(
            "--username", type=str, required=False, help="Username for the superuser"
        )
        parser.add_argument(
            "--email", type=str, required=False, help="Email for the superuser"
        )
        parser.add_argument(
            "--password", type=str, required=False, help="Password for the superuser"
        )

    def handle(self, *args, **options):
        username = options["username"] or settings.SUPERUSER_USERNAME
        email = options["email"] or settings.SUPERUSER_EMAIL
        password = options["password"] or settings.SUPERUSER_PASSWORD

        if not username or not email or not password:
            self.stderr.write(
                self.style.ERROR(
                    "Username, email, and password must be provided either as arguments or in environment variables."
                    "args: --username, --email, --password or,"
                    "env: DJANGO_SUPERUSER_USERNAME, DJANGO_SUPERUSER_EMAIL, DJANGO_SUPERUSER_PASSWORD"
                )
            )
            return

        try:
            if not User.objects.filter(username=username).exists():
                User.objects.create_superuser(
                    username=username, email=email, password=password
                )
                self.stdout.write(
                    self.style.SUCCESS(f"Superuser '{username}' created successfully.")
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"Superuser '{username}' already exists.")
                )
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error creating superuser: {e}"))
