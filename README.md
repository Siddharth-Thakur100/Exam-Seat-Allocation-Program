# Exam Seat Allocation Programme

This project is a complete **automated Exam Seating Allocation System** built using Python, Pandas, and CSV input files.  
It takes student registrations, exam timetables, and room capacities as inputs and generates a **final seating arrangement** showing:

- Which course is assigned to which room  
- How many students are seated in each room  
- Remaining vacant seats  
- Actual roll numbers assigned to seats  
- Separate allocations for Morning and Evening shifts for every exam date  

The final output is exported as both **Excel** and **CSV** files for convenience.

---

##  Features

- **Automatic room allocation** based on room capacities and student strength  
- **Buffer support** (e.g., keep 5% seats empty for invigilation spacing)  
- **Roll-number–wise student assignment**  
- **Handles multiple exam dates and morning/evening shifts**  
- **Greedy room allocation strategy** for efficient packing  
- **Clean final seating sheet** ready for invigilators  

---

## Input Files (CSV Format)

### 1. `ip_1.csv` – Student Registration Data  
Contains which students are registered in which course.

| rollno | register_sem | schedule_sem | course_code |
|--------|--------------|--------------|-------------|

### 2. `ip_2.csv` – Exam Timetable  
Lists courses that have exams in the Morning/Evening for each date.

| Date | Day | Morning | Evening |
|------|-----|---------|---------|

Example Morning cell:  
`HS202; HS212; HS225`

### 3. `ip_3.csv` – Room Capacities  
Details of exam halls and their capacities.

| Room No. | Exam Capacity | Block |

The programme also derives the **floor number** automatically.

### 4. `ip_4.csv` – Roll–Name Mapping (Optional)  
Currently unused, but available for future extensions like printable hall tickets.

---

## How the System Works

### **1. Data Loading**
- Reads all CSV files  
- Cleans course codes  
- Extracts floor numbers from room names  
- Sorts rooms by floor and capacity  

### **2. Count Students Per Course**
Counts how many students are enrolled in each course.

### **3. Room Allocation**
For each date and shift:

- Identify courses having exams  
- Sort courses by student count (largest first)  
- Allocate rooms using a greedy algorithm  
- Apply buffer to reduce effective capacity  
- Track vacant seats  

### **4. Student Roll Number Assignment**
For each `(course, room)`:

- Take the required number of students  
- Assign their roll numbers  
- Remove assigned students from the pool so no one is repeated  

### **5. Output Generation**
Produces the final sheet:

| Exam Date | Shift | course_code | room_no | num_students_allocated | vacant_seats | Roll_no |

Saved as:

- `Final_Seating_Arrangement.xlsx`  
- `Final_Seating_Arrangement.csv`  

---

Exam-Seat-Allocation/
│
├── main.py
├── data_loader.py
├── room_allocation.py
├── student_assignment.py
│
├── ip_1.csv
├── ip_2.csv
├── ip_3.csv
├── ip_4.csv
│
└── Final_Seating_Arrangement.xlsx (output)
