from collections import Counter

counter1 = Counter({'a': 2.5, 'b': 5.0})
counter2 = Counter({'a': 3.1, 'c': 7.2})

result = counter1 + counter2
print(result)