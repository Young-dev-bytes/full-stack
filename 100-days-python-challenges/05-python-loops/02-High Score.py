students_scores = input("Input a list of students heights").split()

for n in range(0, len(students_scores)): 
    print(n)
    students_scores[n] = int(students_scores[n])


print(max(students_scores))
print(min(students_scores))

heightest_score = 0
for score in students_scores:
    if score > heightest_score:
      heightest_score = score
print(f"the heightest score in the code is: {heightest_score}")    



