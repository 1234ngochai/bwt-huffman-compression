import sys
import os
from q1 import build_suffix_tree,collect_suffix_array
from bitarray import bitarray
import heapq


def compute_bwt_from_suffix_array(s, suffix_array):
    n = len(s)
    bwt = [''] * n
    ## we loop over the character
    for i in range(n):
        # if it is 1, then we take the last string
        if suffix_array[i] == 0:
            bwt[i] = s[-1]  # Last character of the string
        else:
            #since it a cyclic, we take the current rank(suffix array) at that position - 1 
            bwt[i] = s[suffix_array[i] - 1]
    return ''.join(bwt)

def elias_omega_encode(N):
    if N < 1:
        raise ValueError("error")

    components = []
    current = N

    while current >= 1:
        binary_rep = bin(current)[2:]  # take the binary reppresentaion of the current int
        components.append(binary_rep)  # append current binary representation to components
        current = len(binary_rep) - 1   # calculate next component, -1 to make sure it will go to an end

    # Initialize the encoded bitarray with '0' for the encoding of the smallest length '1'
    encoded = bitarray('')
    
    # Process each part in reverse order, flipping the MSB, excluding the original number N
    for part in reversed(components[1:]):
        bit_part = bitarray(part)  # convert string to bitarray
        bit_part[0] = 0            # flip the MSB
        encoded.extend(bit_part)   # append to the main encoded bitarray

    # last, append the binary of N without flipping any bit
    encoded.extend(components[0])

    return encoded

class Node:
    #huffman tree
    def __init__(self, char, freq):
        self.char = char # character that been stored
        self.freq = freq # frequencies
        self.left = None # left child
        self.right = None #right child
    
    # function to be later use by heapq 
    def __lt__(self, other):
        return self.freq < other.freq

def calculate_frequencies(text):
    freq = [0] * 91  # ASCII 36 to 126

    #init a list of ASCII 36 to 126, so that we can insert traversed and inserted in linear time
    for char in text:
        index = ord(char) - 36
        freq[index] += 1 # increment the corresponding char


    # an initial heap, keep track of smallest node, so we can sort in log time and pop in constant
    heap = []
    for i in range(91):
        if freq[i] > 0:
            node = Node(chr(i + 36), freq[i])
            heapq.heappush(heap, node)

    return heap

def build_huffman_tree(heap):
    heapq.heapify(heap)  # Make sure the list is a heap

    # while their still element in the heap
    while len(heap) > 1:
        # smaller element go to leaf, larger go to right
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)

        # create a new node, which is a merged between the last to poped nodes
        merged = Node(None, left.freq + right.freq)
        merged.left = left
        merged.right = right

        heapq.heappush(heap, merged)

    return heap[0]  # The root of the Huffman tree

def generate_huffman_codes(node, prefix="", codes=None):
    # graph traversal, using recursive called to reach the leaf, and append the binary code along the way
    if codes is None:
        codes = [''] * 91  # Initialize code list for ASCII 36 to 126

    #stop condition
    if node.char is not None:
        index = ord(node.char) - 36
        codes[index] = prefix
    else:
        generate_huffman_codes(node.left, prefix + "0", codes) # go to left child
        generate_huffman_codes(node.right, prefix + "1", codes) # go to right child 

    return codes


def encode_bwt_length(bwt_string):
    #grab the length
    bwt_length = len(bwt_string)
    #called elias encode for the length
    encoded_length = elias_omega_encode(bwt_length)
    return encoded_length.to01()  # Convert bitarray to a binary string for display or further processing.

def encode_distinct_char_count(bwt_string):
    #count distinct_chars using a set, and calculate the length of that set
    distinct_chars = len(set(bwt_string))  # Count distinct characters
    # called elias encode for the length
    encoded_count = elias_omega_encode(distinct_chars)
    return encoded_count.to01()

def encode_character_details(bwt_string, huffman_codes):
    # get a set of unique characters
    distinct_chars = set(bwt_string)  
    encoded_char_details = bitarray()

    for char in distinct_chars:
        ascii_code = bitarray(f"{ord(char):07b}")  # 7-bit ASCII format for that unique character
        huffman_code = bitarray(huffman_codes[ord(char) - 36])  # Get Huffman code, since huffman code was an array of ascii
        huffman_length = elias_omega_encode(len(huffman_code))  # Elias for length of Huffman code

        # Combine all parts for this character
        encoded_char_details.extend(ascii_code)
        encoded_char_details.extend(huffman_length)
        encoded_char_details.extend(huffman_code)

        # Debug output for each character
        print(f"Character: {char}")
        print("ASCII Code (7-bit):", ascii_code.to01())
        print("Huffman Code Length (Elias ):", huffman_length.to01())
        print("Huffman Code:", huffman_code.to01())
        print("---")

    return encoded_char_details.to01()

