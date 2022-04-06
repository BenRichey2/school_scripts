"""
    Shakespeare Impersonator
    by Ben Richey

        This script implements a character recurrent neural network
    using PyTorch for nitty gritty of the model, training, optimizer,
    loss, etc.
        The model trains on the tiny Shakespeare dataset, provided
    by Dr. Brent Harrison at the Univeristy of Kentucky as part of
    homework assignment 4 for CS460G (Machine Learning) at UK.
        The output of the RNN is characters, and ideally, sentences
    that make sense, and sound like something Shakespear would write.

    Copyright © 2022 Ben Richey

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the “Software”), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is furnished
    to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all copies
    or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
    INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
    PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE
    FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
    ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
    THE SOFTWARE
"""
import os
import sys

import ipdb

FILENAME = "tiny-shakespeare.txt"

def load_file_data(data_dir):
    try:
        with open(os.path.join(data_dir, FILENAME), "r") as f:
            return f.readlines()

    except IOError as err:
        print("ERROR: Unable to open {}\n{}".format(FILENAME, err))
        sys.exit()

def generate_sequences(data):
    """
        Generate input and target sequences for each example. The input sequence for one
        example is every character but the last, and the output sequence is every
        character but the first.
        @param data: list of exampels (sentences), where each sentence ends in a newline
        @return: two lists -> one for the input sequence for each example and another for
                 the target sequence for each example.
    """
    input_sequences = []
    target_sequences = []
    for i in range(len(data)):
        input_sequences.append(data[i][:-1])
        target_sequences.append(data[i][1:])

    return input_sequences, target_sequences

def char_to_int(mapping, data):
    """
        Converts a list of sentences to integers using the given mapping.
        @param mapping: dict that provides mapping from chars to ints.
        @param data: list of sentences
    """
    for i in range(len(data)):
        data[i] = [mapping[character] for character in data[i]]

if __name__ == "__main__":
    try:
        data_dir = sys.argv[1]

    except IndexError as err:
        print("Usage: python3 shakespeare_impersonator.py <path to directory containing data file>")
        sys.exit()

    data = load_file_data(data_dir)
    dictionary = set(''.join(data)) # All characters in data set (our dictionary)
    intChar = dict(enumerate(dictionary)) # to convert integers to chars
    charInt = {character: index for index, character in intChar.items()} # to convert chars to ints
    input_sequences, target_sequences = generate_sequences(data)
    # Convert input and target sequences to number representations
    char_to_int(charInt, input_sequences)
    char_to_int(charInt, target_sequences)