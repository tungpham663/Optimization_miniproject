#Sorting subject by number of attendants and constraint
#INPUT
import time as timegp
import os

#Change this folder path input if you wish to experiment with different test categories
FOLDER_PATH_INPUT = r"C:\Users\savag\Desktop\Project 8\medium_size_many_constraints"
FOLDER_PATH_OUTPUT = r"C:\Users\savag\Desktop\Project 8\Greedy_output_2\medium_size_many_constraints"
num_of_test = 100
def filename_input(i):
    return "input_" + str(i) + ".txt"
def filename_output(i):
    return "output_" + str(i) + ".txt"


#These arrays will be used to save the run time and the results of each test case
list_of_result = []
list_of_time = []


#Following path is to read in all the input test case
for num_of_file in range(1, num_of_test + 1):
    start = timegp.time()
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





    # Assume that the needed number of timeslot starts at equal to number of subject (max number of iterations needed)
    p = n

    #Following code is to prepare the order of subject in desired input

    sub_dict_tmp = dict()
    for i in range(n):
        sub_dict_tmp[str(i)] = d[i]

    #Store number of attendants of each subject in a dictionary
    conflict_count = [0 for i in range(n)]
    for pair in conflict_pairs:
        for i in pair:
            conflict_count[i] += 1



    # Assign each value of subject with value = avg(ratio of number of conflict, ratio of number of attendant)
    sub_dict_tmp_score = dict()
    tmp_arr = list(sub_dict_tmp.values())
    max_1 = max(tmp_arr)
    tmp_arr_2 = conflict_count
    max_2 = max(tmp_arr_2)
    for i in range(len(tmp_arr)):
        tmp_arr[i] /= max_1
    for i in range(len(tmp_arr_2)):
        tmp_arr_2[i] /= max_2
    score = [0 for i in range(n)]
    for i in range(n):
        score[i] = tmp_arr[i] + tmp_arr_2[i]
    for i in range(n):
        sub_dict_tmp_score[str(i)] = score[i]


    #Build a new dictionary (sub_dict)to store room according to capacity + number of constraint
    sub_dict_key = sorted(sub_dict_tmp, key = sub_dict_tmp_score.get)
    sub_dict = dict()
    for key in sub_dict_key:
        sub_dict[key] = sub_dict_tmp[key]  # Assign number of attendants



    # Translate number of attendants back to original list d (with different order):
    d = list(sub_dict.values())
    d = d[::-1]
    sub = []
    for key in sub_dict_key:
        sub.append(int(key))
    sub=sub[::-1] #This array is used to store the subject in order of their ratio

    # End preparing data

    # Building conflict matrix, con[i][j] : sub i and j can't be organized at the same time
    conf_mat = [[0 for i in range(n)] for j in range(n)]
    for pair in conflict_pairs:
        sub1, sub2 = pair
        conf_mat[sub1][sub2] = 1
        conf_mat[sub2][sub1] = 1

    # Check room capacity, return 1 for all k means the room is large enough and can organize i-th subject at given k-th timeslot
    cap = [[[0 for k in range(p)] for j in range(m)] for i in range(n)]
    for i in range(n):
        for j in range(m):
            if d[i] <= c[j]:
                for k in range(p):
                    cap[sub[i]][j][k] = 1


    sol = [] #This array is used to store the solution found by alg
    check = [False for i in range(n)] #This array store whether subjects have been organized or not (False means not organized)
    count = 0
    remain_sub = [] #This is array of remaining subject

    #Check for remaining subject, subs will be added in the odd of decreasing numbers of attendants
    for i in range(len(sub)):
        if check[sub[i]] == False:
            remain_sub.append(sub[i])

    for k in range(p): #Run for at max p = n timeslot, each timeslot we try to schedule for as many subjects as possible
        count +=1 #This varible is used to count number of  timeslots used



        print("REMAINING SUB", remain_sub)
        available_room = [j for j in range(m)] #This list keeps track of which room has not been used during this timeslots

        #List to keep which subjects have been registered this timeslot
        sub_registered_this_time = []
        for subject in remain_sub: #Loop through all subjects
            found_room = False

            #psb var is used to check if a subject in conflicted pair is already orgranized into this timeslot
            psb = True
            for sub_registered in sub_registered_this_time:
                if conf_mat[sub_registered][subject] == 1:
                    psb = False
                    break
            if not psb:
                continue
            for j in range(len(available_room)): #Check all remaining rooms for a room for the subject

                if cap[subject][available_room[j]][k] == 1 and psb: #If this room can hold this subject and there is not a conflicted subject with current considering subject
                    sol.append(subject)
                    sol.append(available_room[j])   #Assign information to sol
                    sol.append(k)
                    sub_registered = subject      #Add this subject to list of registed subject this time
                    room = j
                    time = k
                    check[sub_registered] = True   #The array keeping track of subject scheduled will get True as this subject has been scheduled
                    found_room = True
                    sub_registered_this_time.append(sub_registered)
                    break

            print(available_room)
            if found_room: #If found_room mean the room has been found for current subject
                available_room.pop(room)

        remain_sub = [] #Reconstruct list of remaining subjects
        for i in range(len(sub)):
            if check[sub[i]] == False:
                remain_sub.append(sub[i])

        #If there is no remaining subject: we stop
        if len(remain_sub) == 0:
            print("ALL SUBS HAVE BEEN ASSIGNED")
            break



    end = timegp.time()


    print(f"sol of {count} timeslot used")
    list_of_result.append(count)
    list_of_time.append(end-start)
    sol_sub = []
    sol_room = []
    sol_time = []
    for i in range(len(sol)):
        if i % 3 == 0:
            sol_sub.append(sol[i])
        if i % 3 == 1:
            sol_room.append(sol[i])
        if i % 3 == 2:
            sol_time.append((sol[i]))
    with open(file_output, "w") as f:
        f.write(str(count)+"\n")
        for i in range(len(sol_sub)):
            f.write(str(sol_sub[i]) +" " + str(sol_room[i]) + " " + str(sol_time[i]) + "\n")
        f.close()


    print(count, "timeslot has been used")
with open (r"C:\Users\savag\Desktop\Project 8\Greedy_output_2\summary_msmc.txt", "w") as f:
    for i in range(len(list_of_result)):
        f.write(str(list_of_result[i]) + " ")
    f.write("\n")
    for i in range(len(list_of_time)):
        f.write(str(list_of_time[i]) + " ")
    f.write("\n")
    f.close()