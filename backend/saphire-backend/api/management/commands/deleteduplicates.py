"""
Delete duplicate stock days for every company in the database
"""
import argparse
from django.core.management.base import BaseCommand, CommandError
from api.models import Stock


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            for row in Stock.objects.all():
                if Stock.objects.filter(company=row.company, date=row.date).count() > 1:
                    row.delete()
                    print("duplicate deleted")
        except Exception as e:
            print(e)
