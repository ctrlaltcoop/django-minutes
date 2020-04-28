import json

from django.core.management.base import BaseCommand, CommandError
from rest_framework.schemas.openapi import SchemaGenerator

from minutes.urls import schema_patterns


class Command(BaseCommand):
    help = 'Updates the api specification in the frontend module'

    def handle(self, *args, **options):
        generator = SchemaGenerator(
            title='Minutes API V1',
            description='django-minutes API specifications',
            patterns=schema_patterns,
            version='1.0'
        )
        schema = generator.get_schema()
        schema_json = json.dumps(schema)
        print(schema_json)
