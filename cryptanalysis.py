#! usr/bin/env python3

"""
I intend this to be a crytanalysis suite that can analyze an arbitrary
ciphertext and provide details on what the encryption method might be,
what the key might look like, and/or a potential cipher text solution.
"""

ORIGINAL_CIPHERTEXT = "\
NAGQNXIIZAGBGIIYXQOMQUGQUZAXTNGMYXQGTTASNISQO\
AMFGZAGEZVOOGUZAGIGMTAMQUTZYMXQGUMCMYZDECMLWS\
RVQYVIEASVQUTXLMQQSZTZMYZZAGDMOMXQSQMPVMYYESR\
WQSNIGUOGZAGEAMZGZSAVQZXLMQAMVIZAGDMQUVYOGZAG\
DQSDSYGQSDSYGLMQXGQUVYGZSBGMYZAGBYVQZSRZAGBSS\
WTZAMZIXGSVZSQZAGUGTWTMRVIIZAYGGTLSYGSRTGFGYM\
IXQTVIZTSRBISZZGUCMOGTMQUTLYMNISRTISFGQIENSYW\
ZAMZZAGEAMFGSRRGYGUDGXMDTXLWMQUZXYGUDSYGZAMQM\
QEZAYMIIVCSQZAGNSSUTZMLWTNSYWXQONGMYXGUIE"

# Letter frequencies taken from Table 1.1 from Understanding Crypto, page 9
ENGLISH_LETTER_FREQUENCY = {
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

substitution_dict = {
    'A' : '_',
    'B' : '_',
    'C' : '_',
    'D' : '_',
    'E' : '_',
    'F' : '_',
    'G' : '_',
    'H' : '_',
    'I' : '_',
    'J' : '_',
    'K' : '_',
    'L' : '_',
    'M' : '_',
    'N' : '_',
    'O' : '_',
    'P' : '_',
    'Q' : '_',
    'R' : '_',
    'S' : '_',
    'T' : '_',
    'U' : '_',
    'V' : '_',
    'W' : '_',
    'X' : '_',
    'Y' : '_',
    'Z' : '_'
}

def find_letter_distribution(ciphertext, percentage = False):
    """ 
    Returns a dictionary containing letter frequencies of each
    letter included in the string  (Normalized if 'percentage',
    absolute otherwise.)
    """
    distribution = dict()

    for character in ciphertext:
    # Keep a running total in 'distribution' of character count
        if character not in distribution:
            distribution[character] = 1
        else:
            distribution[character] += 1
    
    # Normalize the data if percentage is requested
    if percentage:
        for char in distribution:
            distribution[char] /= len(ciphertext)

    return distribution
    
    # Print the highest frequency letters first
#    for char in sorted(distribution, key=distribution.get, reverse=True):
#        print(char,'has a frequency of',distribution[char])
    

def translate_from_dictionary(ciphertext, translate):
    """
    Translate the ciphertext using the 
    'translate' dictionary as a substitution table.
    """
    plaintext = ''
    for character in ciphertext:
        plaintext += translate[character]

    return plaintext

def count_digraphs(ciphertext):
    """
    Count and print the most frequent 2-letter 
    combinations in the ciphertext.
    """
    # Zip the ciphertext with an offset to get 2char elements
    two_letter_set = [x+y for x,y in zip(*[ciphertext[i:] 
                       for i in range(2)])]

    digraph_frequency = dict()

    for digraph in two_letter_set:
        if digraph not in digraph_frequency:
            digraph_frequency[digraph] = 1
        else:
            digraph_frequency[digraph] += 1

    print('2-letter sequences:')
    for digraph in sorted(digraph_frequency, 
                          key=digraph_frequency.get, 
                          reverse=True):
        
        if digraph_frequency[digraph] > 5:
            print(digraph, digraph_frequency[digraph])
    print()


def count_trigraphs(ciphertext):
    """
    Count and print the most frequent 
    3-letter combinations in ciphertext.
    """
    # Zip the ciphertext with an offset to get 3char elements
    three_letter_set = [x+y+z for x,y,z in zip(*[ciphertext[i:] 
                       for i in range(3)])]

    trigraph_frequency = dict()
    
    for trigraph in three_letter_set:
        if trigraph not in trigraph_frequency:
            trigraph_frequency[trigraph] = 1
        else:
            trigraph_frequency[trigraph] += 1

    print('3 letter sequences:')
    for trigraph in sorted(trigraph_frequency, 
                          key=trigraph_frequency.get, 
                          reverse=True):
        
        if trigraph_frequency[trigraph] > 3:
            print(trigraph, trigraph_frequency[trigraph])
    print()

def vigenere_split_substrings(ciphertext, keylength):
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

def index_of_coincidence(ciphertext):
    """ Calculates the index of coincidence of ciphertext, as 
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

def general_analysis(ciphertext):
    """ 
    Prints general analysis of a ciphertext to the console.
    Included are: length, unique letters, ...
    """
    print('Total length of ciphertext:', len(ciphertext))
    print('Unique letters:',len(find_letter_distribution(ciphertext)))

count_digraphs(ORIGINAL_CIPHERTEXT)
count_trigraphs(ORIGINAL_CIPHERTEXT)

print('Translation:\n', translate(ORIGINAL_CIPHERTEXT))
