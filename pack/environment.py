import re
import cgi
import urlparse

parse_qs = urlparse.parse_qs or cgi.parse_qs

import route

def path(e):
  return e.get('PATH_INFO', '')

def query_string(e):
  return e.get('QUERY_STRING', '')

def full_path(e):
  if not query_string(e):
    return path(e)
  return "%s?%s" % (path(e), query_string(e))

def method(e):
  return e.get('REQUEST_METHOD', 'GET').upper()

def params(e):
  # merge
  params = dict(_parse_get_params(e), **_parse_post_params(e))

  # parses fields like a[b] into dictionaries
  params = _parse_dict_params(params)

  return params

def get_handler_for_request(e, route_map):
  "Returns (handler, url_arguments) or (None, [])."

  for r, handler in route_map.iteritems():
    if route.method(r) == method(e):
      match = re.search(route.pattern(r), path(e), re.I)
      if match is not None:
        return handler, list(match.groups())
  return None, []

def _parse_get_params(e):
  parsed = parse_qs(query_string(e), keep_blank_values=True)
  params = {}
  for key, val in parsed.items():
    if len(val) == 0:
      params[key] = ''
    elif len(val) == 1:
      params[key] = val[0]
    else:
      params[key] = val
  return params

def _parse_post_params(e):
  parsed = cgi.FieldStorage(fp=e.get('wsgi.input'), environ=e,
                            keep_blank_values=True)
  params = {}
  for key in parsed:
    val = parsed[key]
    if hasattr(val, 'filename') and val.filename:
      params[key] = val
    elif (isinstance(val, cgi.FieldStorage) or
          isinstance(val, cgi.MiniFieldStorage)):
      params[key] = val.value
    else:
      params[key] = [f.value for f in val]
  return params

def _parse_dict_params(p):
  # There must be a better way...

  params = {}
  for key, value in p.iteritems():
    d = _parse_param_as_dict(key, value)
    for k, v in d.iteritems():
      if isinstance(v, dict):
        if not params.get(k):
          params[k] = {}
        params[k] = _recursive_dict_update(params[k], v)
      elif isinstance(v, list):
        if not params.get(k):
          params[k] = []
        params[k].extend(v)
      else:
        params[k] = v

  return params

def _parse_param_as_dict(key, value):
  # I'm not proud of this.

  match = re.compile('^(.+)\[([^\[\]]*)\]$').match(key)
  if not match:
    return {key: value}

  k, v = match.groups()
  if v == '':
    if isinstance(value, list):
      return _parse_param_as_dict(k, value)
    return _parse_param_as_dict(k, [value])

  return _parse_param_as_dict(k, {v: value})

def _recursive_dict_update(x, y):
  for key, val in y.iteritems():
    if isinstance(val, dict):
      if not x.has_key(key):
        x[key] = {}
      x[key] = _recursive_dict_update(x[key], val)
    elif isinstance(val, list):
      if not x.has_key(key):
        x[key] = []
      x[key].extend(val)
    else:
      x[key] = val
  return x
