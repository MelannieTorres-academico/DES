#references: https://stackoverflow.com/questions/19705638/how-to-concatenate-bits-in-python


def permutations(new_positions, original_bits):
    new_bits = #initialize with 0's of the same size new_positions
    i = 0
    for pos in new_positions:
        new_bits[i] = original_bits[pos]
        i += 1
    return new_bits

def get_matrix_position(row, col, matrix):
    #returns the value of the given position in binary

def main:
    plaintext = input()
    key = input()
    is_encryption = input()
    s_box0 = [[1,0,3,2],[3,2,1,0],[0,2,1,3],[3,1,3,2]]
    s_box1 = [[0,1,2,3],[2,0,1,3],[3,0,1,0],[2,1,0,3]]

    if (is_encryption):
        permuted_plaintext = permutations([1,5,2,0,3,7,4,6], plaintext)
        permuted_key = permutations([2,4,1,6,3,9,0,8,7,5], key)
        #split in half
        key_half_1 = permuted_key[:5]
        key_half_2 = permuted_key[5:]
        #create subkey1
        #one shift to the left
        key_half_1 = permutations([1,2,3,4,0], key_half_1)
        key_half_2 = permutations([1,2,3,4,0], key_half_2)
        key = (key_half_1<<4) | (key_half_2>>4)
        subkey_1 = permutations([5,2,6,3,7,4,9,8], key)
        #create subkey2
        key_half_1 = permutations([2,3,4,0,1], key_half_1)
        key_half_2 = permutations([2,3,4,0,1], key_half_2)
        key2 = (key_half_1<<4) | (key_half_2>>4)
        subkey_2 = permutations([5,2,6,3,7,4,9,8], key2)
        #the mixing function
        permuted_plaintext_first_4_bits= permuted_plaintext[:4]
        permuted_plaintext_last_4_bits= permuted_plaintext[4:]
        expanded_plaintext_right = permutation([3,0,1,2,1,2,3,0],permuted_plaintext_last_4_bits)
        xored_plain_key_1 = expanded_plaintext_right ^ subkey_1
        row = int(permutation ([0,3], xored_plain_key_1[:4]), 2)
        col = int(permutation ([1,2], xored_plain_key_1[:4]), 2)
        s0 = get_matrix_position(row, col, s_box0)

        row = int(permutation ([0,3], xored_plain_key_1[4:]), 2)
        col = int(permutation ([1,2], xored_plain_key_1[4:]), 2)
        s1 = get_matrix_position(row, col, s_box1)

        s0s1 = (s0<<2) | (s1>>2)
        s0s1 = permutation([1,3,2,0], s0s1) #duda
        xor_left= permuted_plaintext_first_4_bits ^ s0s1
        left_right_halves= (permuted_plaintext_last_4_bits<<4)|(xor_left>>4)

        #step 4
        permuted_plaintext_first_4_bits = left_right_halves[:4]
        permuted_plaintext_last_4_bits = left_right_halves[4:]
        expanded_plaintext_right = permutation([3,0,1,2,1,2,3,0],permuted_plaintext_last_4_bits)
        xored_plain_key2 = expanded_plaintext_right ^ subkey2
        row = int(permutation ([0,3], xored_plain_key_2[:4]), 2)
        col = int(permutation ([1,2], xored_plain_key_2[:4]), 2)
        s0 = get_matrix_position(row, col, s_box0)

        row = int(permutation ([0,3], xored_plain_key_2[4:]), 2)
        col = int(permutation ([1,2], xored_plain_key_2[4:]), 2)
        s1 = get_matrix_position(row, col, s_box1)
        s0s1 = (s0<<2) | (s1>>2)
        s0s1 = permutation([1,3,2,0], s0s1) #duda
        xor_left = permuted_plaintext_first_4_bits ^s0s1

        left_right_halves= (xor_left<<4)|(permuted_plaintext_last_4_bits>>4)
        inverse = permutation([3,0,2,4,6,1,7,5], left_right_halves)
        print(inverse)
    else:
        #use key2 first then key1
