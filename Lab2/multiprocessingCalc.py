from multiprocessing import Process
import time

def compute_gwa_mp(grades):
    gwa = sum(grades) / len(grades)
    print(f"[Process] Calculated GWA: {gwa}")

if __name__ == "__main__":
    grades_list = []

    n = int(input("Enter number of subjects: "))
    for i in range(n):
        grade = float(input(f"Enter grade for subject {i + 1}: "))
        grades_list.append(grade)
    
    processes = []

    for grade in grades_list:
        p = Process(target=compute_gwa_mp, args=([grade],))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    print("All processes finished.")