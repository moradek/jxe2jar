from Common import *

import struct

JBOpcode = enum(
    JBnop=0x00, JBaconstnull=0x01, JBiconstm1=0x02, JBiconst0=0x03, JBiconst1=0x04, JBiconst2=0x05,
    JBiconst3=0x06, JBiconst4=0x07, JBiconst5=0x08, JBlconst0=0x09, JBlconst1=0x0a, JBfconst0=0x0b,
    JBfconst1=0x0c, JBfconst2=0x0d, JBdconst0=0x0e, JBdconst1=0x0f, JBbipush=0x10, JBsipush=0x11,
    JBldc=0x12, JBldcw=0x13, JBldc2lw=0x14, JBiload=0x15, JBlload=0x16, JBfload=0x17, JBdload=0x18,
    JBaload=0x19, JBiload0=0x1a, JBiload1=0x1b, JBiload2=0x1c, JBiload3=0x1d, JBlload0=0x1e,
    JBlload1=0x1f, JBlload2=0x20, JBlload3=0x21, JBfload0=0x22, JBfload1=0x23, JBfload2=0x24,
    JBfload3=0x25, JBdload0=0x26, JBdload1=0x27, JBdload2=0x28, JBdload3=0x29, JBaload0=0x2a,
    JBaload1=0x2b, JBaload2=0x2c, JBaload3=0x2d, JBiaload=0x2e, JBlaload=0x2f, JBfaload=0x30,
    JBdaload=0x31, JBaaload=0x32, JBbaload=0x33, JBcaload=0x34, JBsaload=0x35, JBistore=0x36,
    JBlstore=0x37, JBfstore=0x38, JBdstore=0x39, JBastore=0x3a, JBistore0=0x3b, JBistore1=0x3c,
    JBistore2=0x3d, JBistore3=0x3e, JBlstore0=0x3f, JBlstore1=0x40, JBlstore2=0x41, JBlstore3=0x42,
    JBfstore0=0x43, JBfstore1=0x44, JBfstore2=0x45, JBfstore3=0x46, JBdstore0=0x47, JBdstore1=0x48,
    JBdstore2=0x49, JBdstore3=0x4a, JBastore0=0x4b, JBastore1=0x4c, JBastore2=0x4d, JBastore3=0x4e,
    JBiastore=0x4f, JBlastore=0x50, JBfastore=0x51, JBdastore=0x52, JBaastore=0x53, JBbastore=0x54,
    JBcastore=0x55, JBsastore=0x56, JBpop=0x57, JBpop2=0x58, JBdup=0x59, JBdupx1=0x5a, JBdupx2=0x5b,
    JBdup2=0x5c, JBdup2x1=0x5d, JBdup2x2=0x5e, JBswap=0x5f, JBiadd=0x60, JBladd=0x61, JBfadd=0x62,
    JBdadd=0x63, JBisub=0x64, JBlsub=0x65, JBfsub=0x66, JBdsub=0x67, JBimul=0x68, JBlmul=0x69,
    JBfmul=0x6a, JBdmul=0x6b, JBidiv=0x6c, JBldiv=0x6d, JBfdiv=0x6e, JBddiv=0x6f, JBirem=0x70,
    JBlrem=0x71, JBfrem=0x72, JBdrem=0x73, JBineg=0x74, JBlneg=0x75, JBfneg=0x76, JBdneg=0x77,
    JBishl=0x78, JBlshl=0x79, JBishr=0x7a, JBlshr=0x7b, JBiushr=0x7c, JBlushr=0x7d, JBiand=0x7e,
    JBland=0x7f, JBior=0x80, JBlor=0x81, JBixor=0x82, JBlxor=0x83, JBiinc=0x84, JBi2l=0x85,
    JBi2f=0x86, JBi2d=0x87, JBl2i=0x88, JBl2f=0x89, JBl2d=0x8a, JBf2i=0x8b, JBf2l=0x8c, JBf2d=0x8d,
    JBd2i=0x8e, JBd2l=0x8f, JBd2f=0x90, JBi2b=0x91, JBi2c=0x92, JBi2s=0x93, JBlcmp=0x94, JBfcmpl=0x95,
    JBfcmpg=0x96, JBdcmpl=0x97, JBdcmpg=0x98, JBifeq=0x99, JBifne=0x9a, JBiflt=0x9b, JBifge=0x9c,
    JBifgt=0x9d, JBifle=0x9e, JBificmpeq=0x9f, JBificmpne=0xa0, JBificmplt=0xa1, JBificmpge=0xa2,
    JBificmpgt=0xa3, JBificmple=0xa4, JBifacmpeq=0xa5, JBifacmpne=0xa6, JBgoto=0xa7, JBjsr=0xa8, JBret=0xa9,
    JBtableswitch=0xaa, JBlookupswitch=0xab, JBreturn0=0xac, JBreturn1=0xad, JBreturn2=0xae, JBsyncReturn0=0xaf,
    JBsyncReturn1=0xb0, JBsyncReturn2=0xb1, JBgetstatic=0xb2, JBputstatic=0xb3, JBgetfield=0xb4, JBputfield=0xb5,
    JBinvokevirtual=0xb6, JBinvokespecial=0xb7, JBinvokestatic=0xb8, JBinvokeinterface=0xb9, JBnew=0xbb,
    JBnewarray=0xbc, JBanewarray=0xbd, JBarraylength=0xbe, JBathrow=0xbf, JBcheckcast=0xc0,
    JBinstanceof=0xc1, JBmonitorenter=0xc2, JBmonitorexit=0xc3, JBmultianewarray=0xc5, JBifnull=0xc6,
    JBifnonnull=0xc7, JBgotow=0xc8, JBbreakpoint=0xca, JBiloadw=0xcb, JBlloadw=0xcc, JBfloadw=0xcd,
    JBdloadw=0xce, JBaloadw=0xcf, JBistorew=0xd0, JBlstorew=0xd1, JBfstorew=0xd2, JBdstorew=0xd3,
    JBastorew=0xd4, JBiincw=0xd5, JBaload0getfield=0xd7, JBreturnFromConstructor=0xe4,
    JBgenericReturn=0xe5, JBinvokeinterface2=0xe7, JBreturnToMicroJIT=0xf3, JBretFromNative0=0xf4,
    JBretFromNative1=0xf5, JBretFromNativeF=0xf6, JBretFromNativeD=0xf7, JBretFromNativeJ=0xf8,
    JBldc2dw=0xf9, JBasyncCheck=0xfa, JBimpdep1=0xfe, JBimpdep2=0xff
)

