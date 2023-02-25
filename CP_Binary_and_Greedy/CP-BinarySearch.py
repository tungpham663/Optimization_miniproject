#ORTOOLS with binary search for optimal p
import time
from ortools.sat.python import cp_model
import os

#Change this folder path input if you wish to experiment with different test categories
FOLDER_PATH_INPUT = r"C:\Users\savag\Desktop\Project 8\medium_size_many_constraints"
FOLDER_PATH_OUTPUT = r"C:\Users\savag\Desktop\Project 8\CP_output\medium_size_many_constraints"
num_of_test = 100

def filename_input(i):
    return "input_" + str(i) + ".txt"
def filename_output(i):
    return "output_" + str(i) + ".txt"

#These arrays will be used to save the run time and the results of each test case and the test cases algorithm returns uncertain answers
list_of_result = []
list_of_time = []
list_of_uncertain_result = []
for num_of_file in range(1, num_of_test+1):
    file_input = os.path.join(FOLDER_PATH_INPUT, filename_input(num_of_file))
    file_output = os.path.join(FOLDER_PATH_OUTPUT, filename_output(num_of_file))
    print("currently at file ", num_of_file)
    with open(file_input) as f:
        n = int(f.readline())
        d = [int(x) for x in f.readline().split()]
        m = int(f.readline())
        c = [int(x) for x in f.readline().split()]
        k = int(f.readline())
        conflict_pairs = []
        for i in range(k):
            conflict_pairs.append([int(x) for x in f.readline().split()])
        print("read file done")
        f.close()
    start = time.time()  #This variable keeps track of time used
    unknown_check = False #This variable leeps track of whether the test case is uncertain

    #3 following arrays is to store the anwser
    sol_sub = []
    sol_time = []
    sol_room = []
    p = n # Assume that the needed number of timeslot starts at equal to number of subject (max number of iterations needed)
    p_checked = [] #This array keeps track of which value of p has already been checked by alg
    stop = False
    psb = True
    #Following code return psb value as False if the capacity condition is not met
    for i in range(len(d)):
        check = False
        for j in range(len(c)):
            if d[i] <= c[j]:
                check = True
        if check == False:
            psb = False


    count = 0  #This variable keeps track of how many iteration the alg has run

    if psb:
        upper_bound = n #Set the upperbound equal the highest number of timeslots needed
        lower_bound = 0
        while not stop:
            count += 1
            print(""" 
            
            """)
            print(f"========Reaching {count}-th iteration:")
            print("Checked value :")
            print(p_checked)
            print(f'=============current p is {p}')
            #Construct a new solver model
            model = cp_model.CpModel()
            X = [[[0 for k in range(p)] for j in range(m)] for i in range(n)]

            #Define binary Var X: X_ijk: subject i, room j, timeslot k, if the capacity of room j can hold subject i then the X[i][j][k] = [0,1] for all k
            for i in range(n):
                for j in range(m):
                    if d[i] <= c[j]:
                        for k in range(p):
                            X[i][j][k] = model.NewIntVar(0,1, "x_" + str(i) +str(j) + str(k))



            #Some pair of subject cannot be scheduled at the same time
            for pair in conflict_pairs:
                i1, i2 = pair
                for k in range(p):
                    sum = 0
                    for j in range(m):
                        sum += X[i1][j][k]
                        sum += X[i2][j][k]
                    #At any timeslot there can be at max one subject in conflict pair be organized
                    model.AddLinearExpressionInDomain(sum, cp_model.Domain.FromValues([0, 1]))


            # Any room at any given time can only organize ar max one subject
            for j in range(m):
                for k in range(p):
                    sum = 0
                    for i in range(n):
                        sum += X[i][j][k]
                    model.AddLinearExpressionInDomain(sum, cp_model.Domain.FromValues([0, 1]))


            # Any subject must be organized once
            for i in range(n):
                sum = 0
                for j in range(m):
                    for k in range(p):
                        sum += X[i][j][k]
                model.Add(sum == 1)

            solver = cp_model.CpSolver()
            solver.parameters.max_time_in_seconds = 50 #If any iteration (value of timeslot needed) takes more than 50sec then the solver will consider this res as uncertain
            status = solver.Solve(model)
            #Do binary search for p
            #Reduce p if it is solvable, set anew check point for a solved point
            if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
                upper_bound = p
                new_p = (upper_bound + lower_bound) //2

            #If model cannot solve this p, then assign a bigger p
            elif status == cp_model.INFEASIBLE or status == cp_model.UNKNOWN:
                lower_bound = p+1
                new_p = (upper_bound + lower_bound) //2
            if status == cp_model.UNKNOWN:
                unknown_check = True #If the alg cannot check for this value then it will mark this test case as uncertain

            print("upper bound is: ", upper_bound)
            print("lower_bound is: ", lower_bound)

            if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
                print(f"SOLVABLE, p = [{p}]")
                # for i in range(n):
                #     for j in range(m):
                #         for k in range(p):
                #             if solver.Value(X[i][j][k]) == 1:
                #                 print(f'Subject[{i}] at room [{j}], timeslot [{k}]')

            elif status == cp_model.INFEASIBLE:
                print(f'No solution, p = [{p}]')


            #If the new value of p has already been checked then we terminate
            if p in p_checked:
                p_checked.append(p)
                stop = True
                break
            p_checked.append(p)
            p = new_p #setting p_value for new loop

        print(""" 
        
        """)
        print(f"stop at p = [{p}]")
        if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            for i in range(n):
                for j in range(m):
                    for k in range(p):
                        if solver.Value(X[i][j][k]) == 1:

                            sol_sub.append(i)
                            sol_room.append(j)
                            sol_time.append(k)
    else:
        print("There is no psb way to arrange exam due to limit in room capacity")
    with open(file_output, "w") as f:

        f.write(str(p_checked[-1])+"\n")
        for i in range(len(sol_sub)):
            f.write(str(sol_sub[i]) +" " + str(sol_room[i]) + " " + str(sol_time[i]) + "\n")
        f.close()

    end = time.time()
    print("TIME USED", end-start,"SEC")
    print(p_checked[-1],"timeslots used") #last value of list is the value which has been checked last 
    list_of_result.append(p_checked[-1])
    list_of_time.append(end-start)
    if unknown_check:
        list_of_uncertain_result.append(num_of_file)
print(list_of_time)
print(list_of_result)
for i in range(len(list_of_uncertain_result)):
    print(list_of_result[i])

with open (r"C:\Users\savag\Desktop\Project 8\CP_output\summary_msmc.txt", "w") as f:

    for i in range(len(list_of_result)):
        f.write(str(list_of_result[i]) + " ")
    f.write("\n")

    for i in range(len(list_of_time)):
        f.write(str(list_of_time[i]) + " ")
    f.write("\n")

    for i in range(len(list_of_uncertain_result)):
        f.write(str(list_of_uncertain_result[i]) + " ")
    f.write("\n")
    f.close()