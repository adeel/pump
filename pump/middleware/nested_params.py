# A middleware for parsing nested params, like
#     {"a[b]": 'c'}  =>  {'a': {'b': 'c'}}.

import re
from itertools import chain

def wrap_nested_params(app, options={}):
  def wrapped_app(req):
    # You can specify a custom key parsing function with the key_parser option.
    key_parser = options.get('key_parser', parse_nested_keys)
    req["params"] = nest_params(req["params"], key_parser)
    return app(req)
  return wrapped_app

# Takes a flat string of parameters and turns it into a nested dict of
# parameters, using the function key_parser to split the parameter names
# into keys.
def nest_params(params, key_parser):
  return reduce(lambda d, kv: set_nested_value(d, key_parser(kv[0]), kv[1]),
    param_pairs(params), {})

def param_pairs(params):
  return sum(
    [[(key, v) for v in val] if isinstance(val, list) else [(key, val)]
      for (key, val) in params.items()], [])

# Set a new value, v, in the dict d, at the key given by keys.  For example,
# 
#     set_nested_value({"a": {"b": {"c": "val"}}}, ["a", "b", "c"], "newval")
#       # => {"a": {"b": {"c": "newval"}}}
# 
#     set_nested_value({"a": {"b": {"c": "val"}}}, ["a", "x", "y"], "newval")
#       # => {"a": {"b": {"c": "val"}}, {"x": {"y": "newval"}}}
# 
# Treats values of blank keys as elements in a list.
def set_nested_value(d, keys, v):
  k, ks = None, None
  if keys:
    k = keys[0]
    if len(keys) > 1:
      ks = keys[1:]

  updates = {}
  if k:
    if ks:
      j, js = ks[0], ks[1:]
      if j == "":
        updates = {k: set_nested_value(d.get(k, []), js, v)}
      else:
        updates = {k: set_nested_value(d.get(k, {}), ks, v)}
    else:
      updates = {k: v}
  else:
    updates = v

  if isinstance(d, list):
    return d + [updates]
  return dict(d, **updates)

#    "a[b][c]"  =>  ["a", "b", "c"]
def parse_nested_keys(string):
  k, ks = re.compile(r"^(.*?)((?:\[.*?\])*)$").match(string).groups()
  if not ks:
    return [k]
  keys = re.compile('\[(.*?)\]').findall(ks)
  return [k] + keys