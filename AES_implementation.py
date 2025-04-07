from pprint import pprint
import numpy as np

# AES 
# Author : Edoardo Diana, 13/12/2024

# Check the main to uncomment the desired function to execute

sbox = [
    0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
    0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
    0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
    0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
    0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
    0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
    0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
    0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
    0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
    0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
    0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
    0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
    0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
    0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
    0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
    0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16,
]

# Addition corresponds to bit-wise addition mod 2
def GF28_add(x, y):                  
    return x^y

# Subtraction corresponds to bit-wise addition mod 2
def GF28_sub(x, y):                  
    return x^y

def GF28_multiply(x, y):
    p = 0b100011011             # Using the AES irreducible polynomial x^8 +x^4 + x^3 + x + 1
    m = 0                       # Performing school book multiplication (bit-wise), m holds product
    for i in range(8):
        m = m << 1              # Left shift intermediate sum each bit
        if m & 0b100000000:     # If larger than 255 then reduce
            m = m ^ p
        if y & 0b010000000:     # If multiplier bit is set, then add y
            m = m ^ x
        y = y << 1              # Left shift multiplier to check next bit in next iteration
    return m

# Your turn: implement the special case where we multiply by "x" (i.e. 2) without doing an explicit finite field multiplication
# Question n. 3.b inside the associated produced documentation  
def xTimes(x):      
    temp = x << 1               # Left shift 
    x = x >> 7                  # Extract the MSB
    x = x * 0x1B                # Multiply for 0x1B (if MSB is 1, else 0)
    x = x ^ temp                # Modular reduction using the AES irreducible polynomial x^8 + x^4 + x^3 + x + 1
    return x

# Your turn: implement finite field inversion
# Question n. 4.b inside the associated produced documentation  
def GF28_inv(x):        
    """"Implementation based on the Fermat Little Theorem """
    t0 = GF28_multiply(x, x)  # x^2
    t1 = GF28_multiply(t0, x)  # x^3
    t0 = GF28_multiply(t0, t0)  # x^4
    t1 = GF28_multiply(t1, t0)  # x^7
    t0 = GF28_multiply(t0, t0)  # x^8
    t0 = GF28_multiply(t1, t0)  # x^15
    t0 = GF28_multiply(t0, t0)  # x^30
    t0 = GF28_multiply(t0, t0)  # x^60
    t1 = GF28_multiply(t1, t0)  # x^67
    t0 = GF28_multiply(t0, t1)  # x^127
    t0 = GF28_multiply(t0, t0)  # x^254
    
    return t0

def pprint_state(state):
    pprint([["{0:0{1}x}".format(i, 2).upper() for i in row] for row in state])


def SubBytes(state):
    return [[sbox[i] for i in row] for row in state]

def ShiftRows(state):
    return [
        state[0],
        state[1][1:] + state[1][:1],
        state[2][2:] + state[2][:2],
        state[3][3:] + state[3][:3],
    ]

def AddRoundKey(state, rkey):
    pairs = [zip(a, b) for a, b in zip(state, rkey)]
    return [[a ^ b for a, b in row] for row in pairs]

# Helper funtion to mix coulmn elements, It was taken from the official AES paper.
def mix_single_column(col):
    return [
        GF28_add(GF28_add(GF28_multiply(0x02, col[0]), GF28_multiply(0x03, col[1])), GF28_add(col[2], col[3])),
        GF28_add(GF28_add(col[0], GF28_multiply(0x02, col[1])), GF28_add(GF28_multiply(0x03, col[2]), col[3])),
        GF28_add(GF28_add(col[0], col[1]), GF28_add(GF28_multiply(0x02, col[2]), GF28_multiply(0x03, col[3]))),
        GF28_add(GF28_add(GF28_multiply(0x03, col[0]), col[1]), GF28_add(col[2], GF28_multiply(0x02, col[3])))
    ]

