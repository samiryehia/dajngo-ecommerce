from .models import LoggingRecord

class LoggingMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Log the incoming request
        user = request.user if request.user.is_authenticated else None  # Get authenticated user (if available)
        logging_record = LoggingRecord.objects.create(
            user=user,
            method=request.method,
            path=request.path,
            status_code=None  # Will be updated later after getting the response
        )

        # Pass the request to the next middleware or view
        response = self.get_response(request)

        # Update the status code in the logging record with the response status code
        logging_record.status_code = response.status_code
        logging_record.save()

        return response

