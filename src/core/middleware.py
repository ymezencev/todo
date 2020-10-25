import logging


logger = logging.getLogger('todo')


class ExceptionHandler:
    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request):
        response = self._get_response(request)
        return response

    def process_exception(self, request, exception):
        logger.exception(f'Uncaught exception. [core.middleware.ExceptionHandler]')
        return None
