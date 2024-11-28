from bitarray import bitarray
import sys

def elias_omega_decode(encoded):
    # just checking for not crashing, invalid input
    if not encoded.any() or len(encoded) == 0:
        return 0, encoded  

    pos = 0
    readlen = 1
    component = bitarray()

    #keep traverse untill find an int or end of the stream
    while pos + readlen <= len(encoded):
        # first iter len alway = 1
        component = encoded[pos:pos + readlen]
        # move forward
        pos += readlen

        if component[0] == 1:  # If MSB is 1, return it right away when we hit 1 as out first bit in the combination of bit
            N = int(component.to01(), 2)  # Convert bitarray to integer
            return N, encoded[pos:]  # Return the decoded integer and the remainder of the stream

        if component[0] == 0:  # If MSB is 0, flip to 1 and calculate new readlen
            component[0] = 1  # Flip 0 to 1
            readlen = int(component.to01(), 2) + 1  #convert the current combination into int and + 1 since we -1 when we encode

    # If the loop exits without returning, raise an error or handle the case
    raise ValueError("Failed to decode the complete integer")

def decode_character_details(bitstream, num_distinct_chars):
    # a dictionaries of char detail
    char_details = {}
    pos = 0

    # we only go for the number of unique character, no more or less base on the decode part of unique char
    for _ in range(num_distinct_chars):
        
        # Decode the 7-bit ASCII code
        ascii_code = bitstream[pos:pos+7].to01()
        char = chr(int(ascii_code, 2))
        pos += 7

        print(f"Decoded ASCII for '{char}': {ascii_code} using bits from pos {pos-7} to {pos}")


        # Decode the length of the Huffman codeword using Elias decoding
        huffman_length, new_stream = elias_omega_decode(bitstream[pos:])
        print(f"Decoded Huffman length for '{char}': {huffman_length} starting at pos {pos}")
        pos += len(bitstream[pos:]) - len(new_stream)  # Update pos with the number of bits read

        
        # Extract the Huffman codeword
        huffman_codeword = new_stream[:huffman_length]
        pos += huffman_length #udpate the position since we just traverse the huffman code bit
        print(f"Decoded Huffman codeword for '{char}': {huffman_codeword.to01()} using bits from pos {pos-huffman_length} to {pos}")

        # Store the results
        char_details[char] = (huffman_length, huffman_codeword.to01())
    #return the char detail with the remaining string
    return char_details, bitstream[pos:]

def decode_run_length_tuples(bitstream, char_details):

    decoded_sequence = []
    pos = 0

    # decode untill we extracted all the run length detail or end of the stream
    while pos < len(bitstream):
        # bool to keep track and break the loop
        found = False
        for char, (huff_len, code) in char_details.items():
            huffman_codeword = bitarray(code)  # extract the code in the char detail dictionaries
            expected_codeword_length = len(huffman_codeword) # keep track of the traversed length 

            # Check if the next segment in the bitstream matches this Huffman codeword
            if bitstream[pos:pos + expected_codeword_length] == huffman_codeword:
                # if matched, then incremented the position
                pos += expected_codeword_length
                # Now decode the Elias Omega encoded run length, which is followed back after back with the Huffman codeword
                run_length, new_stream = elias_omega_decode(bitstream[pos:])
                pos += (len(bitstream[pos:]) - len(new_stream))  # Update position after decoding run length
                
                decoded_sequence.append((char, run_length))
                found = True
                break
        # we just need to traverse throught the part that related to run length, break after finished 
        if not found:
            break

    return decoded_sequence, bitstream[pos:]

def reconstruct_from_run_length(run_length_tuples):
    # reconstruct the BWT word from the run length detail
    reconstructed_string = ""
    for char, length in run_length_tuples:
        if length > 0:# since I decode the 0 that make up the bite
            reconstructed_string += char * length

    return reconstructed_string

def decode_bwt_using_counting_sort(bwt):
    ascii_min, ascii_max = 36, 126
    
    # a freq array, for stable counting sort rank
    freq_array = [0] * (ascii_max - ascii_min + 1)
    # construct the occurences array while doing counting sort, which will allowed
    # us to access the occurrences information in constant time
    occurrences_array = [0] * len(bwt)

    # we traverse throught the bwt
    for i, char in enumerate(bwt):
        index = ord(char) - ascii_min
        freq_array[index] += 1 # tracking the frequencies
        # Track occurrences, since this is exclusive so -1
        occurrences_array[i] = freq_array[index] - 1

    # Generate rank tuples
    rank_tuples = []
    current_position = 0

    # just accumulate the frequencies to determine the starting position
    for i in range(len(freq_array)):
        if freq_array[i] > 0:
            char = chr(i + ascii_min)
            # first character will start at position 0 since it is a $
            rank_tuples.append((char, current_position))
            # the sum it from this point
            current_position += freq_array[i]

    print(rank_tuples)
    print(occurrences_array)
    
    # Transform rank_tuples into a dictionary for quick rank lookup
    rank_dict = dict(rank_tuples)

    # Reconstruct the original string from BWT
    original = [''] * len(bwt)
    idx = bwt.index('$')  # we alway start with $, since we know string will alway end with $
    for i in range(len(bwt) - 1, -1, -1):
        #grab original char based on the position of the last char
        char = bwt[idx]
        original[i] = char
        # Compute the LF mapping using rank and occurrences
        idx = rank_dict[char] + occurrences_array[idx]

    return ''.join(original)  # Remove the end marker if used


def read_input_file(filename):
    with open(filename, 'r') as file:
        return file.read().strip()

def write_output_file(data, filename):
    with open(filename, 'w') as file:
        file.write(data)

def decode(input_file):
    # Example usage:
    encoded_data = read_input_file(input_file)
    encoded_stream = bitarray(encoded_data)

    #decoded the length of the word
    decoded_value, remaining_stream = elias_omega_decode(encoded_stream)
    print("Decoded Value:", decoded_value)
    print("Remaining Stream:", remaining_stream.to01())

    # decoded the length of the set of unique character
    num_distinct_chars, remaining_stream = elias_omega_decode(remaining_stream)
    print("Decoded Value:", num_distinct_chars)
    print("Remaining Stream:", remaining_stream.to01())

    #decode the character detail
    char_details, remaining_stream = decode_character_details(remaining_stream, num_distinct_chars)
    print("Character Details:", char_details)
    print("Remaining Stream:", remaining_stream.to01())

    #decode run lenght detail
    run_length_tuples, remaining_stream = decode_run_length_tuples(remaining_stream, char_details)
    print("Decoded Run-Length Sequence:", run_length_tuples)
    print("Remaining Stream:", remaining_stream.to01())

    # Reconstruct the string
    reconstructed_bwt = reconstruct_from_run_length(run_length_tuples)
    print("Reconstructed BWT String:", reconstructed_bwt)

    #invert the BWT to the origin string
    original_text = decode_bwt_using_counting_sort(reconstructed_bwt)
    print("Original Text:", original_text)

    write_output_file(original_text, "q2_decoder_output.txt")

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python q2_decoder.py <binary_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    decode(input_file)