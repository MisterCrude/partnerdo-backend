from rest_framework.views import exception_handler


def exception_with_status_code_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        print(response.status_code)
        response.data['status_code'] = response.status_code

    return response