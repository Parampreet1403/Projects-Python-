# Parampreet Singh - 22/06/20
# Data structures in Python

"""
Type            Indexing?       Changeable?

List:           Ordered,        Mutable,               Duplicates
Tuple:          Ordered,        Unmutable,             Duplicates  
Set:            Unodered,       addable/removable,     NO Duplicates   
Dictionary:     Unordered,      Mutable,               NO Duplicates
"""
# Set is a collection with no indexing

# Declaring
myList = [1, 3, 4.9, "Name", 3]
myTuple = (1, 3, 4.9, "Name", 3)
mySet = {1, 3, 4.9, "Name", 3}
myDict = {0: "First", "B": 2, "C": "Three"}


# Accessing
print(myList[1])
print(myTuple[1])
print(3 in mySet)  # Bool
print(myDict["B"])


# Adding and removing from a set
mySet.add("new item")
print(mySet)
mySet.update({"More", "Items"})
print(mySet)
mySet.remove("More")  # Remove
print(mySet)


# Dictionaries
print(myDict)
myDict["New Key"] = "New Value"
print(myDict)

# You cannot add two dictionaries together
# However you can use Dict.update(new_dict)


# Lists
L2 = myList
print(L2)
L2[1] = "New Value"
print(L2)
print(myList)
# Both have changes as Lists are mutable
# Therefore the location of memory has been adjusted
# To change only L2 need to create a copy
L3 = myList.copy()
print(L3)
L3[1] = "Copy Value"
print(myList)
print(L3)
