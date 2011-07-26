# A middleware for serving static files that is more selective than
# pump.middleware.file.

from pump.middleware.file import *

# Wrap the app so that if the request URL falls under any of the URLs in
# static_urls (the URL must start with one of the static_urls), it looks in
# public_dir for a file corresponding to the request URL.  If no such file is
# not found, the request is handled normally.
# 
# Note that the paths in static_urls should include the leading '/'.
def wrap_static(app, public_dir, static_urls):
  app_with_file = wrap_file(app, public_dir)
  def wrapped_app(req):
    if any([req["uri"].startswith(s) for s in static_urls]):
      return app_with_file(req)
    else:
      return app(req)
  return wrapped_app