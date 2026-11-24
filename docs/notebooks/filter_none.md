# Python filtering falsey ~ `filter(None, iterable)`

Start by making a bunch of random lists

```python
import random

res = [random.randrange(1, 300, 1) for i in range(100)]
for _i in range(100):
    res.append(None)
lists = [res]
for _i in range(40):
    random.shuffle(res)
    lists.append(res)
```

## Make the two functions one using `filter(None, iterable)` the other using a generator comprehension

```python
def filter_none_gen_comprehension(it):
    return (i for i in it if i)
```

```python
def filter_none(it):
    return filter(None, it)
```

## Below you can see the functions produce the same thing

```python
for l in lists[:3]:
    print("\n__________")
    print(l)
    gen = list(filter_none_gen_comprehension(l))
    fil = list(filter_none(l))
    print("__VIA_GEN_FUNK__")
    print(gen)
    print("__VIA_FILTER_NONE__")
    print(fil)
    assert gen == fil
```

```text
__________
[283, 121, 39, 147, 160, 148, 241, None, 57, None, 252, None, None, None, 190, None, None, None, 222, None, None, None, 104, None, None, 85, None, 229, None, 219, None, None, None, 13, 124, None, None, 68, None, 143, 250, None, 153, 255, None, None, None, 26, None, None, 169, None, None, 199, 151, 259, 110, None, 72, 46, 262, None, 94, 20, None, 91, 225, None, None, 149, 211, 216, None, 129, None, 252, None, 109, None, 220, None, None, 113, None, 160, 145, None, 90, 294, 105, None, 236, None, 127, 196, 243, None, 188, 297, None, None, 171, 86, None, None, 224, 98, None, 258, 39, None, 43, None, 69, 271, 221, 12, None, None, None, None, 141, None, None, 200, None, None, 125, None, None, None, None, None, 293, 265, 48, 115, None, 220, None, 168, None, None, None, None, None, 87, None, None, 3, 227, None, 75, None, None, None, None, None, None, 199, None, None, 116, 245, 87, None, 231, 118, 204, None, None, 197, None, 117, None, None, None, 124, 257, 33, 151, None, 54, None, 92, None, 216, 208, 234, None, None, None, None, None, None, 192, None, 221, 51, 197]
__VIA_GEN_FUNK__
[283, 121, 39, 147, 160, 148, 241, 57, 252, 190, 222, 104, 85, 229, 219, 13, 124, 68, 143, 250, 153, 255, 26, 169, 199, 151, 259, 110, 72, 46, 262, 94, 20, 91, 225, 149, 211, 216, 129, 252, 109, 220, 113, 160, 145, 90, 294, 105, 236, 127, 196, 243, 188, 297, 171, 86, 224, 98, 258, 39, 43, 69, 271, 221, 12, 141, 200, 125, 293, 265, 48, 115, 220, 168, 87, 3, 227, 75, 199, 116, 245, 87, 231, 118, 204, 197, 117, 124, 257, 33, 151, 54, 92, 216, 208, 234, 192, 221, 51, 197]
__VIA_FILTER_NONE__
[283, 121, 39, 147, 160, 148, 241, 57, 252, 190, 222, 104, 85, 229, 219, 13, 124, 68, 143, 250, 153, 255, 26, 169, 199, 151, 259, 110, 72, 46, 262, 94, 20, 91, 225, 149, 211, 216, 129, 252, 109, 220, 113, 160, 145, 90, 294, 105, 236, 127, 196, 243, 188, 297, 171, 86, 224, 98, 258, 39, 43, 69, 271, 221, 12, 141, 200, 125, 293, 265, 48, 115, 220, 168, 87, 3, 227, 75, 199, 116, 245, 87, 231, 118, 204, 197, 117, 124, 257, 33, 151, 54, 92, 216, 208, 234, 192, 221, 51, 197]

__________
[283, 121, 39, 147, 160, 148, 241, None, 57, None, 252, None, None, None, 190, None, None, None, 222, None, None, None, 104, None, None, 85, None, 229, None, 219, None, None, None, 13, 124, None, None, 68, None, 143, 250, None, 153, 255, None, None, None, 26, None, None, 169, None, None, 199, 151, 259, 110, None, 72, 46, 262, None, 94, 20, None, 91, 225, None, None, 149, 211, 216, None, 129, None, 252, None, 109, None, 220, None, None, 113, None, 160, 145, None, 90, 294, 105, None, 236, None, 127, 196, 243, None, 188, 297, None, None, 171, 86, None, None, 224, 98, None, 258, 39, None, 43, None, 69, 271, 221, 12, None, None, None, None, 141, None, None, 200, None, None, 125, None, None, None, None, None, 293, 265, 48, 115, None, 220, None, 168, None, None, None, None, None, 87, None, None, 3, 227, None, 75, None, None, None, None, None, None, 199, None, None, 116, 245, 87, None, 231, 118, 204, None, None, 197, None, 117, None, None, None, 124, 257, 33, 151, None, 54, None, 92, None, 216, 208, 234, None, None, None, None, None, None, 192, None, 221, 51, 197]
__VIA_GEN_FUNK__
[283, 121, 39, 147, 160, 148, 241, 57, 252, 190, 222, 104, 85, 229, 219, 13, 124, 68, 143, 250, 153, 255, 26, 169, 199, 151, 259, 110, 72, 46, 262, 94, 20, 91, 225, 149, 211, 216, 129, 252, 109, 220, 113, 160, 145, 90, 294, 105, 236, 127, 196, 243, 188, 297, 171, 86, 224, 98, 258, 39, 43, 69, 271, 221, 12, 141, 200, 125, 293, 265, 48, 115, 220, 168, 87, 3, 227, 75, 199, 116, 245, 87, 231, 118, 204, 197, 117, 124, 257, 33, 151, 54, 92, 216, 208, 234, 192, 221, 51, 197]
__VIA_FILTER_NONE__
[283, 121, 39, 147, 160, 148, 241, 57, 252, 190, 222, 104, 85, 229, 219, 13, 124, 68, 143, 250, 153, 255, 26, 169, 199, 151, 259, 110, 72, 46, 262, 94, 20, 91, 225, 149, 211, 216, 129, 252, 109, 220, 113, 160, 145, 90, 294, 105, 236, 127, 196, 243, 188, 297, 171, 86, 224, 98, 258, 39, 43, 69, 271, 221, 12, 141, 200, 125, 293, 265, 48, 115, 220, 168, 87, 3, 227, 75, 199, 116, 245, 87, 231, 118, 204, 197, 117, 124, 257, 33, 151, 54, 92, 216, 208, 234, 192, 221, 51, 197]

__________
[283, 121, 39, 147, 160, 148, 241, None, 57, None, 252, None, None, None, 190, None, None, None, 222, None, None, None, 104, None, None, 85, None, 229, None, 219, None, None, None, 13, 124, None, None, 68, None, 143, 250, None, 153, 255, None, None, None, 26, None, None, 169, None, None, 199, 151, 259, 110, None, 72, 46, 262, None, 94, 20, None, 91, 225, None, None, 149, 211, 216, None, 129, None, 252, None, 109, None, 220, None, None, 113, None, 160, 145, None, 90, 294, 105, None, 236, None, 127, 196, 243, None, 188, 297, None, None, 171, 86, None, None, 224, 98, None, 258, 39, None, 43, None, 69, 271, 221, 12, None, None, None, None, 141, None, None, 200, None, None, 125, None, None, None, None, None, 293, 265, 48, 115, None, 220, None, 168, None, None, None, None, None, 87, None, None, 3, 227, None, 75, None, None, None, None, None, None, 199, None, None, 116, 245, 87, None, 231, 118, 204, None, None, 197, None, 117, None, None, None, 124, 257, 33, 151, None, 54, None, 92, None, 216, 208, 234, None, None, None, None, None, None, 192, None, 221, 51, 197]
__VIA_GEN_FUNK__
[283, 121, 39, 147, 160, 148, 241, 57, 252, 190, 222, 104, 85, 229, 219, 13, 124, 68, 143, 250, 153, 255, 26, 169, 199, 151, 259, 110, 72, 46, 262, 94, 20, 91, 225, 149, 211, 216, 129, 252, 109, 220, 113, 160, 145, 90, 294, 105, 236, 127, 196, 243, 188, 297, 171, 86, 224, 98, 258, 39, 43, 69, 271, 221, 12, 141, 200, 125, 293, 265, 48, 115, 220, 168, 87, 3, 227, 75, 199, 116, 245, 87, 231, 118, 204, 197, 117, 124, 257, 33, 151, 54, 92, 216, 208, 234, 192, 221, 51, 197]
__VIA_FILTER_NONE__
[283, 121, 39, 147, 160, 148, 241, 57, 252, 190, 222, 104, 85, 229, 219, 13, 124, 68, 143, 250, 153, 255, 26, 169, 199, 151, 259, 110, 72, 46, 262, 94, 20, 91, 225, 149, 211, 216, 129, 252, 109, 220, 113, 160, 145, 90, 294, 105, 236, 127, 196, 243, 188, 297, 171, 86, 224, 98, 258, 39, 43, 69, 271, 221, 12, 141, 200, 125, 293, 265, 48, 115, 220, 168, 87, 3, 227, 75, 199, 116, 245, 87, 231, 118, 204, 197, 117, 124, 257, 33, 151, 54, 92, 216, 208, 234, 192, 221, 51, 197]
```

```python
%%timeit
# NBVAL_IGNORE_OUTPUT
for l in lists:
    a = list(filter_none_gen_comprehension(l))
```

```text
446 µs ± 26 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)
```

```python
%%timeit
# NBVAL_IGNORE_OUTPUT
for l in lists:
    a = list(filter_none(l))
```

```text
122 µs ± 2.54 µs per loop (mean ± std. dev. of 7 runs, 10000 loops each)
```

## Timing the two functions reveals that the function using filter takes about 1/4th - 1/5th of the time the generator comprehension does
