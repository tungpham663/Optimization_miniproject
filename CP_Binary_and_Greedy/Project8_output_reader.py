import os
FOLDER_PATH = r"C:\Users\savag\Desktop\Project 8\Greedy_output"
FILE_NAME = "summary_msfc.txt"
file_input = os.path.join(FOLDER_PATH, FILE_NAME)
def avg(x):
    sum = 0
    for i in x:
        sum += i
    sum /= len(x)
    return(sum)
with open (file_input) as f:
    res = [int(x) for x in f.readline().split()]
    time = [float(x) for x in f.readline().split()]
    uncertain = [int(x) for x in f.readline().split()]
    f.close()
freq_dict = dict()
uncertain_value = []
for i in uncertain:
    uncertain_value.append(res[i-1])
for val in uncertain_value:
    if val not in freq_dict:
        freq_dict[str(val)] = uncertain_value.count(val)
print(avg(res))
print(avg(time))

print(freq_dict)

print(len(uncertain_value))
print(max(res))
print(min(res))
