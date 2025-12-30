from .constants import *

# === Instruction Classes ===

class Instr:
    pass

class RType(Instr):
    def __init__(self, rd, rs1, rs2, funct3, funct7, opcode):
        self.rd = rd
        self.rs1 = rs1
        self.rs2 = rs2
        self.funct3 = funct3
        self.funct7 = funct7
        self.opcode = opcode

    def encode(self): 
        instr = self.opcode
        instr |= (self.rd & RD_MASK) << RD_SHIFT
        instr |= (self.funct3 & FUNCT3_MASK) << FUNCT3_SHIFT
        instr |= (self.rs1 & RS1_MASK) << RS1_SHIFT
        instr |= (self.rs2 & RS2_MASK) << RS2_SHIFT
        instr |= (self.funct7 & FUNCT7_MASK) << FUNCT7_SHIFT
        return instr & 0xFFFFFFFF
    
class IType(Instr):
    def __init__(self, rd, rs1, imm, funct3, opcode):
        self.rd = rd
        self.rs1 = rs1
        self.imm = imm
        self.funct3 = funct3
        self.opcode = opcode

    def encode(self):
        instr = self.opcode
        instr |= (self.rd & RD_MASK) << RD_SHIFT
        instr |= (self.funct3 & FUNCT3_MASK) << FUNCT3_SHIFT
        instr |= (self.rs1 & RS1_MASK) << RS1_SHIFT
        instr |= (self.imm & IMM_I_MASK) << IMM_I_SHIFT
        return instr & 0xFFFFFFFF

class SType(Instr):
    def __init__(self, rs1, rs2, imm, funct3, opcode):
        self.rs1 = rs1
        self.rs2 = rs2
        self.imm = imm
        self.funct3 = funct3
        self.opcode = opcode

    def encode(self):
        instr = self.opcode
        instr |= ((self.imm & IMM_S_LO_MASK)) << IMM_S_LO_SHIFT
        instr |= (self.funct3 & FUNCT3_MASK) << FUNCT3_SHIFT
        instr |= (self.rs1 & RS1_MASK) << RS1_SHIFT
        instr |= (self.rs2 & RS2_MASK) << RS2_SHIFT
        instr |= ((self.imm >> 5) & IMM_S_HI_MASK) << IMM_S_HI_SHIFT
        return instr & 0xFFFFFFFF

class BType(Instr):
    def __init__(self, rs1, rs2, imm, funct3, opcode):
        self.rs1 = rs1
        self.rs2 = rs2
        self.imm = imm
        self.funct3 = funct3
        self.opcode = opcode

    def encode(self):
        instr = self.opcode
        instr |= ((self.imm & IMM_B_BIT11_MASK) << IMM_B_BIT11_SHIFT)
        instr |= ((self.imm >> 1) & IMM_B_BITS4_1_MASK) << IMM_B_BITS4_1_SHIFT
        instr |= (self.funct3 & FUNCT3_MASK) << FUNCT3_SHIFT
        instr |= (self.rs1 & RS1_MASK) << RS1_SHIFT
        instr |= (self.rs2 & RS2_MASK) << RS2_SHIFT
        instr |= ((self.imm >> 5) & IMM_B_BITS10_5_MASK) << IMM_B_BITS10_5_SHIFT
        instr |= ((self.imm >> 11) & IMM_B_BIT12_MASK) << IMM_B_BIT12_SHIFT
        return instr & 0xFFFFFFFF
    
class UType(Instr):
    def __init__(self, rd, imm, opcode):
        self.rd = rd
        self.imm = imm
        self.opcode = opcode

    def encode(self):
        instr = self.opcode
        instr |= (self.rd & RD_MASK) << RD_SHIFT
        instr |= (self.imm & IMM_U_MASK) << IMM_U_SHIFT
        return instr & 0xFFFFFFFF
    
class JType(Instr):
    def __init__(self, rd, imm, opcode):
        self.rd = rd
        self.imm = imm
        self.opcode = opcode

    def encode(self):
        instr = self.opcode
        instr |= (self.rd & RD_MASK) << RD_SHIFT
        instr |= ((self.imm & IMM_J_BITS19_12_MASK) << IMM_J_BITS19_12_SHIFT)
        instr |= ((self.imm >> 11) & IMM_J_BIT11_MASK) << IMM_J_BIT11_SHIFT
        instr |= ((self.imm >> 1) & IMM_J_BITS10_1_MASK) << IMM_J_BITS10_1_SHIFT
        instr |= ((self.imm >> 20) & IMM_J_BIT20_MASK) << IMM_J_BIT20_SHIFT
        return instr & 0xFFFFFFFF

