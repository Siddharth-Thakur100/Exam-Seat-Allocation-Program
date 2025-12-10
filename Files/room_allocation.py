import pandas as pd

def allocate_rooms(course_counts, room_cap, buffer):
    allocations = []

    for _, course in course_counts.iterrows():
        course_code = course["course_code"]
        remaining_students = course["count"]
        course_allocations = []

        for i, room in room_cap.iterrows():
            effective_capacity = room["effective_capacity"]
            buffered_capacity = room["Exam Capacity"] * buffer

            if remaining_students <= 0:
                break

            if effective_capacity > 0:
                if remaining_students <= effective_capacity:
                    course_allocations.append({
                        "course_code": course_code,
                        "room_no": room["Room No."],
                        "num_students_allocated": remaining_students,
                        "vacant_seats": effective_capacity - remaining_students,
                        "buffered_capacity": buffered_capacity
                    })
                    room_cap.at[i, "effective_capacity"] -= remaining_students
                    remaining_students = 0
                else:
                    course_allocations.append({
                        "course_code": course_code,
                        "room_no": room["Room No."],
                        "num_students_allocated": effective_capacity,
                        "vacant_seats": 0,
                        "buffered_capacity": buffered_capacity
                    })
                    remaining_students -= effective_capacity
                    room_cap.at[i, "effective_capacity"] = 0

        if remaining_students > 0:
            course_allocations.append({
                "course_code": course_code,
                "room_no": None,
                "num_students_allocated": remaining_students,
                "vacant_seats": 0,
                "buffered_capacity": 0
            })

        allocations.extend(course_allocations)

    return pd.DataFrame(allocations)
