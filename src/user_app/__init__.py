"""
Initialize the logger for the application.
"""
import logging

logger = logging.getLogger('sample_logger.' + __name__)
default_app_config = 'user_app.apps.UserAppConfig'