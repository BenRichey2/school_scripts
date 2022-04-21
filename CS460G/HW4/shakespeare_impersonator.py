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
from msilib.schema import Error
import os
import sys
import numpy as np
import torch
from torch import nn

FILENAME = "tiny-shakespeare.txt"
BATCH_SIZE = 1   # NOTE: This only works with a batch size of 1.
SEQ_LENGTH = 100 #       I haven't yet figured out how to get this to work for BATCH_SIZE > 1
NUM_LAYERS = 2    # Best setting: 2
HIDDEN_SIZE = 200   # Best setting: 200
EPOCHS = 1000  # Each epoch is about 3 minutes
BENCHMARK = 1.39 # Network has yet to improve upon 1.38
VOCAB_SIZE = 65  # Number of unique characters in data set. Must be updated if training on different data set
START = "First Citizen"
FREQ = 2000     # Number of examples to average loss over before checking training loss

def load_file_data(data_dir):
    try:
        with open(os.path.join(data_dir, FILENAME), "r") as f:
            whole_file = f.readlines()
            data = []
            for i in range(len(whole_file)):
                if len(whole_file[i]) == 1:
                    pass
                else:
                    data.append(whole_file[i])
            return data

    except IOError as err:
        print("ERROR: Unable to open {}\n{}".format(FILENAME, err))
        sys.exit()

def setup(data_dir):
    """
        Perform necessary set up for training and prediction
        @param data_dir: directory containing training data
        @return: device to train on, loaded in file data, dictionary,
                 character encoder, character decoder
    """
    device = "cuda" if torch.cuda.is_available() else "cpu" # Use gpu if possible
    data = load_file_data(data_dir)
    dictionary = set(''.join(data)) # All characters in data set (our dictionary)
    VOCAB_SIZE = len(dictionary) # Update global
    intChar = dict(enumerate(dictionary)) # to convert integers to chars
    charInt = {character: index for index, character in intChar.items()} # to convert chars to ints

    return device, data, dictionary, intChar, charInt

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

def create_pred_one_hot(data):
    """
        Create one hot vector for one example.
        @param data: list of integers representing a sentence.
        @return 3D numpy array to be converted to Tensors later
    """
    one_hot = np.zeros((1, len(data), VOCAB_SIZE), dtype=np.float32)
    for k in range(len(data)):
        one_hot[0, k, data[k]] = 1

    return one_hot

class Fakespeare(nn.Module):

    def __init__(self, input_size, output_size, hidden_size, num_layers, batch_size, device):
        super(Fakespeare, self).__init__()

        self.input_size = input_size
        self.output_size = output_size
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.batch_size = batch_size 
        self.device = device

        # Define recurrent neural network
        self.rnn = nn.RNN(self.input_size, self.hidden_size, self.num_layers, batch_first=True)
        # Define fully connected layer to get actual output
        self.fc = nn.Linear(hidden_size, output_size)

    def forward(self, input):
        output, hidden_state = self.rnn(input, self.init_hidden_state())
        output = output.contiguous().view(-1, self.hidden_size)
        output = self.fc(output)

        return output, hidden_state

    def init_hidden_state(self):
        return torch.zeros(self.num_layers, self.batch_size, self.hidden_size).to(self.device)

def train_model(model, optimizer, loss, input_sequences, target_sequences):
    """
        Train the given model using the given optimizer, loss, input, and target
        sequences.
        @param model: Fakespeare object that is model we want to train
        @param optimizer: a PyTorch optimizer for the given model
        @param loss: a PyTorch loss function
        @param input_sequences: input sequences to train on. Python list of 3D numpy arrays.
        @param target_sequences: target sequences to train on. Python list of 3D numpy arrays.
    """
    avg = 0
    avg_loss = 0
    halt = False
    for epoch in range(EPOCHS):
        if not halt:
            try:
                epoch_loss = 0
                num_losses = 0
                for sequence in range(len(input_sequences)):
                    optimizer.zero_grad()
                    input = input_sequences[sequence]
                    target = target_sequences[sequence]
                    output, hidden = model(input)
                    loss_val = loss(output, target.view(-1).long())
                    avg += loss_val.item()
                    loss_val.backward()
                    optimizer.step()

                    if sequence % FREQ == 0 and sequence != 0:
                        avg_loss = avg / FREQ
                        epoch_loss += avg_loss
                        num_losses += 1
                        if avg_loss < BENCHMARK:
                            print("Loss reached acceptable amount. Ending Training.")
                            return
                        avg = 0
                        print("Epoch: {} Loss: {}".format(epoch, round(avg_loss, 2))) 
                        print("------------")
                
                print("Epoch {} Average Loss: {}".format(epoch, epoch_loss / num_losses))
                print("------------")
                epoch_loss = 0
                num_losses = 0
            except KeyboardInterrupt as err:
                print("Ending training early.")
                halt = True
        else:
            return

    print("Maximum epochs reached. Ending training.")