# Your turn to implement MixColumn
# Question n. 4.a inside the associated produced documentation  
def MixColumns(state):
    """AES MixColumns transformation"""
    new_state = []
    for col_idx in range(4):
        # Extract the coulmn as a list
        col = [state[row_idx][col_idx] for row_idx in range(4)]
        # Mix
        mixed_col = mix_single_column(col)
        # Put transformed values inside the state
        # After mixing a coulmn, update the corrispondent column insite the output state.
        for row_idx in range(4):
            if len(new_state) <= row_idx:
                new_state.append([0] * 4)
            new_state[row_idx][col_idx] = mixed_col[row_idx]
    
    return new_state

def word_rotation(word):
    """Helper function for key expansion"""
    return word[1:] + word[:1]

def substitution_word(word):
    """Helper function for key expansion"""
    return [sbox[b] for b in word]

# Constants RCON defined as words of 4 byte
Rcon = [
    [0x01, 0x00, 0x00, 0x00],
    [0x02, 0x00, 0x00, 0x00],
    [0x04, 0x00, 0x00, 0x00],
    [0x08, 0x00, 0x00, 0x00],
    [0x10, 0x00, 0x00, 0x00],
    [0x20, 0x00, 0x00, 0x00],
    [0x40, 0x00, 0x00, 0x00],
    [0x80, 0x00, 0x00, 0x00],
    [0x1b, 0x00, 0x00, 0x00],
    [0x36, 0x00, 0x00, 0x00],
]

