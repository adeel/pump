"A middleware that adds cookie support."

from Cookie import SimpleCookie as Cookie
from pack.util import codec

# TODO: When there are multiple cookies, it inserts "Set-Cookie" before each one.

def wrap_cookies(app):
  """
  A middleware that parses the cookies in the request map and assigns the
  resulting dict to the "cookies" key of the request.  If the response dict
  contains a cookies key, whose value is a dict with name-value pairs, then
  those cookies will be sent to the browser with the response.
  """
  def wrapped_app(request):
    if not request.get('cookies'):
      request["cookies"] = parse_cookies(request)
    response = app(request)
    response = set_cookies(response)
    return response
  return wrapped_app

def parse_cookies(request):
  "Parse the cookies from a request."
  cookie = request["headers"].get("cookie")
  return Cookie(cookie)

def set_cookies(response):
  "Add a set_cookie header to the response if it has a \"cookies\" key."
  cookies = response.get("cookies")
  if not cookies:
    return response
  response["headers"]["set_cookie"] = write_cookies(cookies)
  del response["cookies"]
  return response

def write_cookies(cookies):
  "Turn a dict of cookies into a list of strings for the set_cookie header."
  cookie = Cookie()
  for key, val in cookies.items():
    if isinstance(val, dict):
      cookie[key] = val["value"]
      for val_key, val_val in val.items():
        if val_key != "value":
          cookie[key][val_key] = val_val
    else:
      cookie[key] = val
  return cookie.output()