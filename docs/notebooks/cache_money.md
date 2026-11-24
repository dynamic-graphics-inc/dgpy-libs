## Python's built in lru_cache

There's a module in Python's standard lib called functools and in that module is one of the best python secrets there is...

Below is a function for computing the fibonacci sequence (you might be thinking 'thats a super naive way of computing the fibonacci sequence,' but bear with me).

```python
def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)
```

```python
from time import time

for i in range(40 + 1):
    ti = time()
    f = fib(i)
    tf = time()
    total_time = tf - ti
    print(f"n:{i:02d}   fib(n): {f}   funk-run-time: {total_time:.4f} sec")
```

```text
n:00   fib(n): 0   funk-run-time: 0.0000 sec
n:01   fib(n): 1   funk-run-time: 0.0000 sec
n:02   fib(n): 1   funk-run-time: 0.0000 sec
n:03   fib(n): 2   funk-run-time: 0.0000 sec
n:04   fib(n): 3   funk-run-time: 0.0000 sec
n:05   fib(n): 5   funk-run-time: 0.0000 sec
n:06   fib(n): 8   funk-run-time: 0.0000 sec
n:07   fib(n): 13   funk-run-time: 0.0000 sec
n:08   fib(n): 21   funk-run-time: 0.0000 sec
n:09   fib(n): 34   funk-run-time: 0.0000 sec
n:10   fib(n): 55   funk-run-time: 0.0000 sec
n:11   fib(n): 89   funk-run-time: 0.0000 sec
n:12   fib(n): 144   funk-run-time: 0.0000 sec
n:13   fib(n): 233   funk-run-time: 0.0010 sec
n:14   fib(n): 377   funk-run-time: 0.0000 sec
n:15   fib(n): 610   funk-run-time: 0.0000 sec
n:16   fib(n): 987   funk-run-time: 0.0010 sec
n:17   fib(n): 1597   funk-run-time: 0.0000 sec
n:18   fib(n): 2584   funk-run-time: 0.0010 sec
n:19   fib(n): 4181   funk-run-time: 0.0030 sec
n:20   fib(n): 6765   funk-run-time: 0.0020 sec
n:21   fib(n): 10946   funk-run-time: 0.0060 sec
n:22   fib(n): 17711   funk-run-time: 0.0050 sec
n:23   fib(n): 28657   funk-run-time: 0.0080 sec
n:24   fib(n): 46368   funk-run-time: 0.0160 sec
n:25   fib(n): 75025   funk-run-time: 0.0240 sec
n:26   fib(n): 121393   funk-run-time: 0.0370 sec
n:27   fib(n): 196418   funk-run-time: 0.0520 sec
n:28   fib(n): 317811   funk-run-time: 0.0870 sec
n:29   fib(n): 514229   funk-run-time: 0.1420 sec
n:30   fib(n): 832040   funk-run-time: 0.2490 sec
n:31   fib(n): 1346269   funk-run-time: 0.3990 sec
n:32   fib(n): 2178309   funk-run-time: 0.6040 sec
n:33   fib(n): 3524578   funk-run-time: 1.0010 sec
n:34   fib(n): 5702887   funk-run-time: 1.6340 sec
n:35   fib(n): 9227465   funk-run-time: 2.6530 sec
n:36   fib(n): 14930352   funk-run-time: 4.1060 sec
n:37   fib(n): 24157817   funk-run-time: 6.9640 sec
n:38   fib(n): 39088169   funk-run-time: 12.1551 sec
n:39   fib(n): 63245986   funk-run-time: 18.8260 sec
n:40   fib(n): 102334155   funk-run-time: 28.9990 sec
```

## THAT WAS SLOW

Python is 'ok' with recursion, but it generally tends to slow down quite a bit.
How can we speed this up quickly?
Can we do it without messing with our OG-function?
(NOTE: the run-times roughly resemble the fibonacci sequence)

We can!
The function below is the exact same function as the orig-fib-funk, BUT it has been decorated with the lru_cache decorator; this decorator was added in python 3 and caches a function's \*args and \*\*kwargs => return values as key => value pairs. lru_cache is perfect for recursive functions!
The maxsize arg allows one to set the max cache size, but for most cases maxsize=None is perfectly fine.

```python
from functools import cache, lru_cache


@cache
def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)
```

```python
for i in range(40 + 1):
    ti = time()
    f = fib(i)
    tf = time()
    total_time = tf - ti
    print(f"n:{i:02d}   fib(n): {f}   funk-run-time: {total_time:.4f} sec")
```

```text
n:00   fib(n): 0   funk-run-time: 0.0000 sec
n:01   fib(n): 1   funk-run-time: 0.0000 sec
n:02   fib(n): 1   funk-run-time: 0.0000 sec
n:03   fib(n): 2   funk-run-time: 0.0000 sec
n:04   fib(n): 3   funk-run-time: 0.0000 sec
n:05   fib(n): 5   funk-run-time: 0.0000 sec
n:06   fib(n): 8   funk-run-time: 0.0000 sec
n:07   fib(n): 13   funk-run-time: 0.0000 sec
n:08   fib(n): 21   funk-run-time: 0.0000 sec
n:09   fib(n): 34   funk-run-time: 0.0000 sec
n:10   fib(n): 55   funk-run-time: 0.0000 sec
n:11   fib(n): 89   funk-run-time: 0.0000 sec
n:12   fib(n): 144   funk-run-time: 0.0000 sec
n:13   fib(n): 233   funk-run-time: 0.0000 sec
n:14   fib(n): 377   funk-run-time: 0.0000 sec
n:15   fib(n): 610   funk-run-time: 0.0000 sec
n:16   fib(n): 987   funk-run-time: 0.0000 sec
n:17   fib(n): 1597   funk-run-time: 0.0000 sec
n:18   fib(n): 2584   funk-run-time: 0.0000 sec
n:19   fib(n): 4181   funk-run-time: 0.0000 sec
n:20   fib(n): 6765   funk-run-time: 0.0000 sec
n:21   fib(n): 10946   funk-run-time: 0.0000 sec
n:22   fib(n): 17711   funk-run-time: 0.0000 sec
n:23   fib(n): 28657   funk-run-time: 0.0000 sec
n:24   fib(n): 46368   funk-run-time: 0.0000 sec
n:25   fib(n): 75025   funk-run-time: 0.0000 sec
n:26   fib(n): 121393   funk-run-time: 0.0000 sec
n:27   fib(n): 196418   funk-run-time: 0.0000 sec
n:28   fib(n): 317811   funk-run-time: 0.0000 sec
n:29   fib(n): 514229   funk-run-time: 0.0000 sec
n:30   fib(n): 832040   funk-run-time: 0.0000 sec
n:31   fib(n): 1346269   funk-run-time: 0.0000 sec
n:32   fib(n): 2178309   funk-run-time: 0.0000 sec
n:33   fib(n): 3524578   funk-run-time: 0.0000 sec
n:34   fib(n): 5702887   funk-run-time: 0.0000 sec
n:35   fib(n): 9227465   funk-run-time: 0.0000 sec
n:36   fib(n): 14930352   funk-run-time: 0.0000 sec
n:37   fib(n): 24157817   funk-run-time: 0.0000 sec
n:38   fib(n): 39088169   funk-run-time: 0.0000 sec
n:39   fib(n): 63245986   funk-run-time: 0.0000 sec
n:40   fib(n): 102334155   funk-run-time: 0.0000 sec
```

# Much Better
