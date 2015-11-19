# coding=utf8
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        if User.objects.count() == 0:
            # create a superuser
            User.objects.create_superuser(
                'admin',
                'admin@example.com',
                'admin',
            )
            self.stdout.write('Successfully created superuser. change password asap.')
