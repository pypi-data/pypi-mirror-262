# DotIndex
Allows you to use dot notation to index dicts, like how you can in javascript

When printed, DotIndex objects are printed as a normal dict would be, however
the curly braces have a full stop before them, to signify that it is a
DotIndex object. (`.{}` would be an empty object)

## Code Examples
Basic usage:
```py
from DotIndex import DotIndex

x = {
  "foo": "bar"
}

y = DotIndex(x)

print(y) # Expected output: ".{'foo': 'bar'}"
print(y.foo) # Expected output: "bar"
print(y["foo"]) # Expected output: "bar"

y["cat"] = "dog"

print(y.cat) # Expected output: "dog"
```

Adding together objects:
```py
from DotIndex import DotIndex

x = DotIndex({
  "foo": "bar"
})

y = DotIndex({
  "cat": "dog"
})

# Adds all values in y to x
# Also works if you do `x = x + y`
x += y

print(x) # Expected output: ".{'cat': 'dog', 'foo': 'bar'}"

# Adding a DotIndex and a dict
z = x + {
  "dicts": True
}

print(z) # Expected output: ".{'cat': 'dog', 'dicts': True, 'foo': 'bar'}"

# The second value overwrites any duplicate keys from the original object
z += {
  "cat": "not dog"
}

print(z) # Expected output: ".{'cat': 'not dog', 'dicts': True, 'foo': 'bar'}"

```

## Documentation
Creating the object
- Parameters
  - obj (`dict[str, Any]`) - the dict object that should be turned into a DotIndex object
  - recursive (`bool`, default: True) - whether or not to DotIndex-ify any dicts inside the original object
  - verbose_logs (`bool`, default: False) - whether or not to print out extra logs
  - ignore_errors (`bool`, default: False) - whether or not to ignore non-critical errors
- Other information:
  - Keys in `obj` must be strings, any other types will throw a `TypeError` (ignored with `ignore_errors`)
  - Keys in `obj` cannot start with two underscores (`"__"`) as those could be used to overwrite preexisting instance variables used for the class itself
  - If `recursive` is true, the values of `verbose_logs` and `ignore_errors` will be passed through into any new DotIndex objects created

Converting types
- `iter(...)` - Returns all keys in alphabetical order
- `str(...)` - Returns a string formatted like the `str(...)` value of a dict object, with a full stop (`"."`) at the start to show that it is a DotIndex type. Example: `".{'foo': 'bar'}"`
- `repr(...)` - Same as `str(...)`
- `int(...)` - Returns the amount of keys in the object
- `float(...)` - Same as `int(...)` except as a float type
- `bool(...)` - Returns `True` if there are any keys in the object, and if there aren't it returns `False`

Comparisons
- `==` - Checks if the two objects have all the values the same. Works with both DotIndex objects and dict objects
- `!=` - Opposite of `==`
- `>`, `<`, `>=`, `<=` - Compares the amount of keys in the object

Misc.
- `+` - Takes the keys from the object on the right and adds them to the object on the left, overwriting any duplicates
- `len(...)` - Returns the amount of keys in the object
- `'val' in ...` - Returns true if `"val"` is a key in the object
