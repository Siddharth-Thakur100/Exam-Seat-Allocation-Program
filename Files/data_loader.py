import pandas as pd

def load_data():
    # Load input data files
    ip_1 = pd.read_csv("ip_1.csv", header=1)
    ip_2 = pd.read_csv("ip_2.csv", header=1)
    ip_3 = pd.read_csv("ip_3.csv", header=0)
    ip_4 = pd.read_csv("ip_4.csv", header=0)

    # Strip whitespace from course codes in ip_1
    ip_1['course_code'] = ip_1['course_code'].str.strip()

    # Helper function to extract the floor or prefix from room numbers
    def extract_floor(room_no):
        if room_no[:2].isalpha():  # For room identifiers starting with letters
            return room_no[:]
        else:  # Numeric room numbers
            return int(room_no[0])

    # Add a 'floor' column to ip_3 for sorting purposes
    ip_3['floor'] = ip_3['Room No.'].apply(extract_floor)

    # Sort rooms by floor and capacity
    room_cap = ip_3.sort_values(by=['floor', 'Exam Capacity'], ascending=[True, True])

    return ip_1, ip_2, room_cap

def prepare_course_counts(ip_1):
    # Count the number of students enrolled in each course
    course_counts = ip_1['course_code'].value_counts().reset_index()
    course_counts.columns = ['course_code', 'count']
    return course_counts
