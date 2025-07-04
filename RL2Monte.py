size=0
strands=0
policy=[]
visitCtLimit=0
strandCtLimit=0
probList=[]
vtxRwds=[]
strads=[]
def updateStruct(actionReport):
    for i in actionReport:
        if type(i)==tuple and type(i[0]) ==list:
            x=i[0]
            print(i,x)
            l=x.split(" ")
            for i in range(len(l)):
                for j in range(1,len(l)):
                    strands.append((visited[l[i]],visited[l[i]]|l[j]))
            if i[1]>0:
                vtxRwds.append(l[-1])
    return strands
def lowerProbs(visited):
    probs=[]
    for k in visited.keys():
        for v in visited[k]:
            probs.append((k,v),0.05)
    return probs
def bfs(vtx, edges):
    queue=[]
    seen={}
    for i in vtx:
        queue.append((i,0))
    temp=queue.copy()

    while queue:
        node,distance=queue.pop(0)
        if node in seen:
            continue
        seen.add(node)

        if node not in set(rwds)-set(vtx):
            for neighbors in edges[node]:
                if neighbors not in seen and (neighbors,(distance+1)) not in queue and neighbors not in seen:
                    
                    queue.append((neighbors,distance+1))
                    temp.append((neighbors,(distance+1)/vtx))
    return temp,seen
def getPolicy(vtxRwds,edges):
    results,covered=bfs(vtxRwds,edges)
    return []
def monteCarlo(sz,actionReport):
    global size,strands,policy,visitCtLimit,strandCtLimit,vtxRwds, probList,visited
    if sz>0: 
        size=sz
        visitCtLimit=actionReport[0][1]
        strandCtLimit=actionReport[1][1]

        policy=[set() for v in range(sz)]
        # visited=[set() for v in range(sz)]
        return []
    if len(actionReport)>1 and actionReport[-1][-1]>0: policy[actionReport[-2][0]].add(actionReport[-1][0])
    if sz<=0:
        updateStruct(actionReport)
    if sz<0:
        probList=lowerProbs(strands)
        return probList
    if sz==0:
        return getPolicy(vtxRwds,strands)



def main():
    print(strands)



                          

#Ashwin Pulla 6 2024