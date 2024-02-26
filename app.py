import heapq
import os
import pickle
import customtkinter as ctk
from tkinter import filedialog

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
       

# Save decompressed text to a file
def save_decompressed_text(decompressed_text):
   file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                          filetypes=[("Text files", "*.txt")])
   if file_path:
       with open(file_path, 'w') as file:
           file.write(decompressed_text)
       
       
# Compress button clicked
def compress_button_clicked():
   file_path = filedialog.askopenfilename()
   if file_path:
       compressed_data, tree, codes = compress_file(file_path)
       output_file_path = filedialog.asksaveasfilename(defaultextension=".bin",
                                                     filetypes=[("Binary files", "*.bin")])
       if output_file_path:
        save_compressed_file(compressed_data, tree, codes, output_file_path)
        
        result = ctk.CTk()
        result.title("Résultat")
        result.geometry("250x50")
        result.mainloop()


# Decompress button clicked
def decompress_button_clicked():
   compressed_file_path = filedialog.askopenfilename(filetypes=[("Binary files", "*.bin")])
   if compressed_file_path:
       decompressed_text = decompress_file(compressed_file_path)
       save_decompressed_text(decompressed_text)


# Create main window
root = ctk.CTk()
root.title("Huffman Compression/Decompression")
root.geometry("200x100")



# Create buttons
compress_button = ctk.CTkButton(root, text="Compresser un fichier", command=compress_button_clicked)
decompress_button = ctk.CTkButton(root, text="decompresser un fichier", command=decompress_button_clicked)

# Layout buttons
compress_button.pack(expand=True)
decompress_button.pack(expand=True)

# Run application
root.mainloop()
