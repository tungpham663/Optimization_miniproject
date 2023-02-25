from ortools.sat.python import cp_model
import time

    
def main():
    with open(r"C:\Users\DELL\data.txt") as f:
        n = int(f.readline())
        sub = [int(x) for x in f.readline().split()]
        m = int(f.readline())
        room = [int(x) for x in f.readline().split()]
        k = int(f.readline())
        conf = []
        for i in range(k):
            conf.append([int(x) for x in f.readline().split()])
        print("read file done")
        f.close()

    # create solver
    model = cp_model.CpModel()

    # create variables
    x = [[[model.NewBoolVar('x(' + str(i) + ',' + str(j) + ',' + str(k) + ')') for k in range(m)] for j in range(n)] for i in range(n)]

    # create constraints
    
    # constraint: x[i][k] = 0 if sub[i] > room[k]
    
    for i in range(n):
        for k in range(m):
            if sub[i] > room[k]:
                for j in range(n):
                    model.Add(x[i][j][k] == 0)

    # constraint: for each sub  i, sum of x[i][j][k] = 1
    for i in range(n):
        model.AddExactlyOne(x[i][j][k] for j in range(n) for k in range(m))

    # constraint: for each period j, and room k, sum of x[i][j][k] <= 1
    for j in range(n):
        for k in range(m):
            model.AddAtMostOne(x[i][j][k] for i in range(n))

    # constraint: number of subjects in previous period >= number of subjects in current period
    prev = [model.NewIntVar(0, n, 'prev_' + str(j)) for j in range(n)]
    for j in range(n):
        model.Add(prev[j] == sum(x[i][j][k] for i in range(n) for k in range(m)))
    for j in range(1, n):
        model.Add(prev[j] <= prev[j-1])

    # constraint: for each sub i1, i2 in conflict, x[i1][j][k] + x[i2][j][k] <= 1
    for [i1, i2] in conf:
        for j in range(n):
            model.AddAtMostOne([x[i1-1][j][k] for k in range(m)] + [x[i2-1][j][k] for k in range(m)])

    # constraint: for each period j, P[j] = max(x[i][j][k])
    p = [model.NewIntVar(0, 1, 'P(' + str(j) + ')') for j in range(n)]
    for j in range(n):
        for i in range(n):
            for k in range(m):
                model.Add(p[j] >= x[i][j][k])

    # objective function
    model.Minimize(sum(p))

    # create solver
    solver = cp_model.CpSolver()

    # solve
    start = time.time()
    status = solver.Solve(model)
    end = time.time()
    print("Time: ", end - start)

    # print result
    if status == cp_model.OPTIMAL:
        print("objective value: ", int(solver.ObjectiveValue()))
        for k in range(m):
            print("room ", k+1, ": ", end='')
            for j in range(n):
                check = True
                for i in range(n):
                    if solver.Value(x[i][j][k]) == 1:
                        if i + 1 < 10:
                            print("0", end="")
                        print(i + 1, end="  ")
                        check = False
                if check:
                    print("--", end="  ")
            print()
    else:
        print("no optimal solution found")


if __name__ == '__main__':
    main()
