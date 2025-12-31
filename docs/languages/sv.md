# SystemVerilog: Hardware Design Guide

SystemVerilog is an extension of Verilog that enables digital hardware design and verification. It's used to create Register Transfer Logic (RTL) descriptions that can be simulated or synthesized into actual hardware.

## Table of Contents
1. [Language Fundamentals](#language-fundamentals)
2. [Basic Syntax](#basic-syntax)
3. [Logic and Data Types](#logic-and-data-types)
4. [Combinational Logic](#combinational-logic)
5. [Sequential Logic](#sequential-logic)
6. [Module Instantiation](#module-instantiation)
7. [Parameters and Generics](#parameters-and-generics)
8. [Advanced Features](#advanced-features)
9. [Centurion-Specific Examples](#centurion-specific-examples)

---

## Language Fundamentals

### What is SystemVerilog?

SystemVerilog describes hardware at the Register Transfer Logic (RTL) level. Your code describes how data moves between registers and how it's transformed by combinational logic.

**Key Mental Model:**
- `always_comb`: Combinational logic (output is purely a function of inputs)
- `always_ff`: Sequential logic (operates on clock edges, has state)
- `assign`: Continuous assignment for simple combinational logic
- `module`: Reusable hardware building block

### Hardware vs Software Thinking

| Hardware (SystemVerilog) | Software (C) |
|--------------------------|--------------|
| All logic runs in parallel | Code executes sequentially |
| `always` blocks are concurrent | `if` statements are conditional |
| Time flows with clock pulses | Time flows with instruction count |
| Physical gates are your resource | CPU cycles are your resource |
| Wires are permanent connections | Variables are temporary storage |

---

## Basic Syntax

### Module Declaration

```systemverilog
module adder(
  input  logic [7:0] a,
  input  logic [7:0] b,
  output logic [7:0] sum
);
  assign sum = a + b;
endmodule
```

**Breakdown:**
- `module adder`: declares a module named `adder`
- `input logic [7:0] a`: 8-bit input wire named `a`
- `output logic [7:0] sum`: 8-bit output wire named `sum`
- `assign sum = a + b`: combinational logic that adds inputs
- `endmodule`: closes the module

### Port Directions

- `input`: data flows INTO the module
- `output`: data flows OUT of the module
- `inout`: bidirectional (used for bus lines)

### Wire Types

```systemverilog
logic       x;        // Single bit, can be assigned
logic [7:0] byte_val; // 8-bit vector
logic [15:0][7:0] matrix; // 2D array of 8-bit values
```

---

## Logic and Data Types

### Basic Types

```systemverilog
// Single-bit signals
logic a;
logic b;

// Multi-bit vectors (bus width specified as [MSB:LSB])
logic [7:0] byte_val;   // bits 7 down to 0
logic [31:0] word;      // 32-bit word
logic [0:15] reverse;   // counting upward (unusual but allowed)

// Unsigned and signed types
logic unsigned [7:0]  u8;    // 0 to 255
logic signed   [7:0]  s8;    // -128 to 127
logic signed   [31:0] s32;   // 32-bit signed integer

// Wide vectors (for memories, wide buses)
logic [63:0] bus;
```

### Bit Indexing and Ranges

```systemverilog
logic [31:0] word;

wire a     = word[0];      // Access single bit
wire b     = word[15:8];   // Access bits 15 down to 8 (8-bit slice)
wire c     = word[3:0];    // Access lower 4 bits
wire d     = word[31:16];  // Access upper 16 bits
```

### Constants and Literals

```systemverilog
logic [7:0] a = 8'h42;      // Hexadecimal: 42 (hex) = 66 (decimal)
logic [7:0] b = 8'b1010_1100; // Binary with separator
logic [7:0] c = 8'd123;     // Decimal
logic [7:0] d = 255;        // Default to decimal

// Common patterns for Centurion
logic [31:0] addr = 32'h8000_0000;  // RISC-V base address
logic [7:0] uart_byte = 8'hFF;      // Send 0xFF to UART
```

---

## Combinational Logic

Combinational logic produces outputs that are purely a function of current inputs (no memory).

### Continuous Assignment

```systemverilog
module mux_2to1(
  input  logic a, b, sel,
  output logic y
);
  assign y = sel ? a : b;  // Ternary operator (multiplexer)
endmodule
```

**Usage:**
```systemverilog
logic [7:0] in0, in1, result;
logic sel;
assign result = sel ? in0 : in1;
```

### always_comb Block

Use `always_comb` for combinational logic that's complex or multi-statement.

```systemverilog
module priority_encoder(
  input  logic [3:0] req,
  output logic [1:0] priority
);
  always_comb begin
    if (req[3])
      priority = 3;
    else if (req[2])
      priority = 2;
    else if (req[1])
      priority = 1;
    else
      priority = 0;
  end
endmodule
```

### Logic Gates and Operators

```systemverilog
logic a, b, c;

// Bitwise operators (operate on each bit independently)
c = a & b;       // AND
c = a | b;       // OR
c = a ^ b;       // XOR
c = ~a;          // NOT

// Logical operators (used in conditions)
if (a && b)      // AND condition (boolean result)
if (a || b)      // OR condition
if (!a)          // NOT condition

// Shifts
logic [7:0] byte_val;
logic [7:0] shifted;
shifted = byte_val >> 2;  // Shift right by 2
shifted = byte_val << 1;  // Shift left by 1
```

### Arithmetic

```systemverilog
logic [7:0] a, b, sum, product;
logic [15:0] wide_sum;

sum = a + b;           // 8-bit add (result wraps)
wide_sum = a + b;      // Extends to 16-bit
product = a * b;       // Multiply (result size varies)
diff = a - b;          // Subtract
quotient = a / b;      // Divide (avoid in synthesis!)
remainder = a % b;     // Modulo (avoid in synthesis!)
```

### Replicate and Concatenation

```systemverilog
logic a, b, c;
logic [7:0] byte_val;

// Concatenation (putting things together)
logic [9:0] concat = {a, b, c, byte_val};  // 1+1+1+8 = 11 bits

// Replication (repeat a value)
logic [15:0] wide = {8{a}};  // a repeated 8 times

// Common Centurion pattern: assembling bytes
logic [7:0] byte0, byte1, byte2, byte3;
logic [31:0] word = {byte3, byte2, byte1, byte0};
```

---

## Sequential Logic

Sequential logic has memory and changes on clock edges.

### The Clock and Reset

Every digital system needs:
- **Clock (clk)**: periodic pulse that synchronizes all operations
- **Reset (rst)**: initializes all state to known values

```systemverilog
module counter(
  input  logic       clk, rst,
  input  logic [7:0] increment,
  output logic [7:0] count
);
  // Logic here...
endmodule
```

### always_ff Block

`always_ff` describes behavior on clock edges.

```systemverilog
module simple_counter(
  input  logic       clk, rst,
  output logic [3:0] count
);
  always_ff @(posedge clk) begin
    if (rst)
      count <= 0;
    else
      count <= count + 1;
  end
endmodule
```

**Key points:**
- `@(posedge clk)`: trigger on rising clock edge (most common)
- `@(negedge clk)`: trigger on falling clock edge (rare)
- `<=`: non-blocking assignment (use ONLY in `always_ff`)
- `=`: blocking assignment (use ONLY in `always_comb`)

### State Machines

State machines are fundamental to hardware design.

```systemverilog
module simple_fsm(
  input  logic clk, rst, start,
  output logic busy, done
);
  // Define states
  typedef enum logic [1:0] {
    IDLE = 2'b00,
    ACTIVE = 2'b01,
    DONE_STATE = 2'b10
  } state_t;
  
  state_t current_state, next_state;
  
  // State register (sequential)
  always_ff @(posedge clk) begin
    if (rst)
      current_state <= IDLE;
    else
      current_state <= next_state;
  end
  
  // Next state logic (combinational)
  always_comb begin
    case (current_state)
      IDLE: begin
        if (start)
          next_state = ACTIVE;
        else
          next_state = IDLE;
      end
      ACTIVE: begin
        next_state = DONE_STATE;
      end
      DONE_STATE: begin
        next_state = IDLE;
      end
      default: next_state = IDLE;
    endcase
  end
  
  // Output logic (combinational)
  assign busy = (current_state == ACTIVE);
  assign done = (current_state == DONE_STATE);
endmodule
```

### Flip-Flops for Storage

```systemverilog
logic d, clk;
logic q, q_next;

// Register description (D flip-flop)
always_ff @(posedge clk) begin
  q <= d;  // Sample input d on clock edge, output it as q
end

// Shift register
logic [7:0] shift_register;
logic serial_in, serial_out;

always_ff @(posedge clk) begin
  shift_register <= {shift_register[6:0], serial_in};
end
assign serial_out = shift_register[7];
```

---

## Module Instantiation

Modules are the building blocks of larger designs. Instantiate them like variables.

### Basic Instantiation

```systemverilog
module top_level(
  input  logic [7:0] a, b,
  output logic [7:0] sum
);
  // Instantiate the adder module
  adder my_adder(
    .a(a),
    .b(b),
    .sum(sum)
  );
endmodule
```

### Multiple Instances

```systemverilog
module quad_adder(
  input  logic [7:0] a0, a1, a2, a3,
  input  logic [7:0] b0, b1, b2, b3,
  output logic [7:0] sum0, sum1, sum2, sum3
);
  // Create 4 adders
  adder add0(.a(a0), .b(b0), .sum(sum0));
  adder add1(.a(a1), .b(b1), .sum(sum1));
  adder add2(.a(a2), .b(b2), .sum(sum2));
  adder add3(.a(a3), .b(b3), .sum(sum3));
endmodule
```

### Positional Connection (avoid in large designs)

```systemverilog
// Positional (order-dependent, error-prone)
adder add0(a, b, sum);

// Named (explicit, preferred)
adder add0(.a(a), .b(b), .sum(sum));
```

---

## Parameters and Generics

Parameters make modules reusable with different sizes/configurations.

### Parameter Basics

```systemverilog
module parameterized_adder #(
  parameter int WIDTH = 8
)(
  input  logic [WIDTH-1:0] a, b,
  output logic [WIDTH-1:0] sum
);
  assign sum = a + b;
endmodule
```

**Usage:**
```systemverilog
// Use default WIDTH=8
parameterized_adder add8(.a(a8), .b(b8), .sum(sum8));

// Override WIDTH to 16
parameterized_adder #(.WIDTH(16)) add16(
  .a(a16), .b(b16), .sum(sum16)
);

// Override WIDTH to 32
parameterized_adder #(.WIDTH(32)) add32(
  .a(a32), .b(b32), .sum(sum32)
);
```

### Useful Macros for Parameterized Design

```systemverilog
module counter #(
  parameter int MAX = 255
)(
  input  logic clk, rst,
  output logic [clog2(MAX)-1:0] count
);
  // $clog2: computes log2 of a number, rounded up
  // For MAX=256, clog2(256) = 8
  // For MAX=100, clog2(100) = 7 (because 2^7=128 > 100)
endmodule
```

---

## Advanced Features

### Interfaces and Bundles

Group related signals together for cleaner code.

```systemverilog
// Define an interface for a memory bus
interface mem_bus #(
  parameter ADDR_WIDTH = 16,
  parameter DATA_WIDTH = 32
);
  logic [ADDR_WIDTH-1:0] addr;
  logic [DATA_WIDTH-1:0] data;
  logic                  valid;
  logic                  ready;
  
  modport master(
    output addr, data, valid,
    input  ready
  );
  
  modport slave(
    input  addr, data, valid,
    output ready
  );
endinterface

// Use in a module
module memory_controller(
  mem_bus.slave bus
);
  always_comb begin
    bus.ready = 1;  // Always ready for simplicity
  end
endmodule
```

### Always_latch (Avoid in most designs)

```systemverilog
// Creates a latch (level-sensitive, not recommended)
always_latch begin
  if (!clk)
    q <= d;
end
```

### Generate Blocks

Generate repeated hardware structures.

```systemverilog
module adder_tree #(
  parameter int NUM_INPUTS = 4
)(
  input  logic [7:0] inputs [NUM_INPUTS],
  output logic [15:0] sum
);
  if (NUM_INPUTS == 1) begin
    assign sum = inputs[0];
  end else begin
    // Recursively create smaller trees
  end
endmodule
```

---

## Centurion-Specific Examples

### LED Blinker

The LED blinker is the first circuit in Centurion. It toggles an LED at a fixed frequency.

```systemverilog
module led_blinker #(
  parameter int CLOCK_FREQ = 50_000_000,  // 50 MHz
  parameter int BLINK_FREQ = 1             // 1 Hz
)(
  input  logic clk, rst,
  output logic led
);
  // Calculate how many clock cycles for half period
  localparam int HALF_PERIOD = CLOCK_FREQ / (2 * BLINK_FREQ);
  localparam int COUNTER_WIDTH = $clog2(HALF_PERIOD);
  
  logic [COUNTER_WIDTH-1:0] counter;
  
  always_ff @(posedge clk) begin
    if (rst) begin
      counter <= 0;
      led <= 0;
    end else if (counter == HALF_PERIOD - 1) begin
      counter <= 0;
      led <= ~led;  // Toggle LED
    end else begin
      counter <= counter + 1;
    end
  end
endmodule
```

**How it works:**
1. Count clock cycles up to HALF_PERIOD
2. When count reaches HALF_PERIOD, toggle LED and reset counter
3. Result: LED blinks at BLINK_FREQ Hz

**For 50MHz clock and 1Hz blink:**
- HALF_PERIOD = 50,000,000 / 2 = 25,000,000
- COUNTER_WIDTH = ⌈log₂(25,000,000)⌉ = 25 bits
- LED toggles every 25,000,000 clock cycles = 0.5 seconds on, 0.5 seconds off

### UART Transmitter

UART sends data serially, one bit at a time.

```systemverilog
module uart_tx #(
  parameter int CLOCK_FREQ = 50_000_000,
  parameter int BAUD_RATE = 115_200
)(
  input  logic clk, rst,
  input  logic [7:0] data_in,
  input  logic       data_valid,
  output logic       tx,
  output logic       tx_ready
);
  // Calculate baud period in clock cycles
  localparam int BAUD_PERIOD = CLOCK_FREQ / BAUD_RATE;
  localparam int BAUD_COUNTER_WIDTH = $clog2(BAUD_PERIOD);
  
  typedef enum logic [2:0] {
    IDLE = 0,
    START_BIT = 1,
    DATA_BITS = 2,
    STOP_BIT = 3
  } state_t;
  
  state_t state, next_state;
  logic [BAUD_COUNTER_WIDTH-1:0] baud_counter;
  logic [2:0] bit_index;
  logic [7:0] shift_register;
  
  // State machine
  always_ff @(posedge clk) begin
    if (rst) begin
      state <= IDLE;
      baud_counter <= 0;
      bit_index <= 0;
      tx <= 1;  // Idle high
    end else begin
      state <= next_state;
      
      if (state == IDLE) begin
        baud_counter <= 0;
      end else if (baud_counter == BAUD_PERIOD - 1) begin
        baud_counter <= 0;
        bit_index <= bit_index + 1;
      end else begin
        baud_counter <= baud_counter + 1;
      end
      
      // Load shift register on transition to START_BIT
      if (state == IDLE && next_state == START_BIT)
        shift_register <= data_in;
    end
  end
  
  always_comb begin
    next_state = state;
    tx_ready = (state == IDLE);
    
    case (state)
      IDLE: begin
        tx = 1;
        if (data_valid)
          next_state = START_BIT;
      end
      START_BIT: begin
        tx = 0;  // Start bit is low
        if (baud_counter == BAUD_PERIOD - 1)
          next_state = DATA_BITS;
      end
      DATA_BITS: begin
        tx = shift_register[bit_index];
        if (bit_index == 7 && baud_counter == BAUD_PERIOD - 1)
          next_state = STOP_BIT;
      end
      STOP_BIT: begin
        tx = 1;  // Stop bit is high
        if (baud_counter == BAUD_PERIOD - 1)
          next_state = IDLE;
      end
    endcase
  end
endmodule
```

**Protocol:**
- Frame: [START(1) | DATA(8) | STOP(1)] = 10 bits total
- START bit: 0 (low)
- STOP bit: 1 (high)
- Data bits: LSB first
- Timing: 115200 baud = 115200 bits/second = 1 bit every ~8.68 microseconds

At 50MHz: 50,000,000 / 115,200 ≈ 434 clock cycles per bit

### Simple 5-Stage Pipeline

The Centurion processor uses a 5-stage pipeline: Fetch → Decode → Execute → Memory → Writeback.

```systemverilog
module simple_pipeline(
  input  logic clk, rst,
  input  logic [31:0] instruction,
  output logic [31:0] result
);
  // Pipeline stage registers
  logic [31:0] if_insn, id_insn, ex_insn, mem_insn, wb_insn;
  logic [31:0] ex_result, mem_result, wb_result;
  
  // Stage 1: Fetch (instruction already provided)
  always_ff @(posedge clk) begin
    if (rst) begin
      if_insn <= 0;
    end else begin
      if_insn <= instruction;
    end
  end
  
  // Stage 2: Decode (extract opcode, registers)
  always_ff @(posedge clk) begin
    if (rst) begin
      id_insn <= 0;
    end else begin
      id_insn <= if_insn;
    end
  end
  
  // Stage 3: Execute (perform ALU operation)
  always_ff @(posedge clk) begin
    if (rst) begin
      ex_insn <= 0;
      ex_result <= 0;
    end else begin
      ex_insn <= id_insn;
      // Simplified: just add some value
      ex_result <= id_insn[15:0] + id_insn[31:16];
    end
  end
  
  // Stage 4: Memory (load/store if needed)
  always_ff @(posedge clk) begin
    if (rst) begin
      mem_insn <= 0;
      mem_result <= 0;
    end else begin
      mem_insn <= ex_insn;
      mem_result <= ex_result;
    end
  end
  
  // Stage 5: Writeback (write result back to registers)
  always_ff @(posedge clk) begin
    if (rst) begin
      wb_insn <= 0;
      wb_result <= 0;
    end else begin
      wb_insn <= mem_insn;
      wb_result <= mem_result;
    end
  end
  
  assign result = wb_result;
endmodule
```

### Register File

The register file stores 32 RISC-V registers.

```systemverilog
module register_file(
  input  logic       clk,
  input  logic [4:0] read_addr1, read_addr2, write_addr,
  input  logic [31:0] write_data,
  input  logic       write_enable,
  output logic [31:0] read_data1, read_data2
);
  logic [31:0] registers [32];  // 32 x 32-bit registers
  
  // x0 (zero register) is hardwired to 0
  assign registers[0] = 0;
  
  // Read (combinational)
  assign read_data1 = registers[read_addr1];
  assign read_data2 = registers[read_addr2];
  
  // Write (sequential)
  always_ff @(posedge clk) begin
    if (write_enable && write_addr != 0)
      registers[write_addr] <= write_data;
  end
endmodule
```

### ALU (Arithmetic Logic Unit)

Performs arithmetic and logical operations.

```systemverilog
module alu #(
  parameter int WIDTH = 32
)(
  input  logic [WIDTH-1:0] a, b,
  input  logic [3:0] op,
  output logic [WIDTH-1:0] result
);
  always_comb begin
    case (op)
      4'h0: result = a + b;      // ADD
      4'h1: result = a - b;      // SUB
      4'h2: result = a & b;      // AND
      4'h3: result = a | b;      // OR
      4'h4: result = a ^ b;      // XOR
      4'h5: result = a << b[4:0]; // SHL
      4'h6: result = a >> b[4:0]; // SHR
      4'h7: result = a < b ? 1 : 0; // SLT (set less than)
      default: result = 0;
    endcase
  end
endmodule
```

---

## Best Practices

1. **Use `always_comb` for combinational**: easier to understand intent
2. **Use `always_ff` for sequential**: never mix logic types
3. **Always use non-blocking `<=` in `always_ff`**: prevents race conditions
4. **Always use blocking `=` in `always_comb`**: natural for combinational logic
5. **Initialize all logic to zero or sensible default**: prevents X propagation
6. **Use meaningful names**: `uart_tx_valid` better than `utv`
7. **Keep modules small**: aim for 100-500 lines per module
8. **Use parameters for size/frequency**: enables reusability

---

## Useful SystemVerilog Functions

```systemverilog
logic [31:0] value = 32'h12345678;

// clog2: logarithm base 2, rounded up
int bits_needed = $clog2(256);  // Returns 8 (because 2^8=256)
int bits_for_100 = $clog2(100); // Returns 7 (because 2^7=128 > 100)

// Bit operations
int width = $bits(value);  // 32
int ones = $countones(value); // Count 1s in binary representation
int lsb = $ctz(value);     // Count trailing zeros (lowest set bit)
int msb = $clz(value);     // Count leading zeros (highest set bit)

// String operations
string msg = $sformatf("Value is %d", 42);

// Random (for testbenches)
int rand_val = $urandom(); // 32-bit random
int rand_range = $urandom_range(0, 100); // Random 0-100
```

---

## Summary

SystemVerilog enables hardware design by:
- Describing combinational logic with `assign` or `always_comb`
- Describing sequential logic with `always_ff`
- Organizing designs into reusable `module` blocks
- Making designs flexible with `parameter`s
- Using meaningful identifiers and proper simulation

Start simple with LEDs and UARTs, then build toward processors and memory systems. Each Centurion section builds on SystemVerilog fundamentals: the 5-stage pipeline is just registers and combinational logic organized into stages.
