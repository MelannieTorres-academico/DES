#references: https://stackoverflow.com/questions/19705638/how-to-concatenate-bits-in-python

import fileinput

# Rearanges the original_bits depending on the positions given in the new_positions list
# new_positions is a list
# original_bits is a binary-like string
# retruns a binary-like string
def permutation(new_positions, original_bits):
    new_bits = []
    for pos in new_positions:
        new_bits.append(original_bits[pos])
    return ''.join(map(str, new_bits)) # turns array to bits: https://github.com/LyleScott/DES-Encryption-in-Python/blob/master/src/des.py

#generates the subkeys
# key is a binary-like string
# returns two binary-like strings
def generateSubkeys(key):
    permuted_key = permutation([2,4,1,6,3,9,0,8,7,5], key)
    #split in half
    left_key = permuted_key[:5]
    right_key = permuted_key[5:]
    #one shift to the left
    left_key = permutation([1,2,3,4,0], left_key)
    right_key = permutation([1,2,3,4,0], right_key)
    subkey1 = left_key+right_key
    subkey1 = permutation([5,2,6,3,7,4,9,8], subkey1)
    #two shifts to the left
    left_key = permutation([2,3,4,0,1], left_key)
    right_key = permutation([2,3,4,0,1], right_key)
    subkey2 = left_key+right_key # these are strings
    subkey2 = permutation([5,2,6,3,7,4,9,8], subkey2)
    return subkey1, subkey2

# xors two binary-like strings converting them first to ints
# returns an int value
def xor_strings(str1, str2):
    return int(str1, base=2) ^ int(str2, base=2)

#uses the feistel algorithm
#permuted_plaintext is a binary-like string
#subkey is a binary-like string
#s_box0 and s_box1 are matrixes
#returns the left and the right as binary-like string
def feistel(permuted_plaintext, subkey, s_box0, s_box1):
    left = permuted_plaintext[:4]
    right = permuted_plaintext[4:]
    exp_right = permutation([3,0,1,2,1,2,3,0],right)

    xor_right = xor_strings(exp_right, subkey)
    xor_right = format(xor_right, '08b')

    row = int(permutation([0,3], xor_right[:4]), base=2)
    col = int(permutation([1,2], xor_right[:4]), base=2)
    s0 = s_box0[row][col]

    row = int(permutation ([0,3], xor_right[4:]), base=2)
    col = int(permutation ([1,2], xor_right[4:]), base=2)
    s1 = s_box1[row][col]

    s0s1 = format(s0, '02b')+format(s1, '02b') #these are strings
    s0s1 = permutation([1,3,2,0], s0s1)
    xor_left = xor_strings(left, s0s1)
    xor_left = format(xor_left, '04b')
    return xor_left, right


def main():
    file_input = fileinput.input()
    encrypt = file_input[0].replace("\n", "")
    key = file_input[1].replace("\n", "")
    plaintext = file_input[2].replace("\n", "")
    is_encryption = True if (encrypt == 'E') else False

    s_box0 = [[1,0,3,2],[3,2,1,0],[0,2,1,3],[3,1,3,2]]
    s_box1 = [[0,1,2,3],[2,0,1,3],[3,0,1,0],[2,1,0,3]]

    if (is_encryption):
        subkey1, subkey2 = generateSubkeys(key)
    else:
        subkey2, subkey1 = generateSubkeys(key)

    #step 1
    permuted_plaintext = permutation([1,5,2,0,3,7,4,6], plaintext)
    #step 2
    left, right = feistel(permuted_plaintext, subkey1, s_box0, s_box1)
    #step 3
    right_left = right+left
    #step 4
    left, right = feistel(right_left, subkey2, s_box0, s_box1)
    left_right = left+right
    #step 5
    inverse = permutation([3,0,2,4,6,1,7,5],left_right)
    print(inverse)


if __name__ == "__main__":
    main()
