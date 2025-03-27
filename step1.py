import pandas as pd

def find_absent_streaks(attendance_df):
    attendance_df = attendance_df.sort_values(by=["student_id", "attendance_date"])
    
    absent_df = attendance_df[attendance_df['status'] == 'Absent']

    absent_df['gap'] = (absent_df['attendance_date'] - absent_df['attendance_date'].shift()).dt.days
    absent_df['streak_id'] = (absent_df['gap'] > 1).cumsum()

    grouped = absent_df.groupby(['student_id', 'streak_id']).agg(
        absence_start_date=('attendance_date', 'first'),
        absence_end_date=('attendance_date', 'last'),
        total_absent_days=('attendance_date', 'count')
    ).reset_index()

    grouped = grouped[grouped['total_absent_days'] > 3]

    latest_streaks = grouped.groupby('student_id').last().reset_index()

    return latest_streaks[['student_id', 'absence_start_date', 'absence_end_date', 'total_absent_days']]
