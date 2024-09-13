from collections import deque
de = deque(maxlen=3)
de.append(4)
de.append(3)
de.append(2)
de.append(1)
print("\nThe deque after appending at right is : ")
print(de)

print(de[0])