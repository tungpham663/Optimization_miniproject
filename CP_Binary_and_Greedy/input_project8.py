#GUARANTEE OF CAPACITY AND CONFLICT CONSTRAINT
import os
import random
FOLDER_PATH = r"C:\Users\savag\Desktop\Project 8\medium_size_many_constraints"
num_of_test = 100
def listDir(dir):
    filenames = os.listdir(dir)
    for filename in filenames:
        print(filename)
        print("PATH", os.path.abspath(os.path.join(dir, filename)))
def filename(i):
    return "input_" + str(i) + ".txt"

for num in range(1, num_of_test+1):

    n = 50
    m = 10
    d = [None for i in range(n)]
    c = [None for j in range(m)]
    k = 500
    conflict_pairs = []
    valid = False
    while not valid:
        for i in range(n):
            d[i] = random.randrange(0,1000)
        for j in range(m):
            c[j] = random.randrange(0,1000)

        # This condition guarantees at least one room can hold any subject exam
        if max(d) < max(c):
            valid = True
    for cnt in range(k):

        valid = False
        while not valid:
            sub1 = random.randrange(0,n)
            sub2 = random.randrange(0,n)
            rev_pair = [sub2,sub1]
            pair = [sub1, sub2]
            if sub1 != sub2:
                valid = True
            if pair in conflict_pairs:
                valid = False
            if rev_pair in conflict_pairs:
                valid = False

        conflict_pairs.append(pair)

    file = os.path.join(FOLDER_PATH, filename(num))
    print(file)
    with open(file, "w") as f:
        f.write(str(n) +"\n")

        for i in range(len(d)):
            f.write(str(d[i])+" ")
        f.write("\n")
        f.write(str(m) + "\n")
        for j in range(len(c)):
            f.write(str(c[j]) +" ")
        f.write("\n")
        f.write(str(k)+ "\n")
        for pair in conflict_pairs:
            sub1,sub2 = pair
            f.write(str(sub1) + " " + str(sub2)+"\n")

        f.close()
