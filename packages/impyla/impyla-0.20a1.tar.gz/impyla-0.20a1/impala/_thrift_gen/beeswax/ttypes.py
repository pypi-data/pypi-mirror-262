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

import impala._thrift_gen.hive_metastore.ttypes

from thrift.transport import TTransport
all_structs = []


class QueryState(object):
    CREATED = 0
    INITIALIZED = 1
    COMPILED = 2
    RUNNING = 3
    FINISHED = 4
    EXCEPTION = 5

    _VALUES_TO_NAMES = {
        0: "CREATED",
        1: "INITIALIZED",
        2: "COMPILED",
        3: "RUNNING",
        4: "FINISHED",
        5: "EXCEPTION",
    }

    _NAMES_TO_VALUES = {
        "CREATED": 0,
        "INITIALIZED": 1,
        "COMPILED": 2,
        "RUNNING": 3,
        "FINISHED": 4,
        "EXCEPTION": 5,
    }


class TQueryOptionLevel(object):
    REGULAR = 0
    ADVANCED = 1
    DEVELOPMENT = 2
    DEPRECATED = 3
    REMOVED = 4

    _VALUES_TO_NAMES = {
        0: "REGULAR",
        1: "ADVANCED",
        2: "DEVELOPMENT",
        3: "DEPRECATED",
        4: "REMOVED",
    }

    _NAMES_TO_VALUES = {
        "REGULAR": 0,
        "ADVANCED": 1,
        "DEVELOPMENT": 2,
        "DEPRECATED": 3,
        "REMOVED": 4,
    }


class Query(object):
    """
    Attributes:
     - query
     - configuration
     - hadoop_user

    """


    def __init__(self, query=None, configuration=None, hadoop_user=None,):
        self.query = query
        self.configuration = configuration
        self.hadoop_user = hadoop_user

    def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.STRING:
                    self.query = iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 3:
                if ftype == TType.LIST:
                    self.configuration = []
                    (_etype3, _size0) = iprot.readListBegin()
                    for _i4 in range(_size0):
                        _elem5 = iprot.readString()
                        self.configuration.append(_elem5)
                    iprot.readListEnd()
                else:
                    iprot.skip(ftype)
            elif fid == 4:
                if ftype == TType.STRING:
                    self.hadoop_user = iprot.readString()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
            return
        oprot.writeStructBegin('Query')
        if self.query is not None:
            oprot.writeFieldBegin('query', TType.STRING, 1)
            oprot.writeString(self.query)
            oprot.writeFieldEnd()
        if self.configuration is not None:
            oprot.writeFieldBegin('configuration', TType.LIST, 3)
            oprot.writeListBegin(TType.STRING, len(self.configuration))
            for iter6 in self.configuration:
                oprot.writeString(iter6)
            oprot.writeListEnd()
            oprot.writeFieldEnd()
        if self.hadoop_user is not None:
            oprot.writeFieldBegin('hadoop_user', TType.STRING, 4)
            oprot.writeString(self.hadoop_user)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)


class QueryHandle(object):
    """
    Attributes:
     - id
     - log_context

    """


    def __init__(self, id=None, log_context=None,):
        self.id = id
        self.log_context = log_context

    def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.STRING:
                    self.id = iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.STRING:
                    self.log_context = iprot.readString()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
            return
        oprot.writeStructBegin('QueryHandle')
        if self.id is not None:
            oprot.writeFieldBegin('id', TType.STRING, 1)
            oprot.writeString(self.id)
            oprot.writeFieldEnd()
        if self.log_context is not None:
            oprot.writeFieldBegin('log_context', TType.STRING, 2)
            oprot.writeString(self.log_context)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)


class QueryExplanation(object):
    """
    Attributes:
     - textual

    """


    def __init__(self, textual=None,):
        self.textual = textual

    def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.STRING:
                    self.textual = iprot.readString()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
            return
        oprot.writeStructBegin('QueryExplanation')
        if self.textual is not None:
            oprot.writeFieldBegin('textual', TType.STRING, 1)
            oprot.writeString(self.textual)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)


