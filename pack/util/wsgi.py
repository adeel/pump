"Methods for converting between Pack apps and WSGI apps."

from pack.util.response import skeleton

def build(app):
  "Turns a Pack app into a WSGI app."

  def wsgi_app(request, start_response):
    response_map = dict(skeleton, **app(build_request_map(request)))
    return build_wsgi_response(response_map, start_response)
  return wsgi_app

def build_request_map(request):
  "Create a Pack request map from the WSGI request (environ variable)."

  return {
    'server_port':    request.get('SERVER_PORT'),
    'server_name':    request.get('SERVER_NAME'),
    'remote_addr':    request.get('REMOTE_ADDR'),
    'uri':            request.get('RAW_URI') or request.get('PATH_INFO'),
    'query_string':   request.get('QUERY_STRING', ''),
    'scheme':         request.get('wsgi.url_scheme'),
    'method':         request.get('REQUEST_METHOD', 'get').lower(),
    'headers':        get_headers(request),
    'content_type':   request.get('CONTENT_TYPE'),
    'content_length': request.get('CONTENT_LENGTH'),
    'body':           request.get('wsgi.input'),
  }

def get_headers(request):
  return dict([(k.replace('HTTP_', '').lower(), v) for k, v in request.items()
    if k.startswith('HTTP_')])

def build_wsgi_response(response_map, start_response):
  "Create a WSGI response from a Pack response map."

  response = {}
  response = set_status(response, response_map["status"])
  response = set_headers(response, response_map["headers"])
  response = set_body(response, response_map["body"])

  start_response(response["status"], response["headers"])
  return response["body"]

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
    504: "504 Gateway Timeout"
  }

  response["status"] = status_map.get(status, str(status))
  return response

def set_headers(response, headers):
  response["headers"] = [(k.replace('_', '-').title(), v)
    for k, v in headers.items()]
  return response

def set_body(response, body):
  if isinstance(body, str):
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