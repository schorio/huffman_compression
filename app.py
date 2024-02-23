import heapq
import os

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