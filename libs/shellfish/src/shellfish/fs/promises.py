# -*- coding: utf-8 -*-
"""shellfish.fs.promises"""

from __future__ import annotations

from shellfish.fs._async import (
    dir_exists_async as dir_exists,
    exists_async as exists,
    file_exists_async as file_exists,
    is_dir_async as is_dir,
    is_file_async as is_file,
    is_link_async as is_link,
    isdir_async as isdir,
    isfile_async as isfile,
    islink_async as islink,
    lbytes_async as lbytes,
    lbytes_gen_async as lbytes_gen,
    lstat_async as lstat,
    lstr_async as lstr,
    lstring_async as lstring,
    rbin_async as rbin,
    rbin_gen_async as rbin_gen,
    rbytes_async as rbytes,
    rbytes_gen_async as rbytes_gen,
    read_bytes_async as read_bytes,
    read_bytes_gen_async as read_bytes_gen,
    read_str_async as read_str,
    rstr_async as rstr,
    rstring_async as rstring,
    sbin_async as sbin,
    sbytes_async as sbytes,
    sbytes_gen_async as sbytes_gen,
    sstr_async as sstr,
    sstring_async as sstring,
    stat_async as stat,
    wbin_async as wbin,
    wbin_gen_async as wbin_gen,
    wbytes_async as wbytes,
    wbytes_gen_async as wbytes_gen,
    write_bytes_async as write_bytes,
    write_bytes_gen_async as write_bytes_gen,
    write_str_async as write_str,
    wstr_async as wstr,
    wstring_async as wstring,
)

__all__ = (
    "dir_exists",
    "exists",
    "file_exists",
    "is_dir",
    "is_file",
    "is_link",
    "isdir",
    "isfile",
    "islink",
    "lbytes",
    "lbytes_gen",
    "lstat",
    "lstr",
    "lstring",
    "rbin",
    "rbin_gen",
    "rbytes",
    "rbytes_gen",
    "read_bytes",
    "read_bytes_gen",
    "read_str",
    "rstr",
    "rstring",
    "sbin",
    "sbytes",
    "sbytes_gen",
    "sstr",
    "sstring",
    "stat",
    "wbin",
    "wbin_gen",
    "wbytes",
    "wbytes_gen",
    "write_bytes",
    "write_bytes_gen",
    "write_str",
    "wstr",
    "wstring",
)
