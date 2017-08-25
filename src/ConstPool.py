import struct
from Common import *

CONST = enum(
    Class = '\x07',
    FieldRef = '\x09',
    MethodRef = '\x0a',
    InterfaceMethodRef = '\x0b',
    String = '\x08',
    Integer = '\x03',
    Float = '\x04',
    Long = '\x05',
    Double = '\x06',
    NameAndType = '\x0c',
    Utf8 = '\x01'
)

J9CONST = enum(
    INT = 0,
    STRING = 1,
    CLASS = 2,
    LONG = 3,
    REF = 4
)

class ConstPool(object):
    def __init__(self, romclass):
        self.pool = []
        self.transform = {}
        stack = []
        # self.pool.append([-1, None])
        for i, constant in enumerate(romclass.constant_pool):
            if constant.type == J9CONST.INT:
                index = len(self.pool)
                self.pool.append([CONST.Integer, constant.value])
                self.transform[i] = {'new_index': index, 'type': CONST.Integer}
            elif constant.type == J9CONST.LONG:
                index = len(self.pool)
                self.pool.append([CONST.Double, constant.value[::-1]])
                self.pool.append([-1, None])
                self.transform[i] = {'new_index': index, 'type': CONST.Double}
            elif constant.type == J9CONST.STRING:
                index = len(self.pool)
                self.pool.append([CONST.String, ''])
                stack.append((index, CONST.Utf8, struct.pack('>H', len(constant.value)) + constant.value))
                self.transform[i] = {'new_index': index, 'type': CONST.String}
            elif constant.type == J9CONST.CLASS:
                index = len(self.pool)
                self.pool.append([CONST.Class, ''])
                stack.append((index, CONST.Utf8, struct.pack('>H', len(constant.value)) + constant.value))
                self.transform[i] = {'new_index': index, 'type': CONST.Class}
            elif constant.type == J9CONST.REF:
                index = len(self.pool)
                const_type = CONST.MethodRef if constant.descriptor.find('(') >= 0 else CONST.FieldRef
                self.pool.append([const_type, '', ''])
                stack.append((index, CONST.Class, struct.pack('>H', len(constant._class)) + constant._class))
                stack.append((index, CONST.NameAndType, struct.pack('>H', len(constant.name)) + constant.name,
                              struct.pack('>H', len(constant.descriptor)) + constant.descriptor))
                self.transform[i] = {'new_index': index, 'type': const_type}
        for elem in stack:
            cp_id = len(self.pool)
            if elem[1] == CONST.Utf8:
                self.pool.append([elem[1], elem[2]])
                if self.pool[elem[0]][1]:
                    self.pool[elem[0]][2] = struct.pack('>H', cp_id + 1)
                else:
                    self.pool[elem[0]][1] = struct.pack('>H', cp_id + 1)
            elif elem[1] == CONST.Class:
                self.pool.append([elem[1], ''])
                stack.append((cp_id, CONST.Utf8, elem[2]))
                self.pool[elem[0]][1] = struct.pack('>H', cp_id + 1)
            elif elem[1] == CONST.NameAndType:
                self.pool.append([elem[1], '', ''])
                stack.append((cp_id, CONST.Utf8, elem[2]))
                stack.append((cp_id, CONST.Utf8, elem[3]))
                self.pool[elem[0]][2] = struct.pack('>H', cp_id + 1)

    def add(self, type, value):
        if type == CONST.Class:
            index = len(self.pool)
            self.pool.append([CONST.Utf8, struct.pack('>H', len(value)) + bytearray(value, 'utf8')])
            self.pool.append([CONST.Class, struct.pack('>H', index + 1)])
            return index + 2
        elif type == CONST.Utf8:
            index = len(self.pool)
            self.pool.append([CONST.Utf8, struct.pack('>H', len(value)) + bytearray(value, 'utf8')])
            return index + 1

    def apply_transform(self, index, type):
        self.pool[index][0] = type

    def check_transform(self, index, type=None):
        return index in self.transform and (type and self.transform[index]['type'] == '\x06')

    def get_transform(self, index):
        return self.transform[index]

    def write(self, stream):
        stream.write_u16(len(self.pool) + 1)
        for elem in self.pool:
            if elem[0] == -1:
                continue
            stream.write_raw_bytes(elem[0])
            stream.write_raw_bytes(elem[1])
            if len(elem) > 2:
                stream.write_raw_bytes(elem[2])
