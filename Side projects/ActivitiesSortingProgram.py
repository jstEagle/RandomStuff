import csv
from datetime import datetime

# Alter this to change which year groups will be left out when sorting term 4!
study_leave_years = [11, 12, 13]

# Function to check if a student has been fully assigned
def checkFull(student):
    total = 0
    
    # Calculate the total duration of activities the student is assigned to
    for activity in student.activities:
        total += activity.duration
        
    # Mark the student as fully assigned if the total duration is exactly 2 hours
    if total == 2:
        student.full = True
    elif total > 2:
        # If overassigned, remove the last activity and recheck
        student.activities.pop()
        checkFull(student)
    elif total < 2:
        # If underassigned, mark as not fully assigned
        student.full = False

# Create a student class to handle all the student objects
class Student:
    def __init__(self, name, year, choices, email):
        self.name = name
        self.year = year
        self.choices = choices
        self.activities = [] # List to store assigned activities
        self.email = email
        self.full = False # Flag to track if fully assigned

# Create an Activity class to handle all the activity objects 
class Activity:
    def __init__(self, name, minCap, maxCap, duration, years):
        self.name = name
        self.minCap = minCap
        self.maxCap = maxCap
        self.duration = duration
        self.years = years
        self.students = [] # List to store assigned students
        
    def addStudent(self, student):
        # Add student to the activity's student list
        self.students.append(student)
        # Add the activity to the student's activities list
        student.activities.append(self)
        
        # Check if the student is fully assigned after adding this activity
        checkFull(student)
    
    def removeStudent(self, student):
        # Remove student from the activity's student list
        self.students.remove(student)
        # Remove the activity from the student's activities list
        student.activities.remove(self)
        
        # Check if the student needs to be marked as not fully assigned
        checkFull(student)

# Stable marriage algorithm for 2 hour activities 
# The first run, only students that have a 2 hour activity in their top 3 choices will be assigned that activity
def stable_matching_2(student_list, activities_table, error):
    free_students = student_list.copy()  # Create a copy of the list
    done_students = []
    error_students = []
    
    while free_students:
        student = free_students.pop(0)
        
        # Include all choices for students with errors, only top 3 otherwise
        if error:
            choices = student.choices
        else:
            choices = student.choices[0:3]
        
        for activity_name in choices:
            activity = activities_table.get(activity_name)
            
            if activity and len(activity.students) < activity.maxCap and student.year in activity.years and activity.duration == 2:
                activity.addStudent(student)
                
                if student.full:
                    done_students.append(student)
                    
                break
            elif activity and student.year in activity.years and activity.duration == 2:
                least_preferred = min(activity.students, key=lambda s: s.choices.index(activity_name))
                
                if student.choices.index(activity_name) < least_preferred.choices.index(activity_name):
                    activity.removeStudent(least_preferred)
                    activity.addStudent(student)
                    free_students.append(least_preferred)
                    
                    if student.full:
                        done_students.append(student)
                    
                    if least_preferred in done_students:
                        done_students.remove(least_preferred)
                    break
        
        if not student.full:
            error_students.append(student)
    
    temp_list = stable_matching(error_students, activities_table)
    
    return done_students + temp_list
                  
# Stable marriage algorithm for single hour activities
def stable_matching(student_list, activities_table):
    free_students  = student_list.copy()  # Create a copy of the list
    done_students = []
    error_students = []
    
    while free_students:
        student = free_students.pop(0)
        
        for activity_name in student.choices:
            activity = activities_table.get(activity_name)
            
            if activity and len(activity.students) < activity.maxCap and student.year in activity.years and not activity in student.activities and activity.duration != 2:
                activity.addStudent(student)
                
                if not student.full:
                    free_students.append(student)
                break
            elif activity and student.year in activity.years and not activity in student.activities and activity.duration != 2:
                least_preferred = min(activity.students, key=lambda s: s.choices.index(activity_name))
                
                if student.choices.index(activity_name) < least_preferred.choices.index(activity_name):
                    activity.removeStudent(least_preferred)
                    activity.addStudent(student)
                    free_students.append(least_preferred)
                    
                    if least_preferred in done_students:
                        done_students.remove(least_preferred)
                    
                    if not student.full:
                        free_students.append(student)
                    break
        else:
            error_students.append(student)
        
        if student.full:
            done_students.append(student)
            
    return done_students + error_students
            
