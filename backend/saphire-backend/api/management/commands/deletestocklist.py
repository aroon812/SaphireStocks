"""
Delete all stocks for a company when provided a ticker.
"""
import argparse
from django.core.management.base import BaseCommand, CommandError
from api.models import Stock


class Command(BaseCommand):

    help = 'Delete all stock days when a ticker is provided.'

    def add_arguments(self, parser):
        parser.add_argument(
            'company_ticker', help='Ticker for the company that should have its stocks deleted')

    def handle(self, *args, **options):
        try:
            stocks = Stock.objects.filter(company=options['company_ticker'])
            stocks.delete()
        except Exception as e:
            print(e)
