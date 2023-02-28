from random import sample

randon = sample(range(0, 100), 100)
rand75 = []
rand25 = []

for x in range(100):
   if x < 75:
      rand75.append(randon[x])
   else:
      rand25.append(randon[x])

print(randon)
print()
print(rand75)
print()
print(rand25)
