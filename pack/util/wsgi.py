"Methods for converting between Pack apps and WSGI apps."

import threading
from pack.util.response import skeleton

def build_app(wsgi_app):
  "Convert a WSGI app to a Pack app."
  def app(request):
    # A thread-local storage is required here, because of the way WSGI is
    # implemented (start_response in particular).  As far as I can tell,
    # it's necessary to give the WSGI app a custom start_response function
    # that just saves the status and headers to a thread-local variable.
    # Then we combine these with the body, returned by the WSGI app, to build
    # the Pack response.
    data = threading.local()
    def start_response(status, headers, _=None):
      data.status = status
      data.headers = headers

    body = wsgi_app(build_wsgi_request(request), start_response)
    return build_response((data.status, data.headers, body))
  return app

def build_request(wsgi_req):
  "Convert a WSGI request (environ) to a Pack request."
  return dict({
    'uri':     wsgi_req.get('RAW_URI') or wsgi_req.get('PATH_INFO'),
    'scheme':  wsgi_req.get('wsgi.url_scheme'),
    'method':  wsgi_req.get('REQUEST_METHOD', 'get').lower(),
    'headers': get_headers(wsgi_req),
    'body':    wsgi_req.get('wsgi.input')
  }, **dict([(k.lower(), v) for k, v in wsgi_req.iteritems()]))

def build_response(wsgi_response):
  "Convert a WSGI response to a Pack response."
  status, headers, body = wsgi_response
  return {
    "status":  int(status[:3]),
    "headers": dict([(k.replace("-", "_"), v) for k, v in headers]),
    "body":    body}

def build_middleware(wsgi_middleware, *args):
  """
  Converts a WSGI middleware into Pack middleware.  You can pass additional
  arguments which will be passed to the middleware given.
  """
  def middleware(app):
    return build_app(wsgi_middleware(build_wsgi_app(app), *args))
  return middleware

def build_wsgi_app(app):
  "Convert a Pack app to a WSGI app."
  def wsgi_app(request, start_response, _=None):
    response = app(build_request(request)) or {}
    response_map = dict(skeleton, **response)
    return build_wsgi_response(response_map, start_response)
  return wsgi_app

def build_wsgi_request(request):
  "Convert a Pack request to a WSGI request."
  wsgi_request = {
    "SERVER_PORT":     request.get("server_port"),
    "SERVER_NAME":     request.get("server_name"),
    "REMOTE_ADDR":     request.get("remote_addr"),
    "RAW_URI":         request.get("uri"),
    "PATH_INFO":       request.get("uri"),
    "QUERY_STRING":    request.get("query_string"),
    "wsgi.url_scheme": request.get("scheme"),
    "REQUEST_METHOD":  request.get("method", "GET").upper(),
    "CONTENT_TYPE":    request.get("content_type"),
    "CONTENT_LENGTH":  request.get("content_length"),
    "wsgi.input":      request.get("body")}
  for key, value in request.get("headers", {}).iteritems():
    wsgi_request["HTTP_%s" % key.upper()] = value

  for key, value in request.iteritems():
    if key.upper() not in wsgi_request:
      wsgi_request[key] = value

  return wsgi_request

def build_wsgi_response(response_map, start_response):
  "Convert a Pack response to a WSGI response."
  response = {}
  response = set_status(response, response_map["status"])
  response = set_headers(response, response_map["headers"])
  response = set_body(response, response_map["body"])

  start_response(response["status"], response["headers"])
  return response["body"]

def get_headers(request):
  return dict([(k.replace('HTTP_', '').lower(), v) for k, v in request.items()
    if k.startswith('HTTP_')])

def set_status(response, status):
  status_map = {
    200: "200 OK",
    301: "301 Moved Permanently",
    302: "302 Found",
    303: "303 See Other",
    304: "304 Not Modified",
    307: "307 Temporary Redirect",
    400: "400 Bad Request",
    401: "401 Unauthorized",
    403: "403 Forbidden",
    404: "404 Not Found",
    405: "405 Method Not Allowed",
    418: "418 I'm a teapot",
    500: "500 Internal Server Error",
    502: "502 Bad Gateway",
    503: "503 Service Unavailable",
    504: "504 Gateway Timeout"}

  response["status"] = status_map.get(status, str(status))
  return response

def set_headers(response, headers):
  response["headers"] = [(k.replace('_', '-').title(), v)
    for k, v in headers.items()]
  return response

def set_body(response, body):
  if isinstance(body, str) or isinstance(body, unicode):
    response["body"] = body
  elif isinstance(body, list):
    response["body"] = ''.join(body)
  elif isinstance(body, file):
    response["body"] = body.read()
  elif not body:
    response["body"] = ""
  else:
    raise Exception("Unrecognized body: %s" % repr(body))

  return response