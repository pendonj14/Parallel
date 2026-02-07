import threading
import time

def compute_gwa(grades):
    gwa = sum(grades) / len(grades)
    print(f"[Thread] Calculated GWA: {gwa}")

    grades_list = []

    n = int(input("Enter number of subjects: "))
    for i in range(n):
        grade = float(input(f"Enter grade for subject {i + 1}: "))
        grades_list.append(grade)

    threads = []


                                