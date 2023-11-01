import json
import os
from catalog.models import Products, Category

from django.core.management import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        Products.objects.all().delete()
        Category.objects.all().delete()
        os.system('python -Xutf8 manage.py loaddata data.json')
        # with open('data.json', 'r', encoding='utf-8') as f:
            # data = json.load(f)
            # print(data)
