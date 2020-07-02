"""
Update historical stock data for Fortune 100 companies.
"""
import argparse
from django.core.management.base import BaseCommand, CommandError
from api.utils import update_historical_stocks


class Command(BaseCommand):

    def handle(self, *args, **options):
        update_historical_stocks()
