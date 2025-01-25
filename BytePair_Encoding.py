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

#Encode text
integers = tokenizer.encode(text, allowed_special={"<|endoftext|>"})
print(integers)

#Decode text
strings = tokenizer.decode(integers)
print(strings)