# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

from enum import Enum

from azure.core import CaseInsensitiveEnumMeta


class SourceType(Enum, metaclass=CaseInsensitiveEnumMeta):
    """Represents feature source type"""

    MLTABLE = "mltable"
    CSV = "csv"
    PARQUET = "parquet"
    DELTATABLE = "deltaTable"
    CUSTOM = "custom"
    FEATURE_SET = "featureset"

    def __str__(self):
        return self.value
