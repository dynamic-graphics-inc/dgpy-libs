from enum import Enum

__all__ = (
    "LICENSES",
    "License",
)

LICENSES = (
    "Apache-2.0",
    "BSD-2-Clause",
    "BSD-3-Clause",
    "BSD-4-Clause",
    "GPL-2.0-only",
    "GPL-2.0-or-later",
    "GPL-3.0-only",
    "GPL-3.0-or-later",
    "LGPL-2.1-only",
    "LGPL-2.1-or-later",
    "LGPL-3.0-only",
    "LGPL-3.0-or-later",
    "MIT",
    "Proprietary",
)


class License(Enum):
    Apache_2_0 = "Apache-2.0"
    BSD_2_Clause = "BSD-2-Clause"
    BSD_3_Clause = "BSD-3-Clause"
    BSD_4_Clause = "BSD-4-Clause"
    GPL_2_0_only = "GPL-2.0-only"
    GPL_2_0_or_later = "GPL-2.0-or-later"
    GPL_3_0_only = "GPL-3.0-only"
    GPL_3_0_or_later = "GPL-3.0-or-later"
    LGPL_2_1_only = "LGPL-2.1-only"
    LGPL_2_1_or_later = "LGPL-2.1-or-later"
    LGPL_3_0_only = "LGPL-3.0-only"
    LGPL_3_0_or_later = "LGPL-3.0-or-later"
    MIT = "MIT"
    # proprietary
    Proprietary = "Proprietary"
