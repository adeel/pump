"A middleware for parsing GET and POST params."

import re
from pack.util import codec

def wrap_params(app, options={}):
  """
  Middleware to parse GET and POST params.  Adds the following keys to the
  request map:

    -- get_params
    -- post_params
    -- params

  You can specify an encoding to decode the URL-encoded params with.  If not
  specified, uses the character encoding specified in the request, or UTF-8 by
  default.
  """
  def wrapped_app(request):
    encoding = (options.get('encoding') or request.get('character_encoding')
            or ("utf8"))
    if not request.get('get_params'):
      request = parse_get_params(request, encoding)
    if not request.get('post_params'):
      request = parse_post_params(request, encoding)
    return app(request)

  return wrapped_app

def parse_get_params(request, encoding):
  "Parse params from the query string."

  if request.get("query_string"):
    params = parse_params(request["query_string"], encoding)
  else:
    params = {}

  return _recursive_merge(request, {'get_params': params, 'params': params})

def parse_post_params(request, encoding):
  "Parse params from the request body."

  if _does_have_urlencoded_form(request) and request.get("body"):
    params = parse_params(request["body"].read(), encoding)
  else:
    params = {}

  return _recursive_merge(request, {'post_params': params, 'params': params})

def parse_params(params_string, encoding):
  "Parse params from a string (e.g. \"a=b&c=d\") into a map."

  def _parse(params_dict, encoded_param):
    match = re.compile(r'([^=]+)=(.*)').match(encoded_param)
    if not match:
      return params_dict
    key, val = match.groups()
    return set_param(params_dict,
      codec.url_decode(key, encoding), codec.url_decode(val or '', encoding))

  return reduce(_parse, params_string.split('&'), {})

def set_param(params, key, val):
  "Set a value for a key.  If it already has a value, make a list of values."

  cur = params.get(key)
  if cur:
    if isinstance(cur, list):
      params[key].append(val)
    else:
      params[key] = [cur, val]
  else:
    params[key] = val
  return params

def _does_have_urlencoded_form(request):
  "Check whether a urlencoded form was submitted."

  return request.get('content_type', '').startswith(
    'application/x-www-form-urlencoded')

def _recursive_merge(x, y):
  "Merge two dictionaries recursively."

  z = x.copy()
  for key, val in y.iteritems():
    if isinstance(val, dict):
      if not z.has_key(key):
        z[key] = {}
      z[key] = _recursive_merge(z[key], val)
    else:
      z[key] = val
  return z
