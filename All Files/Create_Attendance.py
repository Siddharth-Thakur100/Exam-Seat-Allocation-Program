import pandas as pd
import os

# Load data from Final_Seating_Arrangement.csv
final_with_students = pd.read_csv("Final_Seating_Arrangement.csv")

# Read ip_4 to get student names
ip_4 = pd.read_csv("ip_4.csv")

# Ensure correct column names in ip_4
ip_4.columns = ['Roll', 'Name']

# Clean data to ensure proper merging
final_with_students['Roll_no'] = final_with_students['Roll_no'].astype(str).str.strip()
ip_4['Roll'] = ip_4['Roll'].astype(str).str.strip()

# Create a folder for attendance sheets
attendance_folder = "attendance_sheets"
os.makedirs(attendance_folder, exist_ok=True)

# Generate attendance sheets for each room, date, and shift
for (exam_date, shift, room_no), group in final_with_students.groupby(['Exam Date', 'Shift', 'room_no']):
    # Create a filename for the attendance sheet
    formatted_date = exam_date.replace('/', '-')  # Format date to be file-safe
    file_name = f"{attendance_folder}/attendance_{room_no}_{formatted_date}_{shift}.csv"
    
    # Ensure roll numbers are properly separated into rows
    group['Roll_no'] = group['Roll_no'].str.split(', ')  # Split multiple roll numbers into lists
    expanded_students = group.explode('Roll_no').reset_index(drop=True)  # Expand each roll number into its own row

    # Merge with ip_4 to get student names based on Roll_no
    attendance = pd.merge(expanded_students[['Roll_no']], ip_4, left_on='Roll_no', right_on='Roll', how='left')[['Roll_no', 'Name']]
    
    # Add an empty Signature column
    attendance['Signature'] = ''  # Empty column for signatures
    
    # Write the attendance sheet to a CSV file
    attendance.to_csv(file_name, index=False)
    
    print(f"Attendance sheet created for {room_no} on {exam_date} ({shift}): {file_name}")

# Final message
print("Attendance sheets have been successfully created.")
