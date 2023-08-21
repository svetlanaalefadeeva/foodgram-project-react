import csv

from django.core.management.base import BaseCommand

from cookbook.models import Ingredient


class Command(BaseCommand):
    help = 'Add ingredients to the database'

    def handle(self, **kwargs):
        try:
            with open(
                '/app/data/ingredients.csv', 'r',
                encoding='utf-8'
            ) as f:
                reader = csv.reader(f, delimiter=',')
                for row in reader:
                    Ingredient.objects.get_or_create(
                        name=row[0],
                        measurement_unit=row[1],
                    )
                self.stdout.write(
                    self.style.SUCCESS('Загружено!')
                )
        except FileNotFoundError:
            self.stdout.write(
                self.style.ERROR('Файл не найден!')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR('Произошла ошибка: ' + str(e))
            )
