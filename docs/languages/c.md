# C: The Language of Operating Systems

C is used throughout Centurion for the bootloader, kernel, libc (standard library), and user programs. It's a simple but powerful language that compiles directly to RISC-V assembly.

## Table of Contents
1. [C Fundamentals](#c-fundamentals)
2. [Data Types](#data-types)
3. [Variables and Scope](#variables-and-scope)
4. [Operators](#operators)
5. [Control Flow](#control-flow)
6. [Functions](#functions)
7. [Pointers and Memory](#pointers-and-memory)
8. [Arrays and Strings](#arrays-and-strings)
9. [Structures](#structures)
10. [File I/O](#file-io)
11. [Centurion: Building Systems with C](#centurion-building-systems-with-c)

---

## C Fundamentals

### What is C?

C is a low-level, procedural language that:
- Compiles to efficient machine code
- Provides direct memory access via pointers
- Has minimal runtime overhead
- Enables writing both high-level and low-level code

### Why C for Centurion?

1. **Efficiency**: Minimal overhead, suitable for kernels and bootloaders
2. **Portability**: Easy to compile to different ISAs (RISC-V, ARM, x86)
3. **Simplicity**: ~35 keywords, easy to understand
4. **Control**: Direct access to memory and hardware registers
5. **Ubiquity**: Unix, Linux, Windows kernels are written in C

### Hello World

```c
#include <stdio.h>

int main() {
    printf("Hello, World!\n");
    return 0;
}
```

Compile and run:
```bash
gcc hello.c -o hello
./hello
```

---

## Data Types

### Primitive Types

```c
// Integer types
int x = 42;           // 32-bit signed integer
unsigned int y = 100; // 32-bit unsigned integer
short s = 10;         // 16-bit signed integer
unsigned short us = 20; // 16-bit unsigned integer
long l = 1000000;     // 32-bit or 64-bit signed integer
unsigned long ul = 2000000; // Unsigned version

// Character type
char c = 'A';         // 8-bit, can be signed or unsigned
unsigned char uc = 255;

// Boolean (in C99+)
#include <stdbool.h>
bool flag = true;

// Floating point (usually avoided in Centurion kernel)
float f = 3.14f;      // 32-bit floating point
double d = 2.71828;   // 64-bit floating point
```

### Type Sizes

```c
#include <stdio.h>
#include <limits.h>

int main() {
    printf("Size of int: %zu bytes\n", sizeof(int));    // Typically 4
    printf("Size of long: %zu bytes\n", sizeof(long));  // 4 or 8
    printf("Size of char: %zu bytes\n", sizeof(char));  // 1
    printf("INT_MAX: %d\n", INT_MAX);     // 2147483647
    printf("INT_MIN: %d\n", INT_MIN);     // -2147483648
    return 0;
}
```

### Type Conversion

```c
int x = 42;
float f = (float)x;    // Explicit cast to float

int a = 10, b = 3;
float quotient = (float)a / b;  // Cast to float for proper division (3.333...)
// vs.
int int_quotient = a / b;       // Integer division (3)

char ch = 65;
int ascii = ch;        // Implicit conversion: ascii = 65

unsigned int u = (unsigned int)-1;  // -1 as unsigned = 2^32 - 1 = 4294967295
```

---

## Variables and Scope

### Declaration and Initialization

```c
int x;                 // Declare, uninitialized (dangerous!)
int y = 5;             // Declare and initialize
int a, b, c;           // Multiple declarations
int d = 10, e = 20;    // Multiple declarations with initialization

const int MAX = 100;   // Constant (cannot change)
volatile int hw_reg;   // Volatile (value can change unexpectedly, don't optimize)
static int counter;    // Static: initializes to 0, persists between calls
```

### Scope

```c
int global = 100;      // Global scope

void function1() {
    int local = 50;    // Local scope (visible only in this function)
    {
        int block_local = 25;  // Even more local (this block)
        // block_local visible here
    }
    // block_local not visible here
    
    // local visible here
}

// global visible anywhere

void function2() {
    // global visible here
    // local and block_local NOT visible here
}
```

---

## Operators

### Arithmetic

```c
int a = 10, b = 3;

int sum = a + b;       // 13
int diff = a - b;      // 7
int prod = a * b;      // 30
int quotient = a / b;  // 3 (integer division)
int remainder = a % b; // 1 (modulo)
int power = a * a;     // 100 (no power operator, use multiplication)

// Increment and decrement
int x = 5;
x++;                   // x = 6
x--;                   // x = 5
++x;                   // x = 6 (prefix, returns new value)
int y = x++;           // y = 6, x = 7 (postfix, returns old value)
```

### Comparison

```c
int a = 10, b = 5;

a == b;                // false
a != b;                // true
a < b;                 // false
a > b;                 // true
a <= b;                // false
a >= b;                // true
```

### Logical

```c
int a = 1, b = 0;

a && b;                // false (AND)
a || b;                // true (OR)
!a;                    // false (NOT)

if (a > 0 && b == 0) { // true && true = true
    printf("Both conditions met\n");
}
```

### Bitwise

```c
int a = 0b1100;        // 12
int b = 0b1010;        // 10

a & b;                 // 0b1000 = 8 (AND)
a | b;                 // 0b1110 = 14 (OR)
a ^ b;                 // 0b0110 = 6 (XOR)
~a;                    // Bitwise NOT (inverts all bits)
a << 2;                // 0b110000 = 48 (shift left by 2)
a >> 1;                // 0b0110 = 6 (shift right by 1)

// Setting, clearing, and toggling bits
#define BIT0 1
#define BIT1 2

int flags = 0;
flags |= BIT0;         // Set BIT0
flags &= ~BIT1;        // Clear BIT1
flags ^= BIT0;         // Toggle BIT0
if (flags & BIT1) {    // Check if BIT1 is set
    printf("Bit 1 is set\n");
}
```

### Ternary Operator

```c
int age = 20;
char *status = (age >= 18) ? "Adult" : "Minor";
// "Adult"

int x = 5;
int abs_x = (x < 0) ? -x : x;
```

### Assignment Operators

```c
int x = 10;
x += 5;                // x = x + 5 = 15
x -= 3;                // x = x - 3 = 12
x *= 2;                // x = x * 2 = 24
x /= 4;                // x = x / 4 = 6
x %= 3;                // x = x % 3 = 0
x |= 0x0F;             // x = x | 0x0F (bitwise OR)
x &= 0xF0;             // x = x & 0xF0 (bitwise AND)
```

---

## Control Flow

### if, else if, else

```c
int x = 15;

if (x < 0) {
    printf("Negative\n");
} else if (x == 0) {
    printf("Zero\n");
} else if (x < 10) {
    printf("Small positive\n");
} else {
    printf("Large positive\n");
}

// Single statement doesn't need braces
if (x > 0)
    printf("Positive\n");
```

### switch Statement

```c
int choice = 2;

switch (choice) {
    case 1:
        printf("Choice 1\n");
        break;       // Exit switch
    case 2:
        printf("Choice 2\n");
        break;
    case 3:
        printf("Choice 3\n");
        // Fall through to default
    default:
        printf("Invalid choice\n");
}
```

### while Loop

```c
int i = 0;

while (i < 5) {
    printf("%d\n", i);
    i++;
}

// do-while: runs at least once
do {
    printf("This runs\n");
} while (0);  // Condition is false, but body ran once
```

### for Loop

```c
// Standard for loop
for (int i = 0; i < 5; i++) {
    printf("%d\n", i);
}

// Without some parts
for (;;) {              // Infinite loop
    printf("Forever\n");
    break;              // Exit
}

// Multiple initializers/increments
for (int i = 0, j = 9; i < 5; i++, j--) {
    printf("%d, %d\n", i, j);
}
```

### break and continue

```c
for (int i = 0; i < 10; i++) {
    if (i == 3)
        continue;       // Skip to next iteration
    if (i == 7)
        break;          // Exit loop
    printf("%d\n", i);  // Prints 0, 1, 2, 4, 5, 6
}
```

---

## Functions

### Function Definition

```c
// Return type: int
// Name: add
// Parameters: int a, int b
int add(int a, int b) {
    return a + b;
}

// No parameters
void print_hello() {
    printf("Hello!\n");
}

// No return value
void set_flag(int value) {
    global_flag = value;
}

// Forward declaration (function prototype)
int multiply(int a, int b);  // Tell compiler function exists

void caller() {
    int result = multiply(3, 4);  // Can use multiply now
}

// Function definition
int multiply(int a, int b) {
    return a * b;
}
```

### Function Calls

```c
int result = add(5, 3);        // Positional arguments
result = add(a, b);

void print_twice(const char *str) {
    printf("%s\n", str);
    printf("%s\n", str);
}

print_twice("Hello");          // Call with string literal
char buffer[100];
print_twice(buffer);           // Call with array
```

### Variable Arguments

```c
// Printf-like functions (variadic)
#include <stdarg.h>

int sum_all(int count, ...) {
    va_list args;
    va_start(args, count);
    
    int total = 0;
    for (int i = 0; i < count; i++) {
        total += va_arg(args, int);  // Get next argument as int
    }
    
    va_end(args);
    return total;
}

// Usage
int result = sum_all(3, 10, 20, 30);  // count=3, then 3 integers
// result = 60
```

### Recursion

```c
int factorial(int n) {
    if (n <= 1)
        return 1;
    return n * factorial(n - 1);
}

// Fibonacci (inefficient due to redundant calls)
int fib(int n) {
    if (n <= 1)
        return n;
    return fib(n - 1) + fib(n - 2);
}

// Better: tail recursion (compiler may optimize to loop)
int factorial_tail(int n, int acc) {
    if (n <= 1)
        return acc;
    return factorial_tail(n - 1, n * acc);
}

// Usage
int result = factorial_tail(5, 1);  // acc=1 initially
```

---

## Pointers and Memory

### Pointer Basics

```c
int x = 42;
int *ptr = &x;         // ptr = address of x

printf("%d\n", x);     // 42
printf("%d\n", *ptr);  // 42 (dereference)
printf("%p\n", ptr);   // Memory address (e.g., 0x7fff5fbf8ac8)

*ptr = 100;            // Change x through pointer
printf("%d\n", x);     // 100
```

### Pointer Arithmetic

```c
int arr[] = {10, 20, 30, 40, 50};
int *ptr = arr;        // ptr points to arr[0]

printf("%d\n", *ptr);          // 10
printf("%d\n", *(ptr + 1));    // 20
printf("%d\n", *(ptr + 2));    // 30

ptr++;                 // Move to next element
printf("%d\n", *ptr);  // 20

ptr--;                 // Move to previous element
printf("%d\n", *ptr);  // 10

int *ptr2 = &arr[3];
printf("%d\n", ptr2 - ptr);  // 3 (difference in elements, not bytes)
```

### Dynamic Memory

```c
#include <stdlib.h>

// Allocate 100 bytes
int *buffer = (int *)malloc(100);
if (buffer == NULL) {
    printf("Memory allocation failed\n");
    return;
}

// Use buffer
buffer[0] = 42;
buffer[1] = 50;

// Free memory
free(buffer);
buffer = NULL;         // Good practice

// Allocate and initialize
int *arr = (int *)calloc(10, sizeof(int));  // 10 ints, all zero
if (arr == NULL) return;

// Reallocate
int *larger = (int *)realloc(arr, 20 * sizeof(int));
if (larger == NULL) {
    free(arr);
    return;
}
arr = larger;

free(arr);
```

### Pointer to Pointer

```c
int x = 42;
int *ptr = &x;         // ptr points to x
int **ptr_ptr = &ptr;  // ptr_ptr points to ptr

printf("%d\n", **ptr_ptr);  // 42
```

### Void Pointer

```c
void *generic_ptr;     // Can point to any type

int x = 42;
generic_ptr = &x;
printf("%d\n", *(int *)generic_ptr);  // Cast to int* to dereference

char c = 'A';
generic_ptr = &c;
printf("%c\n", *(char *)generic_ptr); // Cast to char*
```

### Function Pointers

```c
// Function that takes two ints and returns int
int add(int a, int b) { return a + b; }
int subtract(int a, int b) { return a - b; }

// Pointer to function
int (*op)(int, int);
op = add;
printf("%d\n", op(10, 3));  // 13

op = subtract;
printf("%d\n", op(10, 3));  // 7

// Array of function pointers
int (*operations[2])(int, int) = {add, subtract};
printf("%d\n", operations[0](10, 3));  // 13
printf("%d\n", operations[1](10, 3));  // 7
```

---

## Arrays and Strings

### Arrays

```c
// Fixed-size array
int numbers[5];                // Uninitialized
int values[3] = {10, 20, 30};  // Initialized
int arr[] = {1, 2, 3, 4, 5};   // Size inferred from initialization

// Access elements
numbers[0] = 100;
printf("%d\n", numbers[0]);    // 100

// Arrays decay to pointers
int *ptr = numbers;            // ptr = &numbers[0]
printf("%d\n", ptr[0]);        // 100
printf("%d\n", *ptr);          // 100
printf("%d\n", *(ptr + 1));    // numbers[1]

// Length of array (only works for static arrays!)
int len = sizeof(arr) / sizeof(arr[0]);  // 5

// 2D arrays
int matrix[3][4];              // 3x4 matrix
matrix[0][0] = 1;
matrix[1][2] = 5;

// Iterate
for (int i = 0; i < 3; i++) {
    for (int j = 0; j < 4; j++) {
        matrix[i][j] = i * 4 + j;
    }
}
```

### Strings

```c
// String literal (null-terminated)
const char *msg = "Hello";
printf("%s\n", msg);           // Hello
printf("%c\n", msg[0]);        // H
printf("%c\n", msg[4]);        // o
printf("%c\n", msg[5]);        // \0 (null terminator)

// String array
char str[20];                  // Can hold up to 19 characters + null terminator
strcpy(str, "Hello");          // Copy string (unsafe!)
printf("%s\n", str);           // Hello

// Safer: strncpy
char buffer[20];
strncpy(buffer, "World", sizeof(buffer) - 1);
buffer[sizeof(buffer) - 1] = '\0';

// String operations
#include <string.h>

char s1[] = "Hello";
char s2[] = "World";

strlen(s1);                    // 5
strcmp(s1, s2);                // Non-zero (not equal)
strcpy(s1, s2);                // Copy s2 to s1
strcat(s1, " and ");           // Concatenate (unsafe!)
strncat(s1, s2, 20);           // Safer: concatenate with limit

// Find character
char *ptr = strchr("Hello", 'l');  // Find 'l'
// ptr = &"Hello"[2]

// Find substring
char *substr = strstr("Hello World", "Wor");  // Find "Wor"
```

---

## Structures

### Structure Definition

```c
struct Point {
    int x;
    int y;
};

struct Rectangle {
    struct Point top_left;
    struct Point bottom_right;
    int color;
};

// Typedef for convenience
typedef struct {
    int x;
    int y;
} Point;

// Typedef with same name as struct
typedef struct Node {
    int data;
    struct Node *next;  // Must use "struct Node" for recursive reference
} Node;
```

### Using Structures

```c
struct Point p;
p.x = 10;
p.y = 20;

struct Point p2 = {30, 40};  // Initializer list
struct Point p3 = {.x = 50, .y = 60};  // Designated initializers

// Via pointer
struct Point *ptr = &p;
printf("%d\n", ptr->x);      // Arrow operator
printf("%d\n", (*ptr).x);    // Equivalent

// Arrays of structures
struct Point path[10];
path[0].x = 0;
path[0].y = 0;
path[1].x = 10;
path[1].y = 10;
```

### Nested Structures

```c
struct Address {
    char street[100];
    char city[50];
    int zip;
};

struct Person {
    char name[50];
    int age;
    struct Address address;
};

struct Person bob = {
    "Bob Smith",
    30,
    {"123 Main St", "Springfield", 12345}
};

printf("%s\n", bob.address.city);  // Springfield
```

---

## File I/O

### File Operations

```c
#include <stdio.h>

// Open file
FILE *file = fopen("data.txt", "r");  // "r" = read
if (file == NULL) {
    printf("Error opening file\n");
    return;
}

// Read line by line
char buffer[100];
while (fgets(buffer, sizeof(buffer), file) != NULL) {
    printf("%s", buffer);
}

// Close file
fclose(file);

// Write to file
file = fopen("output.txt", "w");  // "w" = write
fprintf(file, "Hello, File!\n");
fprintf(file, "Number: %d\n", 42);
fclose(file);

// Append to file
file = fopen("output.txt", "a");  // "a" = append
fprintf(file, "More data\n");
fclose(file);
```

### Binary File I/O

```c
// Write binary data
FILE *file = fopen("data.bin", "wb");
int data[] = {1, 2, 3, 4, 5};
fwrite(data, sizeof(int), 5, file);
fclose(file);

// Read binary data
file = fopen("data.bin", "rb");
int buffer[5];
fread(buffer, sizeof(int), 5, file);
for (int i = 0; i < 5; i++) {
    printf("%d\n", buffer[i]);
}
fclose(file);
```

---

## Centurion: Building Systems with C

### Bootloader

The bootloader initializes hardware and loads the kernel.

```c
// bootloader.c
#include "uart.h"
#include "memory.h"

#define KERNEL_BASE 0x80010000
#define KERNEL_MAX_SIZE 1048576  // 1MB

void bootloader_main() {
    // Initialize UART for console
    uart_init(115200);
    uart_puts("Bootloader started\n");
    
    // Load kernel from UART
    uart_puts("Loading kernel...\n");
    unsigned char *kernel = (unsigned char *)KERNEL_BASE;
    
    for (int i = 0; i < KERNEL_MAX_SIZE; i++) {
        int byte = uart_getc();
        if (byte < 0) break;  // No more data
        
        kernel[i] = (unsigned char)byte;
        
        if ((i + 1) % 1024 == 0) {
            uart_puts(".");
        }
    }
    
    uart_puts("\nKernel loaded successfully\n");
    uart_puts("Jumping to kernel...\n");
    
    // Jump to kernel entry point
    void (*kernel_entry)(void) = (void (*)(void))KERNEL_BASE;
    kernel_entry();
    
    // Should not return
    while (1) {
        uart_puts("Error: kernel returned\n");
    }
}
```

### UART Driver

```c
// uart.c
#define UART_BASE 0x10000000
#define UART_TXDATA   0x00
#define UART_RXDATA   0x04
#define UART_TXCTRL   0x08
#define UART_RXCTRL   0x0c
#define UART_IE       0x10
#define UART_IP       0x14
#define UART_DIV      0x18

typedef struct {
    unsigned int addr;
} uart_t;

uart_t uart0 = {UART_BASE};

void uart_init(int baud) {
    unsigned int div = (50000000 / baud) - 1;
    *(unsigned int *)(uart0.addr + UART_DIV) = div;
    
    // Enable transmit and receive
    *(unsigned int *)(uart0.addr + UART_TXCTRL) = 1;
    *(unsigned int *)(uart0.addr + UART_RXCTRL) = 1;
}

void uart_putc(char c) {
    *(unsigned char *)(uart0.addr + UART_TXDATA) = c;
    
    // Wait for transmission complete
    while ((*(unsigned int *)(uart0.addr + UART_TXCTRL) & 0x80000000) == 0) {
        // Busy wait
    }
}

int uart_getc(void) {
    unsigned int rxdata = *(unsigned int *)(uart0.addr + UART_RXDATA);
    if (rxdata & 0x80000000) {  // Valid bit set
        return rxdata & 0xFF;
    }
    return -1;  // No data available
}

void uart_puts(const char *str) {
    while (*str) {
        uart_putc(*str++);
    }
}
```

### Memory Management

```c
// malloc.c - Simple memory allocator for kernel
#define HEAP_SIZE 65536
static unsigned char heap[HEAP_SIZE];
static unsigned char *heap_top = heap;

void *malloc(unsigned int size) {
    if (heap_top + size > heap + HEAP_SIZE) {
        return NULL;  // Out of memory
    }
    
    void *ptr = heap_top;
    heap_top += size;
    return ptr;
}

void free(void *ptr) {
    // Simple allocator: cannot free (but kernel typically doesn't need to)
    (void)ptr;  // Suppress unused warning
}

void *memcpy(void *dest, const void *src, unsigned int n) {
    unsigned char *d = (unsigned char *)dest;
    const unsigned char *s = (const unsigned char *)src;
    
    for (unsigned int i = 0; i < n; i++) {
        d[i] = s[i];
    }
    
    return dest;
}

void *memset(void *s, int c, unsigned int n) {
    unsigned char *ptr = (unsigned char *)s;
    
    for (unsigned int i = 0; i < n; i++) {
        ptr[i] = (unsigned char)c;
    }
    
    return s;
}
```

### Simple Kernel Entry

```c
// kernel.c - Minimal OS kernel
#include "uart.h"
#include "memory.h"

void kernel_main() {
    uart_puts("Centurion OS\n");
    uart_puts("============\n\n");
    
    uart_puts("Starting kernel initialization...\n");
    
    // Initialize various subsystems
    uart_puts("- Initializing memory manager\n");
    // init_memory();
    
    uart_puts("- Initializing process manager\n");
    // init_processes();
    
    uart_puts("- Initializing filesystem\n");
    // init_filesystem();
    
    uart_puts("\nKernel ready. Type 'help' for commands.\n");
    
    // Main command loop
    char buffer[100];
    while (1) {
        uart_puts("$ ");
        
        // Read command from UART
        int i = 0;
        while (i < sizeof(buffer) - 1) {
            int c = uart_getc();
            if (c < 0) continue;
            
            if (c == '\r' || c == '\n') {
                buffer[i] = '\0';
                uart_putc('\n');
                break;
            } else if (c == 8 || c == 127) {  // Backspace
                if (i > 0) {
                    i--;
                    uart_puts("\b \b");
                }
            } else {
                buffer[i++] = c;
                uart_putc(c);
            }
        }
        
        // Process command
        if (buffer[0] == 'h' && buffer[1] == 'e') {
            uart_puts("Commands: help, echo, stat, reboot\n");
        } else if (buffer[0] == 'e' && buffer[1] == 'c') {
            uart_puts("Echo: ");
            uart_puts(&buffer[5]);
            uart_putc('\n');
        } else if (buffer[0] == 's' && buffer[1] == 't') {
            uart_puts("System stats:\n");
            uart_puts("- CPU: RISC-V RV32I\n");
            uart_puts("- RAM: 64KB\n");
        } else if (buffer[0] != '\0') {
            uart_puts("Unknown command\n");
        }
    }
}
```

---

## Best Practices

1. **Check return values**: `malloc`, `fopen`, etc. can fail
2. **Initialize variables**: Uninitialized variables contain garbage
3. **Limit scope**: Use local variables, minimize global state
4. **Const-correctness**: Mark read-only parameters with `const`
5. **Safe string handling**: Use `strncpy` instead of `strcpy`
6. **Free memory**: Every `malloc` needs a `free`
7. **Use `typedef`**: Simplifies structure names
8. **Function prototypes**: Declare before use
9. **Comments**: Explain the "why", not the "what"
10. **Test edge cases**: Empty arrays, NULL pointers, large values

---

## Useful C Functions

```c
// String functions
strlen, strcpy, strncpy, strcat, strncat, strcmp, strncmp
strchr, strstr, strtok
toupper, tolower

// Memory functions
malloc, calloc, realloc, free
memcpy, memmove, memset, memcmp

// I/O functions
printf, fprintf, sprintf
gets, fgets, scanf, fscanf
fopen, fclose, fread, fwrite

// Utility
rand, srand
abs, labs, atoi, atol, strtol
qsort, bsearch
```

---

## Summary

C is ideal for systems programming because:
- **Efficiency**: Minimal overhead, tight control
- **Simplicity**: Easy to understand what it does
- **Portability**: Compiles to any architecture
- **Direct hardware access**: Pointers enable register/memory manipulation
- **Minimal runtime**: No garbage collector or virtual machine

Centurion uses C for:
1. **Bootloader**: Initialize hardware, load kernel
2. **Kernel**: Process management, memory management, syscalls
3. **libc**: Standard library functions (`printf`, `malloc`, string ops)
4. **User programs**: Applications running on the OS

The Centurion C compiler (written in Haskell) compiles C to RISC-V assembly, which the assembler (Python) converts to machine code.
