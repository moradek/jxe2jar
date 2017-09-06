import re
import subprocess
import sys
import StringIO
import zipfile
from Bytecode import transform_bytecode
from ConstPool import *
from JXE import *

def dump_romclass(stream, romclass):
    stream.write_raw_bytes('\xca\xfe\xba\xbe')
    stream.write_u16(romclass.minor)
    stream.write_u16(romclass.major)
    cp = ConstPool(romclass)
    class_name_id = cp.add(CONST.Class, romclass.class_name)
    superclass_name_id = cp.add(CONST.Class, romclass.superclass_name)
    interface_id_list = []
    for interface in romclass.interfaces:
        interface_id_list.append(cp.add(CONST.Class, interface.name))
    field_info_list = []
    for field in romclass.fields:
        field_info_list.append(
            {
                'access_flags': field.access_flag,
                'name_index': cp.add(CONST.Utf8, field.name),
                'descriptor_index': cp.add(CONST.Utf8, field.signature),
                'attributes_count': 0,
                'attributes': []
            }
        )
    code_attr_name_index = cp.add(CONST.Utf8, 'Code')
    method_info_list = []
    for method in romclass.methods:
        bytecode = transform_bytecode(bytearray(method.bytecode), cp)
        method_info_list.append(
            {
                'access_flags': method.modifier,
                'name_index': cp.add(CONST.Utf8, method.name),
                'descriptor_index': cp.add(CONST.Utf8, method.signature),
                'attributes_count': 1,
                'attributes': [
                    {
                        'attribute_name_index': code_attr_name_index,
                        'attribute_length': len(bytecode) + len(method.catch_exceptions) * 8 + (0x8 if (romclass.major, romclass.minor) < (45, 3) else 0xc) ,
                        'max_stack': method.max_stack,
                        'max_locals': method.temp_count,
                        'code_length': len(bytecode),
                        'code': bytecode,
                        'exception_table_length': len(method.catch_exceptions),
                        'exception_table': [
                            (exception.start, exception.end, exception.handler, exception.catch_type + 1 if exception.catch_type > 0 else 0)
                            for exception in method.catch_exceptions
                        ],
                        'attributes_count': 0,
                        'attributes': []
                    }
                ]
            }
        )
    cp.write(stream)
    stream.write_u16(romclass.access_flags & 0xffff)
    stream.write_u16(class_name_id)
    stream.write_u16(superclass_name_id)
    stream.write_u16(len(interface_id_list))
    for elem in interface_id_list:
        stream.write_u16(elem)
    stream.write_u16(len(field_info_list))
    for field_info in field_info_list:
        stream.write_u16(field_info['access_flags'] & 0xffff)
        stream.write_u16(field_info['name_index'])
        stream.write_u16(field_info['descriptor_index'])
        stream.write_u16(field_info['attributes_count'])
        if field_info['attributes_count']:
            raise NotImplementedError()
    stream.write_u16(len(method_info_list))
    for method_info in method_info_list:
        stream.write_u16(method_info['access_flags'] & 0xffff)
        stream.write_u16(method_info['name_index'])
        stream.write_u16(method_info['descriptor_index'])
        stream.write_u16(method_info['attributes_count'])
        attribute = method_info['attributes'][0]
        stream.write_u16(attribute['attribute_name_index'])
        stream.write_u32(attribute['attribute_length'])
        if (romclass.major, romclass.minor) < (45, 3):
            stream.write_u8(attribute['max_stack'])
            stream.write_u8(attribute['max_locals'])
            stream.write_u16(attribute['code_length'])
        else:
            stream.write_u16(attribute['max_stack'])
            stream.write_u16(attribute['max_locals'])
            stream.write_u32(attribute['code_length'])
        stream.write_raw_bytes(attribute['code'])
        stream.write_u16(attribute['exception_table_length'])
        for exception in attribute['exception_table']:
            stream.write_u16(exception[0])
            stream.write_u16(exception[1])
            stream.write_u16(exception[2])
            stream.write_u16(exception[3])
        stream.write_u16(attribute['attributes_count'])
        if attribute['attributes_count']:
            raise NotImplementedError()
    stream.write_u16(0)

def create_class(romclass, jarfile):
    class_name = romclass.class_name  # .replace('/', '.')
    class_file = '{0}.class'.format(class_name)
    f = StringIO.StringIO()
    stream = WriterStream(f)
    dump_romclass(stream, romclass)
    stream.write()
    jarfile.writestr(class_file, f.getvalue())

def create_jar(jar_name, jxe, decompilation_check=True):
    jarfile = zipfile.ZipFile(jar_name, 'w')
    for romclass in jxe.image.classes:
        print 'Creating class', romclass.class_name
        try:
            create_class(romclass, jarfile)
        except:
            print 'bad class, skip', romclass.class_name

def process(jxe_name, jar_name):
    with open(jxe_name, 'rb') as f:
        stream = ReaderStream(f)
        jxe = JXE.read(stream)
        create_jar(jar_name, jxe)

def main():
    jxe_name = sys.argv[1]
    jar_name = sys.argv[2]
    process(jxe_name, jar_name)

if __name__ == '__main__':
    main()