def transform_bytecode(bytecode, cp):
    i = 0
    new_cp_transform = {}
    new_bytecode = bytearray()
    while i < len(bytecode):
        opcode = bytecode[i]
        if opcode in (
                    JBOpcode.JBgetstatic, JBOpcode.JBputstatic, JBOpcode.JBgetfield,
                    JBOpcode.JBputfield, JBOpcode.JBinvokevirtual, JBOpcode.JBinvokespecial,
                    JBOpcode.JBinvokestatic, JBOpcode.JBnew,
                    JBOpcode.JBanewarray, JBOpcode.JBcheckcast, JBOpcode.JBinstanceof,
                ):
            new_bytecode.append(opcode)
            index = struct.unpack('<H', bytecode[i + 1: i + 3])[0]
            transform = cp.get_transform(index)
            new_index = transform['new_index']
            tmp = struct.pack('>H', new_index + 1)
            new_bytecode += tmp
            i += 3
        elif opcode in (JBOpcode.JBldcw,):
            new_bytecode.append(opcode)
            index = struct.unpack('<H', bytecode[i + 1: i + 3])[0]
            transform = cp.get_transform(index)
            new_index = transform['new_index']
            tmp = struct.pack('>H', new_index + 1)
            new_bytecode += tmp
            i += 3
        elif opcode in (JBOpcode.JBldc2lw,):
            index = struct.unpack('<H', bytecode[i + 1: i + 3])[0]
            if cp.check_transform(index, '\x06'):
                new_bytecode.append(JBOpcode.JBldc2lw)
                transform = cp.get_transform(index)
                new_index = transform['new_index']
                tmp = struct.pack('>H', new_index + 1)
                new_cp_transform[new_index]= '\x05'
                new_bytecode += tmp
            else:
                new_bytecode.append(JBOpcode.JBldcw)
                if cp.check_transform(index):
                    transform = cp.get_transform(index)
                    new_index = transform['new_index']
                else:
                    # TODO very dirty hack, because we incorrectly parse constant pool used in 1 case
                    new_index = 0
                tmp = struct.pack('>H', new_index + 1)
                new_bytecode += tmp
            i += 3
        elif opcode in (JBOpcode.JBldc2dw,):
            new_bytecode.append(JBOpcode.JBldc2lw)
            index = struct.unpack('<H', bytecode[i + 1: i + 3])[0]
            transform = cp.get_transform(index)
            new_index = transform['new_index']
            tmp = struct.pack('>H', new_index + 1)
            new_cp_transform[new_index] = '\x06'
            new_bytecode += tmp
            i += 3
        elif opcode in (JBOpcode.JBiincw,):
            new_bytecode.append(JBOpcode.JBiincw)
            o1 = struct.unpack('<H', bytecode[i + 1: i + 3])[0]
            o2 = struct.unpack('<H', bytecode[i + 3: i + 5])[0]
            t1 = struct.pack('>H', o1)
            t2 = struct.pack('>H', o2)
            new_bytecode += t1 + t2
            i += 5
        elif opcode in (
                    JBOpcode.JBiloadw, JBOpcode.JBlloadw,
                    JBOpcode.JBfloadw, JBOpcode.JBdloadw, JBOpcode.JBaloadw, JBOpcode.JBistorew,
                    JBOpcode.JBlstorew, JBOpcode.JBfstorew, JBOpcode.JBdstorew, JBOpcode.JBastorew,
                ):
            new_bytecode.append(opcode)
            value = struct.unpack('<H', bytecode[i + 1: i + 3])[0]
            tmp = struct.pack('>H', value)
            new_bytecode += tmp
            i += 3
        elif opcode in (
                    JBOpcode.JBsipush, JBOpcode.JBifeq, JBOpcode.JBifne, JBOpcode.JBiflt, JBOpcode.JBifge,
                    JBOpcode.JBifgt, JBOpcode.JBifle, JBOpcode.JBificmpeq, JBOpcode.JBificmpne,
                    JBOpcode.JBificmplt, JBOpcode.JBificmpge, JBOpcode.JBificmpgt,
                    JBOpcode.JBificmple, JBOpcode.JBifacmpeq, JBOpcode.JBifacmpne, JBOpcode.JBgoto,
                    JBOpcode.JBjsr, JBOpcode.JBifnull, JBOpcode.JBifnonnull,
                ):
            new_bytecode.append(opcode)
            index = struct.unpack('<H', bytecode[i + 1: i + 3])[0]
            tmp = struct.pack('>H', index)
            new_bytecode += tmp
            i += 3
        elif opcode in (JBOpcode.JBaload0getfield,):
            new_bytecode.append(JBOpcode.JBaload0)
            i += 1
        elif opcode in (
                    JBOpcode.JBreturn0, JBOpcode.JBsyncReturn0
                ):
            # JBreturn0 -> return (0xb1)
            # Used only if function return void
            new_bytecode.append(0xb1)
            i += 1
        elif opcode in (JBOpcode.JBreturn1, JBOpcode.JBsyncReturn1):
            # JBreturn1 -> areturn (0xb0)
            # Used only after push on stack
            new_bytecode.append(0xb0)
            i += 1
        elif opcode in (JBOpcode.JBinvokeinterface2,):
            # JBinvokeinterface2 -> invokeinterface
            # Usually placed as JBinvokeinterface2 JBnop JBinvokeinterface
            # invokeinterface in Oracle get 4 bytes but j9 get 2
            # JBinvokeinterface2 JBnop correlate with this to fix this misalign
            new_bytecode.append(JBOpcode.JBinvokeinterface)
            index = struct.unpack('<H', bytecode[i + 3: i + 5])[0]
            transform = cp.get_transform(index)
            new_index = transform['new_index']
            tmp = struct.pack('>H', new_index + 1)
            new_cp_transform[index] = '\x0b'
            new_bytecode += tmp
            new_bytecode.append(0)
            new_bytecode.append(0)
            i += 5
        elif opcode in (JBOpcode.JBinvokeinterface,):
            raise NotImplementedError
        elif opcode in (JBOpcode.JBldc,):
            new_bytecode.append(opcode)
            index = bytecode[i + 1]
            transform = cp.get_transform(index)
            new_index = transform['new_index']
            new_bytecode.append(new_index + 1)
            i += 2
        elif opcode in (
                    JBOpcode.JBbipush, JBOpcode.JBnewarray,
                    JBOpcode.JBiload, JBOpcode.JBlload, JBOpcode.JBfload, JBOpcode.JBdload,
                    JBOpcode.JBaload, JBOpcode.JBistore, JBOpcode.JBlstore, JBOpcode.JBfstore,
                    JBOpcode.JBdstore, JBOpcode.JBastore, JBOpcode.JBret
                ):
            new_bytecode.append(opcode)
            new_bytecode.append(bytecode[i + 1])
            i += 2
        elif opcode in (JBOpcode.JBiinc,):
            new_bytecode.append(opcode)
            new_bytecode.append(bytecode[i + 1])
            new_bytecode.append(bytecode[i + 2])
            i += 3
        elif opcode in (JBOpcode.JBtableswitch,):
            new_bytecode.append(opcode)
            padding = ((i + 1) % 4)
            padding = padding if padding == 0 else (4 - padding)
            for j in xrange(padding):
                new_bytecode.append(0x0)
            i += padding + 1
            default = struct.unpack('<I', bytecode[i: i + 4])[0]
            tmp = struct.pack('>I', default)
            new_bytecode += tmp
            i += 4
            low = struct.unpack('<i', bytecode[i: i + 4])[0]
            tmp = struct.pack('>i', low)
            new_bytecode += tmp
            i += 4
            high = struct.unpack('<i', bytecode[i: i + 4])[0]
            tmp = struct.pack('>i', high)
            new_bytecode += tmp
            try:
                for j in xrange(high - low + 1):
                    i += 4
                    left = struct.unpack('<I', bytecode[i: i + 4])[0]
                    tmp = struct.pack('>I', left)
                    new_bytecode += tmp
            except OverflowError as err:
                raise err
            i += 4
        elif opcode in (JBOpcode.JBlookupswitch,):
            new_bytecode.append(opcode)
            padding = ((i + 1) % 4)
            padding = padding if padding == 0 else (4 - padding)
            for j in xrange(padding):
                new_bytecode.append(0x0)
            i += padding + 1
            default = struct.unpack('<I', bytecode[i: i + 4])[0]
            tmp = struct.pack('>I', default)
            new_bytecode += tmp
            i += 4
            n = struct.unpack('<I', bytecode[i: i + 4])[0]
            tmp = struct.pack('>I', n)
            new_bytecode += tmp
            for j in xrange(n):
                i += 4
                left = struct.unpack('<I', bytecode[i: i + 4])[0]
                tmp = struct.pack('>I', left)
                new_bytecode += tmp
                i += 4
                right = struct.unpack('<I', bytecode[i: i + 4])[0]
                tmp = struct.pack('>I', right)
                new_bytecode += tmp
            i += 4
        elif opcode in (JBOpcode.JBmultianewarray,):
            new_bytecode.append(opcode)
            index = struct.unpack('<H', bytecode[i + 1: i + 3])[0]
            transform = cp.get_transform(index)
            new_index = transform['new_index']
            tmp = struct.pack('>H', new_index + 1)
            new_bytecode += tmp
            new_bytecode.append(bytecode[i + 3])
            i += 4
        elif opcode in (JBOpcode.JBgotow,):
            new_bytecode.append(opcode)
            value = struct.unpack('<I', bytecode[i + 1: i + 5])[0]
            tmp = struct.pack('>I', value)
            new_bytecode += tmp
            i += 5
        else:
            new_bytecode.append(opcode)
            i += 1
    for index in new_cp_transform:
        cp.apply_transform(index, new_cp_transform[index])
    return new_bytecode