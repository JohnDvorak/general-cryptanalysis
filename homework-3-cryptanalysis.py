#! usr/bin/env python3

import sys

x1 = [0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1]
x2 = [0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1]
x3 = [0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1]
x4 = [0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1]

y1 = [1,0,0,0,1,0,0,1,1,0,1,0,1,1,1,0]
y2 = [0,1,0,0,1,1,0,1,0,1,1,1,1,0,0,0]
y3 = [0,0,1,0,0,1,1,0,1,0,1,1,1,1,0,0]
y4 = [0,0,0,1,0,0,1,1,0,1,0,1,1,1,1,0]

def find_cell_value(inputs, outputs):
    """
    returns the linear approximation of the cell at coordinates 
    (inputs, outputs) where inputs and outputs are strings with
    format '0110', '1010', etc. 
    """

    # xor each list of input/output to get different values
    in_vals = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    if inputs[0] == '1':
        in_vals = list_xor(in_vals, x1)
    if inputs[1] == '1':
        in_vals = list_xor(in_vals, x2)
    if inputs[2] == '1':
        in_vals = list_xor(in_vals, x3)
    if inputs[3] == '1':
        in_vals = list_xor(in_vals, x4)

    out_vals = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    if outputs[0] == '1':
        out_vals = list_xor(out_vals, y1)
    if outputs[1] == '1':
        out_vals = list_xor(out_vals, y2)
    if outputs[2] == '1':
        out_vals = list_xor(out_vals, y3)
    if outputs[3] == '1':
        out_vals = list_xor(out_vals, y4)
    
    # number of pairs where in != out
    differences = list_xor(in_vals, out_vals)

    # the cell differences from the middle
    return 8 - sum(differences)

def list_xor(list1, list2):
    """ Returns the pair-wise xor of elements in the lists. """
    new_list = []
    for index in range(len(list1)):
        new_list.append(list1[index] ^ list2[index])

    return new_list

def create_table():
    """ Creates the linear approximation table of each row/col """

    for row in range(16):
        # find the padded value of the row, such as '0100'
        row_bin = bin(row)[2:].zfill(4)
        for col in range(16):
            # find the padded value of the col, such as '0100'
            col_bin = bin(col)[2:].zfill(4)
            cell_val = find_cell_value(row_bin, col_bin)
            cell_val = str(cell_val).rjust(3)
            print(cell_val, end='')
        print()
    print()

create_table()
