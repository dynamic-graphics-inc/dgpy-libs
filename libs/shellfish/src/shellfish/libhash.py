from __future__ import annotations

from dataclasses import dataclass
from hashlib import blake2b, blake2s, md5, sha1, sha224, sha256, sha384, sha512
from typing import TYPE_CHECKING, Callable, Dict, Iterator, Union

if TYPE_CHECKING:
    from hashlib import _Hash

__all__ = ("hash_bytes_gen", "string2hasher")

_HASHERS: Dict[str, Callable[[], "_Hash"]] = {
    "blake2b": blake2b,  # type: ignore[dict-item]
    "blake2s": blake2s,  # type: ignore[dict-item]
    "md5": md5,
    "sha1": sha1,
    "sha224": sha224,
    "sha256": sha256,
    "sha384": sha384,
    "sha512": sha512,
}

HashLike = Union[str, "_Hash"]


@dataclass
class Hashed:
    """Hashed Result"""

    b: bytes
    s: str

    __slots__ = ("b", "s")


def string2hasher(string: str) -> "_Hash":
    """Return a hash object from a string

    Args:
        string (str): String to hash

    Returns:
        hash: Hash object

    """
    try:
        return _HASHERS[string]()
    except KeyError:
        raise ValueError(
            f"Invalid hash algorithm: {string} (valid: {list(_HASHERS.keys())})"
        ) from None


def hasher(obj: HashLike) -> "_Hash":
    """Return a hash object from a string or a hash object

    Args:
        obj (Union[str, hash]): String or hash object

    Returns:
        hash: Hash object

    Examples:
        >>> hashobj = hasher("sha256")
        >>> hashobj.update(b"Hello World")
        >>> hashobj.hexdigest()
        'a591a6d40bf420404a011733cfb7b190d62c65bf0bcda32b57b277d9ad9f146e'

    """
    if isinstance(obj, str):
        return string2hasher(obj)
    return obj


def hash_bytes_gen(it: Iterator[bytes], hashlike: HashLike) -> str:
    """Return the hash of an iterator of bytes

    Args:
        it (Iterator[bytes]): Iterator of bytes
        hashlike (hash): Hash like object; can be a string or a '_Hash' object

    Returns:
        str: Hash of the iterator

    """
    _hasher = hasher(hashlike)
    for chunk in it:
        _hasher.update(chunk)
    return _hasher.hexdigest()
