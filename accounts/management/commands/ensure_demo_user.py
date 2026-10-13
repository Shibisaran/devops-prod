from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create a demo user for local and demo environments."

    def handle(self, *args, **options):
        user_model = get_user_model()
        username = "demo"
        password = "demo1234"
        user, created = user_model.objects.get_or_create(
            username=username,
            defaults={"email": "demo@example.com"},
        )
        user.set_password(password)
        user.is_staff = True
        user.save()
        action = "Created" if created else "Updated"
        self.stdout.write(self.style.SUCCESS(f"{action} demo user '{username}'."))
