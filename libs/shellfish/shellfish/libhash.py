from hashlib import blake2b, blake2s, md5, sha1, sha224, sha256, sha384, sha512
from typing import TYPE_CHECKING, Callable, Dict, Iterator

if TYPE_CHECKING:
    from hashlib import _Hash

__all__ = ("string2hasher", "hash_bytes_gen")

_HASHERS: Dict[str, Callable[[], "_Hash"]] = {
    "blake2b": blake2b,
    "blake2s": blake2s,
    "md5": md5,
    "sha1": sha1,
    "sha224": sha224,
    "sha256": sha256,
    "sha384": sha384,
    "sha512": sha512,
}


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
        )


def hash_bytes_gen(it: Iterator[bytes], hasher: "_Hash") -> str:
    """Return the hash of an iterator of bytes

    Args:
        it (Iterator[bytes]): Iterator of bytes
        hasher (hash): Hash object

    Returns:
        str: Hash of the iterator

    """
    for chunk in it:
        hasher.update(chunk)
    return hasher.hexdigest()
