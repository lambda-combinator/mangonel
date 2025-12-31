# Testbenching and Miscellaneous Tools for Centurion

This guide covers hardware testbenching with cocotb, simulation scripts, build infrastructure, and other essential tools for the Centurion project.

## Table of Contents
1. [Testbenching Fundamentals](#testbenching-fundamentals)
2. [cocotb: Python Hardware Testbenches](#cocotb-python-hardware-testbenches)
3. [Simulation Environment](#simulation-environment)
4. [Verilator Integration](#verilator-integration)
5. [Build Systems and Scripts](#build-systems-and-scripts)
6. [Testing Strategies](#testing-strategies)
7. [Debugging Tools](#debugging-tools)
8. [Project Organization](#project-organization)

---

## Testbenching Fundamentals

### What is a Testbench?

A testbench is a software program that:
- Provides inputs to hardware under test (UUT)
- Monitors outputs
- Checks behavior against expected results
- Reports pass/fail

### Why Test Hardware?

1. **Correctness**: Verify design works before synthesis
2. **Speed**: Simulation is 1000x faster than physical hardware
3. **Observability**: Monitor internal signals (impossible on real silicon)
4. **Reproducibility**: Automated tests catch regressions
5. **Documentation**: Tests define expected behavior

### Testing Hierarchy

```
Integration Tests (full system)
    ↑
Component Tests (subsystems like UART, ALU)
    ↑
Unit Tests (individual modules)
    ↑
Simulation Environment (Verilator + Python)
```

---

## cocotb: Python Hardware Testbenches

cocotb is a Python framework for testbenching SystemVerilog/Verilog modules.

### Installation

```bash
pip install cocotb
# Also need Verilator or other simulator
# On macOS:
brew install verilator
```

### Basic Testbench Structure

```python
# tb_led_blinker.py

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer

@cocotb.test()
async def test_led_blink(dut):
    """Test LED blinker toggles correctly."""
    
    # Create clock signal (50 MHz = 20 ns period)
    clock_task = cocotb.start_soon(Clock(dut.clk, 20, units="ns").start())
    
    # Reset the module
    dut.rst.value = 1
    await RisingEdge(dut.clk)
    dut.rst.value = 0
    await RisingEdge(dut.clk)
    
    # Initial state should be off
    assert dut.led.value == 0, "LED should be off initially"
    
    # Wait for LED to turn on
    # With 50MHz clock and 1Hz blink frequency:
    # Half period = 25 million clock cycles
    for _ in range(25_000_000 + 10):
        await RisingEdge(dut.clk)
    
    assert dut.led.value == 1, "LED should be on after half period"
    
    # Wait for LED to turn off
    for _ in range(25_000_000 + 10):
        await RisingEdge(dut.clk)
    
    assert dut.led.value == 0, "LED should be off again"
    
    dut._log.info("Test passed!")
```

### Signals and Access

```python
@cocotb.test()
async def test_signal_access(dut):
    """Demonstrate signal access."""
    
    # Read a signal
    current_value = dut.some_signal.value
    
    # Write a signal
    dut.input_signal.value = 42
    dut.input_signal.value = 0xFF
    dut.input_signal.value = 0b1010_1100
    
    # Multi-bit extraction
    dut.bus.value = 0x12345678
    byte0 = (dut.bus.value >> 0) & 0xFF   # 0x78
    byte1 = (dut.bus.value >> 8) & 0xFF   # 0x56
    
    # String representation
    dut._log.info(f"Signal value: {dut.signal.value:08b}")  # Binary
    dut._log.info(f"Signal value: {dut.signal.value:04x}")  # Hex
    dut._log.info(f"Signal value: {dut.signal.value}")      # Decimal
```

### Clocks and Timing

```python
@cocotb.test()
async def test_timing(dut):
    """Test timing-sensitive behavior."""
    
    # Start clock in background
    clock_task = cocotb.start_soon(Clock(dut.clk, 10, units="us").start())
    
    # Wait for rising edge
    await RisingEdge(dut.clk)
    
    # Wait for falling edge
    from cocotb.triggers import FallingEdge
    await FallingEdge(dut.clk)
    
    # Wait for fixed time
    await Timer(100, units="ns")
    
    # Wait for multiple events
    from cocotb.triggers import First
    clock_tick = RisingEdge(dut.clk)
    timeout = Timer(1000, units="us")
    winner = await First(clock_tick, timeout)
    
    dut._log.info(f"Event won: {winner}")
```

### UART Testbench Example

```python
# tb_uart.py

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer
import random

class UARTDriver:
    """Helper class to interact with UART."""
    
    def __init__(self, dut):
        self.dut = dut
        self.bit_period = 434  # Clock cycles per bit at 115200 baud, 50MHz clock
    
    async def send_byte(self, byte):
        """Send a byte over UART TX."""
        # Start bit (0)
        self.dut.tx_data.value = 0
        for _ in range(self.bit_period):
            await RisingEdge(self.dut.clk)
        
        # Data bits (LSB first)
        for i in range(8):
            bit = (byte >> i) & 1
            self.dut.tx_data.value = bit
            for _ in range(self.bit_period):
                await RisingEdge(self.dut.clk)
        
        # Stop bit (1)
        self.dut.tx_data.value = 1
        for _ in range(self.bit_period):
            await RisingEdge(self.dut.clk)
    
    async def receive_byte(self):
        """Receive a byte over UART RX."""
        # Wait for start bit (0)
        while self.dut.rx.value == 1:
            await RisingEdge(self.dut.clk)
        
        # Wait for middle of start bit
        for _ in range(self.bit_period // 2):
            await RisingEdge(self.dut.clk)
        
        byte = 0
        # Receive 8 data bits
        for i in range(8):
            byte |= self.dut.rx.value << i
            for _ in range(self.bit_period):
                await RisingEdge(self.dut.clk)
        
        return byte

@cocotb.test()
async def test_uart_loopback(dut):
    """Test UART loopback: send a byte and receive it back."""
    
    # Setup
    clock_task = cocotb.start_soon(Clock(dut.clk, 20, units="ns").start())
    driver = UARTDriver(dut)
    
    dut.rst.value = 1
    await RisingEdge(dut.clk)
    dut.rst.value = 0
    
    # Send byte 0xA5
    await driver.send_byte(0xA5)
    
    # Receive should give back 0xA5 in loopback mode
    received = await driver.receive_byte()
    
    assert received == 0xA5, f"Expected 0xA5, got 0x{received:02x}"
    dut._log.info("UART loopback test passed!")

@cocotb.test()
async def test_uart_random_bytes(dut):
    """Send and receive random bytes."""
    
    clock_task = cocotb.start_soon(Clock(dut.clk, 20, units="ns").start())
    driver = UARTDriver(dut)
    
    dut.rst.value = 1
    await RisingEdge(dut.clk)
    dut.rst.value = 0
    
    test_values = [0x00, 0xFF, 0x55, 0xAA, 0x12, 0x34, 0x56, 0x78]
    
    for test_byte in test_values:
        await driver.send_byte(test_byte)
        received = await driver.receive_byte()
        assert received == test_byte, f"Mismatch: sent 0x{test_byte:02x}, got 0x{received:02x}"
    
    dut._log.info(f"All {len(test_values)} random byte tests passed!")
```

### Memory/Register Testbench

```python
# tb_register_file.py

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge

@cocotb.test()
async def test_register_write_read(dut):
    """Test writing and reading registers."""
    
    clock_task = cocotb.start_soon(Clock(dut.clk, 20, units="ns").start())
    
    # Test case 1: Write to register 1, read back
    dut.write_addr.value = 1
    dut.write_data.value = 0xDEADBEEF
    dut.write_en.value = 1
    
    await RisingEdge(dut.clk)
    
    dut.write_en.value = 0
    dut.read_addr.value = 1
    
    await RisingEdge(dut.clk)
    
    assert dut.read_data.value == 0xDEADBEEF, \
        f"Expected 0xDEADBEEF, got 0x{dut.read_data.value:08x}"
    
    # Test case 2: x0 always reads as zero
    dut.read_addr.value = 0
    await RisingEdge(dut.clk)
    
    assert dut.read_data.value == 0, "x0 should always be zero"
    
    dut._log.info("Register file test passed!")

@cocotb.test()
async def test_register_dual_read(dut):
    """Test dual-port read (read two registers simultaneously)."""
    
    clock_task = cocotb.start_soon(Clock(dut.clk, 20, units="ns").start())
    
    # Write test values
    test_values = [
        (5, 0x12345678),
        (10, 0xABCDEF00),
        (15, 0xCAFEBABE),
    ]
    
    for addr, value in test_values:
        dut.write_addr.value = addr
        dut.write_data.value = value
        dut.write_en.value = 1
        await RisingEdge(dut.clk)
    
    dut.write_en.value = 0
    
    # Read dual ports
    dut.read_addr1.value = 5
    dut.read_addr2.value = 10
    
    await RisingEdge(dut.clk)
    
    assert dut.read_data1.value == 0x12345678, \
        f"Port 1 mismatch: 0x{dut.read_data1.value:08x}"
    assert dut.read_data2.value == 0xABCDEF00, \
        f"Port 2 mismatch: 0x{dut.read_data2.value:08x}"
    
    dut._log.info("Dual-port read test passed!")
```

---

## Simulation Environment

### Makefile for cocotb Simulation

```makefile
# Makefile

VERILOG_SOURCES = $(shell find rtl -name "*.sv")
TOPLEVEL_MODULE = top_module
MODULE = tb_module

# Use Verilator as simulator
SIM = verilator
SIM_ARGS = --trace

# Include cocotb makefiles
include $(COCOTB)/makefiles/Makefile.sim

# Clean simulation artifacts
clean::
	rm -rf obj_dir sim_build *.vcd
```

### Running Tests

```bash
# Run all tests
make

# Run specific test
make MODULE=tb_uart TESTCASE=test_uart_loopback

# With waveform output
make SIM_ARGS="--trace" MODULE=tb_uart

# View waveforms in GTKWave
gtkwave sim.vcd
```

### Test Organization

```
centurion/
├── tb/
│   ├── test_led_blinker.py
│   ├── test_uart.py
│   ├── test_register_file.py
│   ├── test_alu.py
│   ├── test_pipeline.py
│   └── Makefile
├── rtl/
│   ├── led_blinker.sv
│   ├── uart.sv
│   ├── register_file.sv
│   └── ...
```

---

## Verilator Integration

### Compiling with Verilator

```bash
# Basic compilation
verilator --cc rtl/top.sv --trace

# With C++ wrapper
verilator --cc rtl/top.sv --trace -o top

# For cocotb
verilator --cc rtl/top.sv --trace --verilog-std 2012
```

### Waveform Generation and Viewing

```bash
# Generate VCD (Value Change Dump) file
verilator --cc rtl/top.sv --trace -o top

# Run simulation and generate wave.vcd
./obj_dir/Vtop

# View in GTKWave
gtkwave wave.vcd

# View in other tools
# - Vivado (Xilinx)
# - ModelSim
# - Online viewers
```

### Understanding VCD Format

VCD files contain signal traces. Useful for:
- Timing verification
- Debug pipeline stages
- Verify clock/reset behavior
- Check data path correctness

---

## Build Systems and Scripts

### Python Build Script

```python
#!/usr/bin/env python3
# build.py

import os
import subprocess
import sys
from pathlib import Path

class Build:
    def __init__(self):
        self.root = Path(__file__).parent
        self.build_dir = self.root / "build"
        self.rtl_dir = self.root / "rtl"
        self.tb_dir = self.root / "tb"
        self.sw_dir = self.root / "sw"
    
    def clean(self):
        """Remove build artifacts."""
        print("Cleaning...")
        subprocess.run(["make", "-C", self.tb_dir, "clean"], check=False)
        if self.build_dir.exists():
            subprocess.run(["rm", "-rf", self.build_dir])
    
    def build_rtl(self):
        """Compile RTL."""
        print("Building RTL...")
        self.build_dir.mkdir(exist_ok=True)
        
        result = subprocess.run(
            ["verilator", "--cc", str(self.rtl_dir / "top.sv"), 
             "--trace", "-o", "top"],
            cwd=self.build_dir,
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            print("RTL compilation failed:")
            print(result.stderr)
            return False
        
        return True
    
    def build_assembler(self):
        """Build assembler."""
        print("Building assembler...")
        result = subprocess.run(
            [sys.executable, "-m", "py_compile", 
             str(self.sw_dir / "assembler" / "riscv_asm.py")],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            print("Assembler build failed:")
            print(result.stderr)
            return False
        
        return True
    
    def run_tests(self):
        """Run simulation tests."""
        print("Running tests...")
        result = subprocess.run(
            ["make", "-C", self.tb_dir],
            capture_output=True,
            text=True
        )
        
        print(result.stdout)
        
        if result.returncode != 0:
            print("Tests failed:")
            print(result.stderr)
            return False
        
        return True
    
    def build_all(self):
        """Build everything."""
        self.clean()
        
        if not self.build_rtl():
            return False
        
        if not self.build_assembler():
            return False
        
        if not self.run_tests():
            return False
        
        print("\nBuild successful!")
        return True

if __name__ == "__main__":
    build = Build()
    
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "clean":
            build.clean()
        elif cmd == "rtl":
            build.build_rtl()
        elif cmd == "asm":
            build.build_assembler()
        elif cmd == "test":
            build.run_tests()
        else:
            print(f"Unknown command: {cmd}")
    else:
        build.build_all()
```

### Shell Build Script

```bash
#!/bin/bash
# build.sh

set -e  # Exit on first error

ROOT=$(cd "$(dirname "$0")" && pwd)
BUILD_DIR="$ROOT/build"

echo "=== Centurion Build ==="

# Clean
echo "Cleaning..."
make -C "$ROOT/tb" clean || true
rm -rf "$BUILD_DIR"

# Create build directory
mkdir -p "$BUILD_DIR"

# Build RTL
echo "Building RTL..."
cd "$BUILD_DIR"
verilator --cc "$ROOT/rtl/top.sv" --trace -o top
cd "$ROOT"

# Build assembler
echo "Building assembler..."
python3 -m py_compile "$ROOT/sw/assembler/riscv_asm.py"

# Run tests
echo "Running tests..."
make -C "$ROOT/tb"

echo ""
echo "=== Build successful! ==="
```

---

## Testing Strategies

### Unit Testing

Test individual modules in isolation.

```python
@cocotb.test()
async def test_alu_add(dut):
    """Test ALU addition."""
    dut.a.value = 100
    dut.b.value = 50
    dut.op.value = 0  # ADD opcode
    
    await Timer(1, units="ns")  # Combinational: just wait for propagation
    
    assert dut.result.value == 150

@cocotb.test()
async def test_alu_all_operations(dut):
    """Test all ALU operations."""
    test_cases = [
        (10, 3, 0, 13),   # ADD
        (10, 3, 1, 7),    # SUB
        (10, 3, 2, 30),   # MUL
        (10, 3, 3, 3),    # DIV
    ]
    
    for a, b, op, expected in test_cases:
        dut.a.value = a
        dut.b.value = b
        dut.op.value = op
        
        await Timer(1, units="ns")
        
        assert dut.result.value == expected, \
            f"ALU({a}, {b}, {op}) = {dut.result.value}, expected {expected}"
```

### Integration Testing

Test multiple modules together.

```python
@cocotb.test()
async def test_pipeline(dut):
    """Test complete 5-stage pipeline."""
    
    clock_task = cocotb.start_soon(Clock(dut.clk, 20, units="ns").start())
    
    # Program: addi x1, x0, 10
    instruction = 0x00A00093  # encoding of addi x1, x0, 10
    
    dut.instruction.value = instruction
    dut.rst.value = 1
    await RisingEdge(dut.clk)
    dut.rst.value = 0
    
    # Wait for instruction to flow through pipeline
    for _ in range(5):
        await RisingEdge(dut.clk)
    
    # Check result in register x1
    assert dut.register_file_x1.value == 10
```

### Property-Based Testing

Test invariants that should always hold.

```python
@cocotb.test()
async def test_register_file_invariant(dut):
    """Test that x0 always reads as zero."""
    
    clock_task = cocotb.start_soon(Clock(dut.clk, 20, units="ns").start())
    
    # Write any value to x0 (should be ignored)
    for i in range(100):
        dut.write_addr.value = 0
        dut.write_data.value = random.randint(0, 2**32 - 1)
        dut.write_en.value = 1
        
        await RisingEdge(dut.clk)
        
        dut.write_en.value = 0
        dut.read_addr.value = 0
        
        await RisingEdge(dut.clk)
        
        # x0 should ALWAYS be zero
        assert dut.read_data.value == 0, \
            f"x0 is not zero! Got 0x{dut.read_data.value:08x}"
```

---

## Debugging Tools

### Logging in Testbenches

```python
@cocotb.test()
async def test_with_logging(dut):
    """Demonstrate logging."""
    
    dut._log.info("Starting test")
    dut._log.debug(f"Input value: {dut.input.value}")
    dut._log.warning("This is a warning")
    dut._log.error("This is an error (doesn't fail test)")
    
    # Check with assertions
    assert dut.output.value == 42, "Output mismatch"
    dut._log.info("Assertion passed!")
```

### Print Statements for Debugging

```python
@cocotb.test()
async def test_debug(dut):
    """Debug with print statements."""
    
    print(f"Input signal: 0x{dut.input.value:08x}")
    print(f"Output signal: {dut.output.value}")
    
    for i in range(10):
        print(f"Cycle {i}: addr={dut.addr.value}, data={dut.data.value}")
        await RisingEdge(dut.clk)
```

### Waveform Inspection

1. Generate VCD file from simulation
2. Open in GTKWave:
   ```bash
   gtkwave sim_build/sim.vcd
   ```
3. Add signals to view
4. Zoom in/out to see timing
5. Check state transitions

### Common Issues and Fixes

| Issue | Cause | Fix |
|-------|-------|-----|
| Test times out | Infinite loop in DUT | Check control flow, add timeout |
| Signal always 0 | Not connected properly | Check port names, bit widths |
| Wrong value | Off-by-one error | Check timing, sampling at right edge |
| Simulation hangs | Deadlock or infinite wait | Add timeout trigger, check synchronization |

---

## Project Organization

### Recommended Directory Structure

```
centurion/
├── README.md              # Project overview
├── build.py               # Build automation
├── Makefile               # Top-level make rules
├──
├── rtl/                   # SystemVerilog source
│   ├── core/              # CPU pipeline
│   │   ├── fetch.sv
│   │   ├── decode.sv
│   │   ├── execute.sv
│   │   ├── memory.sv
│   │   ├── writeback.sv
│   │   ├── register_file.sv
│   │   └── alu.sv
│   ├── peripherals/       # I/O devices
│   │   ├── uart.sv
│   │   ├── led_blinker.sv
│   │   └── ethernet.sv
│   ├── memory/            # Storage
│   │   ├── bram.sv
│   │   └── mmu.sv
│   └── top.sv             # Top-level module
│
├── tb/                    # Testbenches
│   ├── Makefile
│   ├── test_led_blinker.py
│   ├── test_uart.py
│   ├── test_register_file.py
│   ├── test_alu.py
│   ├── test_pipeline.py
│   └── conftest.py        # pytest configuration
│
├── sw/                    # Software
│   ├── assembler/         # RISC-V assembler
│   │   ├── riscv_asm.py
│   │   ├── lexer.py
│   │   ├── parser.py
│   │   └── encoder.py
│   ├── compiler/          # C compiler
│   │   ├── c_compiler.hs
│   │   └── Stack.yaml
│   ├── linker/            # Linker
│   │   └── linker.py
│   ├── libc/              # Standard library
│   │   ├── stdio.c
│   │   ├── stdlib.c
│   │   └── string.c
│   ├── bootrom/           # Boot code
│   │   └── bootrom.s
│   ├── bootloader/        # Bootloader
│   │   └── bootloader.c
│   └── kernel/            # OS kernel
│       ├── main.c
│       ├── process.c
│       └── syscall.c
│
├── sim/                   # Simulation scripts
│   ├── run_tests.py
│   ├── run_comprehensive.sh
│   └── generate_waveform.py
│
└── synth/                 # Synthesis scripts
    ├── synthesis.tcl      # Vivado script
    └── constraints.xdc    # FPGA constraints
```

### Makefile for Project

```makefile
# Top-level Makefile

.PHONY: all clean test sim rtl asm compiler linker

all: test

clean:
	python3 build.py clean

rtl:
	python3 build.py rtl

asm:
	python3 build.py asm

compiler:
	cd sw/compiler && stack build

test:
	python3 build.py test

sim:
	make -C tb

help:
	@echo "Targets:"
	@echo "  make all       - Build and test everything"
	@echo "  make clean     - Remove build artifacts"
	@echo "  make rtl       - Compile RTL only"
	@echo "  make asm       - Build assembler"
	@echo "  make compiler  - Build C compiler"
	@echo "  make test      - Run all tests"
	@echo "  make sim       - Run simulations"
```

---

## Summary

Testbenching is critical for reliable hardware:
1. **cocotb**: Write tests in Python, not Verilog
2. **Drivers**: Create helper classes for complex interfaces
3. **Assertions**: Verify expected behavior
4. **Logging**: Debug with clear, informative messages
5. **Organization**: Keep tests organized by module
6. **Automation**: Use build scripts to run tests consistently

Key tools:
- **Verilator**: Fast simulation engine
- **cocotb**: Python testbench framework
- **GTKWave**: Waveform viewer
- **Python/Bash**: Build automation

Next steps:
1. Write testbenches alongside RTL
2. Run tests frequently (before each commit)
3. Aim for >90% code coverage
4. Document test purpose and assumptions
5. Keep tests simple and focused

Remember: a hardware bug caught in simulation costs minutes to fix; the same bug in silicon costs millions.
