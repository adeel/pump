"A middleware for serving files."

import os
from pack.util import codec
from pack.util import response

def wrap_file(app, root_path, options={}):
  """
  Wrap the app so that instead of handling requests normally, it first looks
  for a file in the root_path directory that corresponds to the request URL.
  If the file is not found, the request is handled normally.
  """
  if not os.path.isdir(root_path):
    raise Exception("Directory does not exist: %s" % root_path)

  options = dict(options, **{'root': root_path, 'index_files': True})

  def wrapped_app(req):
    if req['method'] != 'get':
      return app(req)

    path = codec.url_decode(req['uri'])[1:]
    return response.file_response(path, options) or app(req)

  return wrapped_app