# Advanced Text Compression System

## Overview
This project implements a sophisticated text compression system combining multiple compression techniques to achieve efficient data compression while maintaining fast decompression speeds. The system is particularly optimized for scientific computing applications and high-performance I/O operations.

## Compression Pipeline
The system implements a multi-stage compression pipeline:

1. **Burrows-Wheeler Transform (BWT)**
   - Improves compression by grouping similar characters
   - Enables better run-length encoding
   - Reversible transformation

2. **Run-Length Encoding (RLE)**
   - Efficiently handles repeated characters
   - Particularly effective after BWT
   - Linear time complexity

3. **Huffman Coding**
   - Optimal prefix-free encoding
   - Adapts to character frequencies
   - Provides near-entropy compression

4. **Elias Omega Coding**
   - Efficient variable-length integer encoding
   - Used for metadata and run-lengths
   - Self-delimiting codes
