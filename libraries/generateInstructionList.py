try:
    from iced_x86 import *
except:
    input("You need to run pip install iced_x86 in CMD to use this (be sure you enabled the PATH option during Python's installation if it doesn't work!)")

from libraries.FileIO import *

try:
    import pefile
except:
    input("You need to run pip install pefile in CMD to use this (be sure you enabled the PATH option during Python's installation if it doesn't work!)")
    
import random

def generateMnemonicsList():
    mnemonics = [
        Mnemonic.ADD, Mnemonic.SUB, Mnemonic.MUL, Mnemonic.IMUL, Mnemonic.DIV, Mnemonic.IDIV,
        Mnemonic.INC, Mnemonic.DEC, Mnemonic.NEG, Mnemonic.CMP, Mnemonic.TEST,
        Mnemonic.AND, Mnemonic.OR, Mnemonic.XOR, Mnemonic.NOT, Mnemonic.ADC, Mnemonic.SBB,

        Mnemonic.SHL, Mnemonic.SHR, Mnemonic.SAL, Mnemonic.SAR,
        Mnemonic.ROL, Mnemonic.ROR, Mnemonic.RCL, Mnemonic.RCR,
        Mnemonic.BSF, Mnemonic.BSR, Mnemonic.BT, Mnemonic.BTS, Mnemonic.BTR, Mnemonic.BTC,

        Mnemonic.MOV, Mnemonic.XCHG, Mnemonic.PUSH, Mnemonic.POP,
        Mnemonic.MOVZX, Mnemonic.MOVSX, Mnemonic.LEA,
        Mnemonic.STOSB, Mnemonic.LODSB, Mnemonic.SCASB, Mnemonic.CMPSB,

        Mnemonic.JMP, Mnemonic.CALL, Mnemonic.RET,
        Mnemonic.JE, Mnemonic.JNE, Mnemonic.JG, Mnemonic.JL, Mnemonic.JGE, Mnemonic.JLE,
        Mnemonic.JO, Mnemonic.JNO, Mnemonic.JS, Mnemonic.JNS, Mnemonic.JP, Mnemonic.JNP,
        Mnemonic.LOOP, Mnemonic.JECXZ,

        Mnemonic.FADD, Mnemonic.FSUB, Mnemonic.FMUL, Mnemonic.FDIV, Mnemonic.FDIVR,
        Mnemonic.FCHS, Mnemonic.FABS, Mnemonic.FSQRT, Mnemonic.FRNDINT,
        Mnemonic.FLD, Mnemonic.FST, Mnemonic.FSTP, Mnemonic.FXCH,
        Mnemonic.FCOM, Mnemonic.FCOMP, Mnemonic.FINCSTP, Mnemonic.FDECSTP,
        Mnemonic.FNINIT,

        Mnemonic.MOVAPS, Mnemonic.MOVUPS, Mnemonic.MOVDQA, Mnemonic.MOVDQU,
        Mnemonic.ADDPS, Mnemonic.SUBPS, Mnemonic.ADDPD, Mnemonic.SUBPD, 
        Mnemonic.MULPS, Mnemonic.DIVPS, Mnemonic.MULPD, Mnemonic.DIVPD,
        Mnemonic.SQRTPS, Mnemonic.MAXPS, Mnemonic.MINPS, Mnemonic.SQRTPD,
        Mnemonic.PXOR, Mnemonic.PAND, Mnemonic.POR, Mnemonic.PADDB, Mnemonic.PSUBB,
        Mnemonic.PUNPCKLBW, Mnemonic.PACKSSWB, Mnemonic.PSHUFD, Mnemonic.PSLLD,

        Mnemonic.INT, Mnemonic.IRET, Mnemonic.SYSCALL, Mnemonic.SYSRET,
        Mnemonic.IN, Mnemonic.OUT, Mnemonic.INSB, Mnemonic.OUTSB,
        Mnemonic.LGDT, Mnemonic.LIDT, Mnemonic.LTR, Mnemonic.STR,
        Mnemonic.RDMSR, Mnemonic.WRMSR, Mnemonic.RDTSC, Mnemonic.RDPMC,

        Mnemonic.NOP, Mnemonic.HLT, Mnemonic.WAIT,
        Mnemonic.CPUID, Mnemonic.XGETBV, Mnemonic.XSETBV,
        Mnemonic.CLC, Mnemonic.STC, Mnemonic.CLI, Mnemonic.STI,
        Mnemonic.CLD, Mnemonic.STD, Mnemonic.CMC
    ]
    return mnemonics

def getCodeSection(filename):
    pe = pefile.PE(filename)
    
    magic = pe.OPTIONAL_HEADER.Magic
    if magic == 0x10B:
        bits = 32
    elif magic == 0x20B:
        bits = 64
    
    for section in pe.sections:
        if section.Characteristics & 0x20000000:
            if section.Name.startswith(b'.text'):
                return (section.get_data(), 
                       section.VirtualAddress, 
                       section.Misc_VirtualSize, 
                       section.PointerToRawData,
                       pe.OPTIONAL_HEADER.ImageBase,
                       bits)
    return None

def scanForOpcodes(data, virtualAddress, fileOffset, imageBase, bits):
    mnemonics = generateMnemonicsList()
    offsets = []

    decoder = Decoder(bits, data, ip=imageBase + virtualAddress)
    formatter = Formatter(FormatterSyntax.NASM)
    encoder = Encoder(bits)
    
    for instruction in decoder:
        try:
            code = formatter.format(instruction)
            mnemonic = str(code).split()[0].lower()
            if instruction.mnemonic in mnemonics:
                encoder.encode(instruction, instruction.ip)
                data = encoder.take_buffer()
                
                rva = instruction.ip - imageBase
                
                fileOff = rva - virtualAddress + fileOffset
                
                offsets.append([fileOff, code, instruction.ip, len(data)])
        except:
            continue #Unsupported instruction...
    
    return offsets

def instructionListGenerator(file):
    instructionListFile = file.replace("exe", "txt")

    #First, get the main code section data
    result = getCodeSection(file)
    if result:
        sectionData, sectionVA, sectionSize, sectionFileOffset, imageBase, bits = result
        
        #Second, scan for every instance of each instruction
        offsets = scanForOpcodes(sectionData,
                                 sectionVA,
                                 sectionFileOffset,
                                 imageBase,
                                 bits)
        
        with open(instructionListFile, "w+") as o:
            for offset in offsets:
                o.write(f'0x{offset[0]:08x} 0x{offset[3]:02x} {offset[1].split()[0]} \n')
        
