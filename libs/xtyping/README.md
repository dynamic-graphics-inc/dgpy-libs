<a href="https://github.com/dynamic-graphics-inc/dgpy-libs">
<img align="right" src="https://github.com/dynamic-graphics-inc/dgpy-libs/blob/main/docs/images/dgpy_banner.svg?raw=true" alt="drawing" height="120" width="300"/>
</a>

# xtyping

[![Wheel](https://img.shields.io/pypi/wheel/xtyping.svg)](https://img.shields.io/pypi/wheel/xtyping.svg)
[![Version](https://img.shields.io/pypi/v/xtyping.svg)](https://img.shields.io/pypi/v/xtyping.svg)
[![py_versions](https://img.shields.io/pypi/pyversions/xtyping.svg)](https://img.shields.io/pypi/pyversions/xtyping.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**Install:** `pip install xtyping`

---

## What is xtyping?

xtyping (short for extended typing) lets you import all your friends from `typing` as well as `typing_extensions`

- `typing` | `typing_extensions`; xtyping 'exports' everything in `typing.__all__` and `typing_extensions.__all__`
- Common type aliases

## Why not use `typing_extensions`?

Don't have to import both `typing` and `typing_extensions`; BOOM

Instead of writing:

```
from typing import Optional
from typing_extensions import TypedDict
```

you can write:

```
from xtyping import Optional, TypedDict
# or
import xtyping as xt
TypedDict = xt.TypedDict
Optional = xt.Optional
```

```python
import xtyping as xt

from_typing = [
    "  ~  ".join((f"xt.{el}", f"typing.{el}", str(getattr(xt, el))))
    for el in xt.__all_typing__
]
from_typing_extensions = [
    "  ~  ".join((f"xt.{el}", f"typing_extensions.{el}", str(getattr(xt, el))))
    for el in xt.__all_typing__
]
from_xtyping_shed = [
    "  ~  ".join((f"xt.{el}", f"xtyping.shed.{el}", str(getattr(xt, el))))
    for el in xt.__all_shed__
]
print(
    "\n".join(
        [
            "-------------",
            "from `typing`",
            "-------------",
            *from_typing,
            "\n",
            "------------------------",
            "from `typing_extensions`",
            "------------------------",
            *from_typing_extensions,
            "\n",
            "-------------------",
            "from `xtyping.shed`",
            "-------------------",
            *from_xtyping_shed,
            "\n",
        ]
    )
)
```

    -------------
    from `typing`
    -------------
    xt.AbstractSet  ~  typing.AbstractSet  ~  typing.AbstractSet
    xt.Any  ~  typing.Any  ~  typing.Any
    xt.AnyStr  ~  typing.AnyStr  ~  ~AnyStr
    xt.AsyncContextManager  ~  typing.AsyncContextManager  ~  typing.AbstractAsyncContextManager
    xt.AsyncGenerator  ~  typing.AsyncGenerator  ~  typing.AsyncGenerator
    xt.AsyncIterable  ~  typing.AsyncIterable  ~  typing.AsyncIterable
    xt.AsyncIterator  ~  typing.AsyncIterator  ~  typing.AsyncIterator
    xt.Awaitable  ~  typing.Awaitable  ~  typing.Awaitable
    xt.ByteString  ~  typing.ByteString  ~  typing.ByteString
    xt.Callable  ~  typing.Callable  ~  typing.Callable
    xt.ChainMap  ~  typing.ChainMap  ~  typing.ChainMap
    xt.ClassVar  ~  typing.ClassVar  ~  typing.ClassVar
    xt.Collection  ~  typing.Collection  ~  typing.Collection
    xt.Container  ~  typing.Container  ~  typing.Container
    xt.ContextManager  ~  typing.ContextManager  ~  typing.AbstractContextManager
    xt.Coroutine  ~  typing.Coroutine  ~  typing.Coroutine
    xt.Counter  ~  typing.Counter  ~  typing.Counter
    xt.DefaultDict  ~  typing.DefaultDict  ~  typing.DefaultDict
    xt.Deque  ~  typing.Deque  ~  typing.Deque
    xt.Dict  ~  typing.Dict  ~  typing.Dict
    xt.FrozenSet  ~  typing.FrozenSet  ~  typing.FrozenSet
    xt.Generator  ~  typing.Generator  ~  typing.Generator
    xt.Generic  ~  typing.Generic  ~  <class 'typing.Generic'>
    xt.Hashable  ~  typing.Hashable  ~  typing.Hashable
    xt.IO  ~  typing.IO  ~  <class 'typing.IO'>
    xt.ItemsView  ~  typing.ItemsView  ~  typing.ItemsView
    xt.Iterable  ~  typing.Iterable  ~  typing.Iterable
    xt.Iterator  ~  typing.Iterator  ~  typing.Iterator
    xt.KeysView  ~  typing.KeysView  ~  typing.KeysView
    xt.List  ~  typing.List  ~  typing.List
    xt.Mapping  ~  typing.Mapping  ~  typing.Mapping
    xt.MappingView  ~  typing.MappingView  ~  typing.MappingView
    xt.MutableMapping  ~  typing.MutableMapping  ~  typing.MutableMapping
    xt.MutableSequence  ~  typing.MutableSequence  ~  typing.MutableSequence
    xt.MutableSet  ~  typing.MutableSet  ~  typing.MutableSet
    xt.NamedTuple  ~  typing.NamedTuple  ~  <class 'typing.NamedTuple'>
    xt.NewType  ~  typing.NewType  ~  <function NewType at 0x7fd2e534f790>
    xt.Optional  ~  typing.Optional  ~  typing.Optional
    xt.Reversible  ~  typing.Reversible  ~  typing.Reversible
    xt.Sequence  ~  typing.Sequence  ~  typing.Sequence
    xt.Set  ~  typing.Set  ~  typing.Set
    xt.Sized  ~  typing.Sized  ~  typing.Sized
    xt.SupportsAbs  ~  typing.SupportsAbs  ~  <class 'typing.SupportsAbs'>
    xt.SupportsBytes  ~  typing.SupportsBytes  ~  <class 'typing.SupportsBytes'>
    xt.SupportsComplex  ~  typing.SupportsComplex  ~  <class 'typing.SupportsComplex'>
    xt.SupportsFloat  ~  typing.SupportsFloat  ~  <class 'typing.SupportsFloat'>
    xt.SupportsInt  ~  typing.SupportsInt  ~  <class 'typing.SupportsInt'>
    xt.SupportsRound  ~  typing.SupportsRound  ~  <class 'typing.SupportsRound'>
    xt.TYPE_CHECKING  ~  typing.TYPE_CHECKING  ~  False
    xt.Text  ~  typing.Text  ~  <class 'str'>
    xt.Tuple  ~  typing.Tuple  ~  typing.Tuple
    xt.Type  ~  typing.Type  ~  typing.Type
    xt.TypeVar  ~  typing.TypeVar  ~  <class 'typing.TypeVar'>
    xt.Union  ~  typing.Union  ~  typing.Union
    xt.ValuesView  ~  typing.ValuesView  ~  typing.ValuesView
    xt.cast  ~  typing.cast  ~  <function cast at 0x7fd2e53435e0>
    xt.get_type_hints  ~  typing.get_type_hints  ~  <function get_type_hints at 0x7fd2dc7531f0>
    xt.no_type_check  ~  typing.no_type_check  ~  <function no_type_check at 0x7fd2e53438b0>
    xt.no_type_check_decorator  ~  typing.no_type_check_decorator  ~  <function no_type_check_decorator at 0x7fd2e5343940>
    xt.overload  ~  typing.overload  ~  <function overload at 0x7fd2dc721a60>


    ------------------------
    from `typing_extensions`
    ------------------------
    xt.AbstractSet  ~  typing_extensions.AbstractSet  ~  typing.AbstractSet
    xt.Any  ~  typing_extensions.Any  ~  typing.Any
    xt.AnyStr  ~  typing_extensions.AnyStr  ~  ~AnyStr
    xt.AsyncContextManager  ~  typing_extensions.AsyncContextManager  ~  typing.AbstractAsyncContextManager
    xt.AsyncGenerator  ~  typing_extensions.AsyncGenerator  ~  typing.AsyncGenerator
    xt.AsyncIterable  ~  typing_extensions.AsyncIterable  ~  typing.AsyncIterable
    xt.AsyncIterator  ~  typing_extensions.AsyncIterator  ~  typing.AsyncIterator
    xt.Awaitable  ~  typing_extensions.Awaitable  ~  typing.Awaitable
    xt.ByteString  ~  typing_extensions.ByteString  ~  typing.ByteString
    xt.Callable  ~  typing_extensions.Callable  ~  typing.Callable
    xt.ChainMap  ~  typing_extensions.ChainMap  ~  typing.ChainMap
    xt.ClassVar  ~  typing_extensions.ClassVar  ~  typing.ClassVar
    xt.Collection  ~  typing_extensions.Collection  ~  typing.Collection
    xt.Container  ~  typing_extensions.Container  ~  typing.Container
    xt.ContextManager  ~  typing_extensions.ContextManager  ~  typing.AbstractContextManager
    xt.Coroutine  ~  typing_extensions.Coroutine  ~  typing.Coroutine
    xt.Counter  ~  typing_extensions.Counter  ~  typing.Counter
    xt.DefaultDict  ~  typing_extensions.DefaultDict  ~  typing.DefaultDict
    xt.Deque  ~  typing_extensions.Deque  ~  typing.Deque
    xt.Dict  ~  typing_extensions.Dict  ~  typing.Dict
    xt.FrozenSet  ~  typing_extensions.FrozenSet  ~  typing.FrozenSet
    xt.Generator  ~  typing_extensions.Generator  ~  typing.Generator
    xt.Generic  ~  typing_extensions.Generic  ~  <class 'typing.Generic'>
    xt.Hashable  ~  typing_extensions.Hashable  ~  typing.Hashable
    xt.IO  ~  typing_extensions.IO  ~  <class 'typing.IO'>
    xt.ItemsView  ~  typing_extensions.ItemsView  ~  typing.ItemsView
    xt.Iterable  ~  typing_extensions.Iterable  ~  typing.Iterable
    xt.Iterator  ~  typing_extensions.Iterator  ~  typing.Iterator
    xt.KeysView  ~  typing_extensions.KeysView  ~  typing.KeysView
    xt.List  ~  typing_extensions.List  ~  typing.List
    xt.Mapping  ~  typing_extensions.Mapping  ~  typing.Mapping
    xt.MappingView  ~  typing_extensions.MappingView  ~  typing.MappingView
    xt.MutableMapping  ~  typing_extensions.MutableMapping  ~  typing.MutableMapping
    xt.MutableSequence  ~  typing_extensions.MutableSequence  ~  typing.MutableSequence
    xt.MutableSet  ~  typing_extensions.MutableSet  ~  typing.MutableSet
    xt.NamedTuple  ~  typing_extensions.NamedTuple  ~  <class 'typing.NamedTuple'>
    xt.NewType  ~  typing_extensions.NewType  ~  <function NewType at 0x7fd2e534f790>
    xt.Optional  ~  typing_extensions.Optional  ~  typing.Optional
    xt.Reversible  ~  typing_extensions.Reversible  ~  typing.Reversible
    xt.Sequence  ~  typing_extensions.Sequence  ~  typing.Sequence
    xt.Set  ~  typing_extensions.Set  ~  typing.Set
    xt.Sized  ~  typing_extensions.Sized  ~  typing.Sized
    xt.SupportsAbs  ~  typing_extensions.SupportsAbs  ~  <class 'typing.SupportsAbs'>
    xt.SupportsBytes  ~  typing_extensions.SupportsBytes  ~  <class 'typing.SupportsBytes'>
    xt.SupportsComplex  ~  typing_extensions.SupportsComplex  ~  <class 'typing.SupportsComplex'>
    xt.SupportsFloat  ~  typing_extensions.SupportsFloat  ~  <class 'typing.SupportsFloat'>
    xt.SupportsInt  ~  typing_extensions.SupportsInt  ~  <class 'typing.SupportsInt'>
    xt.SupportsRound  ~  typing_extensions.SupportsRound  ~  <class 'typing.SupportsRound'>
    xt.TYPE_CHECKING  ~  typing_extensions.TYPE_CHECKING  ~  False
    xt.Text  ~  typing_extensions.Text  ~  <class 'str'>
    xt.Tuple  ~  typing_extensions.Tuple  ~  typing.Tuple
    xt.Type  ~  typing_extensions.Type  ~  typing.Type
    xt.TypeVar  ~  typing_extensions.TypeVar  ~  <class 'typing.TypeVar'>
    xt.Union  ~  typing_extensions.Union  ~  typing.Union
    xt.ValuesView  ~  typing_extensions.ValuesView  ~  typing.ValuesView
    xt.cast  ~  typing_extensions.cast  ~  <function cast at 0x7fd2e53435e0>
    xt.get_type_hints  ~  typing_extensions.get_type_hints  ~  <function get_type_hints at 0x7fd2dc7531f0>
    xt.no_type_check  ~  typing_extensions.no_type_check  ~  <function no_type_check at 0x7fd2e53438b0>
    xt.no_type_check_decorator  ~  typing_extensions.no_type_check_decorator  ~  <function no_type_check_decorator at 0x7fd2e5343940>
    xt.overload  ~  typing_extensions.overload  ~  <function overload at 0x7fd2dc721a60>


    -------------------
    from `xtyping.shed`
    -------------------
    xt.AF  ~  xtyping.shed.AF  ~  ~AF
    xt.AFn  ~  xtyping.shed.AFn  ~  ~AFn
    xt.AnyAsyncCallable  ~  xtyping.shed.AnyAsyncCallable  ~  typing.Callable[..., typing.Awaitable[typing.Any]]
    xt.AnyCallable  ~  xtyping.shed.AnyCallable  ~  typing.Callable[..., typing.Any]
    xt.AnyFunction  ~  xtyping.shed.AnyFunction  ~  typing.Union[typing.Callable[..., ~R], typing.Callable[..., typing.Awaitable[~R]]]
    xt.AnyIterable  ~  xtyping.shed.AnyIterable  ~  typing.Union[typing.Iterable[~T], typing.AsyncIterable[~T]]
    xt.AnyIterator  ~  xtyping.shed.AnyIterator  ~  typing.Union[typing.Iterator[~T], typing.AsyncIterator[~T]]
    xt.ArrShape  ~  xtyping.shed.ArrShape  ~  typing.Tuple[int, ...]
    xt.ArrayShape  ~  xtyping.shed.ArrayShape  ~  typing.Tuple[int, ...]
    xt.AsyncFn  ~  xtyping.shed.AsyncFn  ~  ~AsyncFn
    xt.AsyncFuncType  ~  xtyping.shed.AsyncFuncType  ~  typing.Callable[..., typing.Awaitable[typing.Any]]
    xt.Bytes  ~  xtyping.shed.Bytes  ~  typing.Union[bytes, bytearray]
    xt.BytesPath  ~  xtyping.shed.BytesPath  ~  typing.Union[bytes, os.PathLike]
    xt.CmdArgs  ~  xtyping.shed.CmdArgs  ~  typing.Union[bytes, str, typing.Sequence[str], typing.Sequence[typing.Union[str, pathlib.Path, os.PathLike]]]
    xt.CmdArgsType  ~  xtyping.shed.CmdArgsType  ~  typing.Union[bytes, str, typing.Sequence[str], typing.Sequence[typing.Union[str, pathlib.Path, os.PathLike]]]
    xt.D  ~  xtyping.shed.D  ~  typing.Dict
    xt.DT  ~  xtyping.shed.DT  ~  ~DT
    xt.DictAny  ~  xtyping.shed.DictAny  ~  typing.Dict[typing.Any, typing.Any]
    xt.DictAnyAny  ~  xtyping.shed.DictAnyAny  ~  typing.Dict[typing.Any, typing.Any]
    xt.DictFloat  ~  xtyping.shed.DictFloat  ~  typing.Dict[float, float]
    xt.DictFloatFloat  ~  xtyping.shed.DictFloatFloat  ~  typing.Dict[float, float]
    xt.DictInt  ~  xtyping.shed.DictInt  ~  typing.Dict[int, int]
    xt.DictIntInt  ~  xtyping.shed.DictIntInt  ~  typing.Dict[int, int]
    xt.DictNumber  ~  xtyping.shed.DictNumber  ~  typing.Dict[typing.Union[float, int], typing.Union[float, int]]
    xt.DictNumberNumber  ~  xtyping.shed.DictNumberNumber  ~  typing.Dict[typing.Union[float, int], typing.Union[float, int]]
    xt.DictStr  ~  xtyping.shed.DictStr  ~  typing.Dict[str, str]
    xt.DictStrAny  ~  xtyping.shed.DictStrAny  ~  typing.Dict[str, typing.Any]
    xt.DictStrInt  ~  xtyping.shed.DictStrInt  ~  typing.Dict[str, int]
    xt.DictStrStr  ~  xtyping.shed.DictStrStr  ~  typing.Dict[str, str]
    xt.El  ~  xtyping.shed.El  ~  ~El
    xt.Element  ~  xtyping.shed.Element  ~  ~Element
    xt.Enum  ~  xtyping.shed.Enum  ~  <enum 'Enum'>
    xt.EnvMap  ~  xtyping.shed.EnvMap  ~  typing.Union[typing.Mapping[bytes, typing.Union[bytes, str]], typing.Mapping[str, typing.Union[bytes, str]]]
    xt.EnvType  ~  xtyping.shed.EnvType  ~  typing.Union[typing.Mapping[bytes, typing.Union[bytes, str]], typing.Mapping[str, typing.Union[bytes, str]]]
    xt.F  ~  xtyping.shed.F  ~  ~F
    xt.FALSE  ~  xtyping.shed.FALSE  ~  typing.Literal[False]
    xt.FN  ~  xtyping.shed.FN  ~  ~FN
    xt.Flint  ~  xtyping.shed.Flint  ~  typing.Union[float, int]
    xt.Fn  ~  xtyping.shed.Fn  ~  ~Fn
    xt.FsPath  ~  xtyping.shed.FsPath  ~  typing.Union[str, pathlib.Path, os.PathLike]
    xt.FsPathLike  ~  xtyping.shed.FsPathLike  ~  <class 'os.PathLike'>
    xt.FuncType  ~  xtyping.shed.FuncType  ~  typing.Callable[..., typing.Any]
    xt.HrTime  ~  xtyping.shed.HrTime  ~  typing.Tuple[int, int]
    xt.IntStr  ~  xtyping.shed.IntStr  ~  typing.Union[int, str]
    xt.IterableAny  ~  xtyping.shed.IterableAny  ~  typing.Iterable[typing.Any]
    xt.IterableFloat  ~  xtyping.shed.IterableFloat  ~  typing.Iterable[float]
    xt.IterableInt  ~  xtyping.shed.IterableInt  ~  typing.Iterable[int]
    xt.IterableNumber  ~  xtyping.shed.IterableNumber  ~  typing.Iterable[typing.Union[float, int]]
    xt.IterableStr  ~  xtyping.shed.IterableStr  ~  typing.Iterable[str]
    xt.IterableT  ~  xtyping.shed.IterableT  ~  typing.Iterable[~T]
    xt.Json  ~  xtyping.shed.Json  ~  typing.Union[typing.Dict[str, ForwardRef('Json')], typing.List[ForwardRef('Json')], str, int, float, bool, NoneType]
    xt.JsonArrT  ~  xtyping.shed.JsonArrT  ~  typing.List[typing.Any]
    xt.JsonDictT  ~  xtyping.shed.JsonDictT  ~  typing.Dict[str, typing.Any]
    xt.JsonListT  ~  xtyping.shed.JsonListT  ~  typing.List[typing.Any]
    xt.JsonObjT  ~  xtyping.shed.JsonObjT  ~  typing.Dict[str, typing.Any]
    xt.JsonPrimitive  ~  xtyping.shed.JsonPrimitive  ~  typing.Union[NoneType, bool, int, float, str]
    xt.JsonT  ~  xtyping.shed.JsonT  ~  typing.Union[typing.Dict[str, ForwardRef('JsonT')], typing.List[ForwardRef('JsonT')], str, int, float, bool, NoneType]
    xt.KT  ~  xtyping.shed.KT  ~  ~KT
    xt.KT_co  ~  xtyping.shed.KT_co  ~  +KT_co
    xt.KT_contra  ~  xtyping.shed.KT_contra  ~  -KT_contra
    xt.KeyT  ~  xtyping.shed.KeyT  ~  ~KeyT
    xt.KeyType  ~  xtyping.shed.KeyType  ~  ~KeyType
    xt.L  ~  xtyping.shed.L  ~  typing.Literal
    xt.ListAny  ~  xtyping.shed.ListAny  ~  typing.List[typing.Any]
    xt.ListFloat  ~  xtyping.shed.ListFloat  ~  typing.List[float]
    xt.ListInt  ~  xtyping.shed.ListInt  ~  typing.List[int]
    xt.ListListStr  ~  xtyping.shed.ListListStr  ~  typing.List[typing.List[str]]
    xt.ListNumber  ~  xtyping.shed.ListNumber  ~  typing.List[typing.Union[float, int]]
    xt.ListStr  ~  xtyping.shed.ListStr  ~  typing.List[str]
    xt.ListT  ~  xtyping.shed.ListT  ~  typing.List[~T]
    xt.Lit  ~  xtyping.shed.Lit  ~  typing.Literal
    xt.Ls  ~  xtyping.shed.Ls  ~  typing.List
    xt.N  ~  xtyping.shed.N  ~  ~N
    xt.NoneBytes  ~  xtyping.shed.NoneBytes  ~  typing.Union[bytes, NoneType]
    xt.NoneStr  ~  xtyping.shed.NoneStr  ~  typing.Union[str, NoneType]
    xt.NoneStrBytes  ~  xtyping.shed.NoneStrBytes  ~  typing.Union[str, bytes, NoneType]
    xt.NoneType  ~  xtyping.shed.NoneType  ~  <class 'NoneType'>
    xt.Null  ~  xtyping.shed.Null  ~  <class 'NoneType'>
    xt.Number  ~  xtyping.shed.Number  ~  typing.Union[float, int]
    xt.ONE  ~  xtyping.shed.ONE  ~  typing.Literal[True]
    xt.OpenBinaryMode  ~  xtyping.shed.OpenBinaryMode  ~  typing.Union[typing.Literal['rb+', 'r+b', '+rb', 'br+', 'b+r', '+br', 'wb+', 'w+b', '+wb', 'bw+', 'b+w', '+bw', 'ab+', 'a+b', '+ab', 'ba+', 'b+a', '+ba', 'xb+', 'x+b', '+xb', 'bx+', 'b+x', '+bx'], typing.Literal['rb', 'br', 'rbU', 'rUb', 'Urb', 'brU', 'bUr', 'Ubr'], typing.Literal['wb', 'bw', 'ab', 'ba', 'xb', 'bx']]
    xt.OpenBinaryModeReading  ~  xtyping.shed.OpenBinaryModeReading  ~  typing.Literal['rb', 'br', 'rbU', 'rUb', 'Urb', 'brU', 'bUr', 'Ubr']
    xt.OpenBinaryModeUpdating  ~  xtyping.shed.OpenBinaryModeUpdating  ~  typing.Literal['rb+', 'r+b', '+rb', 'br+', 'b+r', '+br', 'wb+', 'w+b', '+wb', 'bw+', 'b+w', '+bw', 'ab+', 'a+b', '+ab', 'ba+', 'b+a', '+ba', 'xb+', 'x+b', '+xb', 'bx+', 'b+x', '+bx']
    xt.OpenBinaryModeWriting  ~  xtyping.shed.OpenBinaryModeWriting  ~  typing.Literal['wb', 'bw', 'ab', 'ba', 'xb', 'bx']
    xt.OpenTextMode  ~  xtyping.shed.OpenTextMode  ~  typing.Union[typing.Literal['r+', '+r', 'rt+', 'r+t', '+rt', 'tr+', 't+r', '+tr', 'w+', '+w', 'wt+', 'w+t', '+wt', 'tw+', 't+w', '+tw', 'a+', '+a', 'at+', 'a+t', '+at', 'ta+', 't+a', '+ta', 'x+', '+x', 'xt+', 'x+t', '+xt', 'tx+', 't+x', '+tx'], typing.Literal['w', 'wt', 'tw', 'a', 'at', 'ta', 'x', 'xt', 'tx'], typing.Literal['r', 'rt', 'tr', 'U', 'rU', 'Ur', 'rtU', 'rUt', 'Urt', 'trU', 'tUr', 'Utr']]
    xt.OpenTextModeReading  ~  xtyping.shed.OpenTextModeReading  ~  typing.Literal['r', 'rt', 'tr', 'U', 'rU', 'Ur', 'rtU', 'rUt', 'Urt', 'trU', 'tUr', 'Utr']
    xt.OpenTextModeUpdating  ~  xtyping.shed.OpenTextModeUpdating  ~  typing.Literal['r+', '+r', 'rt+', 'r+t', '+rt', 'tr+', 't+r', '+tr', 'w+', '+w', 'wt+', 'w+t', '+wt', 'tw+', 't+w', '+tw', 'a+', '+a', 'at+', 'a+t', '+at', 'ta+', 't+a', '+ta', 'x+', '+x', 'xt+', 'x+t', '+xt', 'tx+', 't+x', '+tx']
    xt.OpenTextModeWriting  ~  xtyping.shed.OpenTextModeWriting  ~  typing.Literal['w', 'wt', 'tw', 'a', 'at', 'ta', 'x', 'xt', 'tx']
    xt.Opt  ~  xtyping.shed.Opt  ~  typing.Optional
    xt.OptFloat  ~  xtyping.shed.OptFloat  ~  typing.Union[float, NoneType]
    xt.OptInt  ~  xtyping.shed.OptInt  ~  typing.Union[int, NoneType]
    xt.OptStr  ~  xtyping.shed.OptStr  ~  typing.Union[str, NoneType]
    xt.OptionalFloat  ~  xtyping.shed.OptionalFloat  ~  typing.Union[float, NoneType]
    xt.OptionalInt  ~  xtyping.shed.OptionalInt  ~  typing.Union[int, NoneType]
    xt.OptionalStr  ~  xtyping.shed.OptionalStr  ~  typing.Union[str, NoneType]
    xt.P  ~  xtyping.shed.P  ~  ~P
    xt.PT  ~  xtyping.shed.PT  ~  ~PT
    xt.Path  ~  xtyping.shed.Path  ~  <class 'pathlib.Path'>
    xt.PathLike  ~  xtyping.shed.PathLike  ~  <class 'os.PathLike'>
    xt.R  ~  xtyping.shed.R  ~  ~R
    xt.RT  ~  xtyping.shed.RT  ~  ~RT
    xt.ReturnT  ~  xtyping.shed.ReturnT  ~  ~ReturnT
    xt.ReturnType  ~  xtyping.shed.ReturnType  ~  ~ReturnType
    xt.STDIN  ~  xtyping.shed.STDIN  ~  typing.Union[bytes, str, NoneType]
    xt.STDIO  ~  xtyping.shed.STDIO  ~  typing.Union[NoneType, int, bytes, typing.IO[typing.Any]]
    xt.Self  ~  xtyping.shed.Self  ~  ~Self
    xt.Seq  ~  xtyping.shed.Seq  ~  typing.Sequence
    xt.SetAny  ~  xtyping.shed.SetAny  ~  typing.Set[typing.Any]
    xt.SetFloat  ~  xtyping.shed.SetFloat  ~  typing.Set[float]
    xt.SetInt  ~  xtyping.shed.SetInt  ~  typing.Set[int]
    xt.SetNumber  ~  xtyping.shed.SetNumber  ~  typing.Set[typing.Union[float, int]]
    xt.SetStr  ~  xtyping.shed.SetStr  ~  typing.Set[str]
    xt.SetT  ~  xtyping.shed.SetT  ~  typing.Set[~T]
    xt.ShapeType  ~  xtyping.shed.ShapeType  ~  typing.Tuple[int, ...]
    xt.StrBytes  ~  xtyping.shed.StrBytes  ~  typing.Union[str, bytes]
    xt.StrEnum  ~  xtyping.shed.StrEnum  ~  <enum 'StrEnum'>
    xt.StrIntFloat  ~  xtyping.shed.StrIntFloat  ~  typing.Union[str, float, int]
    xt.StrOrBytesPath  ~  xtyping.shed.StrOrBytesPath  ~  typing.Union[str, bytes, os.PathLike]
    xt.StrPath  ~  xtyping.shed.StrPath  ~  typing.Union[str, os.PathLike]
    xt.StringEnum  ~  xtyping.shed.StringEnum  ~  <enum 'StringEnum'>
    xt.T  ~  xtyping.shed.T  ~  ~T
    xt.TRUE  ~  xtyping.shed.TRUE  ~  typing.Literal[True]
    xt.T_ParamSpec  ~  xtyping.shed.T_ParamSpec  ~  ~T_ParamSpec
    xt.T_Retval  ~  xtyping.shed.T_Retval  ~  ~T_Retval
    xt.T_co  ~  xtyping.shed.T_co  ~  +T_co
    xt.T_contra  ~  xtyping.shed.T_contra  ~  -T_contra
    xt.TupleStrStr  ~  xtyping.shed.TupleStrStr  ~  typing.Tuple[str, str]
    xt.TupleStrs  ~  xtyping.shed.TupleStrs  ~  typing.Tuple[str, ...]
    xt.Txt  ~  xtyping.shed.Txt  ~  typing.Union[bytes, str]
    xt.U  ~  xtyping.shed.U  ~  typing.Union
    xt.VT  ~  xtyping.shed.VT  ~  ~VT
    xt.VT_co  ~  xtyping.shed.VT_co  ~  +VT_co
    xt.VT_contra  ~  xtyping.shed.VT_contra  ~  -VT_contra
    xt.V_co  ~  xtyping.shed.V_co  ~  +V_co
    xt.ValT  ~  xtyping.shed.ValT  ~  ~ValT
    xt.ValType  ~  xtyping.shed.ValType  ~  ~ValType
    xt.ZERO  ~  xtyping.shed.ZERO  ~  typing.Literal[False]
    xt._DT  ~  xtyping.shed._DT  ~  ~_DT
    xt._KT  ~  xtyping.shed._KT  ~  ~_KT
    xt._KT_co  ~  xtyping.shed._KT_co  ~  +_KT_co
    xt._KT_contra  ~  xtyping.shed._KT_contra  ~  -_KT_contra
    xt._R  ~  xtyping.shed._R  ~  ~_R
    xt._RT  ~  xtyping.shed._RT  ~  ~_RT
    xt._T  ~  xtyping.shed._T  ~  ~_T
    xt._T_co  ~  xtyping.shed._T_co  ~  +_T_co
    xt._T_contra  ~  xtyping.shed._T_contra  ~  -_T_contra
    xt._VT  ~  xtyping.shed._VT  ~  ~_VT
    xt._VT_co  ~  xtyping.shed._VT_co  ~  +_VT_co
    xt._VT_contra  ~  xtyping.shed._VT_contra  ~  -_VT_contra
    xt._V_co  ~  xtyping.shed._V_co  ~  +_V_co
    xt.__all_shed__  ~  xtyping.shed.__all_shed__  ~  ('AF', 'AFn', 'AnyAsyncCallable', 'AnyCallable', 'AnyFunction', 'AnyIterable', 'AnyIterator', 'ArrShape', 'ArrayShape', 'AsyncFn', 'AsyncFuncType', 'Bytes', 'BytesPath', 'CmdArgs', 'CmdArgsType', 'D', 'DT', 'DictAny', 'DictAnyAny', 'DictFloat', 'DictFloatFloat', 'DictInt', 'DictIntInt', 'DictNumber', 'DictNumberNumber', 'DictStr', 'DictStrAny', 'DictStrInt', 'DictStrStr', 'El', 'Element', 'Enum', 'EnvMap', 'EnvType', 'F', 'FALSE', 'FN', 'Flint', 'Fn', 'FsPath', 'FsPathLike', 'FuncType', 'HrTime', 'IntStr', 'IterableAny', 'IterableFloat', 'IterableInt', 'IterableNumber', 'IterableStr', 'IterableT', 'Json', 'JsonArrT', 'JsonDictT', 'JsonListT', 'JsonObjT', 'JsonPrimitive', 'JsonT', 'KT', 'KT_co', 'KT_contra', 'KeyT', 'KeyType', 'L', 'ListAny', 'ListFloat', 'ListInt', 'ListListStr', 'ListNumber', 'ListStr', 'ListT', 'Lit', 'Ls', 'N', 'NoneBytes', 'NoneStr', 'NoneStrBytes', 'NoneType', 'Null', 'Number', 'ONE', 'OpenBinaryMode', 'OpenBinaryModeReading', 'OpenBinaryModeUpdating', 'OpenBinaryModeWriting', 'OpenTextMode', 'OpenTextModeReading', 'OpenTextModeUpdating', 'OpenTextModeWriting', 'Opt', 'OptFloat', 'OptInt', 'OptStr', 'OptionalFloat', 'OptionalInt', 'OptionalStr', 'P', 'PT', 'Path', 'PathLike', 'R', 'RT', 'ReturnT', 'ReturnType', 'STDIN', 'STDIO', 'Self', 'Seq', 'SetAny', 'SetFloat', 'SetInt', 'SetNumber', 'SetStr', 'SetT', 'ShapeType', 'StrBytes', 'StrEnum', 'StrIntFloat', 'StrOrBytesPath', 'StrPath', 'StringEnum', 'T', 'TRUE', 'T_ParamSpec', 'T_Retval', 'T_co', 'T_contra', 'TupleStrStr', 'TupleStrs', 'Txt', 'U', 'VT', 'VT_co', 'VT_contra', 'V_co', 'ValT', 'ValType', 'ZERO', '_DT', '_KT', '_KT_co', '_KT_contra', '_R', '_RT', '_T', '_T_co', '_T_contra', '_VT', '_VT_co', '_VT_contra', '_V_co', '__all_shed__', '__all_typing__', '__all_typing_extensions__', '__all_typing_extensions_future__', 'null')
    xt.__all_typing__  ~  xtyping.shed.__all_typing__  ~  ('AbstractSet', 'Any', 'AnyStr', 'AsyncContextManager', 'AsyncGenerator', 'AsyncIterable', 'AsyncIterator', 'Awaitable', 'ByteString', 'Callable', 'ChainMap', 'ClassVar', 'Collection', 'Container', 'ContextManager', 'Coroutine', 'Counter', 'DefaultDict', 'Deque', 'Dict', 'FrozenSet', 'Generator', 'Generic', 'Hashable', 'IO', 'ItemsView', 'Iterable', 'Iterator', 'KeysView', 'List', 'Mapping', 'MappingView', 'MutableMapping', 'MutableSequence', 'MutableSet', 'NamedTuple', 'NewType', 'Optional', 'Reversible', 'Sequence', 'Set', 'Sized', 'SupportsAbs', 'SupportsBytes', 'SupportsComplex', 'SupportsFloat', 'SupportsInt', 'SupportsRound', 'TYPE_CHECKING', 'Text', 'Tuple', 'Type', 'TypeVar', 'Union', 'ValuesView', 'cast', 'get_type_hints', 'no_type_check', 'no_type_check_decorator', 'overload')
    xt.__all_typing_extensions__  ~  xtyping.shed.__all_typing_extensions__  ~  ('Annotated', 'AsyncContextManager', 'AsyncGenerator', 'AsyncIterable', 'AsyncIterator', 'Awaitable', 'ChainMap', 'ClassVar', 'Concatenate', 'ContextManager', 'Coroutine', 'Counter', 'DefaultDict', 'Deque', 'Final', 'IntVar', 'Literal', 'NewType', 'NoReturn', 'OrderedDict', 'ParamSpec', 'ParamSpecArgs', 'ParamSpecKwargs', 'Protocol', 'SupportsIndex', 'TYPE_CHECKING', 'Text', 'Type', 'TypeAlias', 'TypeGuard', 'TypedDict', 'final', 'get_args', 'get_origin', 'get_type_hints', 'overload', 'runtime', 'runtime_checkable')
    xt.__all_typing_extensions_future__  ~  xtyping.shed.__all_typing_extensions_future__  ~  ('LiteralString', 'Never', 'NotRequired', 'Required', 'Self', 'TypeVarTuple', 'Unpack', 'assert_never', 'assert_type', 'clear_overloads', 'dataclass_transform', 'get_overloads', 'is_typeddict', 'reveal_type')
    xt.null  ~  xtyping.shed.null  ~  <class 'NoneType'>
