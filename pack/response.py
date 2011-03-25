import environment

default = {'status': 200, 'headers': {'Content-Type': 'text/html'},
  'body': ""}

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

def get(e, route_map):
  handler, url_params = environment.get_handler_for_request(e, route_map)

  if not handler:
    response = {'status': 404, 'body': "<h1>Not Found</h1>"}
  elif isinstance(handler, dict):
    response = handler
  else:
    response = {'body': handler}

  response = dict(default, **response)

  if callable(response['body']):
    try:
      response = (response['body'])(e, *url_params)
      if not isinstance(response, dict):
        response = dict(default, **{'body': str(response)})
    except Exception, exc:
      print exc
      response = dict(response, **{
        'status': 500, 'body': "<h1>Internal Server Error</h1>"})

  return response

def to_wsgi(r, start_response):
  status = r['status']
  if status_map.get(status):
    status = status_map[status]

  # No one understands this.
  start_response(status, r['headers'].items())

  return [r['body']]

def error(code):
  return dict(default, **{"status": code,
    "body": "<h1>%s</h1>" % status_map.get(code)})
