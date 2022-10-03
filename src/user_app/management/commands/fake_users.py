from django.core.management.base import BaseCommand, CommandError

from scripts.create_fake_users import FakeUser

class Command(BaseCommand):
    help = 'Create fake users to test out the system.'

    def add_arguments(self, parser):
        parser.add_argument('amount', type=int)

    def handle(self, *args, **options):
        user_list = FakeUser.create_bulk_users(options.get('amount', 10))