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

def to_wsgi(r, start_response):
  status = r['status']
  if status_map.get(status):
    status = status_map[status]

  # No one understands this.
  start_response(status, r['headers'].items())

  return [r['body']]
