import pyrtl
from utils.constants import *

class RegFile: 
    def __init__(self, bitwidth=REG_WIDTH, num_regs=NUM_REGS): 
        self.bitwidth = bitwidth
        self.num_regs = num_regs

        self.registers = [pyrtl.Register(bitwidth, name=f"x{i}") for i in range(num_regs)]

        self.create_ports()

    def create_ports(self):
        self.rs1_addr = pyrtl.Input(5, "rs1_addr")
        self.rs2_addr = pyrtl.Input(5, "rs2_addr")
        self.rs1_data = pyrtl.Output(self.bitwidth, "rs1_data")
        self.rs2_data = pyrtl.Output(self.bitwidth, "rs2_data")

        self.rd_addr = pyrtl.Input(5, "rd_addr")
        self.rd_data = pyrtl.Input(self.bitwidth, "rd_data")
        self.rd_we   = pyrtl.Input(1, "rd_we")

        self.rs1_data <<= self.read_register(self.rs1_addr)
        self.rs2_data <<= self.read_register(self.rs2_addr)

        self.write_register()

    def read_register(self, addr):
        read_value = pyrtl.mux(addr, *[self.registers[i] for i in range(self.num_regs)])
        result = pyrtl.select(addr == 0, truecase=pyrtl.Const(0, self.bitwidth), falsecase=read_value)

        return result

    def write_register(self):
        for i in range(self.num_regs):
            with pyrtl.conditional_assignment:
                with (self.rd_we == CTRL_REG_WRITE_YES) & (self.rd_addr == i) & (i != 0):
                    self.registers[i].next |= self.rd_data # type: ignore
    
    def get_register(self, index):
        if index < 0 or index >= self.num_regs:
            raise ValueError(f"Register index {index} out of range [0, {self.num_regs - 1}]")
        return self.registers[index]
    
    def reset_all(self):
        for i in range(self.num_regs):
            self.registers[i].reset_value = 0
        
    def __str__(self):
        return f"RegFile(bitwidth={self.bitwidth}, num_regs={self.num_regs})"