# utils.py

import datetime

# --- 1. أدوات تنسيق المخرجات (Formatting) ---

def print_report_title(title):
    """لطباعة عنوان التقرير بشكل احترافي"""
    print("\n" + "=" * 60)
    print(f"                   {title}                   ")
    print("=" * 60 + "\n")

def format_table_header(col1, col2):
    """لطباعة رؤوس الجداول بتنسيق منظم"""
    print(f"{col1:<30} | {col2:<20}")
    print("-" * 55)

def format_table_row(val1, val2):
    """لطباعة صفوف البيانات بمسافات متساوية"""
    print(f"{str(val1):<30} | {str(val2):<20}")


# --- 2. أدوات التأكد من البيانات (Validation) ---

def validate_date(date_text):
    """للتأكد إن التاريخ المكتوب صيغته صح (YYYY-MM-DD)"""
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def validate_numeric(value):
    """للتأكد إن القيمة المدخلة رقمية (زي الوزن أو السن)"""
    return str(value).replace('.', '', 1).isdigit()
