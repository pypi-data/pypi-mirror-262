# PyPilot
A python terminal assistant.</br>
Use PyPilot as a regular python terminal and whenever you need the copilot assistance just write it as a comment.</br>
Don't forget to set the API KEY (supports only OPENAI for now).

## Installation
```bash
$ pip install python-pilot
```

## Usage
Run this command in your terminal
```bash
$ pypilot --api-key sk-....
```
or
```bash
$ export OPENAI_API_KEY=sk-... 
$ pypilot
```

## Examples
Here you can see 3 different interactions with the pypilot terminal:
1. `>>> # Create a hasing function`: comment interaction with the llm that produces code
2. `>>> hash_string("hello")`: python expression evaluated by the terminal
3. `>>> # Nice! Can you tell me what are the advantages vs disadvantages of this specific hash alg?`: comment interaction with the llm that produces chat response
```
Python 3.9.5 (v3.9.5:0a7dcbdb13, May  3 2021, 13:17:02) 
[Clang 6.0 (clang-600.0.57)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
============
PyPilot 0.0.7 - Python Terminal Agent
- Use comments (#) to communicate with the agent.
- The agent is aware of the terminal history and locals.
- Type reset(), clear(), history(), ulocals(), dump() or set_api_key() for custom commands.
- When prompt to approve, any key will approve, ctrl+c will cancel.

>>> # Create an hashing function
LLM[tokens:~450]> 
import hashlib

def hash_string(input_string):
    """
    This function takes a string input and returns the SHA-256 hash of the input.
    
    Args:
    input_string (str): The string to be hashed
    
    Returns:
    str: The SHA-256 hash of the input string
    """
    return hashlib.sha256(input_string.encode()).hexdigest()
EXECUTE?>
>>> hash_string("hello")
'2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824'
>>> # Nice! Can you tell me what are the advantages vs disadvantages of this specific hash alg?
LLM[tokens:~661]> 
Advantages of the SHA-256 hash algorithm:
1. Strong security: SHA-256 provides a high level of cryptographic security.
2. Fixed output size: SHA-256 always produces a 256-bit hash value.
3. Fast computation: SHA-256 is computationally efficient.

Disadvantages of the SHA-256 hash algorithm:
1. Deterministic: Same input always produces the same output, which can be a vulnerability in some cases.
2. Vulnerable to collision attacks: While SHA-256 is considered secure, there is always a possibility of collision attacks.
3. Not suitable for password hashing: SHA-256 is designed for cryptographic hashing, not for securely storing passwords.
```

PyPilot terminal supports also running system commands 
```
>>> !pip install numpy
Collecting numpy
Using cached numpy-1.26.4-cp39-cp39-macosx_10_9_x86_64.whl (20.6 MB)
Installing collected packages: numpy
Successfully installed numpy-1.26.4
```

# TODO
- add a way to use history only with headers of functions...
- docker containers
- add a selector step that decide what context the next llm prompt should have:
    - history: code executed (w/wo expressions), errors, llm requests
    - locals: vars, functions, modules
 (full terminal history, locals only) and if the output should be code or chat
- add support in llm config file