class Results(object):
    """
    Attributes:
     - ready
     - columns
     - data
     - start_row
     - has_more

    """


    def __init__(self, ready=None, columns=None, data=None, start_row=None, has_more=None,):
        self.ready = ready
        self.columns = columns
        self.data = data
        self.start_row = start_row
        self.has_more = has_more

    def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.BOOL:
                    self.ready = iprot.readBool()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.LIST:
                    self.columns = []
                    (_etype10, _size7) = iprot.readListBegin()
                    for _i11 in range(_size7):
                        _elem12 = iprot.readString()
                        self.columns.append(_elem12)
                    iprot.readListEnd()
                else:
                    iprot.skip(ftype)
            elif fid == 3:
                if ftype == TType.LIST:
                    self.data = []
                    (_etype16, _size13) = iprot.readListBegin()
                    for _i17 in range(_size13):
                        _elem18 = iprot.readString()
                        self.data.append(_elem18)
                    iprot.readListEnd()
                else:
                    iprot.skip(ftype)
            elif fid == 4:
                if ftype == TType.I64:
                    self.start_row = iprot.readI64()
                else:
                    iprot.skip(ftype)
            elif fid == 5:
                if ftype == TType.BOOL:
                    self.has_more = iprot.readBool()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
            return
        oprot.writeStructBegin('Results')
        if self.ready is not None:
            oprot.writeFieldBegin('ready', TType.BOOL, 1)
            oprot.writeBool(self.ready)
            oprot.writeFieldEnd()
        if self.columns is not None:
            oprot.writeFieldBegin('columns', TType.LIST, 2)
            oprot.writeListBegin(TType.STRING, len(self.columns))
            for iter19 in self.columns:
                oprot.writeString(iter19)
            oprot.writeListEnd()
            oprot.writeFieldEnd()
        if self.data is not None:
            oprot.writeFieldBegin('data', TType.LIST, 3)
            oprot.writeListBegin(TType.STRING, len(self.data))
            for iter20 in self.data:
                oprot.writeString(iter20)
            oprot.writeListEnd()
            oprot.writeFieldEnd()
        if self.start_row is not None:
            oprot.writeFieldBegin('start_row', TType.I64, 4)
            oprot.writeI64(self.start_row)
            oprot.writeFieldEnd()
        if self.has_more is not None:
            oprot.writeFieldBegin('has_more', TType.BOOL, 5)
            oprot.writeBool(self.has_more)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)


class ResultsMetadata(object):
    """
    Metadata information about the results.
    Applicable only for SELECT.

    Attributes:
     - schema: The schema of the results
     - table_dir: The directory containing the results. Not applicable for partition table.
     - in_tablename: If the results are straight from an existing table, the table name.
     - delim: Field delimiter

    """


    def __init__(self, schema=None, table_dir=None, in_tablename=None, delim=None,):
        self.schema = schema
        self.table_dir = table_dir
        self.in_tablename = in_tablename
        self.delim = delim

    def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.STRUCT:
                    self.schema = impala._thrift_gen.hive_metastore.ttypes.Schema()
                    self.schema.read(iprot)
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.STRING:
                    self.table_dir = iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 3:
                if ftype == TType.STRING:
                    self.in_tablename = iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 4:
                if ftype == TType.STRING:
                    self.delim = iprot.readString()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
            return
        oprot.writeStructBegin('ResultsMetadata')
        if self.schema is not None:
            oprot.writeFieldBegin('schema', TType.STRUCT, 1)
            self.schema.write(oprot)
            oprot.writeFieldEnd()
        if self.table_dir is not None:
            oprot.writeFieldBegin('table_dir', TType.STRING, 2)
            oprot.writeString(self.table_dir)
            oprot.writeFieldEnd()
        if self.in_tablename is not None:
            oprot.writeFieldBegin('in_tablename', TType.STRING, 3)
            oprot.writeString(self.in_tablename)
            oprot.writeFieldEnd()
        if self.delim is not None:
            oprot.writeFieldBegin('delim', TType.STRING, 4)
            oprot.writeString(self.delim)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)


class BeeswaxException(TException):
    """
    Attributes:
     - message
     - log_context
     - handle
     - errorCode
     - SQLState

    """


    def __init__(self, message=None, log_context=None, handle=None, errorCode=0, SQLState="     ",):
        super(BeeswaxException, self).__setattr__('message', message)
        super(BeeswaxException, self).__setattr__('log_context', log_context)
        super(BeeswaxException, self).__setattr__('handle', handle)
        super(BeeswaxException, self).__setattr__('errorCode', errorCode)
        super(BeeswaxException, self).__setattr__('SQLState', SQLState)

    def __setattr__(self, *args):
        raise TypeError("can't modify immutable instance")

    def __delattr__(self, *args):
        raise TypeError("can't modify immutable instance")

    def __hash__(self):
        return hash(self.__class__) ^ hash((self.message, self.log_context, self.handle, self.errorCode, self.SQLState, ))

    @classmethod
    def read(cls, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and cls.thrift_spec is not None:
            return iprot._fast_decode(None, iprot, [cls, cls.thrift_spec])
        iprot.readStructBegin()
        message = None
        log_context = None
        handle = None
        errorCode = 0
        SQLState = "     "
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.STRING:
                    message = iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.STRING:
                    log_context = iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 3:
                if ftype == TType.STRUCT:
                    handle = QueryHandle()
                    handle.read(iprot)
                else:
                    iprot.skip(ftype)
            elif fid == 4:
                if ftype == TType.I32:
                    errorCode = iprot.readI32()
                else:
                    iprot.skip(ftype)
            elif fid == 5:
                if ftype == TType.STRING:
                    SQLState = iprot.readString()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()
        return cls(
            message=message,
            log_context=log_context,
            handle=handle,
            errorCode=errorCode,
            SQLState=SQLState,
        )

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
            return
        oprot.writeStructBegin('BeeswaxException')
        if self.message is not None:
            oprot.writeFieldBegin('message', TType.STRING, 1)
            oprot.writeString(self.message)
            oprot.writeFieldEnd()
        if self.log_context is not None:
            oprot.writeFieldBegin('log_context', TType.STRING, 2)
            oprot.writeString(self.log_context)
            oprot.writeFieldEnd()
        if self.handle is not None:
            oprot.writeFieldBegin('handle', TType.STRUCT, 3)
            self.handle.write(oprot)
            oprot.writeFieldEnd()
        if self.errorCode is not None:
            oprot.writeFieldBegin('errorCode', TType.I32, 4)
            oprot.writeI32(self.errorCode)
            oprot.writeFieldEnd()
        if self.SQLState is not None:
            oprot.writeFieldBegin('SQLState', TType.STRING, 5)
            oprot.writeString(self.SQLState)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __str__(self):
        return repr(self)

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)


