"""
WSGI config for taxiRoka project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
import site

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'taxiRoka.settings')

site.addsitedir(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

application = get_wsgi_application()
