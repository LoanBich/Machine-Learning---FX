import numpy as np 
from pathlib import Path
import pandas as  pd

# open file   

file_path = None

while file_path is None:
    file = input("Enter a class file to grade (i.e. class1): ") + ".txt"
    file_path = Path(__file__).parent / "Data Files" / file

    if not file_path.is_file():
        print("File cannot be found.")
        file_path=None
     
with open(file_path, "r") as data:
    print("Successfully opened", file)

    #  analysing data 
    print("**** ANALYSING ****")

    # báo cáo tổng dữ liệu được nêu trong tệp
    total_lines = data.readlines()
    print("Total lines of data:", len(total_lines))

    # Phân tích từng dòng
    valid_lines = []
    for i in range(len(total_lines)):
        line = total_lines[i].replace("\n", "").split(",")
        if len(line) == 26 and line[0][0] == "N" and line[0][1:].isnumeric() and len(line[0]) == 9:
            valid_lines.append(line)
        else:
            if len(line) != 26:
                print("Invalid line of data: does not contain exactly 26 values:\n", line)
            else:
                print("Invalid line of data: N# is invalid:\n", line)

    print("**** REPORT ****")
    print("Total valid lines of data:", len(valid_lines))
    print("Total invalid lines of data:", len(total_lines)-len(valid_lines))



answer_key = np.array("B,A,D,D,C,B,D,A,C,C,D,B,A,B,A,C,B,D,A,C,A,A,B,D,D".split(","))
student_answer = np.array(valid_lines)

correct_answer = (student_answer[:, 1:] == answer_key)*4
wrong_answer = ((student_answer[:, 1:] != answer_key) & (student_answer[:, 1:] != ""))*-1

grade = np.sum((correct_answer), axis=1) + np.sum((wrong_answer), axis=1)
result = pd.DataFrame({"StudentID": student_answer[:, 0], "Grade": grade})

print("Mean (average):", result.iloc[:, 1].mean())

max_score = result.iloc[:, 1].max()
print("Highest score:", max_score)

min_score = result.iloc[:, 1].min()
print("Lowest score:", min_score)

print("Range of score:", max_score - min_score)

print("Median score:", result.iloc[:, 1].median())

result.to_csv(f"{file_path.stem}_grade.txt", header = False, index = False)