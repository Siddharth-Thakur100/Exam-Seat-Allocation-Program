import pandas as pd

def assign_students_to_rooms(ip_1, final):
    studs = pd.DataFrame(columns=["Course", "Students"])
    courses = []
    students = []

    for group, group_df in ip_1.groupby('course_code'):
        courses.append(group)
        student_list = ', '.join(group_df['rollno'])
        students.append(student_list)

    studs['Course'] = courses
    studs['Students'] = students

    final['Roll_no'] = ''

    for index, row in final.iterrows():
        course = row['course_code']
        no_of_students = int(row['num_students_allocated'])

        studs_row = studs[studs['Course'] == course]

        if not studs_row.empty:
            students_list = studs_row.iloc[0]['Students']

            if isinstance(students_list, str):
                students_list = students_list.split(', ')

            selected = students_list[:no_of_students]
            final.at[index, 'Roll_no'] = ', '.join(selected)

            remaining_students = students_list[no_of_students:]
            # Convert the remaining students list back to a string
            studs.loc[studs['Course'] == course, 'Students'] = ', '.join(remaining_students)

    return final
