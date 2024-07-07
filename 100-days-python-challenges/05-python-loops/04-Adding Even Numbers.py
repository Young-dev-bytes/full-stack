
total = 0

for number in range(0, 101, 2):
    total += number
# print(total)   

total2 = 0

for number in range(0, 101):
    if number % 2 == 0:
      total2 += number
print(total2)  
