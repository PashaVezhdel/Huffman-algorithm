import heapq
import re
from collections import Counter

class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def clean_text(text):
    return re.sub(r'[^a-zA-Zа-яА-ЯіІїЇєЄ0-9 ]', '', text).lower()

def build_huffman_tree(freq_dict):
    heap = [Node(char, freq) for char, freq in freq_dict.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = Node(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(heap, merged)
    return heap[0]

def build_huffman_codes(tree, prefix='', code_dict=None):
    if code_dict is None:
        code_dict = {}
    if tree is None:
        return code_dict
    if tree.char is not None:
        code_dict[tree.char] = prefix
    build_huffman_codes(tree.left, prefix + '0', code_dict)
    build_huffman_codes(tree.right, prefix + '1', code_dict)
    return code_dict

def huffman_compress(text):
    cleaned_text = clean_text(text)
    freq_dict = Counter(cleaned_text)
    tree = build_huffman_tree(freq_dict)
    codes = build_huffman_codes(tree)
    compressed = ''.join(codes[char] for char in cleaned_text)
    return compressed, codes, freq_dict

def huffman_decompress(compressed_text, codes):
    reverse_codes = {code: char for char, code in codes.items()}
    decoded_text = ""
    temp_code = ""
    for bit in compressed_text:
        temp_code += bit
        if temp_code in reverse_codes:
            decoded_text += reverse_codes[temp_code]
            temp_code = ""
    return decoded_text


def corrupt_message(compressed_text, error_rate):
    corrupted_text = list(compressed_text)
    total_bits = len(compressed_text)
    error_count = int(total_bits * error_rate)

    for i in range(0, total_bits, total_bits // (error_count if error_count > 0 else 1)):
        corrupted_text[i] = '1' if corrupted_text[i] == '0' else '0'

    return ''.join(corrupted_text)

import matplotlib.pyplot as plt

def plot_character_frequencies(freq_dict):
    chars, freqs = zip(*sorted(freq_dict.items(), key=lambda x: x[1], reverse=True))

    plt.figure(figsize=(10, 5))
    plt.bar(chars, freqs)
    plt.xlabel('Symbols')
    plt.ylabel('Frequency.')
    plt.title('Frequency of characters in the text')
    plt.show()

from tabulate import tabulate

if __name__ == "__main__":
    error_rate = 0.005  # Рівень пошкодження

    input_text = input("Enter the text to compress: ")
    clean_text_data = clean_text(input_text)
    compressed, codes, freq_dict = huffman_compress(clean_text_data)

    print(f"Original text: {input_text}")
    print("-" * 50)
    print(f"Cleaned text: {clean_text_data}")
    print("-" * 50)
    print(f"Compressed text: {compressed}")
    print("-" * 50)

    damaged_compressed_text = corrupt_message(compressed, error_rate)
    print(f"Corrupted compressed message: {damaged_compressed_text}")
    print("-" * 50)

    decompressed_text = huffman_decompress(compressed, codes)
    print(f"Decoded text: {decompressed_text}")
    print("-" * 50)

    decompressed_damaged_text = huffman_decompress(damaged_compressed_text, codes)
    print(f"Decrypted text with a damaged message: {decompressed_damaged_text}")
    print("-" * 50)

    print("\nCharacter frequencies:")
    freq_table = [(char, freq) for char, freq in freq_dict.items()]
    print(tabulate(freq_table, headers=["Символ", "Частота"], tablefmt="grid"))
    print("-" * 50)

    print("\nHuffman codes:")
    codes_table = [(char, code) for char, code in codes.items()]
    print(tabulate(codes_table, headers=["Символ", "Код"], tablefmt="grid"))
    print("-" * 50)

    plot_character_frequencies(freq_dict)