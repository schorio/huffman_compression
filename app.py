import heapq
import os
import pickle

# Class Algo
class Algo:
   def __init__(self, char, freq):
       self.char = char
       self.freq = freq
       self.left = None
       self.right = None

   def __lt__(self, other):
       return self.freq < other.freq

# Build Huffman Tree
def build_huffman_tree(text):
   frequency = {char: text.count(char) for char in set(text)}
   priority_queue = [Algo(char, freq) for char, freq in frequency.items()]
   heapq.heapify(priority_queue)
   
   while len(priority_queue) > 1:
       left = heapq.heappop(priority_queue)
       right = heapq.heappop(priority_queue)
       merged = Algo(None, left.freq + right.freq)
       merged.left = left
       merged.right = right
       heapq.heappush(priority_queue, merged)
   
   return priority_queue[0]


# Create codes from Huffman Tree
def create_codes(algo, current_code="", codes={}):
   if algo is not None:
       if algo.char is not None:
           codes[algo.char] = current_code
       codes = create_codes(algo.left, current_code + "0", codes)
       codes = create_codes(algo.right, current_code + "1", codes)
   return codes


# Encode text
def huffman_encoding(text, codes):
   return ''.join(codes[char] for char in text)


# Bitstring to bytes
def bitstring_to_bytes(s):
   return int(s, 2).to_bytes((len(s) + 7) // 8, byteorder='big')

# Bytes to bitstring
def bytes_to_bitstring(b):
   return ''.join(format(byte, '08b') for byte in b)


# Compress file
def compress_file(file_path):
   with open(file_path, 'r') as file:
       text = file.read()
       tree = build_huffman_tree(text)
       codes = create_codes(tree)
       encoded_text = huffman_encoding(text, codes)
       return encoded_text, tree, codes
   

# Decompress file
def decompress_file(compressed_file_path):
   with open(compressed_file_path, 'rb') as compressed_file:
       b, tree, codes, padding = pickle.load(compressed_file)
   
   encoded_text = bytes_to_bitstring(b)[padding:]
   
   current_algo = tree
   decoded_text = ''
   for bit in encoded_text:
       current_algo = current_algo.left if bit == '0' else current_algo.right
       if current_algo.char is not None: # Leaf algo
           decoded_text += current_algo.char
           current_algo = tree # Return to the root for the next character
   
   return decoded_text


# Save compressed file
def save_compressed_file(compressed_data, tree, codes, file_path):
   padded_encoded_text = compressed_data
   padding = 8 - (len(padded_encoded_text) % 8)
   padded_encoded_text = "0" * padding + padded_encoded_text
   b = bitstring_to_bytes(padded_encoded_text)
   
   with open(file_path, 'wb') as file:
       pickle.dump((b, tree, codes, padding), file)
