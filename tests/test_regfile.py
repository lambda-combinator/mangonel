import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from core.regfile import *

def setup_function():
    pyrtl.reset_working_block()

def test_creation():
    rf = RegFile()

    assert rf.bitwidth == REG_WIDTH
    assert rf.num_regs == NUM_REGS
    assert len(rf.registers) == NUM_REGS

def test_read_x0():
    rf = RegFile()

    sim = pyrtl.Simulation()
    sim.step({'rs1_addr': 0, 'rs2_addr': 0, 'rd_addr': 0, 'rd_data': 0, 'rd_we': 0})
    assert sim.inspect("rs1_data") == 0

def test_read_nonzero():
    rf = RegFile()

    sim = pyrtl.Simulation()

    sim.step({'rs1_addr': 0, 'rs2_addr': 0, 'rd_addr': 5, 'rd_data': 42, 'rd_we': CTRL_REG_WRITE_YES})
    sim.step({'rs1_addr': 5, 'rs2_addr': 0, 'rd_addr': 0, 'rd_data': 0, 'rd_we': 0})
    assert sim.inspect("rs1_data") == 42

def test_write():
    rf = RegFile()

    sim = pyrtl.Simulation()
    sim.step({'rs1_addr': 0, 'rs2_addr': 0, 'rd_addr': 10, 'rd_data': 100, 'rd_we': CTRL_REG_WRITE_YES})
    sim.step({'rs1_addr': 10, 'rs2_addr': 0, 'rd_addr': 0, 'rd_data': 0, 'rd_we': 0})
    assert sim.inspect("rs1_data") == 100

def test_write_ignored():
    rf = RegFile()

    sim = pyrtl.Simulation()
    sim.step({'rs1_addr': 0, 'rs2_addr': 0, 'rd_addr': 0, 'rd_data': 999, 'rd_we': CTRL_REG_WRITE_YES})
    sim.step({'rs1_addr': 0, 'rs2_addr': 0, 'rd_addr': 0, 'rd_data': 0, 'rd_we': 0})
    assert sim.inspect("rs1_data") == 0

def test_get():
    rf = RegFile()
    r = rf.get_register(7)

    assert r is rf.registers[7]

def test_get_range():
    rf = RegFile()
    with pytest.raises(ValueError):
        rf.get_register(NUM_REGS)
    
if __name__ == "__main__":
    pytest.main()