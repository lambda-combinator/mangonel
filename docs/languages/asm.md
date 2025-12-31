# RISC-V Assembly: The Processor's Native Language

RISC-V is an open-source Instruction Set Architecture (ISA). Centurion implements the RV32I subset (32-bit, integer-only), which provides ~47 instructions sufficient for a complete operating system.

## Table of Contents
1. [RISC-V Fundamentals](#risc-v-fundamentals)
2. [Registers](#registers)
3. [Instruction Formats](#instruction-formats)
4. [Instruction Set](#instruction-set)
5. [Addressing Modes](#addressing-modes)
6. [Calling Conventions](#calling-conventions)
7. [Control Flow](#control-flow)
8. [Memory and Data](#memory-and-data)
9. [Centurion: From C to Assembly](#centurion-from-c-to-assembly)

---

## RISC-V Fundamentals

### What is RISC-V?

RISC-V (Reduced Instruction Set Computer - V) is an instruction set that defines:
- What operations the processor can perform
- How to encode instructions into 32-bit words
- How memory, registers, and I/O work

"RISC" means: simple, regular instructions that execute in one cycle.

### Why RISC-V?

1. **Open Standard**: No licensing fees, anyone can implement it
2. **Modular**: Base (RV32I) + optional extensions (M, A, F, D)
3. **Simple**: ~47 base instructions vs ~500 in x86
4. **Clean Design**: Consistent instruction encoding
5. **Educational**: Perfect for learning architecture and compilers

### RV32I vs Other Variants

| Variant | Bit Width | Float | Atomic | Notes |
|---------|-----------|-------|--------|-------|
| RV32I | 32-bit | No | No | Minimal, suitable for Centurion |
| RV32IM | 32-bit | No | Yes | + Multiplication/Division |
| RV32F | 32-bit | Yes | No | + Single-precision FP |
| RV64I | 64-bit | No | No | Full 64-bit registers |
| RV64G | 64-bit | Yes | Yes | Full-featured |

Centurion uses **RV32I**: 32-bit, integer-only operations.

---

## Registers

### The Register File

RISC-V has 32 registers, each 32 bits wide. Register x0 is hardwired to 0.

```
x0  (zero)   Always 0 (hardwired)
x1  (ra)     Return address
x2  (sp)     Stack pointer
x3  (gp)     Global pointer
x4  (tp)     Thread pointer
x5-x7 (t0-t2)  Temporary (caller-saved)
x8  (s0/fp)  Saved register / Frame pointer
x9  (s1)     Saved register
x10-x11 (a0-a1)     Function arguments / Return value
x12-x17 (a2-a7)     Function arguments
x18-x27 (s2-s11)     Saved registers (callee-saved)
x28-x31 (t3-t6)      Temporary (caller-saved)
```

### Register Naming Conventions

| Register | ABI Name | Purpose |
|----------|----------|---------|
| x0 | zero | Hardwired to zero |
| x1 | ra | Return address (function calls save here) |
| x2 | sp | Stack pointer (points to top of stack) |
| x3 | gp | Global pointer (for global data) |
| x10-x11 | a0-a1 | Arguments / Return value |
| x12-x17 | a2-a7 | Additional arguments |
| x5-x7, x28-x31 | t0-t6 | Temporaries (caller-saved) |
| x8-x9, x18-x27 | s0-s11 | Saved (callee-saved) |

### Register Usage Example

```risc-v
    # Function: int add(int a, int b)
    # Arguments: a0 = a, a1 = b
    # Return: a0 = a + b
add_func:
    add a0, a0, a1       # a0 = a0 + a1
    ret                  # Return to caller (jr ra)
```

---

## Instruction Formats

RISC-V instructions are 32 bits. Different instruction types use different encodings.

### R-Type: Register Operations

```
opcode[6:0] | rd[11:7] | funct3[14:12] | rs1[19:15] | rs2[24:20] | funct7[31:25]
31        25 24      20 19          15 14        12 11        7 6           0
```

Performs operations on registers only.

**Examples:**
```risc-v
add rd, rs1, rs2    # rd = rs1 + rs2
sub rd, rs1, rs2    # rd = rs1 - rs2
and rd, rs1, rs2    # rd = rs1 & rs2
or rd, rs1, rs2     # rd = rs1 | rs2
xor rd, rs1, rs2    # rd = rs1 ^ rs2
sll rd, rs1, rs2    # rd = rs1 << rs2[4:0]
srl rd, rs1, rs2    # rd = rs1 >> rs2[4:0] (logical)
sra rd, rs1, rs2    # rd = rs1 >> rs2[4:0] (arithmetic)
slt rd, rs1, rs2    # rd = (rs1 < rs2) ? 1 : 0
sltu rd, rs1, rs2   # rd = (rs1 < rs2 unsigned) ? 1 : 0
```

**Encoding Example: add x1, x2, x3**
```
funct7=0 | rs2=3 | rs1=2 | funct3=0 | rd=1 | opcode=0x33
0000000  | 00011 | 00010 | 000      | 00001| 0110011
```

### I-Type: Immediate Operations

```
imm[31:20] | rs1[19:15] | funct3[14:12] | rd[11:7] | opcode[6:0]
31       20 19        15 14           12 11       7 6         0
```

Includes a 12-bit immediate value (sign-extended).

**Examples:**
```risc-v
addi rd, rs1, imm    # rd = rs1 + imm (imm is 12-bit signed)
slti rd, rs1, imm    # rd = (rs1 < imm) ? 1 : 0
sltiu rd, rs1, imm   # rd = (rs1 < imm unsigned) ? 1 : 0
andi rd, rs1, imm    # rd = rs1 & imm
ori rd, rs1, imm     # rd = rs1 | imm
xori rd, rs1, imm    # rd = rs1 ^ imm
slli rd, rs1, shamt  # rd = rs1 << shamt (shift amount in imm[4:0])
srli rd, rs1, shamt  # rd = rs1 >> shamt (logical)
srai rd, rs1, shamt  # rd = rs1 >> shamt (arithmetic)
lw rd, imm(rs1)      # rd = *(rs1 + imm) (load word from memory)
```

**Encoding Example: addi x1, x2, 100**
```
imm=100        | rs1=2 | funct3=0 | rd=1 | opcode=0x13
0000 0110 0100 | 00010 | 000      | 00001| 0010011
```

### S-Type: Store (Memory Write)

```
imm[31:25] | rs2[24:20] | rs1[19:15] | funct3[14:12] | imm[11:7] | opcode[6:0]
31       25 24        20 19        15 14           12 11       7 6         0
```

Stores value from rs2 into memory at address rs1 + imm.

**Examples:**
```risc-v
sw rs2, imm(rs1)     # *(rs1 + imm) = rs2 (store word)
sh rs2, imm(rs1)     # *(rs1 + imm) = rs2[15:0] (store half)
sb rs2, imm(rs1)     # *(rs1 + imm) = rs2[7:0] (store byte)
```

### B-Type: Branch

```
imm[31:25] | rs2[24:20] | rs1[19:15] | funct3[14:12] | imm[11:7] | opcode[6:0]
31       25 24        20 19        15 14           12 11       7 6         0
```

Conditional jumps. Immediate is 12-bit, encodes even byte offset.

**Examples:**
```risc-v
beq rs1, rs2, label  # if (rs1 == rs2) jump to label
bne rs1, rs2, label  # if (rs1 != rs2) jump to label
blt rs1, rs2, label  # if (rs1 < rs2) jump to label
bge rs1, rs2, label  # if (rs1 >= rs2) jump to label
bltu rs1, rs2, label # if (rs1 < rs2 unsigned) jump to label
bgeu rs1, rs2, label # if (rs1 >= rs2 unsigned) jump to label
```

### U-Type: Load Upper Immediate

```
imm[31:12] | rd[11:7] | opcode[6:0]
31       12 11       7 6         0
```

Loads 20-bit immediate into upper 20 bits of register.

**Examples:**
```risc-v
lui rd, imm         # rd = imm << 12 (load upper immediate)
auipc rd, imm       # rd = PC + (imm << 12)
```

### J-Type: Jump

```
imm[31:20] | imm[10:1] | imm[11] | imm[19:12] | rd[11:7] | opcode[6:0]
31       20 19        10 11      12          8 11      7 6         0
```

Unconditional jump. Immediate is 20-bit, encodes even byte offset.

**Examples:**
```risc-v
jal rd, label       # rd = PC + 4; PC = PC + offset
jalr rd, rs1, imm   # rd = PC + 4; PC = rs1 + imm
```

---

## Instruction Set

### Arithmetic

```risc-v
# Addition and subtraction
add rd, rs1, rs2     # rd = rs1 + rs2
addi rd, rs1, imm    # rd = rs1 + imm (12-bit signed)
sub rd, rs1, rs2     # rd = rs1 - rs2

# No multiply/divide in RV32I (optional RV32M extension)
# mul rd, rs1, rs2     # rd = rs1 * rs2 (if RV32M)
# div rd, rs1, rs2     # rd = rs1 / rs2 (if RV32M)
```

### Logical Operations

```risc-v
and rd, rs1, rs2     # rd = rs1 & rs2
andi rd, rs1, imm    # rd = rs1 & imm
or rd, rs1, rs2      # rd = rs1 | rs2
ori rd, rs1, imm     # rd = rs1 | imm
xor rd, rs1, rs2     # rd = rs1 ^ rs2
xori rd, rs1, imm    # rd = rs1 ^ imm
```

### Shifts

```risc-v
sll rd, rs1, rs2     # rd = rs1 << rs2[4:0] (shift left logical)
slli rd, rs1, shamt  # rd = rs1 << shamt (shamt in imm[4:0])
srl rd, rs1, rs2     # rd = rs1 >> rs2[4:0] (shift right logical)
srli rd, rs1, shamt  # rd = rs1 >> shamt
sra rd, rs1, rs2     # rd = rs1 >> rs2[4:0] (shift right arithmetic)
srai rd, rs1, shamt  # rd = rs1 >> shamt (preserves sign)
```

### Comparisons

```risc-v
slt rd, rs1, rs2     # rd = (rs1 < rs2) ? 1 : 0 (signed)
slti rd, rs1, imm    # rd = (rs1 < imm) ? 1 : 0
sltu rd, rs1, rs2    # rd = (rs1 < rs2) ? 1 : 0 (unsigned)
sltiu rd, rs1, imm   # rd = (rs1 < imm) ? 1 : 0 (unsigned)
```

### Memory Access

```risc-v
# Load (read from memory)
lw rd, offset(rs1)   # rd = *(rs1 + offset) (32-bit)
lh rd, offset(rs1)   # rd = *(rs1 + offset) (16-bit, sign-extended)
lhu rd, offset(rs1)  # rd = *(rs1 + offset) (16-bit, zero-extended)
lb rd, offset(rs1)   # rd = *(rs1 + offset) (8-bit, sign-extended)
lbu rd, offset(rs1)  # rd = *(rs1 + offset) (8-bit, zero-extended)

# Store (write to memory)
sw rs2, offset(rs1)  # *(rs1 + offset) = rs2 (32-bit)
sh rs2, offset(rs1)  # *(rs1 + offset) = rs2[15:0] (16-bit)
sb rs2, offset(rs1)  # *(rs1 + offset) = rs2[7:0] (8-bit)
```

### Control Flow

```risc-v
# Conditional branches
beq rs1, rs2, label  # if (rs1 == rs2) PC += offset
bne rs1, rs2, label  # if (rs1 != rs2) PC += offset
blt rs1, rs2, label  # if (rs1 < rs2) PC += offset (signed)
bge rs1, rs2, label  # if (rs1 >= rs2) PC += offset (signed)
bltu rs1, rs2, label # if (rs1 < rs2) PC += offset (unsigned)
bgeu rs1, rs2, label # if (rs1 >= rs2) PC += offset (unsigned)

# Unconditional jumps
jal rd, label        # rd = PC + 4; PC += offset
jalr rd, rs1, imm    # rd = PC + 4; PC = rs1 + imm
```

### Upper Immediate

```risc-v
lui rd, imm          # rd = imm << 12 (load upper immediate)
auipc rd, imm        # rd = PC + (imm << 12)
```

### System and Pseudo-Instructions

```risc-v
# Pseudo-instructions (expanded by assembler)
li rd, imm          # Load immediate (may use lui + addi)
la rd, symbol       # Load address
mv rd, rs           # Move register (addi rd, rs, 0)
neg rd, rs          # Negate (sub rd, x0, rs)
not rd, rs          # Bitwise NOT (xori rd, rs, -1)

# System instructions
ecall               # Environment call (trap/syscall)
ebreak              # Debugger breakpoint

# Return from function
ret                 # Pseudo-instruction: jalr x0, 0(ra)
nop                 # No operation (addi x0, x0, 0)
```

---

## Addressing Modes

### Immediate Addressing

Direct use of 12-bit constant.

```risc-v
addi x1, x1, 5      # x1 = x1 + 5
```

### Register Addressing

Operands come from registers.

```risc-v
add x1, x2, x3      # x1 = x2 + x3
```

### Register Indirect (Offset)

Address computed as register + offset.

```risc-v
lw x1, 0(x2)        # x1 = *x2
lw x1, 8(x2)        # x1 = *(x2 + 8)
sw x1, -4(x2)       # *(x2 - 4) = x1
```

### PC-Relative

Address relative to program counter.

```risc-v
beq x1, x2, label   # Jump relative to PC
jal x1, label       # Jump to label, save PC+4 in x1
```

### Global Addressing (via lui + addi)

```risc-v
lui x1, %hi(symbol) # Load upper 20 bits
addi x1, x1, %lo(symbol) # Add lower 12 bits
lw x2, 0(x1)        # Load from global symbol
```

---

## Calling Conventions

### RISC-V ILP32 ABI

Function calling follows a standard convention.

### Argument Passing

- **a0-a7** (x10-x17): First 8 integer arguments
- **Stack**: Additional arguments pushed on stack

```risc-v
# Function: int add3(int a, int b, int c)
# Called as: add3(1, 2, 3)

# At call site:
addi a0, x0, 1      # a0 = 1
addi a1, x0, 2      # a1 = 2
addi a2, x0, 3      # a2 = 3
jal ra, add3        # Call function

# In function:
add3:
    add a0, a0, a1  # a0 = a0 + a1
    add a0, a0, a2  # a0 = a0 + a2
    jalr x0, 0(ra)  # Return
```

### Return Value

- **a0-a1** (x10-x11): Return value (32-bit in a0, or 64-bit in a0:a1)

### Caller-Saved vs Callee-Saved

**Caller-Saved** (function can destroy):
- t0-t6 (x5-x7, x28-x31): Temporaries
- a0-a7 (x10-x17): Arguments and return value

**Callee-Saved** (function must preserve):
- s0-s11 (x8-x9, x18-x27): Saved registers
- sp (x2): Stack pointer
- ra (x1): Must preserve if calling other functions

### Stack Frame

```
    Caller's Stack Frame
    
    sp + n-4:  Parameter 8
    ...
    sp + 0:    Parameter 9+
    
    <-- ra saves return address here if needed
    <-- Function's local variables here
    <-- Callee-saved registers saved here
    
    <-- sp points here at end of prologue
```

### Function Prologue and Epilogue

```risc-v
# Prologue (save callee-saved registers, set up stack)
my_function:
    addi sp, sp, -16    # Allocate 16 bytes on stack
    sw ra, 12(sp)       # Save return address
    sw s0, 8(sp)        # Save saved register
    # Function body here...
    
    # Epilogue (restore registers, return)
    lw s0, 8(sp)        # Restore saved register
    lw ra, 12(sp)       # Restore return address
    addi sp, sp, 16     # Deallocate stack
    jalr x0, 0(ra)      # Return
```

---

## Control Flow

### Conditional Branches

```risc-v
# If x1 == 0, jump to zero_handler
beq x1, x0, zero_handler
# continue here...

# If x1 != x2, jump to not_equal
bne x1, x2, not_equal
# continue here...

# If x1 < 5, jump to less_than_5
slti t0, x1, 5      # t0 = (x1 < 5) ? 1 : 0
bne t0, x0, less_than_5
# continue here...
```

### Loops

```risc-v
# Loop: print x1 times
    addi x2, x0, 10     # x2 = 10 (counter)
loop:
    # Body of loop (do something)
    addi x2, x2, -1     # Decrement counter
    bne x2, x0, loop    # Jump back if counter != 0
# Loop ends here
```

### Switch-like Behavior

```risc-v
# Switch on x1 (values 0-3)
    addi t0, x1, -0     # Check if x1 == 0
    beq t0, x0, case_0
    addi t0, x1, -1     # Check if x1 == 1
    beq t0, x0, case_1
    addi t0, x1, -2     # Check if x1 == 2
    beq t0, x0, case_2
    # Default case
    addi x10, x0, -1    # Return -1
    jalr x0, 0(ra)

case_0:
    addi x10, x0, 0     # Return 0
    jalr x0, 0(ra)

case_1:
    addi x10, x0, 1     # Return 1
    jalr x0, 0(ra)

case_2:
    addi x10, x0, 2     # Return 2
    jalr x0, 0(ra)
```

---

## Memory and Data

### Data Sections

```risc-v
.data                   # Data section
counter: .word 0        # 32-bit word initialized to 0
name: .string "Hello"   # String in memory

.bss                    # Uninitialized data
buffer: .skip 1024      # Reserve 1024 bytes

.text                   # Code section
.globl main             # Make main visible globally
main:
    # Code here...
```

### Global Variables

```risc-v
.data
x: .word 42             # Global variable x = 42

.text
.globl main
main:
    la x1, x            # Load address of x into x1
    lw x2, 0(x1)        # Load value of x into x2 (x2 = 42)
    
    li x3, 100          # x3 = 100
    sw x3, 0(x1)        # Store 100 into x (x = 100)
    
    jalr x0, 0(ra)      # Return
```

### Arrays

```risc-v
.data
arr: .word 10, 20, 30, 40, 50  # Array of 5 integers

.text
main:
    la x1, arr          # x1 = address of array
    
    lw x2, 0(x1)        # x2 = arr[0] = 10
    lw x2, 4(x1)        # x2 = arr[1] = 20
    lw x2, 8(x1)        # x2 = arr[2] = 30
    
    # Loop through array
    li x2, 5            # x2 = array length
    addi x3, x1, 0      # x3 = pointer to current element
    li x4, 0            # x4 = accumulator (sum)

sum_loop:
    beq x2, x0, sum_done
    lw x5, 0(x3)        # x5 = *x3
    add x4, x4, x5      # x4 += x5
    addi x3, x3, 4      # x3 += 4 (next element)
    addi x2, x2, -1     # x2--
    jal x0, sum_loop
sum_done:
    # x4 now contains sum of array
```

### Strings

```risc-v
.data
msg: .string "Hello, RISC-V!"

.text
print_string:
    # x1 = address of string
    addi x2, x0, 0      # x2 = index
loop:
    lb x3, 0(x1)        # x3 = *x1 (load byte)
    beq x3, x0, done    # If null terminator, done
    
    # Send x3 to UART (assuming 0x10010000 is UART)
    li x4, 0x10010000   # x4 = UART address
    sw x3, 0(x4)        # Write to UART
    
    addi x1, x1, 1      # x1++ (next character)
    jal x0, loop
done:
    jalr x0, 0(ra)      # Return
```

---

## Centurion: From C to Assembly

### Simple C Function

```c
// C code
int factorial(int n) {
    if (n <= 1)
        return 1;
    else
        return n * factorial(n - 1);
}
```

### Equivalent RISC-V Assembly

```risc-v
# Factorial function
# Arguments: a0 = n
# Return: a0 = factorial(n)

factorial:
    # Check if n <= 1
    slti t0, a0, 2      # t0 = (n < 2) ? 1 : 0
    bne t0, x0, return_one
    
    # Recursive case: n > 1
    # Save n on stack and prepare to call recursively
    addi sp, sp, -8     # Allocate 8 bytes
    sw ra, 4(sp)        # Save return address
    sw a0, 0(sp)        # Save n
    
    # Call factorial(n - 1)
    addi a0, a0, -1     # a0 = n - 1
    jal ra, factorial
    
    # Multiply n * factorial(n-1)
    lw t0, 0(sp)        # t0 = n
    mul a0, a0, t0      # a0 *= n (if RV32M available)
    
    # Restore and return
    lw ra, 4(sp)        # Restore return address
    addi sp, sp, 8      # Deallocate stack
    jalr x0, 0(ra)      # Return
    
return_one:
    li a0, 1            # a0 = 1
    jalr x0, 0(ra)      # Return
```

### C Array Access

```c
// C code
int sum_array(int *arr, int len) {
    int sum = 0;
    for (int i = 0; i < len; i++) {
        sum += arr[i];
    }
    return sum;
}
```

### Equivalent RISC-V Assembly

```risc-v
# sum_array(arr, len)
# a0 = address of array
# a1 = length
# return: a0 = sum

sum_array:
    li a2, 0            # a2 = sum = 0
    li a3, 0            # a3 = i = 0
    
loop:
    bge a3, a1, done    # if (i >= len) exit
    
    # sum += arr[i]
    # Calculate address: a0 + i*4
    sll t0, a3, 2       # t0 = i * 4
    add t0, a0, t0      # t0 = &arr[i]
    lw t0, 0(t0)        # t0 = arr[i]
    add a2, a2, t0      # sum += arr[i]
    
    addi a3, a3, 1      # i++
    jal x0, loop
    
done:
    mv a0, a2           # a0 = sum
    jalr x0, 0(ra)      # Return
```

### Bootloader Example

The Centurion bootrom loads a program via UART into memory and jumps to it.

```risc-v
.text
.globl _start

_start:
    # Initialize stack pointer
    li sp, 0x80010000   # 64KB RAM end
    
    # Load program from UART into RAM
    li a0, 0x80000000   # RAM base address
    li a1, 0            # Byte counter
    li a2, 65536        # Max program size
    
load_loop:
    bge a1, a2, load_done
    
    # Read byte from UART (address 0x10000000)
    li a3, 0x10000000   # UART address
    lw a4, 0(a3)        # Read from UART
    
    # Check if valid (has data in lower 8 bits)
    andi a4, a4, 0xFF   # Extract byte
    
    # Store to RAM
    add a5, a0, a1      # Address = base + offset
    sb a4, 0(a5)        # Store byte
    
    addi a1, a1, 1      # Increment counter
    jal x0, load_loop
    
load_done:
    # Jump to loaded program
    li ra, 0x80000000   # Set return address to program start
    jalr x0, 0(ra)      # Jump
```

---

## Common Patterns

### Save and Restore Registers

```risc-v
# Function that calls other functions
complicated_task:
    addi sp, sp, -32
    sw ra, 28(sp)       # Save return address
    sw s0, 24(sp)       # Save callee-saved register
    sw s1, 20(sp)
    
    # Function body
    li s0, 100          # Use s0
    jal ra, other_func  # Call other function
    
    # Restore registers
    lw s1, 20(sp)
    lw s0, 24(sp)
    lw ra, 28(sp)
    addi sp, sp, 32
    jalr x0, 0(ra)
```

### 32-Bit Immediate (using lui + addi)

```risc-v
# Load 32-bit value into register
# Value: 0x12345678

lui t0, 0x12345       # t0 = 0x12345000
addi t0, t0, 0x678    # t0 += 0x678 = 0x12345678
```

### Memory Copy Loop

```risc-v
# Copy len bytes from src to dest
# a0 = dest, a1 = src, a2 = len

memcpy:
    li a3, 0            # counter = 0
copy_loop:
    bge a3, a2, copy_done
    
    lb t0, 0(a1)        # t0 = *src
    sb t0, 0(a0)        # *dest = t0
    
    addi a0, a0, 1      # dest++
    addi a1, a1, 1      # src++
    addi a3, a3, 1      # counter++
    
    jal x0, copy_loop
    
copy_done:
    jalr x0, 0(ra)
```

---

## Summary

RISC-V assembly is:
- **Simple**: ~47 instructions for RV32I
- **Regular**: Consistent instruction formats
- **Elegant**: Clean separation of concerns

Centurion uses RISC-V because:
1. Open standard (no licensing)
2. Easy to understand and implement
3. Sufficient for full system (OS, applications)
4. Educational value
5. Modern architecture (unlike MIPS or ARM from 1990s)

Key points to remember:
- Registers are your only fast storage
- Memory operations (load/store) are separate from arithmetic
- Calling conventions enable function interoperability
- Assembly is what your C compiler generates
- Understanding assembly helps debug and optimize code
