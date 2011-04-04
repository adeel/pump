import urllib

def url_decode(string, encoding='utf8'):
  return urllib.unquote(string)

def url_encode(string, encoding='utf8'):
  return urllib.urlencode(string)
