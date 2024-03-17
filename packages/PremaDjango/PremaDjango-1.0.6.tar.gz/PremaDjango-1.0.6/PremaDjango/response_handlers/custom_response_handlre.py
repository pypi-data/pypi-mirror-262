"""Custom Response Handler."""

import math

from rest_framework import status
from rest_framework.response import Response


class CustomResponseHandler:
    """Custom Response Handler Class for Django REST Framework."""

    def __init__(self, serializer_class=None):
        """
        Initialize the class with an optional serializer class.

        Args:
            serializer_class: The serializer class to be used.

        Returns:
            None
        """
        self.serializer_class = serializer_class

    def _generate_response(self, status_code, message, data=None, **kwargs):
        """
        Generate a response with the given status code, message, and optional data.

        :param status_code: The status code for the response
        :param message: The message to be included in the response
        :param data: Optional data to be included in the response
        :param kwargs: Additional keyword arguments
        :return: Response object with the generated data and status code
        """
        response_data = {
            "success": True,
            "status": status_code,
            "message": message,
            "data": data,
            **kwargs,
        }
        return Response(response_data, status=status_code)

    # Informational
    def continue_100(self, message=None, data=None, **kwargs):
        """
        Generate a response with status code 100 (Continue) along with the provided message and data.

        :param message: The message to be included in the response. Defaults to "Continue" if not provided.
        :param data: Additional data to be included in the response.
        :param kwargs: Additional keyword arguments to be passed to _generate_response.

        :return: The generated response with status code 100 (Continue).
        """
        if message is None:
            message = "Continue"
        return self._generate_response(status.HTTP_100_CONTINUE, message, data, **kwargs)

    def switching_protocols_101(self, message=None, data=None, **kwargs):
        """
        Return this function handles the switching protocols with an optional message and data.

        It returns the response generated with the status code 101 switching protocols,
        the provided message, data, and any additional keyword arguments.
        """
        if message is None:
            message = "Switching Protocols"
        return self._generate_response(status.HTTP_101_SWITCHING_PROTOCOLS, message, data, **kwargs)

    def processing_102(self, message=None, data=None, **kwargs):
        """
        Process HTTP 102 response with the given message and data.

        :param message: (str) The message for the response. Defaults to "Processing".
        :param data: The data for the response.
        :param kwargs: Additional keyword arguments.
        :return: The generated response.
        """
        if message is None:
            message = "Processing"
        return self._generate_response(status.HTTP_102_PROCESSING, message, data, **kwargs)

    def early_hints_103(self, message=None, data=None, **kwargs):
        """
        Generate and returns a response with status code 103 (Early Hints) along with the provided message and data.

        :param message: Optional message to be included in the response. Defaults to "Early Hints" if not provided.
        :param data: Optional data to be included in the response.
        :param **kwargs: Additional keyword arguments to be passed to the _generate_response method.
        :return: The response generated with status code 103 (Early Hints).
        """
        if message is None:
            message = "Early Hints"
        return self._generate_response(status.HTTP_103_EARLY_HINTS, message, data, **kwargs)

    # Successful
    def success_200(self, message=None, data=None, **kwargs):
        """
        Return this method to generate a success response with status code 200, an optional message, and optional data.

        :param message: An optional message for the response
        :param data: Optional data for the response
        :param kwargs: Additional keyword arguments
        :return: The response object with status code 200
        """
        if message is None:
            message = "Success"
        return self._generate_response(status.HTTP_200_OK, message, data, **kwargs)

    def created_201(self, message=None, data=None, **kwargs):
        """
        Return a  function that creates a response with status code 201.

        It takes in a message and data as optional parameters,
        as well as any additional keyword arguments.
        """
        if message is None:
            message = "New Record Created"
        return self._generate_response(status.HTTP_201_CREATED, message, data, **kwargs)

    def accepted_202(self, message=None, data=None, **kwargs):
        """
        Generate a response with status code 202 (Accepted) and the provided message and data.

        :param message: The message to be included in the response
        :type message: str
        :param data: Additional data to be included in the response
        :param kwargs: Additional keyword arguments
        :return: The generated response
        """
        if message is None:
            message = "Accepted"
        return self._generate_response(status.HTTP_202_ACCEPTED, message, data, **kwargs)

    def non_authoritative_information_203(self, message=None, data=None, **kwargs):
        """
        Return this function that handles non-authoritative information with an optional message and data.

        :param message: A string representing the message, defaults to "Non-Authoritative Information"
        :param data: Any additional data to be included in the response
        :param kwargs: Additional keyword arguments
        :return: The response generated by calling _generate_response with the appropriate status code, message, data, and kwargs
        """
        if message is None:
            message = "Non-Authoritative Information"
        return self._generate_response(status.HTTP_203_NON_AUTHORITATIVE_INFORMATION, message, data, **kwargs)

    def no_content_204(self, message=None, data=None, **kwargs):
        """
        Return a function that handles the 204 No Content response, with optional message and data parameters.

        Returns the response generated by the _generate_response method.
        """
        if message is None:
            message = "No Content"
        return self._generate_response(status.HTTP_204_NO_CONTENT, message, data, **kwargs)

    def reset_content_205(self, message=None, data=None, **kwargs):
        """
        Reset the content with an optional message and data.

        :param message: str, the optional message (default is "Reset Content")
        :param data: Any, the optional data
        :param kwargs: Any, additional keyword arguments
        :return: Any, the response generated using the given status and message
        """
        if message is None:
            message = "Reset Content"
        return self._generate_response(status.HTTP_205_RESET_CONTENT, message, data, **kwargs)

    def partial_content_206(self, message=None, data=None, **kwargs):
        """
        Generate a partial content response.

        :param message: str, the message to be included in the response
        :param data: str, the data to be included in the response
        :param kwargs: dict, additional keyword arguments
        :return: the response generated using the provided message, data, and any additional keyword arguments
        """
        if message is None:
            message = "Partial Content"
        return self._generate_response(status.HTTP_206_PARTIAL_CONTENT, message, data, **kwargs)

    def multi_status_207(self, message=None, data=None, **kwargs):
        """
        Generate a response with status code 207 (Multi-Status) and optional message and data.

        :param message: Optional message, defaults to "Multi-Status"
        :param data: Optional data
        :param kwargs: Additional keyword arguments
        :return: Response with status code 207 and the provided message and data
        """
        if message is None:
            message = "Multi-Status"
        return self._generate_response(status.HTTP_207_MULTI_STATUS, message, data, **kwargs)

    def already_reported_208(self, message=None, data=None, **kwargs):
        """
        Generate a response with status code 208 for the "Already Reported" message.

        :param message: Optional message to include in the response
        :param data: Optional data to include in the response
        :param kwargs: Additional keyword arguments
        :return: Response with status code 208 and optional message and data
        """
        if message is None:
            message = "Already Reported"
        return self._generate_response(status.HTTP_208_ALREADY_REPORTED, message, data, **kwargs)

    def im_used_226(self, message=None, data=None, **kwargs):
        """
        Generate a response with status HTTP 226 IM USED, using the provided message and data.

        :param message: A string representing the message to be included in the response
        :param data: Additional data to be included in the response
        :param kwargs: Additional keyword arguments
        :return: The response generated with status HTTP 226 IM USED, message, data, and additional kwargs
        """
        if message is None:
            message = "IM Used"
        return self._generate_response(status.HTTP_226_IM_USED, message, data, **kwargs)

    def success_pagination_200(self, request, queryset, message=None):
        """
        Return this function for handling successful pagination with a 200 status code.

        Args:
            self: The object itself.
            request: The HTTP request object.
            queryset: The queryset to be paginated.
            message: Optional. The message to be included in the response. Defaults to "Success".

        Returns:
            Response: The paginated data with a 200 status code.
        """
        try:
            page = int(request.GET.get("page", 1))
            offset = int(request.GET.get("offset", 20))
            if page < 1 or offset < 1:
                raise ValueError("Invalid page, offset value")
        except ValueError:
            return Response({"error": "Invalid page, offset, or limit value"}, status=status.HTTP_400_BAD_REQUEST)

        if message is None:
            message = "Success"

        total = queryset.count()
        start_index = (page - 1) * offset
        end_index = start_index + offset

        paginated_queryset = queryset[start_index:end_index]
        serializer = self.serializer_class(paginated_queryset, many=True, context={'request': request})

        last_page = math.ceil(total / offset)
        next_page = min(page + 1, last_page) if total > 0 else 1

        response_data = {
            "status": status.HTTP_200_OK,
            "message": message,
            "total": total,
            "page": page,
            "next": next_page,
            "last_page": last_page,
            "data": serializer.data,
        }

        return Response(response_data, status=status.HTTP_200_OK)

    # Redirection
    def multiple_choices_300(self, message=None, data=None, **kwargs):
        """
        Generate a response with status 300 for multiple choices.

        :param message: str, the message to be included in the response
        :param data: dict, additional data to be included in the response
        :param **kwargs: additional keyword arguments
        :return: the response with status 300 and the specified message and data
        """
        if message is None:
            message = "Multiple Choices"
        return self._generate_response(status.HTTP_300_MULTIPLE_CHOICES, message, data, **kwargs)

    def moved_permanently_301(self, message=None, data=None, **kwargs):
        """
        Generate a moved permanently response with the provided message and data.

        :param message: str, the message for the response
        :param data: dict, additional data for the response
        :param kwargs: dict, additional keyword arguments
        :return: Response, the generated response
        """
        if message is None:
            message = "Moved Permanently"
        return self._generate_response(status.HTTP_301_MOVED_PERMANENTLY, message, data, **kwargs)

    def found_302(self, message=None, data=None, **kwargs):
        """
        Return this function to handle the HTTP 302 Found status code, with optional message and data parameters.

        Returns a response generated by the _generate_response method.
        """
        if message is None:
            message = "Found"
        return self._generate_response(status.HTTP_302_FOUND, message, data, **kwargs)

    def see_other_303(self, message=None, data=None, **kwargs):
        """
        Generate a response with status code 303 See Other, with an optional message and data.

        :param message: (str) The message to be included in the response. Defaults to "See Other" if not provided.
        :param data: (Any) Any additional data to be included in the response.
        :param kwargs: (Any) Additional keyword arguments for future use.
        :return: (HttpResponse) The generated response with status code 303 See Other.
        """
        if message is None:
            message = "See Other"
        return self._generate_response(status.HTTP_303_SEE_OTHER, message, data, **kwargs)

    def not_modified_304(self, message=None, data=None, **kwargs):
        """
        Return a 304 Not Modified response with the given message and data.

        :param message: The message to include in the response
        :param data: The data to include in the response
        :param kwargs: Additional keyword arguments
        :return: The generated response
        """
        if message is None:
            message = "Not Modified"
        return self._generate_response(status.HTTP_304_NOT_MODIFIED, message, data, **kwargs)

    def use_proxy_305(self, message=None, data=None, **kwargs):
        """Retrun this function uses a proxy to generate a response with the provided message, data, and additional keyword arguments."""
        if message is None:
            message = "Use Proxy"
        return self._generate_response(status.HTTP_305_USE_PROXY, message, data, **kwargs)

    def temporary_redirect_307(self, message=None, data=None, **kwargs):
        """
        Perform a temporary redirect with status code 307.

        :param message: The message to be included in the response
        :param data: Additional data to be included in the response
        :param kwargs: Additional keyword arguments
        :return: The response generated with status code 307 and the provided message and data
        """
        if message is None:
            message = "Temporary Redirect"
        return self._generate_response(status.HTTP_307_TEMPORARY_REDIRECT, message, data, **kwargs)

    def permanent_redirect_308(self, message=None, data=None, **kwargs):
        """
        Return this function for generating a permanent redirect response.

        :param message: Optional message for the redirect response
        :param data: Optional data to include in the response
        :param kwargs: Additional keyword arguments
        :return: Response with status code 308 (Permanent Redirect)
        """
        if message is None:
            message = "Permanent Redirect"
        return self._generate_response(status.HTTP_308_PERMANENT_REDIRECT, message, data, **kwargs)

    # Client errors

    def bad_request_400(self, message=None, data=None, **kwargs):
        """
        Generate a response with a status code of 400 (Bad Request).

        :param message: (optional) The message to include in the response. Defaults to "Bad Request".
        :type message: str
        :param data: (optional) The data to include in the response.
        :type data: Any
        :param kwargs: Additional keyword arguments to include in the response.
        :type kwargs: Any
        :return: The generated response.
        :rtype: Response
        """
        if message is None:
            message = "Bad Request"
        return self._generate_response(status.HTTP_400_BAD_REQUEST, message, data, success=False, **kwargs)

    def serializer_error_400(self, message=None, data=None, **kwargs):
        """
        Generate a response with a status code of 400 (Bad Request).

        :param message: (optional) The message to include in the response. Defaults to "Bad Request".
        :type message: str
        :param data: (optional) The data to include in the response.
        :type data: Any
        :param kwargs: Additional keyword arguments to include in the response.
        :type kwargs: Any
        :return: The generated response.
        :rtype: Response
        """

        def serializer_errorss(error_dictionary):
            errors = ""
            for field, error in error_dictionary.items():
                errors += f"{field}: {error[0]}, "
            return errors

        if message is None:
            message = "Bad Request"
        return self._generate_response(
            status.HTTP_400_BAD_REQUEST, serializer_errorss(message), data, success=False, **kwargs
        )

    def unauthorized_401(self, message=None, data=None, **kwargs):
        """
        Generate a response for unauthorized access.

        :param message: (str) The message to be included in the response. Defaults to "Unauthorized" if not provided.
        :param data: (any) Additional data to be included in the response.
        :param **kwargs: Additional keyword arguments to be included in the response.
        :return: (HttpResponse) The generated response for unauthorized access.
        """
        if message is None:
            message = "Unauthorized"
        return self._generate_response(status.HTTP_401_UNAUTHORIZED, message, data, success=False, **kwargs)

    def payment_required_402(self, message=None, data=None, **kwargs):
        """Generate a response with status code 402 (Payment Required) along with the given message and data. Accepts optional keyword arguments."""
        if message is None:
            message = "Payment Required"
        return self._generate_response(status.HTTP_402_PAYMENT_REQUIRED, message, data, success=False, **kwargs)

    def forbidden_403(self, message=None, data=None, **kwargs):
        """
        Set the response status to 403 Forbidden with an optional message and data.

        :param message: (str) Optional message for the response
        :param data: (dict) Optional data for the response
        :param **kwargs: Additional keyword arguments
        :return: (HttpResponse) The generated response
        """
        if message is None:
            message = "Forbidden"
        return self._generate_response(status.HTTP_403_FORBIDDEN, message, data, success=False, **kwargs)

    def not_found_404(self, message=None, data=None, **kwargs):
        """
        Handle the 404 Not Found error response.

        :param message: A custom error message (default is "Not Found")
        :param data: Additional data to be included in the response
        :param kwargs: Additional keyword arguments
        :return: The response generated for the 404 Not Found error
        """
        if message is None:
            message = "Not Found"
        return self._generate_response(status.HTTP_404_NOT_FOUND, message, data, success=False, **kwargs)

    def method_not_allowed_405(self, message=None, data=None, **kwargs):
        """
        Generate a Method Not Allowed response with the given message and data.

        :param message: The message to be included in the response. Defaults to "Method Not Allowed" if not provided.
        :param data: Additional data to be included in the response.
        :param kwargs: Additional keyword arguments to be passed to _generate_response.
        :return: The response generated by _generate_response with status code 405 and success set to False.
        """
        if message is None:
            message = "Method Not Allowed"
        return self._generate_response(status.HTTP_405_METHOD_NOT_ALLOWED, message, data, success=False, **kwargs)

    def not_acceptable_406(self, message=None, data=None, **kwargs):
        """
        Return this method to handle the 406 Not Acceptable error with an optional message and data.

        :param message: Optional message for the error (default is "Not Acceptable")
        :param data: Optional data to be included in the response
        :param kwargs: Additional keyword arguments
        :return: Response with status 406 Not Acceptable and the provided message and data
        """
        if message is None:
            message = "Not Acceptable"
        return self._generate_response(status.HTTP_406_NOT_ACCEPTABLE, message, data, success=False, **kwargs)

    def proxy_authentication_required_407(self, message=None, data=None, **kwargs):
        """
        Generate a response for proxy authentication required with the given message and data.

        :param message: (str) The message for the response. Defaults to "Proxy Authentication Required" if not provided.
        :param data: (dict) Additional data for the response.
        :param kwargs: Additional keyword arguments for the response.
        :return: (Response) The generated response for proxy authentication required.
        """
        if message is None:
            message = "Proxy Authentication Required"
        return self._generate_response(
            status.HTTP_407_PROXY_AUTHENTICATION_REQUIRED, message, data, success=False, **kwargs
        )

    def request_timeout_408(self, message=None, data=None, **kwargs):
        """
        Set the message to "Request Timeout" if message is None and returns a response with status code 408.

        :param message: (str) The message to be included in the response.
        :param data: (Any) Additional data to be included in the response.
        :param kwargs: (Any) Additional keyword arguments to be passed to _generate_response.
        :return: (Response) The response generated with status code 408.
        """
        if message is None:
            message = "Request Timeout"
        return self._generate_response(status.HTTP_408_REQUEST_TIMEOUT, message, data, success=False, **kwargs)

    def conflict_409(self, message=None, data=None, **kwargs):
        """
        Handle the 409 Conflict status code response.

        :param message: str, the message to be included in the response
        :param data: dict, additional data to be included in the response
        :param kwargs: additional keyword arguments
        :return: the response generated with status 409 Conflict
        """
        if message is None:
            message = "Conflict"
        return self._generate_response(status.HTTP_409_CONFLICT, message, data, success=False, **kwargs)

    def gone_410(self, message=None, data=None, **kwargs):
        """
        Return this function to generate a response with status 410 (Gone) along with a message and optional data.

        :param message: A custom message for the response. Defaults to "Gone" if not provided.
        :param data: Optional data to include in the response.
        :param kwargs: Additional keyword arguments to pass to the _generate_response method.
        :return: The response generated with status 410 (Gone), the provided message, optional data, and success set to False.
        """
        if message is None:
            message = "Gone"
        return self._generate_response(status.HTTP_410_GONE, message, data, success=False, **kwargs)

    def length_required_411(self, message=None, data=None, **kwargs):
        """
        Generate a response with a status code of 411 Length Required, along with a message and additional data.

        :param message: (str) The message to be included in the response, defaults to "Length Required"
        :param data: (dict) Additional data to be included in the response
        :param kwargs: Additional keyword arguments
        :return: The response with the specified status code, message, data, and success status set to False
        """
        if message is None:
            message = "Length Required"
        return self._generate_response(status.HTTP_411_LENGTH_REQUIRED, message, data, success=False, **kwargs)

    def precondition_failed_412(self, message=None, data=None, **kwargs):
        """
        Generate a response for a precondition failed (HTTP 412) status code.

        :param message: A custom error message (default: "Precondition Failed")
        :param data: Additional data to include in the response
        :param kwargs: Additional keyword arguments to pass to _generate_response
        :return: The response generated for the precondition failed status code
        """
        if message is None:
            message = "Precondition Failed"
        return self._generate_response(status.HTTP_412_PRECONDITION_FAILED, message, data, success=False, **kwargs)

    def request_entity_too_large_413(self, message=None, data=None, **kwargs):
        """
        Generate a response for a 413 Request Entity Too Large error.

        :param message: A custom error message (default: "Request Entity Too Large")
        :param data: Additional data to include in the response
        :param kwargs: Additional keyword arguments to pass to _generate_response
        :return: The response generated for the 413 error
        """
        if message is None:
            message = "Request Entity Too Large"
        return self._generate_response(status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, message, data, success=False, **kwargs)

    def request_uri_too_long_414(self, message=None, data=None, **kwargs):
        """
        Generate a response for a Request-URI Too Long error.

        :param message: A custom error message (default is "Request-URI Too Long")
        :param data: Additional data to be included in the response
        :param kwargs: Additional keyword arguments
        :return: The generated response
        """
        if message is None:
            message = "Request-URI Too Long"
        return self._generate_response(status.HTTP_414_REQUEST_URI_TOO_LONG, message, data, success=False, **kwargs)

    def unsupported_media_type_415(self, message=None, data=None, **kwargs):
        """
        Return this function that handles the unsupported media type error (HTTP 415).

        It takes an optional error message and data, as well as additional keyword arguments.
        Returns a response generated with the provided message, data, and additional arguments.
        """
        if message is None:
            message = "Unsupported Media Type"
        return self._generate_response(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, message, data, success=False, **kwargs)

    def requested_range_not_satisfiable_416(self, message=None, data=None, **kwargs):
        """
        Generate a response for a requested range not satisfiable error.

        :param message: The error message to be included in the response
        :param data: Additional data to be included in the response
        :param kwargs: Additional keyword arguments
        :return: The generated response for the requested range not satisfiable error
        """
        if message is None:
            message = "Requested Range Not Satisfiable"
        return self._generate_response(
            status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE, message, data, success=False, **kwargs
        )

    def expectation_failed_417(self, message=None, data=None, **kwargs):
        """
        Return this function that handles the HTTP 417 Expectation Failed status code.

        It takes in an optional message and data, and any additional keyword arguments.
        Returns the response generated with the 417 status code, message, data, and success=False.
        """
        if message is None:
            message = "Expectation Failed"
        return self._generate_response(status.HTTP_417_EXPECTATION_FAILED, message, data, success=False, **kwargs)

    def misdirected_request_421(self, message=None, data=None, **kwargs):
        """
        Generate a misdirected request response.

        :param message: Optional message for the response
        :param data: Optional data for the response
        :param **kwargs: Additional keyword arguments for the response
        :return: Response generated with status code 421 (Misdirected Request)
        """
        if message is None:
            message = "Misdirected Request"
        return self._generate_response(status.HTTP_421_MISDIRECTED_REQUEST, message, data, success=False, **kwargs)

    def unprocessable_entity_422(self, message=None, data=None, **kwargs):
        """
        Handle Unprocessable Entity error and generate the corresponding response.

        :param message: Optional message for the error
        :param data: Optional data to include in the response
        :param kwargs: Additional keyword arguments
        :return: Response with status 422 and error message
        """
        if message is None:
            message = "Unprocessable Entity"
        return self._generate_response(status.HTTP_422_UNPROCESSABLE_ENTITY, message, data, success=False, **kwargs)

    def locked_423(self, message=None, data=None, **kwargs):
        """
        Generate a response with HTTP status code 423 (Locked) including optional message and data.

        :param message: Optional message to include in the response (default is "Locked")
        :param data: Optional data to include in the response
        :param kwargs: Additional keyword arguments to pass to _generate_response
        :return: Response generated with status code 423 (Locked)
        """
        if message is None:
            message = "Locked"
        return self._generate_response(status.HTTP_423_LOCKED, message, data, success=False, **kwargs)

    def failed_dependency_424(self, message=None, data=None, **kwargs):
        """
        Handle the 424 Failed Dependency error response.

        :param message: (str) The error message
        :param data: (dict) Additional data to be returned with the error
        :param kwargs: (dict) Additional keyword arguments
        :return: (HttpResponse) The generated error response
        """
        if message is None:
            message = "Failed Dependency"
        return self._generate_response(status.HTTP_424_FAILED_DEPENDENCY, message, data, success=False, **kwargs)

    def too_early_425(self, message=None, data=None, **kwargs):
        """
        Generate a response with status 425 (Too Early) and the provided message and data.

        :param message: (str) The message to be included in the response. Defaults to "Too Early" if not provided.
        :param data: (any) Additional data to be included in the response.
        :param kwargs: (any) Additional keyword arguments to be included in the response.
        :return: (HttpResponse) The generated response with status 425 (Too Early).
        """
        if message is None:
            message = "Too Early"
        return self._generate_response(status.HTTP_425_TOO_EARLY, message, data, success=False, **kwargs)

    def upgrade_required_426(self, message=None, data=None, **kwargs):
        """
        Generate a 426 Upgrade Required response with the given message and data.

        :param message: The message to include in the response (default: "Upgrade Required")
        :param data: Additional data to include in the response
        :param kwargs: Additional keyword arguments to pass to the response generator
        :return: The generated response with status code 426, the provided message, data, and success=False
        """
        if message is None:
            message = "Upgrade Required"
        return self._generate_response(status.HTTP_426_UPGRADE_REQUIRED, message, data, success=False, **kwargs)

    def precondition_required_428(self, message=None, data=None, **kwargs):
        """
        Generate a response with a status code of 428 (Precondition Required) and the provided message and data.

        :param message: The message to include in the response (default: "Precondition Required")
        :param data: Additional data to include in the response
        :param kwargs: Additional keyword arguments to be passed to the _generate_response method
        :return: The generated response
        """
        if message is None:
            message = "Precondition Required"
        return self._generate_response(status.HTTP_428_PRECONDITION_REQUIRED, message, data, success=False, **kwargs)

    def too_many_requests_429(self, message=None, data=None, **kwargs):
        """
        Handle Too Many Requests error and generate a response.

        :param message: (str) The error message, defaults to "Too Many Requests"
        :param data: (dict) Additional data to include in the response
        :param kwargs: (dict) Additional keyword arguments
        :return: The response generated with status code 429 and provided data
        """
        if message is None:
            message = "Too Many Requests"
        return self._generate_response(status.HTTP_429_TOO_MANY_REQUESTS, message, data, success=False, **kwargs)

    def request_header_fields_too_large_431(self, message=None, data=None, **kwargs):
        """
        Generate a response for the Request Header Fields Too Large error with the given message and data.

        :param message: The error message to be included in the response (default: "Request Header Fields Too Large")
        :param data: Additional data to be included in the response
        :param kwargs: Additional keyword arguments
        :return: The generated response
        """
        if message is None:
            message = "Request Header Fields Too Large"
        return self._generate_response(
            status.HTTP_431_REQUEST_HEADER_FIELDS_TOO_LARGE, message, data, success=False, **kwargs
        )

    def unavailable_for_legal_reasons_451(self, message=None, data=None, **kwargs):
        """
        Generate a response for the 451 Unavailable For Legal Reasons status code.

        :param message: Optional message to include in the response
        :param data: Optional data to include in the response
        :param kwargs: Additional keyword arguments
        :return: Response object with the 451 status code
        """
        if message is None:
            message = "Unavailable For Legal Reasons"
        return self._generate_response(
            status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS, message, data, success=False, **kwargs
        )

        # Server errors

    def internal_server_error_500(self, message=None, data=None, **kwargs):
        """
        Handle internal server error and generate response with status 500.

        :param message: str, optional - Error message
        :param data: dict, optional - Additional data to include in the response
        :param **kwargs: any - Additional keyword arguments

        :return: Response - HTTP 500 Internal Server Error response
        """
        if message is None:
            message = "Internal Server Error"
        return self._generate_response(status.HTTP_500_INTERNAL_SERVER_ERROR, message, data, success=False, **kwargs)

    def not_implemented_501(self, message=None, data=None, **kwargs):
        """
        Generate a 501 Not Implemented response with the given message and data.

        :param message: The message to include in the response
        :param data: Additional data to include in the response
        :param kwargs: Additional keyword arguments
        :return: The generated response
        """
        if message is None:
            message = "Not Implemented"
        return self._generate_response(status.HTTP_501_NOT_IMPLEMENTED, message, data, success=False, **kwargs)

    def bad_gateway_502(self, message=None, data=None, **kwargs):
        """
        Handle Bad Gateway error and generate a response.

        :param message: The error message (default is "Bad Gateway")
        :param data: Additional data to include in the response
        :param kwargs: Additional keyword arguments
        :return: The generated response
        """
        if message is None:
            message = "Bad Gateway"
        return self._generate_response(status.HTTP_502_BAD_GATEWAY, message, data, success=False, **kwargs)

    def service_unavailable_503(self, message=None, data=None, **kwargs):
        """
        Handle Service Unavailable error by generating a response with status 503.

        :param message: (optional) A custom error message, defaults to "Service Unavailable"
        :param data: (optional) Additional data to include in the response
        :param kwargs: Additional keyword arguments for future use
        :return: Response with status 503 and custom message
        """
        if message is None:
            message = "Service Unavailable"
        return self._generate_response(status.HTTP_503_SERVICE_UNAVAILABLE, message, data, success=False, **kwargs)

    def gateway_timeout_504(self, message=None, data=None, **kwargs):
        """
        Generate a gateway timeout response with the specified message and data.

        :param message: The message for the gateway timeout response. Defaults to "Gateway Timeout" if not provided.
        :param data: Additional data to be included in the response.
        :param kwargs: Additional keyword arguments to be passed to _generate_response.
        :return: The generated gateway timeout response.
        """
        if message is None:
            message = "Gateway Timeout"
        return self._generate_response(status.HTTP_504_GATEWAY_TIMEOUT, message, data, success=False, **kwargs)

    def http_version_not_supported_505(self, message=None, data=None, **kwargs):
        """
        Return this function generates a response for the HTTP 505 (HTTP Version Not Supported) status code.

        It takes an optional message and data, along with additional keyword arguments.
        It returns the response generated by the _generate_response method.
        """
        if message is None:
            message = "HTTP Version Not Supported"
        return self._generate_response(
            status.HTTP_505_HTTP_VERSION_NOT_SUPPORTED, message, data, success=False, **kwargs
        )

    def variant_also_negotiates_506(self, message=None, data=None, **kwargs):
        """
        Return this function that handles the variant also negotiates 506 status code.

        It takes an optional message and data as parameters, along with additional keyword arguments.
        It returns the response generated using the input parameters.
        """
        if message is None:
            message = "Variant Also Negotiates"
        return self._generate_response(status.HTTP_506_VARIANT_ALSO_NEGOTIATES, message, data, success=False, **kwargs)

    def insufficient_storage_507(self, message=None, data=None, **kwargs):
        """
        Return function that handles insufficient storage error with an optional message and data.

        :param message: (str) The error message. Defaults to "Insufficient Storage" if not provided.
        :param data: (Any) Additional data related to the error. Defaults to None.
        :param **kwargs: Additional keyword arguments.
        :return: The response generated by the _generate_response method with status code 507, the provided message, data, and success=False.
        """
        if message is None:
            message = "Insufficient Storage"
        return self._generate_response(status.HTTP_507_INSUFFICIENT_STORAGE, message, data, success=False, **kwargs)

    def loop_detected_508(self, message=None, data=None, **kwargs):
        """
        Return this function generates a response with status code 508 (Loop Detected) and the provided message and data.

        It takes optional parameters for message and data, which default to None, and any additional keyword arguments.
        It returns the response generated by the _generate_response method with the provided parameters.
        """
        if message is None:
            message = "Loop Detected"
        return self._generate_response(status.HTTP_508_LOOP_DETECTED, message, data, success=False, **kwargs)

    def bandwidth_limit_exceeded_509(self, message=None, data=None, **kwargs):
        """
        Check if the bandwidth limit has been exceeded and generate a response with the appropriate status code.

        :param message: Optional message to include in the response
        :param data: Optional data to include in the response
        :param kwargs: Additional keyword arguments
        :return: Response generated with the appropriate status code
        """
        if message is None:
            message = "Bandwidth Limit Exceeded"
        return self._generate_response(status.HTTP_509_BANDWIDTH_LIMIT_EXCEEDED, message, data, success=False, **kwargs)

    def not_extended_510(self, message=None, data=None, **kwargs):
        """Generate a response with status HTTP 510 Not Extended, message, and data."""
        if message is None:
            message = "Not Extended"
        return self._generate_response(status.HTTP_510_NOT_EXTENDED, message, data, success=False, **kwargs)

    def network_authentication_required_511(self, message=None, data=None, **kwargs):
        """
        Perform network authentication and generate a response with the specified message and data.

        :param message: The message to be included in the response. Defaults to "Network Authentication Required" if not provided.
        :param data: Additional data to be included in the response.
        :param kwargs: Additional keyword arguments to be included in the response.
        :return: The response generated with the specified status code, message, and additional data.
        """
        if message is None:
            message = "Network Authentication Required"
        return self._generate_response(
            status.HTTP_511_NETWORK_AUTHENTICATION_REQUIRED, message, data, success=False, **kwargs
        )
