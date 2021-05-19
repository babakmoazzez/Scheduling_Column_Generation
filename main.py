from gurobipy import *
from subproblem import subproblem
import time

t1=time.time()

#make some initial shifts to make the master problem feasible
shift0 = [1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
shift1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
shift2 = [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]

#demand is given
d= [2,5,6,5,7,7,4,6,7,7,7,7,6,5,6,6,5,4,7,6,6,4,5,5,6,6,5,7,7,6,9,6,7,6,6,7,7,4,5,5,4,5,3,4,5,3,5,4]

#make master
m = Model()
x = []
x.append(m.addVar(0,GRB.INFINITY,31, GRB.CONTINUOUS,"x_0"))
x.append(m.addVar(0,GRB.INFINITY,28, GRB.CONTINUOUS,"x_1"))
x.append(m.addVar(0,GRB.INFINITY,29, GRB.CONTINUOUS,"x_2"))
m.update()

for i in range(48):
    m.addConstr( shift0[i]*x[0] + shift1[i]*x[1] + shift2[i]*x[2] >= d[i] )
m.update()
    
#Column Generation
num_iter=0
while True:
    #solve master
    m.optimize()
    c = m.getConstrs()
    #get dual vector pi
    pi = [j.Pi for j in c]
    #solve subproblem. sigma is the min reduced cost and out is the new shift
    sigma,out = subproblem(pi)
    #if min reduced cost > 0, we are optimal
    if sigma >=0:
        break
    else:
        num_iter+=1
        #change shift to a column object
        col = Column()
        for k in range(48):
            if out[k] != 0:
                col.addTerms(out[k],c[k])
        #add new variable (column) to the master
        x.append(m.addVar(0,GRB.INFINITY,sum(out), GRB.CONTINUOUS,"x_"+str(3+i), column= col))
        m.update()

#Now LP is optimal, solve IP. First check if the solution is integral
sol = [i.X for i in x]
integral = True
for i in sol:
    if 0.0001<= i <=0.9999:
        integral = False
        break
if not integral:
    for i in x:
        i.setAttr('VType','i')
    m.update()
    m.optimize()
    x=m.getVars()
    sol = [i.X for i in x]

print('\n')
print('optimal objective: ', m.objVal)
print('number of iterations: ', num_iter)
print('time: ',time.time() - t1, 'sec.')
print('\n')
k=0
#print schedule
print('demand   : ',end='')
for i in range(48):
    print(d[i],end=' ')
print('\n')
for i in range(len(sol)):
    if sol[i] >0.99:
        k+=1    
        print('shift ',k,': ',end='')
        for t in range(48):
            print(int(m.getCoeff(c[t],x[i])),end = ' ')
        print('\n')
        

 







    