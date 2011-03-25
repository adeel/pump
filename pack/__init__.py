"Not Rack... but Pack."

import environment
import response

def make_wsgi_app(routes, config={}):
  "Make a WSGI application."

  # routes = {
  #   ('GET', '^/$'): "Hello world",
  #   ('GET', '^users/profile/(\d+)/?$'): controllers.user.profile,
  #   ('GET', '.*'): {"status": 404, "body": (lambda req: "Not Found")}
  # }

  # WSGI sucks.
  def app(env, start_response):
    return response.to_wsgi(environment.get_response(env, routes),
      start_response)

  return app
