import pandas as pd
from data_loader import load_data, prepare_course_counts
from room_allocation import allocate_rooms
from student_assignment import assign_students_to_rooms

# Load and preprocess the data
ip_1, ip_2, room_cap = load_data()

# Calculate the number of students enrolled in each course
course_counts = prepare_course_counts(ip_1)

# Add buffer to the room capacity
buffer = int(input("Enter the buffer percentage (e.g., 5 for 5%): ")) / 100
room_cap["effective_capacity"] = (room_cap["Exam Capacity"] * (1 - buffer)).astype(int)

# Calculate buffered capacity
room_cap["buffered_capacity"] = room_cap["Exam Capacity"] - room_cap["effective_capacity"]

# Allocate rooms
final_allocations = pd.DataFrame()

for _, row in ip_2.iterrows():
    for shift in ["Morning", "Evening"]:  # Loop through morning and evening shifts
        shift_courses = pd.DataFrame({'course_code': row[shift].split('; ')}).dropna()
        shift_courses['course_code'] = shift_courses['course_code'].str.strip()
        shift_courses['count'] = shift_courses['course_code'].apply(
            lambda code: ip_1[ip_1['course_code'] == code].shape[0]
        )
        shift_courses = shift_courses.sort_values(by="count", ascending=False).reset_index(drop=True)

        # Allocate rooms for the shift
        shift_allocations = allocate_rooms(shift_courses, room_cap, buffer)

        # Add Date and Shift columns
        shift_allocations["Exam Date"] = row["Date"]
        shift_allocations["Shift"] = shift

        # Append to final allocations
        final_allocations = pd.concat([final_allocations, shift_allocations], ignore_index=True)

        # Reset effective capacity and buffered capacity for the next allocation
        room_cap["effective_capacity"] = (room_cap["Exam Capacity"] * (1 - buffer)).astype(int)
        room_cap["buffered_capacity"] = room_cap["Exam Capacity"] - room_cap["effective_capacity"]

# Assign students to rooms
final_with_students = assign_students_to_rooms(ip_1, final_allocations)

# Reorder columns for clarity
final_with_students = final_with_students[["Exam Date", "Shift", "course_code", "room_no", 
                                           "num_students_allocated", "vacant_seats", "buffered_capacity", "Roll_no"]]

# Save outputs
final_with_students.to_excel("Final_Seating_Arrangement.xlsx", index=False)
final_with_students.to_csv("Final_Seating_Arrangement.csv", index=False)

# Final Message
print("Room assignments completed. Outputs saved as 'Final_Seating_Arrangement.xlsx' and 'Final_Seating_Arrangement.csv'.")