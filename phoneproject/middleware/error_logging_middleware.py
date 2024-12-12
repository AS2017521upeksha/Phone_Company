import logging

logger = logging.getLogger(__name__)

class ErrorLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = None
        try:
            response = self.get_response(request)
        except Exception as e:
            # Log the error
            logger.error(f"Unhandled exception in {request.path}: {str(e)}", exc_info=True)
            raise  # Re-raise the exception to let Django handle it
        return response
