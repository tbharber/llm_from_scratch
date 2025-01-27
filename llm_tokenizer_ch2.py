# LLM Tokenizer

# Importing the necessary libraries
import os
import urllib.request
import re

# Download 'The Verdict' by 'Edith Wharton' if it does not exist
if not os.path.exists("the-verdict.txt"):
    url = ("https://raw.githubusercontent.com/rasbt/"
           "LLMs-from-scratch/main/ch02/01_main-chapter-code/"
           "the-verdict.txt")
    file_path = "the-verdict.txt"
    urllib.request.urlretrieve(url, file_path)

# Load the text file
with open("the-verdict.txt", "r", encoding="utf-8") as f:
    raw_text = f.read()


# # Debug
# print("Total number of character:", len(raw_text))
# print(raw_text[:99])

# # Split each word to a seperate item in a list
# text = "Hello, world. This, is a test."
# result = result = re.split(r'([,.:;?_!"()\']|--|\s)', text) # Split by punctuation and whitespace
# result = [item for item in result if item.strip()] # Remove empty strings

# print(result)


# Split each word in story to a seperate item in a list
preprocessed = re.split(r'([,.:;?_!"()\']|--|\s)', raw_text) # Split by punctuation and whitespace
preprocessed = [item.strip() for item in preprocessed if item.strip()] # Remove empty strings

'''
print(preprocessed[:30])
print(len(preprocessed))
'''

# Create new list of only unique words in alphabetical order
all_words = sorted(set(preprocessed))

# Size of the vocabulary list
vocab_size = len(all_words)
# print(vocab_size)

# Create a dictionary with the words as keys and integers as values
vocab = {token:integer for integer,token in enumerate(all_words)}

'''
# Print dictionary with words and integers in order
for i, item in enumerate(vocab.items()):
    print(item)
    if i >= 50:
        break
'''
# Create Tokenizer Class
class SimpleTokenizerV1:
    # Initialize the tokenizer
    def __init__(self, vocab):
        self.str_to_int = vocab
        self.int_to_str = {i:s for s,i in vocab.items()}
    
    # Encode the text
    def encode(self, text):
        # Split by punctuation and whitespace
        preprocessed = re.split(r'([,.:;?_!"()\']|--|\s)', text)
         
        # Remove empty strings                      
        preprocessed = [
            item.strip() for item in preprocessed if item.strip()
        ]

        # Convert the words to integers
        ids = [self.str_to_int[s] for s in preprocessed]
        
        return ids
        
    # Decode the text
    def decode(self, ids):
        # Convert the integers to words
        text = " ".join([self.int_to_str[i] for i in ids])
        
        # Replace spaces before the specified punctuations
        text = re.sub(r'\s+([,.?!"()\'])', r'\1', text)
        
        return text

# Create an instance of the tokenizer and pass in vocab
tokenizer = SimpleTokenizerV1(vocab)


# Test text
text = """"It's the last he painted, you know," 
           Mrs. Gisburn said with pardonable pride."""

# Get ID's back from tokenizer
ids = tokenizer.encode(text)
print(ids)

# Decode the ID's back to text
print (tokenizer.decode(ids))

# Encode the text and decode it back to text in one line
print (tokenizer.decode(tokenizer.encode(text)))

'''
# Test that will fail...
tokenizer = SimpleTokenizerV1(vocab)

text = "Hello, do you like tea. Is this-- a test?"

tokenizer.encode(text)
'''

# Create new list of only unique words in alphabetical order
all_tokens = sorted(list(set(preprocessed)))

# Add special tokens
all_tokens.extend(["<|endoftext|>", "<|unk|>"])

# Create a dictionary with the words as keys and integers as values
vocab = {token:integer for integer,token in enumerate(all_tokens)}
# print (len(vocab.items()))

# Print last 5 items in dictionary
for i, item in enumerate(list(vocab.items())[-5:]):
    print(item)

# Create New Tokenizer Class
class SimpleTokenizerV2:
    # Initialize the tokenizer
    def __init__(self, vocab):
        self.str_to_int = vocab
        self.int_to_str = { i:s for s,i in vocab.items()}
    
    # Encode the text
    def encode(self, text):
        # Split by punctuation and whitespace
        preprocessed = re.split(r'([,.:;?_!"()\']|--|\s)', text)
        
        # Remove empty strings   
        preprocessed = [item.strip() for item in preprocessed if item.strip()]
        
        # Replace unknown words with <|unk|>
        preprocessed = [
            item if item in self.str_to_int 
            else "<|unk|>" for item in preprocessed
        ]

        # Convert the words to integers
        ids = [self.str_to_int[s] for s in preprocessed]
        
        return ids
        
    # Decode the text
    def decode(self, ids):
        # Convert the integers to words
        text = " ".join([self.int_to_str[i] for i in ids])

        # Replace spaces before the specified punctuations
        text = re.sub(r'\s+([,.:;?!"()\'])', r'\1', text)

        return text
    
# Create an instance of the tokenizer and pass in vocab
tokenizer = SimpleTokenizerV2(vocab)

# Test text
text1 = "Hello, do you like tea?"
text2 = "In the sunlit terraces of the palace."

# Join test text with special token
text = " <|endoftext|> ".join((text1, text2))

print(text)

print (tokenizer.encode(text))

print (tokenizer.decode(tokenizer.encode(text)))


#BytePair Encoding

import importlib.metadata
import tiktoken

#Print version
print("tiktoken version:", importlib.metadata.version("tiktoken"))

#Initialize tokenizer
tokenizer = tiktoken.get_encoding("gpt2")

#Set sample text
text = (
    "Hello, do you like tea? <|endoftext|> In the sunlit terraces"
     "of someunknownPlace."
)

#Encode text to integers
integers = tokenizer.encode(text, allowed_special={"<|endoftext|>"})
print(integers)

#Decode integers back to text
strings = tokenizer.decode(integers)
print(strings)

