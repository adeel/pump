"A middleware that adds cookie support."

from Cookie import SimpleCookie as Cookie
from pump.util import codec

def wrap_cookies(app):
  """
  Adds a "cookies" key to the request, which contains a dictionary containing
  any cookies sent by the client.  If any new values are found in the
  dictionary after your app is called, the new cookies are sent to the client.
  The values in the dict will be converted to strings, unless they are
  themselves dicts.  In that case, the "value" key will be used as the cookie
  value and the other keys will be interpreted as cookie attributes.

    request["cookies"] = {"a": {"value": "b", "path": "/"}}

  Note: if a cookie is set and is later deleted from request["cookies"], the
  corresponding cookie will not automatically be deleted.  You need to set the
  "expires" attribute of the cookie to a time in the past.
  """
  def wrapped_app(request):
    # Get any cookies from the request.
    req_cookies = request.get("cookies")
    if not req_cookies:
      req_cookies = _parse_cookies(request)
    request["cookies"] = req_cookies

    response = app(request)

    # If the app modified request["cookies"], set the new cookies.
    updated_cookies = request.get("cookies", {}).copy()
    cookie_header = []
    for k, v in updated_cookies.iteritems():
      v = str(v)
      if k not in req_cookies or req_cookies[k] != v:
        cookie_header.append(_format_cookie(k, v))

    response.setdefault("headers", {})["set_cookie"] = cookie_header
    return response
  return wrapped_app

def _parse_cookies(request):
  "Parse the cookies from a request into a dictionary."
  cookie = Cookie(request["headers"].get("cookie"))
  parsed = {}
  for k, v in cookie.iteritems():
    parsed[k] = v.value
  return parsed

def _format_cookie(key, val):
  """
  Formats the dict of cookies for the set_cookie header.  If a value is a dict,
  its "value" key will be used as the value and the other keys will be
  interpreted as cookie attributes.
  """
  if not isinstance(val, dict):
    val = {"value": val}

  cookie = Cookie()
  cookie[key] = val["value"]
  del val["value"]

  morsel = cookie[key]
  for k, v in val.iteritems():
    morsel[k] = v
  return morsel.OutputString()