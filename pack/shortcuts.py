def _make_shortcut_for(method):
  return lambda p, h: (method, p, h)

GET, POST, PUT, DELETE = [_make_shortcut_for(m) for m in [
  'GET', 'POST', 'PUT', 'DELETE']]