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

## Key Features

### Performance Optimization
- Linear time complexity (O(n)) for both compression and decompression
- Minimal memory overhead with fixed-size arrays
- Efficient bit-level operations
- Stream-based processing

### I/O Efficiency
- Sequential access patterns
- Buffered operations
- Minimal memory allocations
- Streaming-capable design

### Scientific Computing Benefits
- Handles large datasets efficiently
- Suitable for numerical and textual data
- Scalable for high-performance computing
- Memory-conscious implementation

## Technical Specifications

### Time Complexity
- Encoding: O(n)
- Decoding: O(n)
- Where n is the input text length

### Space Complexity
- Additional space: O(1) for fixed ASCII range
- Working space: O(n) for input/output buffers

### Supported Features
- ASCII text compression (codes 36-126)
- Lossless compression/decompression
- Stream-based processing
- Error detection

## Why This Implementation?

### Design Choices

1. **Combined Compression Techniques**
   - BWT groups similar characters, improving RLE efficiency
   - Huffman coding provides optimal symbol encoding
   - Elias coding efficiently handles variable-length numbers

2. **Performance Focus**
   ```python
   # Example of efficient counting sort implementation
   freq_array = [0] * (ascii_max - ascii_min + 1)  # Fixed-size array
   occurrences_array = [0] * len(bwt)              # Linear space
   ```

3. **I/O Optimization**
   ```python
   # Stream-based processing
   def decode(input_file):
       encoded_stream = bitarray(read_input_file(input_file))
       # Process stream in chunks
       decoded_value, remaining_stream = elias_omega_decode(encoded_stream)
   ```

### Advantages

1. **Scientific Computing**
   - Efficient handling of large datasets
   - Optimized for numerical data patterns
   - Suitable for distributed systems

2. **Performance**
   - Linear time complexity
   - Minimal memory overhead
   - Efficient bit operations

3. **Scalability**
   - Handles varying input sizes
   - Supports streaming operations
   - Modular design for extensions

## Use Cases

### Scientific Data Processing
- Experimental data compression
- Numerical dataset storage
- Real-time data acquisition

### High-Performance Computing
- Distributed computing systems
- Data transfer optimization
- Storage efficiency

### Big Data Analytics
- Data warehouse optimization
- Analytics pipeline efficiency
- Real-time processing

## Future Improvements

1. **Parallel Processing**
   ```python
   # Planned parallel implementation
   def parallel_decode(input_file, num_threads):
       chunks = split_into_chunks(input_file, num_threads)
       with ThreadPoolExecutor(max_workers=num_threads) as executor:
           results = executor.map(decode_chunk, chunks)
   ```

2. **Memory Mapping**
   - Implementation of memory-mapped file handling
   - Reduced memory footprint
   - Improved I/O performance

3. **Advanced Buffering**
   - Customizable buffer sizes
   - Adaptive buffering strategies
   - Optimized I/O patterns

## Getting Started

### Prerequisites
- Python 3.x
- bitarray library

### Installation