# === Decoding Helpers ===

def extract_opcode(instr):
    return (instr >> OPCODE_SHIFT) & OPCODE_MASK

def extract_rd(instr):
    return (instr >> RD_SHIFT) & RD_MASK

def extract_rs1(instr):
    return (instr >> RS1_SHIFT) & RS1_MASK

def extract_rs2(instr):
    return (instr >> RS2_SHIFT) & RS2_MASK

def extract_funct3(instr):
    return (instr >> FUNCT3_SHIFT) & FUNCT3_MASK

def extract_funct7(instr):
    return (instr >> FUNCT7_SHIFT) & FUNCT7_MASK

def extract_imm_i(instr):
    imm = (instr >> IMM_I_SHIFT) & IMM_I_MASK
    return sign_extend(imm, 12)

def extract_imm_s(instr):
    imm_lo = (instr >> IMM_S_LO_SHIFT) & IMM_S_LO_MASK
    imm_hi = (instr >> IMM_S_HI_SHIFT) & IMM_S_HI_MASK

    imm = (imm_hi << 5) | imm_lo
    return sign_extend(imm, 12)

def extract_imm_b(instr):
    bit11 = (instr >> IMM_B_BIT11_SHIFT) & IMM_B_BIT11_MASK
    bits10_5 = (instr >> IMM_B_BITS10_5_SHIFT) & IMM_B_BITS10_5_MASK
    bits4_1 = (instr >> IMM_B_BITS4_1_SHIFT) & IMM_B_BITS4_1_MASK
    bit12 = (instr >> IMM_B_BIT12_SHIFT) & IMM_B_BIT12_MASK

    imm = (bit12 << 12) | (bit11 << 11) | (bits10_5 << 5) | (bits4_1 << 1)
    return sign_extend(imm, 13)

def extract_imm_u(instr):
    return (instr >> IMM_U_SHIFT) & IMM_U_MASK

def extract_imm_j(instr):
    bits19_12 = (instr >> IMM_J_BITS19_12_SHIFT) & IMM_J_BITS19_12_MASK
    bit11 = (instr >> IMM_J_BIT11_SHIFT) & IMM_J_BIT11_MASK
    bits10_1 = (instr >> IMM_J_BITS10_1_SHIFT) & IMM_J_BITS10_1_MASK
    bit20 = (instr >> IMM_J_BIT20_SHIFT) & IMM_J_BIT20_MASK

    imm = (bit20 << 20) | (bits19_12 << 12) | (bit11 << 11) | (bits10_1 << 1)
    return sign_extend(imm, 21)

# === Decode Instruction ===

class Decoded:
    def __init__(self):
        self.opcode = 0
        self.rd = 0
        self.rs1 = 0
        self.rs2 = 0
        self.funct3 = 0
        self.funct7 = 0
        self.imm = 0
        self.type = ""
        self.mnemonic = ""
    
    def __str__(self):
        return f"{self.mnemonic} (opcode={self.opcode:07b})"
    
def decode_instr(instr):
    decoded = Decoded()
    decoded.opcode = extract_opcode(instr)
    decoded.rd = extract_rd(instr)
    decoded.rs1 = extract_rs1(instr)
    decoded.rs2 = extract_rs2(instr)
    decoded.funct3 = extract_funct3(instr)
    decoded.funct7 = extract_funct7(instr)

    if decoded.opcode == OPCODE_R_TYPE:
            decoded.type = "R"
    elif decoded.opcode in (OPCODE_ADDI, OPCODE_ANDI, OPCODE_ORI, OPCODE_XORI, OPCODE_SLTI, OPCODE_SLTIU, OPCODE_SLLI, OPCODE_SRLI, OPCODE_SRAI, OPCODE_JALR, OPCODE_LOAD):
            decoded.type = "I"
            decoded.imm = extract_imm_i(instr)
    elif decoded.opcode == OPCODE_STORE:
            decoded.type = "S"
            decoded.imm = extract_imm_s(instr)
    elif decoded.opcode == OPCODE_BRANCH:
            decoded.type = "B"
            decoded.imm = extract_imm_b(instr)
    elif decoded.opcode in (OPCODE_LUI, OPCODE_AUIPC):
            decoded.type = "U"
            decoded.imm = extract_imm_u(instr)
    elif decoded.opcode == OPCODE_JAL:
            decoded.type = "J"
            decoded.imm = extract_imm_j(instr)

    decoded.mnemonic = get_mnemonic(decoded)

    return decoded

