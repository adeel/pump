# Pump specification

The Pump specification consists of headers, requests, responses, apps, and middleware.

## Pump headers

**Pump headers** are closely related to HTTP headers.

A Pump header is represented as a key-value pair.  An HTTP header name and value can be transformed into a Pump header by stripping "HTTP_" from the beginning of the name and downcasing; the value stays the same.  A Pump header is transformed into an HTTP header by exactly the reverse operation.

## Pump requests

**Pump requests** are an abstraction of HTTP requests.

A pump request is a dictionary with the following keys.

**server_port** (str, required).  The port on which the request is being handled.

**server_name** (str, required).  The resolved server name, or the server IP address.

**remote_addr** (str, required).  The IP address of the client or the last proxy that sent the request.

**uri** (str, required).  The request URI.  Starts with '/'.

**query_string** (str, optional).  The portion of the request URI that follows the '?'.

**scheme** (str, required).  The transport protocol: "http" or "https".

**method** (str, required).  The HTTP request method: "get", "head", "options", "put", "post", or "delete".

**content_type** (str, optional).  The MIME type of the request body, if known.

**content_length** (int, optional).  The number of bytes in the request body, if known.

**character_encoding** (str, optional).  The character encoding used in the request body, if known.

**headers** (dict, required).  A dict of Pump headers in the request.  In case two headers have the same key, they are merged into one header whose value is a list containing both of their values.

**body** (input stream, optional).  A file-like object containing the request body, if present.

## Pump responses

**Pump responses** are an abstraction of HTTP responses.

A Pump response is a dictionary with the following keys.

**status** (int, required).  The HTTP status code (e.g. 200 or 404).

**headers** (dict, required).  A dict containing the Pump headers in the response (e.g. {"content_type": "text/html"}).  In case the value of some header is a list, the corresponding HTTP response will have multiple headers for each value in the list.

**body** (str or list or file, optional).  The response body.  If it is a string, it will be sent as is.  If it is a list, each element will be sent as a string.  If it is a file, its contents are sent.

## Pump apps

A **Pump app** is a function that takes a Pump request and returns a Pump response.

## Pump middleware

A **Pump middleware** is a higher-order function that takes a Pump app and returns a Pump app.