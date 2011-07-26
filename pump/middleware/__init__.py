# # Pump middleware

# The [content_type](content_type.html) middleware adds a content_type key to
# the response.
import content_type

# The [params](params.html) middleware parses GET and POST params.
import params

# The [nested_params](nested_params.html) middleware parses nested params.
import nested_params

# The [file](file.html) middleware serves files.
import file

# The [static](static.html) middleware serves static files with more
# flexibility than the file middleware.
import static

# The [cookies](cookies.html) middleware adds cookie support.
import cookies

# The [session](session.html) middleware implements cookie-based sessions using
# Beaker.
import session