def get_mnemonic(decoded):
    opcode = decoded.opcode
    funct3 = decoded.funct3
    funct7 = decoded.funct7 if decoded.type == "R" else 0
    
    mnemonic_map = {
        (OPCODE_R_TYPE, FUNCT3_ADD_SUB, FUNCT7_NORMAL): "ADD",
        (OPCODE_R_TYPE, FUNCT3_ADD_SUB, FUNCT7_ALT): "SUB",
        (OPCODE_R_TYPE, FUNCT3_SLL, FUNCT7_NORMAL): "SLL",
        (OPCODE_R_TYPE, FUNCT3_SLT, FUNCT7_NORMAL): "SLT",
        (OPCODE_R_TYPE, FUNCT3_SLTU, FUNCT7_NORMAL): "SLTU",
        (OPCODE_R_TYPE, FUNCT3_XOR, FUNCT7_NORMAL): "XOR",
        (OPCODE_R_TYPE, FUNCT3_SRL_SRA, FUNCT7_NORMAL): "SRL",
        (OPCODE_R_TYPE, FUNCT3_SRL_SRA, FUNCT7_ALT): "SRA",
        (OPCODE_R_TYPE, FUNCT3_OR, FUNCT7_NORMAL): "OR",
        (OPCODE_R_TYPE, FUNCT3_AND, FUNCT7_NORMAL): "AND",
        
        (OPCODE_ADDI, FUNCT3_ADD_SUB, 0): "ADDI",
        (OPCODE_SLLI, FUNCT3_SLL, 0): "SLLI",
        (OPCODE_SLTI, FUNCT3_SLT, 0): "SLTI",
        (OPCODE_SLTIU, FUNCT3_SLTU, 0): "SLTIU",
        (OPCODE_XORI, FUNCT3_XOR, 0): "XORI",
        (OPCODE_SRLI, FUNCT3_SRL_SRA, 0): "SRLI",
        (OPCODE_SRAI, FUNCT3_SRL_SRA, 0): "SRAI",
        (OPCODE_ORI, FUNCT3_OR, 0): "ORI",
        (OPCODE_ANDI, FUNCT3_AND, 0): "ANDI",

        (OPCODE_LOAD, FUNCT3_LB, 0): "LB",
        (OPCODE_LOAD, FUNCT3_LH, 0): "LH",
        (OPCODE_LOAD, FUNCT3_LW, 0): "LW",
        (OPCODE_LOAD, FUNCT3_LBU, 0): "LBU",
        (OPCODE_LOAD, FUNCT3_LHU, 0): "LHU",
        
        (OPCODE_STORE, FUNCT3_SB, 0): "SB",
        (OPCODE_STORE, FUNCT3_SH, 0): "SH",
        (OPCODE_STORE, FUNCT3_SW, 0): "SW",

        (OPCODE_BRANCH, FUNCT3_BEQ, 0): "BEQ",
        (OPCODE_BRANCH, FUNCT3_BNE, 0): "BNE",
        (OPCODE_BRANCH, FUNCT3_BLT, 0): "BLT",
        (OPCODE_BRANCH, FUNCT3_BGE, 0): "BGE",
        (OPCODE_BRANCH, FUNCT3_BLTU, 0): "BLTU",
        (OPCODE_BRANCH, FUNCT3_BGEU, 0): "BGEU",

        (OPCODE_JAL, 0, 0): "JAL",
        (OPCODE_JALR, FUNCT3_ADD_SUB, 0): "JALR",

        (OPCODE_LUI, 0, 0): "LUI",
        (OPCODE_AUIPC, 0, 0): "AUIPC",
    }

    key = (opcode, funct3, funct7)
    return mnemonic_map.get(key, "UNKNOWN")