import traceback
import sys
import requests, json
from django.conf import settings
import os
import platform
import socket
from django.core.exceptions import ImproperlyConfigured


class ConsoleExceptionLoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.key = getattr(settings, 'CONSOLE_EXCEPTION_LOGGER_KEY', None)

        if not self.key:
            raise ImproperlyConfigured("CONSOLE_EXCEPTION_LOGGER_KEY is missing in settings.")

    def __call__(self, request):
        try:
            response = self.get_response(request)
        except Exception as e:
            self.process_exception(request, e)
            raise
        return response


    def process_exception(self, request, exception):

        browserName = request.META.get("HTTP_USER_AGENT")
        user_agent = request.META.get('HTTP_USER_AGENT', '')

        if 'Mobile' in user_agent or 'Android' in user_agent or 'iPhone' in user_agent:
            device_type = 'Mobile Device'
        else:
            device_type = 'System (Desktop or Laptop)'

        exc_info = sys.exc_info()
        version = sys.version

        value = '\n'.join(traceback.format_exception(*(exc_info or sys.exc_info())))

        uri = request.build_absolute_uri()

        base_dir = settings.BASE_DIR

        project_name = os.path.basename(base_dir)
        language = platform.python_implementation()
        url = "https://bugtracking.colanapps.in/api/bugtrack/"
        
        user = socket.gethostname()
        ip_address = socket.gethostbyname(user)
        payload_data = {
            "error": "test",
            "title": str(exception),
            "description": str(value),
            "user": str(user),
            "url": str(uri),
            "user_ip":str(ip_address),
            "device_type": str(device_type),
            "python_version": str(version),
            "browser_name": str(browserName),
            "project_name": str(project_name),
            "language": str(language)
        }

        payload = json.dumps(payload_data)
        
        headers = {
        'Content-Type': 'application/json',
        'Authorization': self.key
        }

        response = requests.request("POST", url, headers=headers, data=payload)

