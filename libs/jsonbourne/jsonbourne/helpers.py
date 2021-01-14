# -*- coding: utf-8 -*-
"""JSONBourne helper funks and utils"""

import re


__all__ = ["rm_js_comments"]


def rm_js_comments(string: str) -> str:
    """Rejects/regex that removes js/ts/json style comments

    Source (stackoverflow):
        https://stackoverflow.com/a/18381470
    """
    pattern = r"(\".*?(?<!\\)\"|\'.*?(?<!\\)\')|(/\*.*?\*/|//[^\r\n]*$)"
    # first group captures quoted strings (double or single)
    # second group captures comments (//single-line or /* multi-line */)
    regex = re.compile(pattern, re.MULTILINE | re.DOTALL)

    def _replacer(match):  # type: ignore
        # if the 2nd group (capturing comments) is not None,
        # it means we have captured a non-quoted (real) comment string.
        if match.group(2) is not None:
            return ""  # so we will return empty to remove the comment
        return match.group(1)  # captured quoted-string

    return regex.sub(_replacer, string)
