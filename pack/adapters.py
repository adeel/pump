from pack.util import wsgi

default_options = {
  "host": "127.0.0.1",
  "port": 8000,
  "server_name": "Pack"}

def serve_with_paste(app, options={}):
  "Serve a Pack app with the WSGI server from Paste."
  wsgi_app = wsgi.build_wsgi_app(app)
  options = dict(default_options, **options)

  from paste.httpserver import serve
  return serve(wsgi_app, **_get_paste_config(options))

def _get_paste_config(options):
  options["server_version"] = options.get("server_name")
  del options["server_name"]
  return options