# -*- coding: utf-8 -*-
"""Collections for component client"""
from .apis.bk_login import CollectionsBkLogin
from .apis.cc import CollectionsCC
from .apis.cmsi import CollectionsCMSI
from .apis.job import CollectionsJOB


# Available components
AVAILABLE_COLLECTIONS = {
    'bk_login': CollectionsBkLogin,
    'cc': CollectionsCC,
    'cmsi': CollectionsCMSI,
    'job': CollectionsJOB,
}