# Question n. 4.c inside the associated produced documentation  
def key_expansion(key):
    """Helper function for key expansion"""
    number_of_key = 4
    number_of_rounds = 10
    
    word = [list(column) for column in zip(*key)]
    for i in range(number_of_key, 4 * (number_of_rounds + 1)):
        temp = word[i-1]
        if i % number_of_key == 0:
            temp = [(substitution_word(word_rotation(temp))[j] ^ Rcon[i // number_of_key - 1][j]) for j in range(4)]
        elif i % number_of_key == 4:
            temp = substitution_word(temp)
        word.append([word[i - number_of_key][j] ^ temp[j] for j in range(4)])

    blocks = [word[i:i + 4] for i in range(0, len(word), 4)]
    # Transpose each block so to obtain a row-wise representation
    transposed_blocks = []
    for block in blocks:
        transposed_blocks.append([list(row) for row in zip(*block)])

    return transposed_blocks

# Question n. 4.d inside the associated produced documentation  
def AES_encr(AES_state, key):
    """
    Function that implements all the AES Rounds.
    There are also other version of this function, this is done in respect with the different request in this laboratoty.
        1 ) AES_encr(state, key)                         (THIS ONE)
        2 ) AES_encr_combined_sb_and_sr(state, key)
        3 ) AES_encr_state_xor_m(state, key)
    """
    round_keys = key_expansion(key)
    
    ##
    print('AES State beginning')
    pprint_state(AES_state)
    ##

    ##
    state = AddRoundKey(AES_state, round_keys[0])
    print('AES State after AddRoundKey')
    pprint_state(state)
    ##

    for i in range(1, 10):

        print(f"\n----------- Start of round {i} -----------\n")

        ##
        state = SubBytes(state)
        print(f'AES State after SubBytes : Round {i}')
        pprint_state(state)
        ##
        
        ##
        state = ShiftRows(state)
        print(f'AES State after ShiftRows : Round {i}')
        pprint_state(state)
        ##

        ##
        state = MixColumns(state)
        print(f'AES State after MixColumns : Round {i}')
        pprint_state(state)
        ##

        ##
        state = AddRoundKey(state, round_keys[i])
        print(f'AES State after AddRoundKey : Round {i+1}')
        pprint_state(state)
        ##

    print("\n----------- Start of round 10 -----------\n")

    state = SubBytes(state)
    print('AES State after SubBytes : Round 10')
    pprint_state(state)

    state = ShiftRows(state)
    print('AES State after ShiftRows : Round 10')
    pprint_state(state)

    state = AddRoundKey(state, round_keys[10])
    print('AES State after AddRoundKey Finale')
    pprint_state(state)
 
    print('AES Round Completed !')

    return state

def aff_transf(x):
    """Helper function for gen_s_box()"""
    # Constant defined in the standard
    const_standard = 0x63
    result = 0
    # Go along all the bits 
    for i in range(8):
        bit = ((x >> i) & 1) ^ ((x >> ((i + 4) % 8)) & 1) ^ ((x >> ((i + 5) % 8)) & 1) \
              ^ ((x >> ((i + 6) % 8)) & 1) ^ ((x >> ((i + 7) % 8)) & 1)
        result |= (bit << i)
    return result ^ const_standard

def gf_inverse(integer_number):
    """Helper function for gen_s_box(). The Finite Field Inversion is not defined for the 0 element of the Galois Field"""
    if integer_number == 0: 
        return 0
    return GF28_inv(integer_number)

# Question n. 5 inside the associated produced documentation  
def gen_s_box():
    """Generates "online" the Substitution Box that is used by SubBytes"""
    s_box = []
    for i in range(256):
        inv = gf_inverse(i)
        value = aff_transf(inv)  
        s_box.append(hex(value))
    return s_box

# Question n. 6 inside the associated produced documentation  
def sb_sr(state):
    """SubBytes and ShiftRows computed in a single run"""
    return [
        [sbox[byte] for byte in state[0]],                # 1^st row, no shift
        [sbox[state[1][(i + 1) % 4]] for i in range(4)],  # 2^nd row, 1 position shift
        [sbox[state[2][(i + 2) % 4]] for i in range(4)],  # 3^rd row, 2 position shift
        [sbox[state[3][(i + 3) % 4]] for i in range(4)],  # 4^th row, 3 position shift
    ]

def AES_encr_combined_sb_and_sr(AES_state, key):
    """
    Function that implements all the AES Rounds.
    This is done using a single function to do both SubBytes and ShiftRows in a single time.
    There are also other version of this function, this is done in respect with the different request in this laboratoty.
        1 ) AES_encr(state, key)                         
        2 ) AES_encr_combined_sb_and_sr(state, key)      (THIS ONE)
        3 ) AES_encr_state_xor_m(state, key)
    """
    round_keys = key_expansion(key)
    
    ##
    print('AES State beginning')
    pprint_state(AES_state)
    ##

    ##
    state = AddRoundKey(AES_state, round_keys[0])
    print('AES State after AddRoundKey')
    pprint_state(state)
    ##

    for i in range(1, 10):

        print(f"\n----------- Start of round {i} -----------\n")
        
        ##
        state = sb_sr(state)
        print(f'AES State after SubBytes + Shift Rows : Round {i}')
        pprint_state(state)
        ##
        
        ##
        state = MixColumns(state)
        print(f'AES State after MixColumns : Round {i}')
        pprint_state(state)
        ##

        ##
        state = AddRoundKey(state, round_keys[i])
        print(f'AES State after AddRoundKey : Round {i+1}')
        pprint_state(state)
        ##

    print("\n----------- Start of round 10 -----------\n")

    ##
    state = sb_sr(state)
    print(f'AES State after SubBytes + Shift Rows : Round 10')
    pprint_state(state)
    ##

    state = AddRoundKey(state, round_keys[10])
    print('AES State after AddRoundKey Finale')
    pprint_state(state)
 
    print('AES Round Completed !')

    return state

# Masking Matrix filled with our masking value 0x42 
m = np.full((4, 4), 0x42).tolist()

# Masking column 
mix_cols_m = [0x42, 0x42, 0x42, 0x42]


def xor_with_m(state):
    """Helper function to do the element-wise XOR of elements of the State Matrix and Masking Matrix"""
    return [[state[row][col] ^ m[row][col] for col in range(len(state[row]))] for row in range(len(state))]

def columnwise_xor_with_m(state):
    """Helper function to do the columns-wise XOR of the State Matrix coumns and the Masking column"""
    return [[state[row][col] ^ mix_cols_m[col] for col in range(len(state[row]))] for row in range(len(state))]

# Question n. 7 inside the associated produced documentation  
def AES_encr_state_xor_m(AES_state, key):
    """
    Function that implements all the AES Rounds.
    This is done using 2 possible cases : 
        - Way 1 : the input of each round function is (a XOR m).
        - Way 2 : the input of each round function is the state (a). Then we do the XOR with the matrix m.  
    We try to spot if there are any differences in the output matrices thus obtained.
    
    There are also other version of this function, this is done in respect with the different request in this laboratoty.
        1 ) AES_encr(state, key)                         
        2 ) AES_encr_combined_sb_and_sr(state, key)
        3 ) AES_encr_state_xor_m(state, key)             (THIS ONE)
    """
    round_keys = key_expansion(key)

    # Do : a XOR m
    # Then : AddRoundKey(a XOR m)
    
    ##
    print("AES State after AddRoundKey(a XOR m) :  -    Way 1 ")
    t0 = AddRoundKey(xor_with_m(AES_state), round_keys[0])
    pprint_state(t0)
    ##

    # Do : AddRoundKey(a)
    # Then : AddRoundKey(a) XOR m
    
    ##
    print("AES State after AddRoundKey(a) XOR m :  -     Way 2 ")
    t1 = AddRoundKey(AES_state, round_keys[0])
    t2 = xor_with_m(t1)
    pprint_state(t2)
    ##

    state = t0

    for i in range(1, 10):
                
        # Devi passare in input a Sub Bytes prima state (che è AddRoundKey(a XOR m)) e poi test 2 ( che è AddRoundKey(a) XOR m)
        state_before_SubBytes = state
        print(f"\n----------- Start of round {i} -----------\n")
        ##
        t0 = SubBytes(xor_with_m(state_before_SubBytes))
        print(f'AES State after SubBytes(a XOR m) : Round {i} -    Way 1 ')
        pprint_state(t0)
        ##

        ##
        t1 = SubBytes(state_before_SubBytes)
        t2 = xor_with_m(t1)
        print(f'AES State after SubBytes(a) XOR m : Round {i} -    Way 2 ')
        pprint_state(t2)
        ##

        state = t0

        # Devi passare in input a ShiftRows prima state (che è AddRoundKey(a XOR m)) e poi test 2 ( che è AddRoundKey(a) XOR m)

        ##
        t0 = ShiftRows(xor_with_m(state))
        print(f'\nAES State after ShiftRows(a XOR m) : Round {i} -    Way 1 ')
        pprint_state(t0)
        ##

        ##
        t1 = ShiftRows(state)
        t2 = xor_with_m(t1)
        print(f'AES State after ShiftRows(a) XOR m : Round {i} -    Way 2 ')
        pprint_state(t2)
        ##

        state = t0

        ##
        state_after_sb_sr = sb_sr(xor_with_m(state_before_SubBytes))
        print(f'\nAES State after SubBytes_&_ShiftRows(a XOR m) : Round {i} -    Way 1 ')
        pprint_state(state_after_sb_sr)
        ##

        ##
        t1 = sb_sr(state_before_SubBytes)
        t2 = xor_with_m(t1)
        print(f'AES State after SubBytes_&_ShiftRows(a) XOR m : Round {i} -    Way 2 ')
        pprint_state(t2)
        ##

        # Here we don't do state = t0 because we already have the correct state that we obtained from the ShiftRows of before

        ##
        t0 = MixColumns(columnwise_xor_with_m(state))
        print(f'\nAES State after MixColumns(a XOR m) : Round {i} -    Way 1 ')
        pprint_state(t0)
        ##

        ##
        t1 = MixColumns(state)
        t2 = columnwise_xor_with_m(t1)
        print(f'AES State after MixColumns(a) XOR m : Round {i} -    Way 2 ')
        pprint_state(t2)
        ##

        state = t0

        ##
        t0 = AddRoundKey(xor_with_m(state), round_keys[i])
        print(f"\nAES State after AddRoundKey(a XOR m) : Round {i} -    Way 1 ")
        pprint_state(t0)
        ##

        ##
        t1 = AddRoundKey(state, round_keys[i])
        t2 = xor_with_m(t1)
        print(f"AES State after AddRoundKey(a) XOR m : Round {i} -    Way 2 ")
        pprint_state(t2)
        ##

        state = t0

    print("\n----------- Start of round 10 -----------\n")

    ##
    t0 = sb_sr(xor_with_m(state))
    print('AES State after SubBytes_&_ShiftRows(a XOR m) : Round 10 -    Way 1 ')
    pprint_state(t0)
    ##

    ##
    t1 = sb_sr(state)
    t2 = xor_with_m(t1)
    print(f'AES State after SubBytes_&_ShiftRows(a) XOR m : Round 10 -    Way 2 ')
    pprint_state(t2)
    ##

    state = t0

    ##
    t0 = AddRoundKey(xor_with_m(state), round_keys[10])
    print("\nAES State after AddRoundKey(a XOR m): : Round 10 -    Way 1 ")
    pprint_state(t0)
    ##

    ##
    t1 = AddRoundKey(state, round_keys[10])
    t2 = xor_with_m(t1)
    print(f"AES State after AddRoundKey(a) XOR m : Round 10 -    Way 2 ")
    pprint_state(t2)
    ##

    state = t0


    print("\nAES Completed with Success!")

    return state

if __name__ == "__main__":

    # Consider the state to be two-dimensional array of bytes
    # The order is defined in FIPS 197
    """
    AES_state = [
        [0x00, 0x04, 0x08, 0x0c],
        [0x01, 0x05, 0x09, 0x0d],
        [0x02, 0x06, 0x0a, 0x0e],
        [0x03, 0x07, 0x0b, 0x0f],
    ]

    k1 = [
        [0x00, 0x00, 0x00, 0x00],
        [0x01, 0x01, 0x01, 0x01],
        [0x02, 0x02, 0x02, 0x02],
        [0x03, 0x03, 0x03, 0x03],
    ]
    """

    AES_state = [
        [0x32, 0x88, 0x31, 0xe0],
        [0x43, 0x5a, 0x31, 0x37],
        [0xf6, 0x30, 0x98, 0x07],
        [0xa8, 0x8d, 0xa2, 0x34],
    ]

    k1 = [
        [0x2b, 0x28, 0xab, 0x09],
        [0x7e, 0xae, 0xf7, 0xcf],
        [0x15, 0xd2, 0x15, 0x4f],
        [0x16, 0xa6, 0x88, 0x3c],
    ]

    # -------------------- Use this code line for laboratory questions 3 and 4 --------------------

    aes_encryption_cipher = AES_encr(AES_state, k1)
    
    # -------------------- Use this code line for laboratory question 5 --------------------

    # Print the Generated S-Box to compare it with the assignment provided one 
    print("\nS-Box generation (online computation) :")
    generated_substitution_box = gen_s_box()
    for i in range(0, len(generated_substitution_box), 16):
        print(" ".join(map(str, generated_substitution_box[i:i + 16])))

    # -------------------- Use this code line for laboratory question 6 --------------------

    #aes_encryption_cipher_sbsr = AES_encr_combined_sb_and_sr(AES_state, k1)

    # -------------------- Use this code line for laboratory questions 7 --------------------

    #aes_encryption_cipher_state_xor_m = AES_encr_state_xor_m(AES_state, k1)

    
