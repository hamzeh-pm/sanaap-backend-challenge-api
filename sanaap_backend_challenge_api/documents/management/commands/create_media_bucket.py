import boto3
from botocore.exceptions import ClientError
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = "Setup storage buckets for the application"

    def handle(self, *args, **options):
        try:
            # Create S3 client
            s3_client = boto3.client(
                "s3",
                endpoint_url=settings.AWS_S3_ENDPOINT_URL,
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=getattr(settings, "AWS_S3_REGION_NAME", "us-east-1"),
                use_ssl=getattr(settings, "AWS_S3_USE_SSL", False),
                verify=getattr(settings, "AWS_S3_VERIFY", False),
            )

            # Check if bucket exists
            bucket_name = settings.AWS_STORAGE_BUCKET_NAME
            try:
                s3_client.head_bucket(Bucket=bucket_name)
                self.stdout.write(
                    self.style.SUCCESS(f'Bucket "{bucket_name}" already exists.')
                )
            except ClientError as e:
                error_code = e.response["Error"]["Code"]
                if error_code == "404":
                    # Bucket doesn't exist, create it
                    try:
                        s3_client.create_bucket(Bucket=bucket_name)
                        self.stdout.write(
                            self.style.SUCCESS(
                                f'Successfully created bucket "{bucket_name}".'
                            )
                        )

                    except ClientError as create_error:
                        self.stdout.write(
                            self.style.ERROR(f"Failed to create bucket: {create_error}")
                        )
                        raise
                else:
                    self.stdout.write(self.style.ERROR(f"Error checking bucket: {e}"))
                    raise

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Storage setup failed: {str(e)}"))
            raise
