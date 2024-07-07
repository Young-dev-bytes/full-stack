
students_heights = input("Input a list of students heights").split()

for n in range(0, len(students_heights)): 
    print(n)
    students_heights[n] = int(students_heights[n])
print(students_heights)  

# print(sum(students_heights))
# print(len(students_heights))
# total_height = sum(students_heights)
# number_of_students = len(students_heights)


# using for loop
total_height = 0
number_of_students = 0
for each_height in students_heights:
    total_height += each_height
    number_of_students += 1
print(total_height)
print(number_of_students)  



# using for loop

# for student in students_heights:
#     number_of_students += 1
# print(number_of_students)    


average_height = round(total_height / number_of_students)
print(average_height)

