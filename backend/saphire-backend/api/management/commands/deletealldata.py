import argparse
from django.core.management.base import BaseCommand, CommandError
from api.models import Stock, Company


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            Company.objects.all().delete()
        except Exception as e:
            print(e)
