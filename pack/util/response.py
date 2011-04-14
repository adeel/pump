import os

skeleton = {"status": 200, "headers": {}, "body": ""}

def with_body(body):
  "Return a skeleton response with the given body."
  return dict(skeleton, body=body)

def redirect(url):
  "Return a redirect response to the given URL."
  return {"status": 302, "headers": {"Location": url}, "body": ""}

def with_status(response, status):
  "Return the given response updated with the given status."
  return dict(response, status=status)

def with_header(response, key, value):
  "Return the given response updated with the given header."
  return dict(response,
    headers=dict(response.get("headers", {}), key=value))

def with_content_type(response, content_type):
  "Return the given response updated with the given content-type."
  return with_header(response, 'content_type', content_type)

def file_response(path, options={}):
  file = _get_file(path, options)
  if file:
    return skeleton_with_body(open(file, 'r'))

def _get_file(path, options={}):
  root = options.get('root')
  if root:
    if _is_path_safe(root, path):
      file = os.path.join(root, path)
  else:
    file = path

  if os.path.isdir(file):
    if options.get('index_files', True):
      return _find_index(file)
  elif os.path.exists(file):
    return file

def _is_path_safe(root, path):
  return os.path.realpath(os.path.join(root, path)).startswith(
    os.path.realpath(root))

def _find_index(dir):
  indexes = [f for f in os.listdir(dir) if f.lower().startswith('index.')]
  if indexes:
    return indexes[0]
