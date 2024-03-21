"""
* Walrus Operator:  ':='
* Syntax: name := expr
*
* Purpose
*   - Allows assignment and return of a value in the same expression 
"""

#Example
# Without Walrus
walrus : bool = False
print(walrus) # False 

print(walrus := False) # False 

print('\nwithout walrus')
#Without Walrus Operators
inputs : list = list()
current : str = input("Write something\n> ")
while current != "quit":
    inputs.append(current)
    current = input("Write Something\n> ")

print('\nwith walrus')
#With Walrus
while (current := input("Write something\n> ")) != "quit":
    inputs.append(current)
