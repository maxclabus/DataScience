import pandas as pd

Students = pd.read_csv("/Users/maxclabus/Desktop/analysis/Python Project/csv_files/StudentsPerformance.csv")

print(Students.iloc[[],[0:1]])