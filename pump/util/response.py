import os

# The minimal Pump response.
skeleton = {"status": 200, "headers": {}, "body": ""}

# Return a skeleton response with the given body.
def with_body(body):
  return dict(skeleton, body=body)

# Return a redirect response to the given URL.
def redirect(url):
  return {"status": 302, "headers": {"Location": url}, "body": ""}

# Return the given response updated with the given status.
def with_status(response, status):
  return dict(response, status=status)

# Return the given response updated with the given header.
def with_header(response, key, value):
  return dict(response,
    headers=dict(response.get("headers", {}), **{key: value}))

# Return the given response updated with the given content-type.
def with_content_type(response, content_type):
  return with_header(response, 'content_type', content_type)

# Returns a response containing the contents of the file at the given path.
# Options:
#
#   - root: the root path for the given file path
#   - index_files: whether to look for index.* files in directories (true by
#                  default)
def file_response(path, options={}):
  file = _get_file(path, options)
  if file:
    return with_body(open(file, 'r'))

def _get_file(path, options={}):
  root = options.get("root")
  if root:
    if _is_path_safe(root, path):
      file = os.path.join(root, path)
  else:
    file = path

  if os.path.isdir(file):
    if options.get("index_files", True):
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
