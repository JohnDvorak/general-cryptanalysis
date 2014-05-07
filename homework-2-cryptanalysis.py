#! usr/bin/env python3

CIPHERTEXT = "BMCWGFPVUNBLKVKRNCYKRQLNLJUULLCCWWAABIXBDGCEG\
ORFBMTUSKCFDSJTHSWXVZAZDNXMKHRRPEUCNMAGKBJGPD\
SIJZPTHEQSHKGSMZJBMUPQIBKUWVRWGTWSLQLZHJFLMHN\
WOTNKENQRPOFFZZDDFIITVROWCFKHIHDAZOKZLVTAMVXX\
PMCUG"

# Letter frequencies taken from Table 1.1 from Understanding Crypto, page 9
ENGLISH_FREQUENCY = {
    'A' : .0817,
    'B' : .0150,
    'C' : .0278,
    'D' : .0425,
    'E' : .1270,
    'F' : .0223,
    'G' : .0202,
    'H' : .0609,
    'I' : .0697,
    'J' : .0015,
    'K' : .0077,
    'L' : .0403,
    'M' : .0241,
    'N' : .0675,
    'O' : .0751,
    'P' : .0193,
    'Q' : .0010,
    'R' : .0599,
    'S' : .0633,
    'T' : .0906,
    'U' : .0276,
    'V' : .0098,
    'W' : .0236,
    'X' : .0015,
    'Y' : .0197,
    'Z' : .0007
}

def split_substrings(ciphertext, keylength):
    """ Splits the ciphertext into 'keylength' substrings and offsets
    them as described in Homework 2 problem 2 """

    substring_list = [''] * keylength
    substring_index = 0
    offset = 0

    # split the ciphertext into substrings
    for letter in ciphertext:
        # offset the letter by which key iteration it is on
        new_letter_value = ord(letter) - offset

        # Can't use modulo, so put it back in range 65-90
        while new_letter_value < 65:
            new_letter_value += 26

        # add it to the list, continue
        substring_list[substring_index] += chr(new_letter_value)
        substring_index += 1
        # If we've gone past the keylength, reset to 0 and increase offset
        if substring_index == keylength:
            substring_index = 0
            offset += 1

    return substring_list

def letter_frequency(string):
    """ Returns a dictionary containing letter frequencies of each
    letter included in the string """

    distribution = dict()

    # Keep a running total in 'distribution' of letter count
    for letter in string:
        if letter not in distribution:
            distribution[letter] = 1
        else:
            distribution[letter] += 1

    return distribution


def index_of_coincidence(ciphertext):
    """ Calculates the index of coincidence as 
    defined in the Vigenere slides """

    distribution = letter_frequency(ciphertext)
    top_sum = 0
    
    # Sum up n(n-1) for each letter n
    for letter in distribution:
        top_sum += (distribution[letter] * (distribution[letter]-1))

    denominator = (len(ciphertext)*(len(ciphertext)-1))
    index_of_coincidence = top_sum / denominator
    return index_of_coincidence

def test_key_lengths():
    """ Find the average index of coincidence for various key lengths. """
    for n in range(1,15):
        n_substrings = split_substrings(CIPHERTEXT,n)
        index_total = 0
        for sub in n_substrings:
            index_total += index_of_coincidence(sub)

        avg_index = index_total / n
        print('Key length:',n,'average index of coincidence:','%.4f' % avg_index)
        # English cipher-text should have roughly .066 index of coincidence. 

def test_g_value(ciphertext, g):
    """ Tests the distribution index of coincidence with an offset of g. 
    High indices ~.066 indicate g is the offset value for the substring. """
    distribution = letter_frequency(ciphertext)
    index_total = 0
    # For each letter, compare its' (decrypted) frequency in the cipher-text
    # to the actual letter's English frequency
    for letter_value in range(65,91):
        letter = chr(letter_value)
        new_letter_value = letter_value + g
        if new_letter_value > 90:
            new_letter_value -= 26

        new_letter = chr(new_letter_value)
        # Default to zero if letter isn't in distribution
        cipher_frequency = distribution.get(new_letter,0)
        english_frequency = ENGLISH_FREQUENCY[letter]

        index_total += english_frequency * cipher_frequency / len(ciphertext)

    return index_total

def compute_key(ciphertext, keylength):
    """ Compute the index of coincidence for all possible offset values (g) and
    print when one is close to an English distribution. """
    substrings = split_substrings(CIPHERTEXT,keylength)
    for sub in substrings:
        print('Testing substring',sub)
        for g in range(0,26):
            tested_value = test_g_value(sub,g)
            if tested_value > .05:
                print('g value of',g,'(letter',chr(g+65)+') gives index of',tested_value)

def decrypt_ciphertext(ciphertext, key):
    """ Decrypts ciphertext assuming a repeated 'key' as the keystring
    where each iteration of 'key' is incremented modulo 26. """
    index = 0
    offset = 0
    plaintext = ''

    for letter in ciphertext:
        letter_value = ord(letter)
        # -65 to account for 'A' = 65, offset to account for repeated key
        letter_value -= ord(key[index]) - 65 + offset

        index += 1
        if index == len(key):
            index = 0
            offset += 1
        # Keep in range 65-90 
        while letter_value < 65:
            letter_value += 26

        plaintext += chr(letter_value)

    return plaintext


test_key_lengths()
print('-----------------')
compute_key(CIPHERTEXT,4)
print('-----------------')
print(decrypt_ciphertext(CIPHERTEXT,'BLOB'))
