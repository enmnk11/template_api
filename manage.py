#!/usr/bin/env python
import os
import sys
from pathlib import Path
from django.core.management.utils import get_random_secret_key

def create_app(app_name):
    """Crea una nueva app con estructura personalizada"""
    try:
        # Crear estructura de directorios
        app_dir = Path('apps') / app_name
        migrations_dir = app_dir / 'migrations'

        # Crear directorios
        app_dir.mkdir(parents=True, exist_ok=True)
        migrations_dir.mkdir(exist_ok=True)

        # Crear archivos
        files = {
            app_dir / '__init__.py': '',
            migrations_dir / '__init__.py': '',
            app_dir / 'apps.py': f'''from django.apps import AppConfig


class {app_name.capitalize()}Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.{app_name}'
''',
            app_dir / 'models.py': '''from django.db import models

# Create your models here
''',
            app_dir / 'serializers.py': '''from rest_framework import serializers

# Create your serializers here
''',
            app_dir / 'viewsets.py': '''from rest_framework import viewsets

# Create your viewsets here
''',
            app_dir / 'urls.py': '''from rest_framework.routers import DefaultRouter

router = DefaultRouter()
# router.register('endpoint', ViewSet)

urlpatterns = router.urls
''',
            app_dir / 'admin.py': '''from django.contrib import admin

# Register your models here
'''
        }

        # Crear los archivos
        for file_path, content in files.items():
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

        print(f'✅ App "{app_name}" creada exitosamente')
        print(f'No olvides agregar "apps.{app_name}" a INSTALLED_APPS en settings.py')
        print(f'No olvides agregar "apps.{app_name}.urls" a urls.py en {{ project_name }}')

    except Exception as e:
        print(f'❌ Error creando la app: {str(e)}')


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{{ project_name }}.settings')

    # Verificar si es nuestro comando personalizado
    if len(sys.argv) > 1 and sys.argv[1] == 'createapp':
        if len(sys.argv) < 3:
            print("❌ Error: Debes especificar el nombre de la app")
            print("Uso: python manage.py createapp nombre_app")
            sys.exit(1)
        create_app(sys.argv[2])
    elif len(sys.argv) > 1 and sys.argv[1] == 'generate-secret-key':
        print('🔑 Secret Key:')
        print(get_random_secret_key())
    else:
        try:
            from django.core.management import execute_from_command_line
        except ImportError as exc:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            ) from exc
        execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()