def generate_run_length_tuples(bwt_string):
    # checking for not crash
    if not bwt_string:
        return []

    # the base value for the loop, need to start with some char
    run_length_tuples = []
    current_char = bwt_string[0]
    current_length = 1

    #loop throught the string
    for char in bwt_string[1:]:
        #increase the frequencies/length of the char as long as it still repeat
        if char == current_char:
            current_length += 1
        else:
        #if it not repeat anymore, then add it to the char and it length to the tuples
            run_length_tuples.append((current_char, current_length))
            # reset the var
            current_char = char
            current_length = 1

    # Append the last run length
    run_length_tuples.append((current_char, current_length))

    return run_length_tuples

def encode_run_length_tuples(run_length_tuples, huffman_codes):

    encoded_rle = bitarray()

    for char, length in run_length_tuples:
        huffman_code = bitarray(huffman_codes[ord(char) - 36])  # Huffman code for the character, since huffman code was store in an
                                                                #array of ascii
        run_length_code = elias_omega_encode(length)  # Elias Omega encoding for the run length

        # add it by this order based on the format
        encoded_rle.extend(huffman_code)
        encoded_rle.extend(run_length_code)
        # Print detailed information for debugging
        # print(f"Character: {char}")
        # print("Huffman Code:", huffman_code.to01())
        # print(f"Run Length: {length}")
        # print("Elias Omega Encoded Run Length:", run_length_code.to01())
        # print("---")

    return encoded_rle.to01()


def read_input_file(filename):

    with open(filename, 'r') as file:
        return file.readline().strip()

def write_output_file(data, filename):

    with open(filename, 'w') as file:
        file.write(data)

def encoder(s):

    # from the given string, build a suffix tree using ukkonen
    root = build_suffix_tree(s)
    # then get the suffix array from the suffix tree
    suffix_array = collect_suffix_array(root, s)

    # compute the BWT string
    bwt_string = compute_bwt_from_suffix_array(s, suffix_array)
    #encode it
    encoded_bwt_length = encode_bwt_length(bwt_string)

    encoded_distinct_chars = encode_distinct_char_count(bwt_string)

    #calculate the frequencies, put it in a heapq for a sorted order, instant pop
    heap = calculate_frequencies(s)
    #build the suffix tree from the heap
    root = build_huffman_tree(heap)
    # then traverse the huffman_tree to extract the binary code
    huffman_codes = generate_huffman_codes(root)

    # encode the detail of the character
    encoded_char_details = encode_character_details(bwt_string, huffman_codes)

    # run length encoding
    run_length_tuples = generate_run_length_tuples(bwt_string)
    encoded_rle = encode_run_length_tuples(run_length_tuples, huffman_codes)

    print("Encoded BWT Length:", encoded_bwt_length)
    print("Encoded Distinct Characters Count:", encoded_distinct_chars)
    print("Encoded Character Details:", encoded_char_details)
    print("Run-Length Tuples:", run_length_tuples)
    print("Encoded Run Length Tuples:", encoded_rle)


    # Combine all encoded parts into a single bitstream
    final_encoded_bitstream = bitarray()
    final_encoded_bitstream.extend(encoded_bwt_length)
    final_encoded_bitstream.extend(encoded_distinct_chars)
    final_encoded_bitstream.extend(encoded_char_details)
    final_encoded_bitstream.extend(encoded_rle)

    # Ensure the bitstream is byte-aligned by padding with '0's if necessary
    extra_bits = 8 - len(final_encoded_bitstream) % 8
    if extra_bits < 8:
        final_encoded_bitstream.extend('0' * extra_bits)

    compressed_data = final_encoded_bitstream.to01()

    print("Final Compressed Data:", compressed_data)
    print("Length of Compressed Data:", len(compressed_data))

    # Write the final compressed data to a binary output file
    write_output_file(final_encoded_bitstream.to01(), 'q2_encoder_output.bin')


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python q2_encoder.py <stringFileName>")
        sys.exit(1)
    s = read_input_file(sys.argv[1])
    encoder(s)