# Get the term for which the students and activities should be assigned 
term = int(input("Enter the term number you would like to sort: \n"))

# Get the paths to the required .csv files
student_list_path = input("Enter the path to the Student .csv file: \n")
activities_list_path = input("Enter the path to the Activities .csv file: \n")

activities_table = {}
student_list = []

# Extract and handle all the activities in the activities .csv file
with open(activities_list_path, 'r', newline='') as file:
    reader = csv.DictReader(file)
    
    for row in reader:
        name = row['Name']
        minCap = int(row['MinCapacity'])
        maxCap = int(row['MaxCapacity'])
        duration = int(row['Duration'])
        temp_years = row['Years']
        temp_terms = row['Terms']
        
        terms = [int(num) for num in temp_terms.split(',')]
        years = [int(num) for num in temp_years.split(',')]
        
        if name not in activities_table and int(term) in terms:
            activities_table[name] = Activity(name, minCap, maxCap, duration, years)

current_year = datetime.now().year

# Extract and handle all the activities in the activities .csv file
with open(student_list_path, 'r', newline='') as file:
    reader = csv.DictReader(file)
    
    for row in reader:
        name = row['First name'] + ' ' + row['Surname']
        year = int(row[f'Year group (as of {current_year})'].split(' ')[1])
        choices = [row[f'[Choice {i+1}]'] for i in range(10)]
        email = row['Email address']
        
        for choice in choices:
            if choice not in activities_table.keys():
                choices.remove(choice)

        if term != 4:
            student = Student(name, year, choices, email)
            student_list.append(student)
        elif term == 4 and not year in study_leave_years:
            student = Student(name, year, choices, email)
            student_list.append(student)

copy_students = student_list
final_student_list = stable_matching_2(student_list, activities_table, False)

error_students = []

# Handle edge cases which have not been sorted properly the first time
# this also accounts for activities that have not had their minimum capacity filled
for student in final_student_list:
    checkFull(student)
    
    if student.full == False:
        error_students.append(student)
        final_student_list.remove(student)
        
        student.activities = []
    
    for activity in student.activities:
        if len(activity.students) < minCap:
            student.activities.remove(activity)
            student.choices.remove(activity.name)
            error_students.append(student)

final_student_list = final_student_list + stable_matching_2(error_students, activities_table, True)

# Create the result file
file_path = f'Term{term}_sorted_activities.csv'

# Write all the information to the result file
with open(file_path, 'w', newline='') as file:
    writer = csv.writer(file)
    
    header = ['Email Address', 'First name', 'Surname', 'Year group (as of 2024)', 'First Hour', 'Second Hour']
    writer.writerow(header)
    
    for student in copy_students:
        if len(student.activities) == 1:
            row = [student.email, student.name.split(' ')[0], student.name.split(' ')[1], f'yr {student.year}', student.activities[0].name, student.activities[0].name]
        elif len(student.activities) == 2:
            row = [student.email, student.name.split(' ')[0], student.name.split(' ')[1], f'yr {student.year}', student.activities[0].name, student.activities[1].name]

        writer.writerow(row)
        
# Print all the results to the console to check everything went well
# Results are printed colour coded to make sense of the data easier
# First Choice - Green
# Second Choice - Yellow
# Third Choice - Red
# If not in top 3 choices - White
RESET = '\033[0m'
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'

for student in copy_students:
    for activity in student.activities:
        if activity.name == student.choices[0]:
            print(GREEN + student.name + ": " + str(student.year) + ": "+ activity.name + RESET)
        elif activity.name == student.choices[1]:
            print(YELLOW + student.name + ": " + str(student.year) + ": " + activity.name + RESET)
        elif activity.name == student.choices[2]:
            print(RED + student.name + ": " + str(student.year) + ": " + activity.name + RESET)
        else:
            print(student.name + ": " + activity.name)

# Note: The Activities.csv and Students.csv file MUST be in the same directory as the program when the program is run.