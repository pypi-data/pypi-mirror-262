# Prema Django

premadjango is a Python package designed to streamline the setup of new Django projects by providing default configurations and settings.

## Installation

You can install premadjango via pip:

pip install premadjango

## Features

### Field Validators

premadjango includes a collection of Django model field validators to ensure data integrity and consistency. These validators cover common validation scenarios and help maintain data quality within your Django models.

#### Basic Usage

from premadjango.models.field_validators import email_validator

class MyModel(models.Model):
    email = models.EmailField(validators=[email_validator])

### Field Converts

premadjango offers a variety of Django model field converters to transform field values into desired formats, such as lowercase, uppercase, etc. These converters help standardize data representation and facilitate data manipulation.

#### Basic Usage

from premadjango.models.field_converts import LowercaseCharField

class MyModel(models.Model):
    name = LowercaseCharField(max_length=100)

### Middleware

The package includes middleware components to enhance the functionality of Django projects. One such middleware is DisableClientSideCachingMiddleware, which disables client-side caching to ensure the most up-to-date content is served to users.

#### Basic Usage

To disable client-side caching, add the middleware to your MIDDLEWARE setting in the Django project's settings.py file:

MIDDLEWARE = [
    # Other middleware classes...
    'premadjango.middleware.DisableClientSideCachingMiddleware',
]

## Response handlers

Custom response handlers in Django Rest Framework (DRF) are used to customize the structure and content of HTTP responses returned by API endpoints. By defining custom response handlers, we can standardize the response format, include additional metadata, and handle common scenarios consistently across the API.


### Why Use Custom Response Handlers?
Standardized Response Format: Custom response handlers allow us to define a standardized response format for our API. This consistency makes it easier for frontend developers to understand and handle API responses.

Include Metadata: We can include additional metadata in the response, such as status codes, error messages, pagination information, and timestamps. This metadata provides valuable context to the consumers of the API.

Handle Common Scenarios: Custom response handlers enable us to handle common scenarios, such as pagination, authentication errors, and validation failures, in a centralized and consistent manner. This reduces code duplication and simplifies maintenance.

### Fields Added to the Response
The custom response handler included in this project adds the following fields to the HTTP response:

`Status`: The HTTP status code indicating the success or failure of the request.

`Message`: An optional message providing additional context about the response. This field is useful for conveying success messages or error descriptions.

`Total`: The total number of objects in the queryset, used for pagination purposes.

`Page`: The current page number in the paginated results.

`Next`: The page number of the next page in the paginated results. This field helps users navigate through the paginated data.

`Last Page`: The page number of the last page in the paginated results. This field provides information about the total number of pages available.

`Data`: The serialized data for the current page of results. This field contains the actual objects returned by the API endpoint.

## Conclusion

With premadjango, setting up new Django projects becomes more efficient and straightforward. By leveraging its default configurations, field validators, converters, and middleware, developers can focus more on building their applications rather than configuring project settings from scratch.
