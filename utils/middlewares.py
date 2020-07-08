import logging

from django.utils.deprecation import MiddlewareMixin

class ExceptionMiddleware(MiddlewareMixin):
    
    logger = logging.getLogger('api_error')

    def process_exception(self, request, exception):
        self.logger.error(exception)