def training(data_dir, load_model):
    """
        Train a model, either from scratch, or load in a model from disk.
        @param data_dir: directory containing data to train on
        @param load_model: Boolean on whether to load in a model or train a new one
    """
    device, data, dictionary, intChar, charInt = setup(data_dir)
    input_sequences, target_sequences = generate_sequences(data)
    # Convert input and target sequences to number representations
    char_to_int(charInt, input_sequences)
    char_to_int(charInt, target_sequences)
    # Create one hot vectors
    input_one_hots = [create_pred_one_hot(input_sequences[i]) for i in range(len(input_sequences))]
    # Send input and target sequences to gpu
    input_one_hots = [torch.from_numpy(input_one_hots[i]).to(device) for i in range(len(input_one_hots))]
    target_sequences = [torch.Tensor(target_sequences[i]).to(device) for i in range(len(target_sequences))]
    # Begin training!
    model = Fakespeare(VOCAB_SIZE, VOCAB_SIZE, HIDDEN_SIZE, NUM_LAYERS, BATCH_SIZE, device)
    if load_model:
        model.load_state_dict(torch.load(os.path.join(load_model, "fakespeare.pth")))
    model.to(device)
    loss = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters())
    train_model(model, optimizer, loss, input_one_hots, target_sequences)
    torch.save(model.state_dict(), os.path.join(os.getcwd(), "fakespeare.pth"))
    print("Saved model to {}".format(os.path.join(os.getcwd(), "fakespeare.pth")))
    print("\nShowing 100 characters of output with {} as starting sequence:".format(START))
    print(prediction(START, 100, False, charInt, intChar, device, model))
    print("\nEntering testing mode where you can give input to the RNN and it will output 100 characters.")
    print("Press ctrl-c to quit.\n")
    predict_loop(100, charInt, intChar, device, model)

def predict(model, input, charInt, intChar, device):
    """
        Using the given Fakespeare model and input, predict a character.
        @param model: Fakespear object
        @param input: python list of characters
        @param charInt: character to number encoder
        @param intChar: number to character decoder
        @param device: gpu or cpu
        @return: a predicted character and  hidden_state pair
    """
    # Convert input characters to Tensors
    char_input = np.array([charInt[c] for c in input])
    char_input = create_pred_one_hot(char_input)
    char_input = torch.from_numpy(char_input).to(device)
    # Predict a character
    output, hidden = model(char_input)
    # Get character probabilities
    prob = nn.functional.softmax(output[-1], dim=0).data
    # Choose most probable character
    character_index = torch.max(prob, dim=0)[1].item()
    
    # Return prediction and hidden state
    return intChar[character_index], hidden

def prediction(input, length, load_model, charInt, intChar, device, model=None):
    """
        Load in model that has already been trained on FILENAME dataset,
        and predict <length> characters starting with input <input>.
        @param input: string of characters to start predictions.
        @param length: number of desired output characters.
        @param load_model: directory containing fakespeare.pth
        @param charInt: character to integer encoder
        @param intChar: integer to character decoder
        @param device: gpu or cpu
        @param model: Already trained and loaded in model. If this is given, load_model must be False.
        @return: string of characters output by model.
    """
    # Load in model
    if load_model:
        model = Fakespeare(VOCAB_SIZE, VOCAB_SIZE, HIDDEN_SIZE, NUM_LAYERS, BATCH_SIZE, device)
        model.load_state_dict(torch.load(os.path.join(load_model, "fakespeare.pth")))
        model.to(device)

    # Predict!
    chars = [c for c in input]
    size = length - len(chars)
    for i in range(size):
        character, hidden = predict(model, chars, charInt, intChar, device) 
        chars.append(character)
    
    return ''.join(chars)

def predict_loop(length, charInt, intChar, device, model):
    try:
        while True:
           start = input("Enter input text: ")
           print("Network output: ")
           print(prediction(start, length, False, charInt, intChar, device, model)) 

    except KeyboardInterrupt as err:
        print("\nExiting.")
        return

def print_help():
        print("Usage: python3 shakespeare_impersonator.py <args>")
        print("Arguments:")
        print("  Training: python3 shakespeare_impersonator.py --train <data_dir> <load_model>")
        print("     <data_dir>:   Required argument. Directory containing training data.")
        print("     <load_model>: Optional argument. Directory containing 'fakespeare.pth' file.")
        sys.exit()

if __name__ == "__main__":

    try:
        arg = sys.argv[1]

    except IndexError as err:
        print_help()

    if arg == "--train":
        try:
            data_dir = sys.argv[2]

        except IndexError as err:
            print_help()

        try:
            load_model = sys.argv[3]

        except IndexError as err:
            load_model = False

        training(data_dir, load_model)
