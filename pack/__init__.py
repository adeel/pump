"Not Rack... but Pack."

import environment
import response
from shortcuts import GET, POST, PUT, DELETE

def pack(routes, config={}):
  "Pack some routes into a WSGI application."

  # WSGI sucks.
  def app(env, start_response):
    return response.to_wsgi(environment.get_response(env, routes),
      start_response)

  return app

def def_routes(*routes):
  return dict([((m, p), h) for (m, p, h) in routes])
