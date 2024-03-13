#
# Autogenerated by Thrift Compiler (0.16.0)
#
# DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
#
#  options string: py:new_style,no_utf8strings
#

from thrift.Thrift import TType, TMessageType, TFrozenDict, TException, TApplicationException
from thrift.protocol.TProtocol import TProtocolException
from thrift.TRecursive import fix_spec

from .ttypes import *
PRIMITIVE_TYPES = set((
    0,
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    15,
    16,
    17,
    18,
    19,
))
COMPLEX_TYPES = set((
    10,
    11,
    12,
    13,
    14,
))
COLLECTION_TYPES = set((
    10,
    11,
))
TYPE_NAMES = {
    10: "ARRAY",
    4: "BIGINT",
    9: "BINARY",
    0: "BOOLEAN",
    19: "CHAR",
    17: "DATE",
    15: "DECIMAL",
    6: "DOUBLE",
    5: "FLOAT",
    3: "INT",
    11: "MAP",
    16: "NULL",
    2: "SMALLINT",
    7: "STRING",
    12: "STRUCT",
    8: "TIMESTAMP",
    1: "TINYINT",
    13: "UNIONTYPE",
    18: "VARCHAR",
}
CHARACTER_MAXIMUM_LENGTH = "characterMaximumLength"
PRECISION = "precision"
SCALE = "scale"
