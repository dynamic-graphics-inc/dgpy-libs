# -*- coding: utf-8 -*-
"""JSONBourne helper funks and utils"""
import re

from typing import Match


__all__ = ["rm_js_comments", "strip_comments"]

STRIP_JSON_COMMENTS_REGEX = r"(\".*?(?<!\\)\"|\'.*?(?<!\\)\')|(/\*.*?\*/|//[^\r\n]*$)"


def _strip_json_comments_regex_replacer(match: Match[str]) -> str:  # type: ignore
    # if the 2nd group (capturing comments) is not None,
    # it means we have captured a non-quoted (real) comment string.
    if match.group(2) is not None:
        return ""  # so we will return empty to remove the comment
    return match.group(1)  # captured quoted-string


def rm_js_comments(string: str) -> str:
    """Rejects/regex that removes js/ts/json style comments

    Source (stackoverflow):
        https://stackoverflow.com/a/18381470
    """
    # first group captures quoted strings (double or single)
    # second group captures comments (//single-line or /* multi-line */)
    regex = re.compile(STRIP_JSON_COMMENTS_REGEX, re.MULTILINE | re.DOTALL)

    return regex.sub(_strip_json_comments_regex_replacer, string)


def strip_comments(string: str) -> str:

    return rm_js_comments(string)
