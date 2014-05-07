#! usr/bin/env python3

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

translate_dict = {
    'A' : 'h',
    'B' : 'b',
    'C' : 'p',
    'D' : 'm',
    'E' : 'y',
    'F' : 'v',
    'G' : 'e',
    'H' : ' ', # H is not present in the ciphertext
    'I' : 'l',
    'J' : ' ', # J is not present in the ciphertext
    'K' : ' ', # H is not present in the ciphertext
    'L' : 'c',
    'M' : 'a',
    'N' : 'w',
    'O' : 'g',
    'P' : 'q', # Only used once
    'Q' : 'n',
    'R' : 'f',
    'S' : 'o',
    'T' : 's',
    'U' : 'd',
    'V' : 'u',
    'W' : 'k',
    'X' : 'i',
    'Y' : 'r',
    'Z' : 't'
}

def print_letter_distribution(ciphertext):
    """
    Prints the letter distribution of ciphertext from 
    highest frequency to lowest.
    """
    distribution = dict()

    for character in ciphertext:
    # Keep a running total in 'distribution' of character count
        if character not in distribution:
            distribution[character] = 1
        else:
            distribution[character] += 1

    # Print the number of unique letters in the ciphertext
    print("Unique characters in ciphertext:", len(distribution), '\n')
    
    # Print the highest frequency letters first
    for char in sorted(distribution, key=distribution.get, reverse=True):
        print(char,'has a frequency of',distribution[char]/4.01)
    print()

def translate(ciphertext):
    """
    Translate the ciphertext using the 
    translate_dict as a substitution table.
    """
    plaintext = ''
    for character in ciphertext:
        plaintext += translate_dict[character]

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


print('Original ciphertext:\n', ORIGINAL_CIPHERTEXT, '\n')
print("Total lengths of ciphertext:", len(ORIGINAL_CIPHERTEXT))

print_letter_distribution(ORIGINAL_CIPHERTEXT)

count_digraphs(ORIGINAL_CIPHERTEXT)
count_trigraphs(ORIGINAL_CIPHERTEXT)

print('Translation:\n', translate(ORIGINAL_CIPHERTEXT))
