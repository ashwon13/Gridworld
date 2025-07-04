size=0
visitCtLimit=0
strandCtLimit=0
strands=[]
rwdPolicy=[]
nonRwdsPolicy=[]
def updateStruct(tupleList):
    print(rwdPolicy,nonRwdsPolicy)
    
    for t in range(len(tupleList)-1):
        if tupleList[t+1][1]!=0:
            rwdPolicy[tupleList[t][0]]|set(tupleList[t+1][0])
        if tupleList[t][1]!=0:
            nonRwdsPolicy[tupleList[t][0]]|set(tupleList[t+1][0])
    return rwdPolicy,nonRwdsPolicy
def monteCarlo(sz,actionReport):
    global size,visitCtLimit,strandCtLimit,nonRwdsPolicy,rwdPolicy
    if sz>0:
        size=sz
        visitCtLimit=actionReport[0][1]
        strandCtLimit=actionReport[1][1]
        nonRwdsPolicy=[set() for v in range(size)]
        rwdPolicy=[set() for v in range(size)]
        print("test",nonRwdsPolicy,rwdPolicy)
        return []


    
    if sz<=0:
        r1,nr=updateStruct(actionReport)
        return r1
    if sz<0:
        return []
    if sz==0:
        return [[] for v in range(size)]

def main():
    strands="""
    Strand 1: 2 3 R12
    Strand 2: 0 3 R12
    Strand 3: 7 0 3 R12
    Strand 4: 7 6 7 8 1 0 1 0 7
    Strand 5: 7 6 7 0 1 5 2 4 3 R12
    Strand 6: 0 3 R12
    Strand 7: 2 1 0 7 6 7 8 5 2
    Strand 8: 7 8 1 4 7 6 3 R12
    Strand 9: 8 7 4 7 4 5 4 7 8
    Strand 10: 8 5 2 3 R12
    Strand 11: 4 3 R12
    Strand 12: 2 6 3 R12
    Strand 13: 3 R12
    Strand 14: 4 1 0 7 8 7 0 3 R12
    Strand 15: 6 3 R12
    Strand 16: 7 0 1 0 7 8 7 6 8
    Strand 17: 7 0 7 8 7 0 1 2 1
    Strand 18: 6 7 0 7 0 3 R12
    Strand 19: 4 5 3 R12
    Strand 20: 7 8 1 2 3 R12
    Strand 21: 2 1 5 2 3 R12
    Strand 22: 6 7 6 7 8 5 3 R12
    Strand 23: 1 0 7 0 1 0 7 8 1
    Strand 24: 3 R12
    Strand 25: 0 7 0 3 R12
    Strand 26: 6 7 0 7 8 5 3 R12
    Strand 27: 5 4 2 4 7 6 8 5 1
    Strand 28: 1 4 1 2 5 2 4 2 1
    """
    strands=strands.replace("Strand","")
    stands=strands.strip()
    strands=strands.split("\n")
    newStrands=[]
    tupleStrands=[]
    for x in strands:
        if ":" in x:
            newStrands.append(x[x.index(":")+2:].split(" "))
    for x in newStrands:
        temp=[]
        s="".join(x)
        for y in range(len(x)):
            if "R" not in s:
                temp.append((int(x[y]),0))
            if "R" in s:
                if y ==len(x)-2:
                    temp.append((int(x[y]),int(x[y+1][1:])))
                
                elif y!=len(x)-1:
                    temp.append((int(x[y]),0))
        tupleStrands.append(temp)
    print(tupleStrands)
    initial=monteCarlo(9,[(-4,270),(-5,28)])
    for i in tupleStrands:
        x=monteCarlo(-2,i)
        print(x)

    
main()


if __name__=="main": main()




#Ashwin Pulla 6 2024