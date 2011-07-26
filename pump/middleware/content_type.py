# A middleware that adds a content_type key to the response.

import mimetypes
from pump.util import response

def wrap_content_type(app, options={}):
  def wrapped_app(req):
    resp = app(req)
    if not resp or resp.get("headers", {}).get("content_type"):
      return resp
    mime_type, _ = mimetypes.guess_type(req["uri"])
    return response.with_content_type(resp,
      mime_type or "application/octet-stream")

  return wrapped_app