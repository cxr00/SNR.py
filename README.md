# SNR.py

SNR is the Signature Near-Ring, a construction based on the INVERT transform. You can read an in-depth explanation of
the signature function and SNR 
[here](https://complexor.files.wordpress.com/2020/10/recursive-signatures-and-the-signature-left-near-ring.pdf).

## Seq

The Seq class is the base class for mathematical manipulations of sequences.

Seq objects may be constructed easily with a list or tuple of integers and floats.
If no argument is specified, the null sequence is created.

```python
a = Seq()
a = Seq([1, 2, 1])
a = Seq((2, 3))
```

### Mathematical operations

The Seq class implements arithmetic builtins. 
Sequences may add, subtract, convolve, and deconvolve.

#### Addition

```python
a = Seq([1, 1])
b = Seq([1, 1, 1])

print(a + b)
```
```
2, 2, 1
```

#### Subtraction

```python
a = Seq([2, 4, 3])
b = Seq([1, 2, 2, 1])

print(a - b)
```
```
1, 2, 1, -1
```

#### Convolution

```python
a = Seq([1, 1])
b = Seq([1, 1, 1])

print(a * b)
```
```
1, 2, 2, 1
```

#### Deconvolution

```python
a = Seq([2, 4, 2])
b = Seq([1, 1])

print(a / b)
```
```
2, 2
```

#### The signature function

The recursive signature function (also known as the INVERT transform)
turns a sequence (or "signature") into a recursive sequence. For example, the signature
[1, 1] returns the Fibonacci numbers.

```python
a = Seq([1, 1])

print(a.f())
```

```
1, 1, 2, 3, 5, 8, 13, 21, ...
```

The default length of the signature function is 30. This length may be altered by changing
the variable `std_l` in snr.py or by calling the function with a length argument.

```python
a = Seq([2, 1])
std_l = 5

print(a.f())
print(a.f(7))
```
```
1, 2, 5, 12, 29
1, 2, 5, 12, 29, 70, 169
```

### The inverse signature function

If a sequence begins with 1, then the inverse signature function can be performed to convert
the sequence into its signature. If the sequence does not begin with 1, then a ValueError is raised.
```python
a = Seq([1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89])

print(a.i())
```
```
1, 1
```

## Sig

The Sig class builds on the arithmetic of Seq to construct the Signature Left Near-Ring.
Sig objects may be constructed with a list, tuple, Seq, or empty input.
```python
a = Seq([1, 1])

b = Sig()
b = Sig(3)
b = Sig([1, 2, 1])
b = Sig(a)
```

### Mathematical operations

Sig objects can perform signature addition and subtraction, and signature convolution and deconvolution.

#### Signature addition
```python
a = Sig([1, 1])
b = Sig([1, 1])

print(a + b)
```
```
2, 1, -2, -1
```

#### Signature subtraction
```python
a = Sig([2, 1, -2, -1])
b = Sig([1, 1])

print(a - b)
```
```
1, 1
```

#### Signature convolution

Signature convolution utilizes the signature function to perform a unique multiplication algorithm.
Note that signature convolution is not commutative!

```python
a = Sig([1, 1])
b = Sig([1, 1, 1])

print(a * b)
print(b * a)
```
```
1, 2, 3, 4, 3, 1
1, 2, 3, 3, 2, 1
```

Because signature convolution is not commutative, there are two division algorithms that may be performed.

#### Left deconvolution

The `__floordiv__` builtin specifies left deconvolution, which produces a left operand for
signature convolution.

```python
a = Sig([1, 2, 3, 4, 3, 1])
b = Sig([1, 1, 1])

print(a // b)
```
```
1, 1
```

#### Right deconvolution

The `__truediv__` builtin specifies right deconvolution, which produces a right operand
for signature convolution. Right deconvolution is right distributive.

```python
a = Sig([1, 2, 3, 4, 3, 1])
b = Sig([1, 1])

print(a / b)
```
```
1, 1, 1
```

#### The signature function

Sig objects may perform the signature and inverse signature function
the same way Seq objects can.

## Block

The Block class exists to perform interesting signature-related operations on
matrices.

### Special Blocks

The Block class comes equipped with several static methods that generate interesting blocks.

#### Blank block

Block.blank() is a square matrix which contains only zeroes.

```python
a = Block.blank(5)

print(a)
```
```
0, 0, 0, 0, 0
0, 0, 0, 0, 0
0, 0, 0, 0, 0
0, 0, 0, 0, 0
0, 0, 0, 0, 0
```

#### Identity matrix

Block.identity() produces the identity matrix. Length can be specified.
Block.identity() is also the zero-th power of any Block.

```python
a = Block.identity(5)

print(a)
```
```
1
0, 1
0, 0, 1
0, 0, 0, 1
0, 0, 0, 0, 1
```

#### Power triangles

Block.power() takes a Seq and produces a power triangle. For example, the Seq [1, 1]
produces Pascal's Triangle.

```python
a = Block.power(Seq([1, 1]), l=5)

print(a)
```
```
1
1, 1
1, 2, 1
1, 3, 3, 1
1, 4, 6, 4, 1
```

#### Sen

Block.sen() takes a Seq and constructs the initial matrix in section 4.5 of my paper.

```python
a = Block.sen(Seq([1, 1]), 6)
b = Block.sen(Seq([2, 1]), 6)

print(a)
print(b)
```
```
1
0
1, 1
0, 1, 1
0, 0, 1, 1
0, 0, 0, 1, 1

1
1
1, 2
0, 1, 2
0, 0, 1, 2
0, 0, 0, 1, 2
```

#### g-matrices

Block.g_matrix() takes an initial Block and a set of Seq objects to produce a novel
matrix as outlined by section 4.5 of my paper.
```python
s = Block.power(Seq([1, 1]))
g = [Seq(1), Seq(1)]
a = Block.g_matrix(s, g)

print(a[:6])
```
```
1
3, 1
6, 4, 1
10, 10, 5, 1
15, 20, 15, 6, 1
21, 35, 35, 21, 7, 1
```

### Mathematical operations

Block objects can be added, subtracted, and multiplied.

#### Addition
```python
a = Block.power(Seq([1, 1]), 6)
b = Block.power(Seq([1, 0, 1]), 6)

print(a + b)
```
```
2
2, 1, 1
2, 2, 3, 0, 1
2, 3, 6, 1, 3, 0, 1
2, 4, 10, 4, 7, 0, 4, 0, 1
2, 5, 15, 10, 15, 1, 10, 0, 5, 0, 1
```

#### Subtraction
```python
a = Block.power(Seq([1, 1, 1]), 6)
b = Block.power(Seq([1, 1]), 6)

print(a - b)
```
```
0
0, 0, 1
0, 0, 2, 2, 1
0, 0, 3, 6, 6, 3, 1
0, 0, 4, 12, 18, 16, 10, 4, 1
0, 0, 5, 20, 40, 50, 45, 30, 15, 5, 1
```

#### Multiplication

Multiplication of Block objects is slightly different from traditional matrix multiplication,
allowing for multiplication of Blocks with different dimensions. This operation
is not commutative.
```python
a = Block.power(Seq([1, 1]))
b = Block.power(Seq([2, 1, 1]))

print(a * b)
print(b * a)
```
```
1
3, 1, 1
9, 6, 7, 2, 1
27, 27, 36, 19, 12, 3
81, 108, 162, 120, 91, 40
243, 405, 675, 630, 555, 331

1
4, 3, 1
16, 24, 17, 6, 1
63, 138, 141, 79, 24, 3
237, 648, 798, 532, 189, 28
843, 2645, 3630, 2650, 1015, 161
```

A Block may also be multiplied by a Seq object.

```python
a = Seq([1, 1])
b = Block.power(Seq([1, 1]))

print(b * a)
```
```
1, 1
1, 2, 1
1, 3, 3, 1
1, 4, 6, 4, 1
1, 5, 10, 10, 5, 1
```

### The signature and inverse signature function

The signature function can be performed on Block objects via antidiagonal summation.

```python
a = Block.power(Seq([1, 1]))

print(a.f()[:9])
```
```
1, 1, 2, 3, 5, 8, 13, 21, 34
```

When Block.i() function is called, it first performs Block.f(), followed by
the inverse signature function.
```python
a = Block.power(Seq([1, 1]))

print(a.i())
```
```
1, 1
```

## Miscellaneous

### Identities

This folder is where implementations of all my important identities reside.

* `snr_column` showcases the identity in Equation 62 of my paper
* `snr_diagonal` showcases the identity in Equation 63
* `snr_triangles` showcases a variety of triangles with interesting signatures as per section 5.1

### Archive

This contains miscellaneous math-ey code bits I've tested out over time. It's available
in case you are interested in seeing the things I've already explored.