class QueryNotFoundException(TException):


    def __setattr__(self, *args):
        raise TypeError("can't modify immutable instance")

    def __delattr__(self, *args):
        raise TypeError("can't modify immutable instance")

    def __hash__(self):
        return hash(self.__class__) ^ hash(())

    @classmethod
    def read(cls, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and cls.thrift_spec is not None:
            return iprot._fast_decode(None, iprot, [cls, cls.thrift_spec])
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()
        return cls(
        )

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
            return
        oprot.writeStructBegin('QueryNotFoundException')
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __str__(self):
        return repr(self)

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)


class ConfigVariable(object):
    """
    Represents a Hadoop-style configuration variable.

    Attributes:
     - key
     - value
     - description
     - level

    """


    def __init__(self, key=None, value=None, description=None, level=None,):
        self.key = key
        self.value = value
        self.description = description
        self.level = level

    def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.STRING:
                    self.key = iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.STRING:
                    self.value = iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 3:
                if ftype == TType.STRING:
                    self.description = iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 4:
                if ftype == TType.I32:
                    self.level = iprot.readI32()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
            return
        oprot.writeStructBegin('ConfigVariable')
        if self.key is not None:
            oprot.writeFieldBegin('key', TType.STRING, 1)
            oprot.writeString(self.key)
            oprot.writeFieldEnd()
        if self.value is not None:
            oprot.writeFieldBegin('value', TType.STRING, 2)
            oprot.writeString(self.value)
            oprot.writeFieldEnd()
        if self.description is not None:
            oprot.writeFieldBegin('description', TType.STRING, 3)
            oprot.writeString(self.description)
            oprot.writeFieldEnd()
        if self.level is not None:
            oprot.writeFieldBegin('level', TType.I32, 4)
            oprot.writeI32(self.level)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)
all_structs.append(Query)
Query.thrift_spec = (
    None,  # 0
    (1, TType.STRING, 'query', None, None, ),  # 1
    None,  # 2
    (3, TType.LIST, 'configuration', (TType.STRING, None, False), None, ),  # 3
    (4, TType.STRING, 'hadoop_user', None, None, ),  # 4
)
all_structs.append(QueryHandle)
QueryHandle.thrift_spec = (
    None,  # 0
    (1, TType.STRING, 'id', None, None, ),  # 1
    (2, TType.STRING, 'log_context', None, None, ),  # 2
)
all_structs.append(QueryExplanation)
QueryExplanation.thrift_spec = (
    None,  # 0
    (1, TType.STRING, 'textual', None, None, ),  # 1
)
all_structs.append(Results)
Results.thrift_spec = (
    None,  # 0
    (1, TType.BOOL, 'ready', None, None, ),  # 1
    (2, TType.LIST, 'columns', (TType.STRING, None, False), None, ),  # 2
    (3, TType.LIST, 'data', (TType.STRING, None, False), None, ),  # 3
    (4, TType.I64, 'start_row', None, None, ),  # 4
    (5, TType.BOOL, 'has_more', None, None, ),  # 5
)
all_structs.append(ResultsMetadata)
ResultsMetadata.thrift_spec = (
    None,  # 0
    (1, TType.STRUCT, 'schema', [impala._thrift_gen.hive_metastore.ttypes.Schema, None], None, ),  # 1
    (2, TType.STRING, 'table_dir', None, None, ),  # 2
    (3, TType.STRING, 'in_tablename', None, None, ),  # 3
    (4, TType.STRING, 'delim', None, None, ),  # 4
)
all_structs.append(BeeswaxException)
BeeswaxException.thrift_spec = (
    None,  # 0
    (1, TType.STRING, 'message', None, None, ),  # 1
    (2, TType.STRING, 'log_context', None, None, ),  # 2
    (3, TType.STRUCT, 'handle', [QueryHandle, None], None, ),  # 3
    (4, TType.I32, 'errorCode', None, 0, ),  # 4
    (5, TType.STRING, 'SQLState', None, "     ", ),  # 5
)
all_structs.append(QueryNotFoundException)
QueryNotFoundException.thrift_spec = (
)
all_structs.append(ConfigVariable)
ConfigVariable.thrift_spec = (
    None,  # 0
    (1, TType.STRING, 'key', None, None, ),  # 1
    (2, TType.STRING, 'value', None, None, ),  # 2
    (3, TType.STRING, 'description', None, None, ),  # 3
    (4, TType.I32, 'level', None, None, ),  # 4
)
fix_spec(all_structs)
del all_structs
