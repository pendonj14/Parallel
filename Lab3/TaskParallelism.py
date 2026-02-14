from concurrent.futures import ThreadPoolExecutor

def compute_sss(salary):
    return salary * 0.045

def compute_philhealth(salary):
    return salary * 0.025

def compute_pagibig(salary):
    return salary * 0.02

def compute_tax(salary):
    return salary * 0.10


def main():
    salary = 30000

    with ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(compute_sss, salary),
            executor.submit(compute_philhealth, salary),
            executor.submit(compute_pagibig, salary),
            executor.submit(compute_tax, salary)
        ]

        results = [f.result() for f in futures]

    sss, philhealth, pagibig, tax = results
    total_deduction = sum(results)

    print("Salary:", salary)
    print("SSS:", sss)
    print("PhilHealth:", philhealth)
    print("Pag-IBIG:", pagibig)
    print("Tax:", tax)
    print("Total Deduction:", total_deduction)


if __name__ == "__main__":
    main()