# SNR.py

SNR is the Signature Near-Ring, a construction based on the INVERT transform. You can read an in-depth explanation of
the signature function and SNR 
[here](https://complexor.files.wordpress.com/2020/10/recursive-signatures-and-the-signature-left-near-ring.pdf).

## Seq

The Seq class is the base class for mathematical manipulations of sequences.

Seq objects may be constructed easily with a list or tuple of integers and floats.
If the list or tuple is empty, the null sequence is created.
If no arguments are specified, the zero sequence is created.

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
a = Seq([2, 4, 2, 1])
b = Seq([1, 1])

print(a / b)
```
```
2, 2, 0, 1
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
the variable `std_l` in snr.pyor by calling the function with a length argument.

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
the same way as Seq objects can.

### Block

The Block class exists to perform interesting signature-related operations on
matrices. These matrices can be added, subtracted, and multiplied.

#### Special Blocks

TODO: This section will discuss the special Blocks constructed via the class' static methods


## Miscellaneous

### Identities

This folder is where implementations of all my important identities reside.

* `snr_column` showcases the identity in Equation 62 of my SNR paper
* `snr_diagonal` showcases the identity in Equation 63
* `snr_triangles` showcases a variety of triangles with interesting signatures as per 5.1

### Archive

This contains miscellaneous math-ey code bits I've tested out over time.