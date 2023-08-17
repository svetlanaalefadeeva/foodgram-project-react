import csv

from django.core.management.base import BaseCommand

from cookbook.models import Ingredient

class Command(BaseCommand):
    help = 'Add ingredients to the database'

    def handle(self, **kwargs):
        with open(
                '../data/ingredients.csv', 'r',
                encoding='UTF-8'
        ) as ingredients:
            reader = csv.reader(
                ingredients,
                delimiter=","
            )
            for row in reader:
                Ingredient.objects.get_or_create(
                    name=row[0],
                    measurement_unit=row[1],
                )
        self.stdout.write(self.style.SUCCESS('Загружено!'))
