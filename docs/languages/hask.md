# Haskell: A Language for Compiler Construction

Haskell is a pure functional programming language used in Centurion to build the C compiler (~2000 lines). Its strong type system and pattern matching make it ideal for compiler implementation.

## Table of Contents
1. [Functional Programming Concepts](#functional-programming-concepts)
2. [Basic Syntax](#basic-syntax)
3. [Types and Type System](#types-and-type-system)
4. [Pattern Matching](#pattern-matching)
5. [Lists and Recursion](#lists-and-recursion)
6. [Higher-Order Functions](#higher-order-functions)
7. [Monads and I/O](#monads-and-io)
8. [Data Structures](#data-structures)
9. [Building a C Compiler](#building-a-c-compiler)

---

## Functional Programming Concepts

### What is Functional Programming?

In Haskell, functions are first-class values. Programming is about **composing functions**, not modifying state.

| Imperative | Functional |
|-----------|-----------|
| `x = 0; while (x < 5) { print(x); x = x + 1; }` | `map print [0..4]` |
| Variables are mutable boxes | Values are immutable |
| State changes over time | Functions transform data |
| Loops control flow | Recursion and higher-order functions |

### Why Haskell for Compilers?

1. **Pattern Matching**: Express syntax rules clearly
2. **Algebraic Data Types**: Model abstract syntax trees naturally
3. **Type Safety**: Catch errors at compile time
4. **Immutability**: No hidden state bugs
5. **Composability**: Build complex operations from simple ones

### Pure Functions

A pure function:
- Returns the same output for the same input
- Has no side effects (doesn't modify external state)

```haskell
-- Pure function: always returns same result
add :: Int -> Int -> Int
add a b = a + b

-- Impure function: depends on external state
import System.Random
getRandomNumber :: IO Int
getRandomNumber = randomIO
```

---

## Basic Syntax

### Function Definition

```haskell
-- Simple function
double :: Int -> Int
double x = x * 2

-- Multiple parameters
add :: Int -> Int -> Int
add x y = x + y

-- Function call
result = double 5           -- 10
result = add 3 4            -- 7

-- Anonymous function (lambda)
multiply = \x y -> x * y

-- With guards (if-like conditions)
sign :: Int -> String
sign x
  | x > 0     = "positive"
  | x < 0     = "negative"
  | otherwise = "zero"

-- Where clause (local definitions)
distances :: [Int]
distances = [d1, d2, d3]
  where
    d1 = distance 0 0
    d2 = distance 3 4
    d3 = distance 5 12

distance x y = sqrt (x^2 + y^2)
```

### Comments

```haskell
-- Single line comment

{- Multi-line comment
   spanning multiple lines
   can be nested {- like this -}
-}

-- Commonly used for function documentation
-- | Calculate the square of a number
square :: Int -> Int
square x = x * x
```

### Operators

```haskell
-- Arithmetic
5 + 3       -- 8
10 - 4      -- 6
7 * 8       -- 56
20 / 4      -- 5.0 (float division)
20 `div` 4  -- 5 (integer division)
20 `mod` 3  -- 2 (modulo)
2 ^ 10      -- 1024 (exponentiation)

-- Comparison
5 == 5      -- True
5 /= 6      -- True (not equal)
5 < 10      -- True
5 <= 5      -- True
10 > 5      -- True
10 >= 10    -- True

-- Boolean
True && True      -- True
True || False     -- True
not True          -- False

-- Function composition (powerful!)
f = negate . double  -- Compose negate and double
f 5                  -- negate (double 5) = negate 10 = -10

-- Pipe operator (for readability)
5 `double` `add` 3   -- (double 5) `add` 3
```

### Operator Precedence

```haskell
-- Precedence matters
2 + 3 * 4       -- 14, not 20 (* has higher precedence)
2 ^ 3 ^ 2       -- 512 (^ is right-associative)
```

---

## Types and Type System

### Basic Types

```haskell
-- Integer types
x :: Int           -- Fixed size: -2^31 to 2^31-1
y :: Integer       -- Arbitrary precision
z = 42             -- Type inferred as Int

-- Floating point
pi :: Float        -- 32-bit (less precise)
pi :: Double       -- 64-bit (more precise, preferred)
e = 2.71828

-- Boolean
b :: Bool
b = True           -- True or False

-- Character and String
c :: Char
c = 'A'

s :: String
s = "Hello, Haskell!"

-- Lists
xs :: [Int]
xs = [1, 2, 3, 4, 5]

-- Tuples (fixed size, mixed types)
pair :: (Int, String)
pair = (42, "answer")

triple :: (String, Int, Bool)
triple = ("name", 10, True)

-- Maybe (optional value)
mx :: Maybe Int
mx = Just 5         -- Contains value 5
nothing = Nothing   -- No value

-- Either (value or error)
result :: Either String Int
result = Right 42           -- Success case
result = Left "Error occurred"  -- Error case
```

### Type Synonyms

```haskell
-- Create alias for complex types
type Address = String
type Age = Int
type Coordinate = (Double, Double)

location :: Coordinate
location = (40.7128, -74.0060)
```

### Function Types

```haskell
-- Function type: input -> output
double :: Int -> Int

-- Multiple arguments: chained arrows
add :: Int -> Int -> Int
add x y = x + y

-- Higher-order function (function as argument/result)
applyTwice :: (a -> a) -> a -> a
applyTwice f x = f (f x)

result = applyTwice double 3  -- double (double 3) = 12

-- Polymorphic type (works with any type)
identity :: a -> a
identity x = x

-- Type class constraint (must support equality)
equal :: (Eq a) => a -> a -> Bool
equal x y = x == y
```

### Type Classes

```haskell
-- Eq: equality comparison
(==) :: (Eq a) => a -> a -> Bool
(/=) :: (Eq a) => a -> a -> Bool

-- Ord: ordering comparison
(<) :: (Ord a) => a -> a -> Bool
(<=) :: (Ord a) => a -> a -> Bool
compare :: (Ord a) => a -> a -> Ordering

-- Show: convert to string
show :: (Show a) => a -> String
show 42             -- "42"
show [1, 2, 3]      -- "[1,2,3]"

-- Read: parse from string
read :: (Read a) => String -> a
read "42" :: Int    -- 42
read "[1,2,3]" :: [Int]  -- [1,2,3]

-- Num: numeric operations
(+) :: (Num a) => a -> a -> a

-- Enum: enumerable types
[1..5]              -- [1, 2, 3, 4, 5]
[1, 3 .. 10]        -- [1, 3, 5, 7, 9]
['a'..'z']          -- "abcdefghijklmnopqrstuvwxyz"
```

---

## Pattern Matching

Pattern matching is Haskell's way to deconstruct values and handle different cases.

### Basic Pattern Matching

```haskell
-- Match on concrete values
describe :: Bool -> String
describe True = "It's true!"
describe False = "It's false!"

-- Match on number ranges (guards)
grade :: Int -> String
grade score
  | score >= 90 = "A"
  | score >= 80 = "B"
  | score >= 70 = "C"
  | otherwise = "F"

-- Catch-all pattern
first :: [a] -> a
first [] = error "Empty list"
first (x:xs) = x
```

### List Pattern Matching

```haskell
-- Match on list structure
isEmpty :: [a] -> Bool
isEmpty [] = True
isEmpty _ = False

-- Extract head and tail
listInfo :: [Int] -> String
listInfo [] = "Empty list"
listInfo [x] = "Single element: " ++ show x
listInfo (x:xs) = "First: " ++ show x ++ ", rest: " ++ show xs

-- Multiple elements
sum3 :: [Int] -> Int
sum3 [a, b, c] = a + b + c
sum3 _ = 0

-- Get nth element
nthElement :: [a] -> Int -> a
nthElement (x:_) 0 = x
nthElement (_:xs) n = nthElement xs (n - 1)
nthElement [] _ = error "Index out of bounds"
```

### Tuple Pattern Matching

```haskell
-- Extract tuple components
fst :: (a, b) -> a
fst (x, _) = x

snd :: (a, b) -> b
snd (_, y) = y

-- Multiple tuple elements
triplet :: (Int, Int, Int) -> String
triplet (0, 0, 0) = "All zeros"
triplet (x, y, z) = show x ++ ", " ++ show y ++ ", " ++ show z

-- Nested patterns
nested :: ((Int, Int), String) -> Int
nested ((x, y), _) = x + y
```

### Custom Data Type Pattern Matching

```haskell
data Color = Red | Green | Blue

colorName :: Color -> String
colorName Red = "Red"
colorName Green = "Green"
colorName Blue = "Blue"

-- With fields
data Person = Person String Int

greetPerson :: Person -> String
greetPerson (Person name age) = "Hi " ++ name ++ ", age " ++ show age

-- Recursive patterns
data BinaryTree a = Empty | Node a (BinaryTree a) (BinaryTree a)

isEmpty :: BinaryTree a -> Bool
isEmpty Empty = True
isEmpty _ = False

height :: BinaryTree a -> Int
height Empty = 0
height (Node _ left right) = 1 + max (height left) (height right)
```

---

## Lists and Recursion

### List Operations

```haskell
-- Basic list syntax
xs = [1, 2, 3, 4, 5]
ys = 1 : [2, 3, 4, 5]   -- (:) is cons operator

-- Empty list
empty = []

-- Ranges
nums = [1..10]          -- [1, 2, ..., 10]
evens = [2, 4 .. 20]    -- [2, 4, 6, ..., 20]
countdown = [5, 4 .. 1] -- [5, 4, 3, 2, 1]

-- List operations
length [1, 2, 3]        -- 3
[1, 2] ++ [3, 4]        -- [1, 2, 3, 4] (concatenation)
reverse [1, 2, 3]       -- [3, 2, 1]
head [1, 2, 3]          -- 1
tail [1, 2, 3]          -- [2, 3]
take 2 [1, 2, 3, 4]     -- [1, 2]
drop 2 [1, 2, 3, 4]     -- [3, 4]
last [1, 2, 3, 4]       -- 4
init [1, 2, 3, 4]       -- [1, 2, 3]
```

### Recursion Patterns

```haskell
-- Recursion is the primary loop mechanism
factorial :: Int -> Int
factorial 0 = 1
factorial n = n * factorial (n - 1)

-- Sum a list
sumList :: [Int] -> Int
sumList [] = 0
sumList (x:xs) = x + sumList xs

-- Length of a list
listLength :: [a] -> Int
listLength [] = 0
listLength (_:xs) = 1 + listLength xs

-- Reverse a list
reverse' :: [a] -> [a]
reverse' [] = []
reverse' (x:xs) = reverse' xs ++ [x]  -- Inefficient O(n^2)

-- Better: accumulator pattern
reverse'' :: [a] -> [a]
reverse'' xs = rev xs []
  where
    rev [] acc = acc
    rev (x:xs) acc = rev xs (x:acc)

-- Multiple recursion (Fibonacci)
fib :: Int -> Int
fib 0 = 0
fib 1 = 1
fib n = fib (n - 1) + fib (n - 2)  -- Inefficient: exponential time
```

### List Comprehensions

List comprehensions provide a concise syntax similar to set notation.

```haskell
-- Basic comprehension
squares = [x^2 | x <- [1..5]]      -- [1, 4, 9, 16, 25]

-- With filter
evens = [x | x <- [1..20], even x]  -- [2, 4, 6, ..., 20]

-- Multiple generators
pairs = [(x, y) | x <- [1..3], y <- [1..3]]
-- [(1,1), (1,2), (1,3), (2,1), (2,2), (2,3), (3,1), (3,2), (3,3)]

-- Conditional filtering
pythagorean = [(x, y, z) | x <- [1..10], y <- [1..10], z <- [1..10], 
                            x^2 + y^2 == z^2]

-- String manipulation
uppercase = [toUpper c | c <- "hello"]  -- "HELLO"
```

---

## Higher-Order Functions

### map, filter, fold

Higher-order functions take functions as arguments.

```haskell
-- map: apply function to each element
map double [1, 2, 3, 4]    -- [2, 4, 6, 8]
map (\x -> x * x) [1..5]   -- [1, 4, 9, 16, 25]

-- filter: keep elements matching condition
filter even [1..10]         -- [2, 4, 6, 8, 10]
filter (\x -> x > 5) [1..10]  -- [6, 7, 8, 9, 10]

-- fold: reduce a list to a single value
sum' = foldl (+) 0          -- Sum elements
product' = foldl (*) 1      -- Product of elements

-- foldl: left fold (process from left to right)
foldl (+) 0 [1, 2, 3, 4]    -- ((((0 + 1) + 2) + 3) + 4) = 10

-- foldr: right fold
foldr (:) [] [1, 2, 3]      -- [1, 2, 3] (reconstruct list)

-- Practical examples
product [1..5] = foldl (*) 1 [1..5]  -- 120
maximum' = foldl1 max
minimum' = foldl1 min
concat' = foldr (++) []
```

### Function Composition

```haskell
-- (.) operator: compose functions
double = \x -> x * 2
square = \x -> x * x

-- Compose double and square
doubleThenSquare = square . double
doubleThenSquare 5          -- (5 * 2)^2 = 100

-- Multiple composition
f = negate . double . (+ 1)
f 5                         -- negate (double (5 + 1)) = -12

-- Partial application
add5 = (+ 5)
double3Times = \x -> x * 2 * 2 * 2
times2and3 = (2 *) . (3 *)  -- x -> (x * 3) * 2
```

### Currying and Partial Application

```haskell
-- All functions in Haskell are curried
add :: Int -> Int -> Int
add x y = x + y

-- These are equivalent:
add 3 4          -- Apply both arguments
(add 3) 4        -- First apply 3, then apply 4

-- Partial application: create new function
add5 = add 5     -- Function that adds 5
add5 10          -- 15

-- Useful for composition
addTo [1..5] list = map (add 5) list  -- Add 5 to each element
```

---

## Monads and I/O

### The IO Monad

Haskell is pure by default, but IO actions need side effects. The `IO` monad encapsulates effects.

```haskell
-- Read from stdin
getLine :: IO String
line <- getLine

-- Write to stdout
putStrLn :: String -> IO ()
putStrLn "Hello, World!"

-- Combine IO actions
main :: IO ()
main = do
  putStrLn "What's your name?"
  name <- getLine
  putStrLn ("Hello, " ++ name ++ "!")

-- IO example: read file
import System.IO

readFile' :: FilePath -> IO String
readFile' path = do
  handle <- openFile path ReadMode
  content <- hGetContents handle
  hClose handle
  return content

-- Simpler: use library function
content <- readFile "input.txt"

-- Write file
writeFile "output.txt" "Hello, File!"

-- Append to file
appendFile "output.txt" "\nMore text"
```

### Maybe Monad

Handle optional values elegantly.

```haskell
-- Extract value from Maybe
getValue :: Maybe Int -> Int
getValue (Just x) = x
getValue Nothing = 0

-- Or with pattern matching
describe :: Maybe Int -> String
describe (Just x) = "Got " ++ show x
describe Nothing = "No value"

-- Do notation with Maybe
maybeDivide :: Int -> Int -> Maybe Int
maybeDivide a b
  | b == 0 = Nothing
  | otherwise = Just (a `div` b)

-- Chain operations
result = do
  x <- maybeDivide 10 2   -- x = Just 5
  y <- maybeDivide x 2    -- y = Just 2
  return (x + y)          -- Maybe 7

-- Or using bind operator
result = maybeDivide 10 2 >>= \x ->
         maybeDivide x 2 >>= \y ->
         return (x + y)
```

### Either Monad

Handle values with error information.

```haskell
-- Either Left (error) or Right (value)
safeDiv :: Int -> Int -> Either String Int
safeDiv _ 0 = Left "Division by zero"
safeDiv a b = Right (a `div` b)

-- Chain operations
result :: Either String Int
result = do
  x <- safeDiv 10 2
  y <- safeDiv x 0      -- Error!
  return (x + y)

-- Handle error
case result of
  Right val -> putStrLn $ "Result: " ++ show val
  Left err -> putStrLn $ "Error: " ++ err
```

---

## Data Structures

### Algebraic Data Types

```haskell
-- Simple enumeration
data Color = Red | Green | Blue
  deriving (Show, Eq)

-- With fields
data Person = Person {
  name :: String,
  age :: Int,
  email :: String
} deriving (Show, Eq)

-- Create and access
alice = Person {name = "Alice", age = 30, email = "alice@example.com"}
name alice          -- "Alice"
alice {age = 31}    -- Update age, return new Person

-- Multiple constructors
data Shape = Circle Double | Rectangle Double Double | Triangle Double Double Double

area :: Shape -> Double
area (Circle r) = pi * r ^ 2
area (Rectangle w h) = w * h
area (Triangle a b c) = sqrt (s * (s - a) * (s - b) * (s - c))
  where s = (a + b + c) / 2

-- Recursive types
data List a = Empty | Cons a (List a)

length' :: List a -> Int
length' Empty = 0
length' (Cons _ rest) = 1 + length' rest

-- Binary tree
data Tree a = Leaf a | Branch (Tree a) (Tree a)

mapTree :: (a -> b) -> Tree a -> Tree b
mapTree f (Leaf x) = Leaf (f x)
mapTree f (Branch left right) = Branch (mapTree f left) (mapTree f right)
```

---

## Building a C Compiler

### AST (Abstract Syntax Tree)

The C compiler represents C programs as data structures.

```haskell
-- Token types
data Token = TIdent String | TInt Int | TKeyword String
           | TPlus | TMinus | TStar | TSlash
           | TLParen | TRParen | TLBrace | TRBrace
           deriving (Show, Eq)

-- Abstract Syntax Tree for expressions
data Expr = IntLit Int
          | Ident String
          | BinOp String Expr Expr  -- op, left, right
          | UnOp String Expr         -- op, operand
          | Call String [Expr]       -- function name, arguments
          deriving (Show, Eq)

-- AST for statements
data Stmt = Expr Expr
          | Decl String Type
          | Assign String Expr
          | If Expr Stmt Stmt
          | While Expr Stmt
          | Compound [Stmt]
          deriving (Show, Eq)

-- Type system
data Type = TInt | TChar | TPtr Type | TVoid
          deriving (Show, Eq)

-- Top-level declarations
data Decl = FuncDecl String Type [String] Stmt
          | VarDecl String Type
          deriving (Show, Eq)

-- Program is a list of declarations
type Program = [Decl]
```

### Lexer

```haskell
import Data.Char (isDigit, isAlpha, isAlphaNum, isSpace)

-- Tokenize source code
lexer :: String -> [Token]
lexer [] = []
lexer (c:cs)
  | isSpace c = lexer cs
  | isDigit c = let (num, rest) = span isDigit (c:cs)
                in TInt (read num) : lexer rest
  | isAlpha c || c == '_' = let (ident, rest) = span isAlphaNum (c:cs)
                            in (if isKeyword ident then TKeyword ident else TIdent ident) : lexer rest
  | c == '+' = TPlus : lexer cs
  | c == '-' = TMinus : lexer cs
  | c == '*' = TStar : lexer cs
  | c == '/' = TSlash : lexer cs
  | c == '(' = TLParen : lexer cs
  | c == ')' = TRParen : lexer cs
  | c == '{' = TLBrace : lexer cs
  | c == '}' = TRBrace : lexer cs
  | otherwise = error $ "Unexpected character: " ++ [c]

isKeyword :: String -> Bool
isKeyword s = s `elem` ["if", "else", "while", "int", "void", "return"]
```

### Parser

```haskell
-- Simple recursive descent parser
data Parser a = Parser (String -> Maybe (a, String))

parseExpr :: [Token] -> Maybe (Expr, [Token])
parseExpr (TInt n : rest) = Just (IntLit n, rest)
parseExpr (TIdent name : rest) = Just (Ident name, rest)
parseExpr (TLParen : rest) = do
  (expr, rest') <- parseExpr rest
  case rest' of
    (TRParen : rest'') -> Just (expr, rest'')
    _ -> Nothing
parseExpr _ = Nothing

parseBinOp :: [Token] -> Maybe (Expr, [Token])
parseBinOp tokens = do
  (left, rest) <- parseExpr tokens
  case rest of
    (TPlus : rest') -> do
      (right, rest'') <- parseExpr rest'
      return (BinOp "+" left right, rest'')
    (TMinus : rest') -> do
      (right, rest'') <- parseExpr rest'
      return (BinOp "-" left right, rest'')
    _ -> Just (left, rest)

parseStmt :: [Token] -> Maybe (Stmt, [Token])
parseStmt tokens = do
  (expr, rest) <- parseExpr tokens
  return (Expr expr, rest)
```

### Code Generator

```haskell
-- Generate RISC-V assembly from AST
codeGen :: Expr -> String
codeGen (IntLit n) = 
  "  addi a0, zero, " ++ show n ++ "\n"

codeGen (BinOp "+" left right) =
  codeGen left ++
  "  addi sp, sp, -4\n" ++
  "  sw a0, 0(sp)\n" ++
  codeGen right ++
  "  lw t0, 0(sp)\n" ++
  "  add a0, t0, a0\n" ++
  "  addi sp, sp, 4\n"

codeGen (BinOp "-" left right) =
  codeGen left ++
  "  addi sp, sp, -4\n" ++
  "  sw a0, 0(sp)\n" ++
  codeGen right ++
  "  lw t0, 0(sp)\n" ++
  "  sub a0, t0, a0\n" ++
  "  addi sp, sp, 4\n"

codeGen (BinOp "*" left right) =
  codeGen left ++
  "  addi sp, sp, -4\n" ++
  "  sw a0, 0(sp)\n" ++
  codeGen right ++
  "  lw t0, 0(sp)\n" ++
  "  mul a0, t0, a0\n" ++
  "  addi sp, sp, 4\n"

codeGen _ = error "Unsupported expression"

-- Compile a full program
compile :: Program -> String
compile decls = unlines $
  [ ".globl main"
  , "main:"
  ] ++ map genDecl decls

genDecl :: Decl -> String
genDecl (VarDecl name _) = "  # Variable: " ++ name
genDecl (FuncDecl name _ _ body) =
  name ++ ":\n" ++ genStmt body

genStmt :: Stmt -> String
genStmt (Expr e) = codeGen e
genStmt _ = ""
```

---

## Best Practices

1. **Use pattern matching**: More readable than if-then-else
2. **Leverage type system**: Let compiler catch errors
3. **Compose functions**: Build complex operations from simple ones
4. **Avoid partial functions**: Handle edge cases with Maybe/Either
5. **Use meaningful names**: `factorial` better than `fact`
6. **Document types**: Type signatures are excellent documentation

---

## Useful Haskell Functions

```haskell
-- List processing
map, filter, foldl, foldr, scanl, scanr
take, drop, takeWhile, dropWhile
any, all, elem, find
zip, unzip, transpose
group, sort, nub

-- String processing
words, unwords
lines, unlines
intercalate, splitOn
map toLower, map toUpper

-- Type conversion
show, read
fromIntegral, toInteger
```

---

## Summary

Haskell is ideal for compiler construction because:
- **Algebraic Data Types**: Express syntax trees naturally
- **Pattern Matching**: Decode tokens and parse rules elegantly
- **Pure Functions**: No hidden state bugs in transformations
- **Strong Types**: Catch errors at compile time
- **List Processing**: Easy manipulation of token streams and ASTs

The Centurion C compiler uses Haskell to:
1. **Lex**: Tokenize C source code
2. **Parse**: Build AST from tokens
3. **Analyze**: Type check and semantic analysis
4. **Codegen**: Generate RISC-V assembly

Next: Learn how to build assemblers and linkers in Python.
