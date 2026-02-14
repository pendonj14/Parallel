import os
from concurrent.futures import ProcessPoolExecutor

employees = [
    ("Alice", 25000),
    ("Bob", 32000),
    ("Charlie", 28000),
    ("Diana", 40000),
    ("Edward", 35000)
]

def compute_employee_payroll(employee):
    name, gross_salary = employee
    
    sss = gross_salary * 0.045
    philhealth = gross_salary * 0.025
    pagibig = gross_salary * 0.02
    tax = gross_salary * 0.10
    
    total_deductions = sss + philhealth + pagibig + tax
    net_salary = gross_salary - total_deductions
    
    process_id = os.getpid()
    
    return {
        "name": name,
        "gross": gross_salary,
        "total_deductions": total_deductions,
        "net": net_salary,
        "pid": process_id
    }