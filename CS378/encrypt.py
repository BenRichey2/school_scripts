#!/usr/bin/python3
import sys

KEY = [[1, 2], [3, 2]]

def encryptBlock(plaintext):
    ciphertext = []
    ciphertext.append((plaintext[0] * KEY[0][0] + plaintext[1] * KEY[0][1]) % 26)
    ciphertext.append((plaintext[0] * KEY[1][0] + plaintext[1] * KEY[1][1]) % 26)
    return ciphertext

def sepBlocks(plaintext):
    blocks = []
    if len(plaintext) % 2 != 0:
        print("Ignore last character of ciphertext")
        plaintext.append(0)
    for i in range(0, len(plaintext), 2):
        blocks.append([plaintext[i], plaintext[i+1]])
    return blocks

if __name__ == "__main__":
    plaintext = sys.argv[1]
    plaintextNum = [ord(char) - 97 for char in plaintext.lower()]
    blocks = sepBlocks(plaintextNum)
    ciphertext = [] 
    for block in blocks:
        C = encryptBlock(block)
        ciphertext.append(C)
    print(ciphertext)
