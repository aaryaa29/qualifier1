import re

import pandas as pd

def validate_email(email):
    """Check if email follows the valid pattern."""
    pattern = r"^[a-zA-Z_][a-zA-Z0-9_]*@[a-zA-Z]+\.(com)$"
    return bool(re.match(pattern, email))

def process_students(absence_data, students_df):
    # Merge student information
    final_df = absence_data.merge(students_df[['student_id', 'student_name', 'parent_email']], on='student_id', how='left')

    # Validate emails
    final_df['email'] = final_df['parent_email'].apply(lambda x: x if validate_email(x) else None)

    # Generate message only for valid emails
    final_df['msg'] = final_df.apply(lambda row: (
        f"Dear Parent, your child {row['student_name']} was absent from "
        f"{row['absence_start_date'].strftime('%Y-%m-%d')} to {row['absence_end_date'].strftime('%Y-%m-%d')} "
        f"for {row['total_absent_days']} days. Please ensure their attendance improves."
    ) if pd.notna(row['email']) else None, axis=1)

    return final_df[['student_id', 'absence_start_date', 'absence_end_date', 'total_absent_days', 'email', 'msg']]
