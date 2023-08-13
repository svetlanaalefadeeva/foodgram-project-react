import csv
from django.conf import settings
from django.core.management.base import BaseCommand

from cookbook.models import Ingredient

class Command(BaseCommand):
    help = 'Add ingredients to the database'

    def handle(self, **kwargs):
        data_path = settings.BASE_DIR
        with open(f'{data_path}/data/ingredients.csv', 'r', encoding='UTF-8') as file:
            reader = csv.reader(file, delimiter=',')
            for row in reader:
                Ingredient.objects.get_or_create(name=row[0], measurement_unit=row[1])
        self.stdout.write(self.style.WARNING(self.style.SUCCESS('Загружено')))
