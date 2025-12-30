import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from utils.isa import *
from utils.constants import *

def test_add_encoding(): 
    instr = RType(rd=1, rs1=2, rs2=3, funct3=FUNCT3_ADD_SUB, funct7=FUNCT7_NORMAL, opcode=OPCODE_R_TYPE)
    encoded = instr.encode()
    assert extract_opcode(encoded) == OPCODE_R_TYPE
    assert extract_rd(encoded) == 1
    assert extract_rs1(encoded) == 2
    assert extract_rs2(encoded) == 3
    assert extract_funct3(encoded) == FUNCT3_ADD_SUB
    assert extract_funct7(encoded) == FUNCT7_NORMAL

def test_addi_encoding():
    instr = IType(rd=5, rs1=10, imm=100, funct3=FUNCT3_ADD_SUB, opcode=OPCODE_ADDI)
    encoded = instr.encode()
    assert extract_opcode(encoded) == OPCODE_ADDI
    assert extract_rd(encoded) == 5
    assert extract_rs1(encoded) == 10
    assert extract_imm_i(encoded) == 100
    assert extract_funct3(encoded) == FUNCT3_ADD_SUB


def test_sw_encoding():
    instr = SType(rs1=1, rs2=2, imm=4, funct3=FUNCT3_SW, opcode=OPCODE_STORE)
    encoded = instr.encode()
    assert extract_opcode(encoded) == OPCODE_STORE
    assert extract_rs1(encoded) == 1
    assert extract_rs2(encoded) == 2
    assert extract_imm_s(encoded) == 4
    assert extract_funct3(encoded) == FUNCT3_SW

def test_beq_encoding():
    instr = BType(rs1=1, rs2=2, imm=16, funct3=FUNCT3_BEQ, opcode=OPCODE_BRANCH)
    encoded = instr.encode()
    assert extract_opcode(encoded) == OPCODE_BRANCH
    assert extract_rs1(encoded) == 1
    assert extract_rs2(encoded) == 2
    assert extract_imm_b(encoded) == 16
    assert extract_funct3(encoded) == FUNCT3_BEQ

def test_jal_encoding():
    instr = JType(rd=1, imm=2048, opcode=OPCODE_JAL)
    encoded = instr.encode()
    assert extract_opcode(encoded) == OPCODE_JAL
    assert extract_rd(encoded) == 1
    assert extract_imm_j(encoded) == 2048

def test_decode_add():
    instr = RType(rd=1, rs1=2, rs2=3, funct3=FUNCT3_ADD_SUB, funct7=FUNCT7_NORMAL, opcode=OPCODE_R_TYPE).encode()
    decoded = decode_instr(instr)
    assert decoded.mnemonic == "ADD"
    assert decoded.type == "R"
    assert decoded.rd == 1
    assert decoded.rs1 == 2
    assert decoded.rs2 == 3

def test_decode_addi():
    instr = IType(rd=5, rs1=10, imm=100, funct3=FUNCT3_ADD_SUB, opcode=OPCODE_ADDI).encode()
    decoded = decode_instr(instr)
    assert decoded.mnemonic == "ADDI"
    assert decoded.type == "I"
    assert decoded.rd == 5
    assert decoded.rs1 == 10
    assert decoded.imm == 100

def test_decode_sw():
    instr = SType(rs1=1, rs2=2, imm=4, funct3=FUNCT3_SW, opcode=OPCODE_STORE).encode()
    decoded = decode_instr(instr)
    assert decoded.mnemonic == "SW"
    assert decoded.type == "S"
    assert decoded.rs1 == 1
    assert decoded.rs2 == 2
    assert decoded.imm == 4

def test_decode_beq():
    instr = BType(rs1=1, rs2=2, imm=16, funct3=FUNCT3_BEQ, opcode=OPCODE_BRANCH).encode()
    decoded = decode_instr(instr)
    assert decoded.mnemonic == "BEQ"
    assert decoded.type == "B"
    assert decoded.rs1 == 1
    assert decoded.rs2 == 2
    assert decoded.imm == 16

def test_decode_jal():
    instr = JType(rd=1, imm=2048, opcode=OPCODE_JAL).encode()
    decoded = decode_instr(instr)
    assert decoded.mnemonic == "JAL"
    assert decoded.type == "J"
    assert decoded.rd == 1
    assert decoded.imm == 2048

if __name__ == "__main__":
    pytest.main()