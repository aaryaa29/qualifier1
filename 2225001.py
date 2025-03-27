import pandas as pd
import re

def find_absent_streaks(attendance):
    attendance = attendance[attendance['status'] == 'Absent']
    attendance['gap'] = attendance.groupby('student_id')['attendance_date'].diff().dt.days
    attendance['streak_id'] = (attendance['gap'] > 1).cumsum()
    
    streaks = attendance.groupby(['student_id', 'streak_id']).agg(
        absence_start_date=('attendance_date', 'first'),
        absence_end_date=('attendance_date', 'last'),
        total_absent_days=('attendance_date', 'count')
    ).reset_index()

    return streaks[streaks['total_absent_days'] > 3]

def is_valid_email(email):
    return bool(re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*@[a-zA-Z]+\.(com)$", str(email)))

def process_students(absences, students):
    students['email'] = students['parent_email'].apply(lambda x: x if is_valid_email(x) else None)
    result = absences.merge(students[['student_id', 'student_name', 'email']], on='student_id', how='left')
    
    result['msg'] = result.apply(lambda row: (
        f"dear parent, your child {row['student_name']} was absent from {row['absence_start_date'].date()} "
        f"to {row['absence_end_date'].date()} for {row['total_absent_days']} days. Please look into this matter. thankyou."
    ) if row['email'] else None, axis=1)

    return result[['student_id', 'absence_start_date', 'absence_end_date', 'total_absent_days', 'email', 'msg']]

def run():
    attendance = pd.read_csv("attendance.csv", parse_dates=["attendance_date"])
    students = pd.read_csv("students.csv")
    
    absences = find_absent_streaks(attendance)
    return process_students(absences, students)

if __name__ == "__main__":
    print(run())
