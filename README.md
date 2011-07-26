# Pump

**Pump** is a dead simple abstraction of HTTP for Python.

## Summary

The Pump specification consists of headers, requests, responses, apps, and middleware.  Below are examples of each.

**Pump requests**.

    {"server_port": "80",
     "server_name": "127.0.0.1",
     "remote_addr": "127.0.0.1",
     "uri": "/",
     "scheme": "http",
     "method": "get",
     "headers":
       {"accept_charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.3",
        "connection": "keep-alive",
        "host": "localhost:8000",
        ...}}

**Pump responses**.

    {"status": 200,
     "headers": {"content_type": "text/plain"},
     "body": "Hello!"}

**Pump apps**.

    def app(req):
      if req["uri"] == "/favicon.ico":
        return {"status": 404, headers: {}, body: "Not Found"}
      return {"status": 200,
              "headers": {"content_type": "text/html"},
              "body": "<h1>Hello!</h1>"}

**Pump middleware**.

    def wrap_with_logger(app):
      def wrapped(req):
        response = app(req)
        print "%s %s\n  => %s" % (req["method"],
                                  req["uri"],
                                  response)
        return response
      return wrapped

For the detailed specification, see `SPEC.md`.

## Getting started

### Installation

To install, type

    $ pip install pump

or grab the code from [Github](https://github.com/adeel/pump):

    $ git clone git://github.com/adeel/pump.git
    $ cd pump
    $ python setup.py install

### Running your app

Pump comes with an adapter for the [Paste WSGI server](http://pythonpaste.org/modules/httpserver.html).  If you don't have that installed, do

    $ pip install Paste

and then to run your app:

    import pump
    pump.adapters.serve_with_paste(app, {"port": 3000})

Soon, Pump will come with adapters for other popular WSGI servers.

## Thanks

Pump was heavily inspired by Clojure's [Ring](https://github.com/mmcgrana/ring).  Thanks, Mark McGranaghan!

## License

Copyright (c) 2011 Adeel Ahmad Khan <adeel@adeel.ru>.

MIT license.