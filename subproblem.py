from gurobipy import *

def subproblem(pi):
    '''solves subproblem given dual vector pi, returns min reduced cost and a new shift with min reduced cost'''
    
    #make subproblem
    m=Model()
    
    S=[]
    P=[]
    Y=[]
    dp=[None]
    dn=[None]
    ep=[None]
    en=[None]
    for i in range(48):
        S.append(m.addVar(0,1,1-pi[i],GRB.BINARY,"s_"+str(i)))
        P.append(m.addVar(0,1,0,GRB.BINARY,"p_"+str(i)))
        Y.append(m.addVar(0,1,0,GRB.BINARY,"y_"+str(i)))
    for i in range(1,48):
        dp.append(m.addVar(0,1,0,GRB.BINARY,"dp_"+str(i)))
        dn.append(m.addVar(0,1,0,GRB.BINARY,"dn_"+str(i)))
        ep.append(m.addVar(0,1,0,GRB.BINARY,"ep_"+str(i)))
        en.append(m.addVar(0,1,0,GRB.BINARY,"en_"+str(i)))
        
    m.update()
    
    m.addConstr(quicksum(S) <= 36)
    m.addConstr(quicksum(S) >= 16)
    for i in range(48):
        m.addConstr(S[i]+P[i]-Y[i] == 0)
        
    m.addConstr(P[0] == 0)
    m.addConstr(P[-1] == 0)
    
    m.addConstr(10.55*quicksum(P) - quicksum(S) <= 1)
    m.addConstr(10.55*quicksum(P) - quicksum(S) >= -10.55)
    
    for t in range(48-13):
        m.addConstr(quicksum([S[j] for j in range(t,t+14)]) <= 13)
    
    m.addConstr(quicksum([dp[i] for i in range(1,48)]) + quicksum([dn[i] for i in range(1,48)]) + S[0] + S[-1] == 2)
    
    for i in range(1,48):
        m.addConstr(dp[i] - dn[i] - Y[i] + Y[i-1] == 0)
        m.addConstr(dp[i] + dn[i] <= 1)
        
    m.addConstr(quicksum([ep[i] for i in range(1,48)]) + quicksum([en[i] for i in range(1,48)]) <= 4)
    m.addConstr(quicksum([ep[i] for i in range(1,48)]) + quicksum([en[i] for i in range(1,48)]) >= 2)
    
    for i in range(1,48):
        m.addConstr(ep[i] - en[i] - P[i] + P[i-1] == 0)
        m.addConstr(ep[i] + en[i] <= 1)
        
    
    #solve subproblem
    m.optimize()
    
    #prepare output
    shift = [0]*48
    for i in range(48):
        if S[i].X + Y[i].X == 2:
            shift[i] = 1
    
    return m.objVal,shift
    
    
    
    
if __name__ == '__main__':
    import random
    shift = subproblem([random.randint(-10,10) for i in range(48)])
    print(shift)
    