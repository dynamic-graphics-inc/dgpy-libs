## String Formatting

In the old robot code and the pydevkit there is a function for surrounding a string in quotes named `qt` and looks something like:

```python
def qt(string):
    return '"' + string + '"'
```

This is not the fastest way to format a string in python 3 nor is it the easiest to edit.
A first revision would be to change the formatting of the string to use python's built in string-format method called `.format()` so that the code looks like:

```python
def qt(string):
    return f'"{string}"'
```

The above code will be faster to run and to edit, and doesn't require the backslashes to escape the double quotes.
The ultimate way to transform this code would be to turn it into:

```python
qt = '"{}"'.format
```

See the pro tip below

## Pro Tip

Say you have to format something (which you might have to do all the time), and you define a function to format a string so it has hyphens around the original string:

```python
def hyphens(string):
    return f"--{string}--"


hyphens("howdy")  # returns: "--howdy--"
hyphens("sheldon")  # returns: "--sheldon--"
```

```text
'--sheldon--'
```

The super slick way of formatting this without having to define a new string is to python's format function alone:

```python
hyphens = "--{}--".format

hyphens("howdy")  # returns: "--howdy--"
hyphens("sheldon")  # returns: "--sheldon--"
```

```text
'--sheldon--'
```
