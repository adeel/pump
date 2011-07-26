"A middleware that implements cookie-based sessions using Beaker."

import beaker.middleware
from pump.util import wsgi

def wrap_session(app, options={}):
  """
  Adds a "session" key to the request.  Takes the following options:

    -- store:
         One of "memory", "database", "file", "cookie", "dbm", "memcached",
         or "google".  Defaults to "memory".
    -- lock_dir:
         The path to the directory to be used as a lock file.  See
         <http://beaker.groovie.org/glossary.html#term-dog-pile-effect>.
    -- data_dir:
         The path to the directory where files are stored.  Used for file and
         dbm stores.
    -- url:
         Used for database and memcached stores.  In the former case, this
         should be a SQLAlchemy database string <http://bit.ly/gvzIlw>, e.g.
         "sqlite:///tmp/sessions.db".  In the latter case, it should be a
         semicolon-separated list of memcached servers.
    -- auto:
         If False, you will need to call request["session"].save() explicitly
         after modifying request["session"].  Defaults to True.
    -- cookie:
         A dictionary with the following keys:

           -- key:
                The name of the cookie.  Defaults to "pump-session".
           -- secret:
                A long, randomly-generated string used to ensure session
                integrity.
           -- domain:
                The domain the cookie will be set on.  Defaults to the current
                domain.
           -- expires:
                The expiration date of the cookie.  If True, expires when the
                browser closes.  If False, never expires.  If a datetime
                instance, expires at that specific date and time.  If a
                timedelta instance, expires after the given time interval.
                Defaults to False.
           -- secure:
                Whether the session cookie should be marked as secure (for
                SSL).
           -- timeout:
                Seconds after the session was last accessed until it is
                invalidated.  Defaults to never expiring.
  
  This uses Beaker in the background, so you can read
  <http://beaker.groovie.org/configuration.html> for more details.
  """

  # Guess which language doesn't support recursively merging dictionaries?
  options = dict(dict({
    "store": "memory",
    "auto": True}, **options), cookies=dict({
      "expires": False,
      "key": "pump-session",
      "secure": False}, **options.get("cookies", {})))

  for middleware in [wrap_unbeaker, wrap_beaker(options)]:
    app = middleware(app)
  return app

def wrap_beaker(options):
  "A Pump middleware that wraps around Beaker's WSGI middleware."
  return wsgi.build_middleware(_beaker_wsgi_middleware, options)

def wrap_unbeaker(app):
  "Renames the beaker.session key in the request to \"session\"."
  def wrapped(req):
    req["session"] = req.get("beaker.session")
    if req.has_key("beaker.session"):
      del req["beaker.session"]
    return app(req)
  return wrapped

def _beaker_wsgi_middleware(app, options):
  "The WSGI middleware provided by Beaker."
  return beaker.middleware.SessionMiddleware(app, _get_beaker_config(options))

def _get_beaker_config(options):
  """
  Reformat options dictionary to match Beaker's configuration settings.  See
  <http://beaker.groovie.org/configuration.html>.
  """
  return {
    "session.data_dir":       options.get("data_dir"),
    "session.lock_dir":       options.get("lock_dir"),
    "session.type":           _get_beaker_session_type(options.get("store")),
    "session.url":            options.get("url"),
    "session.auto":           options.get("auto"),
    "session.cookie_expires": options.get("cookies").get("expires"),
    "session.cookie_domain":  options.get("cookies").get("domain"),
    "session.key":            options.get("cookies").get("key"),
    "session.secret":         options.get("cookies").get("secret"),
    "session.secure":         options.get("cookies").get("secure"),
    "session.timeout":        options.get("cookies").get("timeout")}

def _get_beaker_session_type(store):
  return {
    "database":  "ext:database",
    "memcached": "ext:memcached",
    "google":    "ext:google"}.get(store, store)