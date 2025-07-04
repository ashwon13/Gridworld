import sys; args = sys.argv[1:]

#Ashwin Pulla 4/30/2024
import re
import math
def strEdgesCMD(board,width):
    newBoard=""
    board2=board
    jmps=False
    if "\n" in board:
        board2=board[:board.index("\n")]
        jmps=True
    for i in range(0,len(board2)):
        if i%width==0 and i!=0:
            newBoard+="\n"
            newBoard+=board2[i]
        else:
            newBoard+=board2[i]
    if jmps==False:
        return newBoard
    else:
        return newBoard+board[board.index("\n"):]
def parseVslices(strSlices,size,E):
    if E==False:
        vtxIndexes=set()
    else:
        vtxIndexes=[]
    vslcs=strSlices.split(",")
    for i in vslcs:
        if i.find(":")==-1:
            if E==False:
                vtxIndexes.add([k for k in range(size)][int(i)])
            else:
                vtxIndexes.append([k for k in range(size)][int(i)])
            
    return vtxIndexes
def getNeighborsOfVrtx(vrtx,size,width):
    vtxNeighbors=set()
    neighbors=[vrtx-width,vrtx+1,vrtx+width,vrtx-1]
    if neighbors[0]>=0:
        vtxNeighbors.add(neighbors[0])
    if neighbors[1]//width==vrtx//width:
        vtxNeighbors.add(neighbors[1])
    if neighbors[2]<size:
        vtxNeighbors.add(neighbors[2])
    if neighbors[3]>=0 and neighbors[3]//width==vrtx//width:
        vtxNeighbors.add(neighbors[3])
    return vtxNeighbors
        
def toDelete(edges,W,X,size):
        for vtx in range(size):
            if vtx not in W:
                edges[vtx]=edges[vtx]-W
            else:
                edges[vtx]=edges[vtx]-X
        return edges
def toAdd(edges,W,X,size,width):
    for vtx in range(size):
        
        if edges[vtx] != (Nbrs:=(getNeighborsOfVrtx(vtx,size,width))):
            if vtx in W:
                edges[vtx]=edges[vtx]|Nbrs&X
            elif (edges[vtx]&W)!=(Nbrs:=(getNeighborsOfVrtx(vtx,size,width))&W):
                edges[vtx]=edges[vtx]|Nbrs&W
    return edges
def findWidth(size):
    min=999
    for i in range(math.ceil(size**0.5),size):
        if (size%i)==0 and i<min :
            min=i
    if min!=999:
        return min
    else:
        return size
def edgesDirection(directions,vtx,edges,size,width):
    nbrs=getNeighborsOfVrtx(vtx,size,width)
    if "S" in directions and vtx+width<size:
        if vtx+width not in edges[vtx] and (vtx+width) in nbrs:
            edges[vtx]=edges[vtx]|{vtx+width}
            edges[vtx+width]=edges[vtx+width]|{vtx}
        else:
            edges[vtx]=edges[vtx]-{vtx+width}
            edges[vtx+width]=edges[vtx+width]-{vtx}
    if "N" in directions and vtx-width>=0:
        if vtx-width not in edges[vtx] and (vtx-width) in nbrs:
            edges[vtx]=edges[vtx]|{vtx-width}
            edges[vtx-width]=edges[vtx-width]|{vtx}
        else:
            edges[vtx]=edges[vtx]-{vtx-width}
            edges[vtx-width]=edges[vtx-width]-{vtx}
    if "E" in directions and (vtx+1)//width==(vtx)//width:
        if vtx+1 not in edges[vtx] and (vtx+1) in nbrs:
            edges[vtx]=edges[vtx]|{vtx+1}
            edges[vtx+1]=edges[vtx+1]|{vtx}
        else:
            edges[vtx]=edges[vtx]-{vtx+1}
            edges[vtx+1]=edges[vtx+1]-{vtx}
    if "W" in directions and (vtx-1)//width==(vtx)//width:
        if vtx-1 not in edges[vtx] and (vtx-1) in nbrs:
            edges[vtx]=edges[vtx]|{vtx-1}
            edges[vtx-1]=edges[vtx-1]|{vtx}
        else:
            edges[vtx]=edges[vtx]-{vtx-1}
            edges[vtx-1]=edges[vtx-1]-{vtx}
    return edges
    
    
    
    
def nativeEdges(size,width):
    edges=[]
    for i in range(size):
        vtxNeighbors=set()
        neighbors=[i-width,i+1,i+width,i-1]
        if neighbors[0]>=0:
            vtxNeighbors.add(neighbors[0])
        if neighbors[1]//width==i//width:
            vtxNeighbors.add(neighbors[1])
        if neighbors[2]<size:
            vtxNeighbors.add(neighbors[2])
        if neighbors[3]>=0 and neighbors[3]//width==i//width:
            vtxNeighbors.add(neighbors[3])
        edges.append(vtxNeighbors)
    return edges
def blocking(W,edges,size,width):
    # W=parseVslices(m.group(1),size,False)
    V={*range(size)}
    X=V-W
    updatedEdges=toDelete(edges.copy(),W,X,size)
    toRecover=toAdd(edges.copy(),W,X,size,width)
    diff=[toRecover[i]-edges[i] if toRecover[i]!=set() else edges[i] for i in range(len(toRecover))]
    edges=updatedEdges
    edges=[edges[i]|diff[i] if diff[i]!=set() else edges[i] for i in range(len(edges))]
    return edges
def grfParse(parsedArgs):
    size=0
    width=0
    vtxRwds={}
    option=0
    defaultRwd=12
    graphDatastruct=[]
    graph={}
    edges=[]
    for arg in parsedArgs:
        if isinstance(arg,tuple):
            value=int(arg[0])
            type=arg[1]
            if type==0:
                size=value
            if type==1:
                width=value
        else:
            if (m:=(re.search(r"^G(\d+)",arg)))!=None:

                option=int(m.group(1))
                if width==0:
                    width=findWidth(size)
                if edges==[]:
                    edges=nativeEdges(size,width)
                # if size==1 and len(parsedArgs)==2:
                #     return "."
            if re.search(r"^[Rr](\d+)$",arg)!=None:
                m=re.search(r"^[Rr](\d+)$",arg)
                # if size==1 and len(parsedArgs)==3 and int(m.group(1))==0:
                #     return "*"
                vtxRwds[m.group(1)]=defaultRwd
            if (m:=re.search(r"^[Rr]:(\d+)$",arg))!=None:
                defaultRwd=int(m.group(1))
            if (m:=re.search(r"^[Rr](\d+):(\d+)$",arg))!=None:
                vtxRwds[m.group(1)]=int(m.group(2))
            if width==0:
                width=findWidth(size)
            
            if (m:=re.search(r"^[Bb](\d+)$",arg))!=None:
                if edges==[]:
                    edges=nativeEdges(size,width)
                W=parseVslices(m.group(1),size,False)
                V={*range(size)}
                X=V-W
                updatedEdges=toDelete(edges.copy(),W,X,size)
                toRecover=toAdd(edges.copy(),W,X,size,width)
                diff=[toRecover[i]-edges[i] if toRecover[i]!=set() else edges[i] for i in range(len(toRecover))]
                edges=updatedEdges
                edges=[edges[i]|diff[i] if diff[i]!=set() else edges[i] for i in range(len(edges))]
            if (m:=re.search(r"^[Bb](\d+)([NESW]+)$",arg))!=None:
                if edges==[]:
                    edges=nativeEdges(size,width)
                vtx=int(m.group(1))
                directions=m.group(2)
                edges=edgesDirection(directions,vtx,edges,size,width)
    graphDatastruct.append({"size":size,"width":width,"rwd":defaultRwd,"opt":option})
    graphDatastruct.append(edges)
    graphDatastruct.append([int(k) for k in vtxRwds.keys()])

    graphDatastruct.append(vtxRwds)
    
    # print(graphDatastruct)
    return graphDatastruct
        
            
def bfs2(vtx, edges,seen,rwds,badRwds):
    queue=[]
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
                if neighbors not in seen and (neighbors,distance+1) not in queue and neighbors not in seen and neighbors not in badRwds:
                    
                    queue.append((neighbors,distance+1))
                    temp.append((neighbors,distance+1))
    return temp,seen
def bfs(vtx, edges,seen,rwds,badRwds):
    queue=[]
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
                if neighbors not in seen and (neighbors,(distance+1)) not in queue and neighbors not in seen and neighbors not in badRwds:
                    
                    queue.append((neighbors,distance+1))
                    temp.append((neighbors,(distance+1)/vtx))
    return temp,seen
def getCharacter(direction):
    dictOfSymbols={"F":[0,1,1,1],"M":[0,1,0,1],"L":[0,1,0,0],"E":[0,1,1,0],"U":[0,0,0,1],"N":[1,1,0,1],"+":[1,1,1,1],"T":[1,1,1,0],"D":[0,0,1,0],"V":[1,0,0,1],"R":[1,0,0,0],"S":[1,0,1,0], "W":[1,0,1,1], "-":[1,1,0,0],"|":[0,0,1,1],".":[0,0,0,0]}
    gridRepresentation=list(dictOfSymbols.keys())[list(dictOfSymbols.values()).index(direction)]
    return gridRepresentation

def updateResults(x,y):
    vtxX=[i[0] for i in x]

    for i in y:
        if i[0] not in vtxX:
            x.append(i)
    return x
def getPolicy(paths,rwds,badRwds,grf):
    # print(paths)
    size=grf[0]["size"]
    width=grf[0]["width"]
    edges=grf[1]
    lengths=size*["."]
    board=size*["."]
    for i in range(len(paths)):
        node,distance=paths[i]
        if lengths[node]=="." or distance<lengths[node]:
            lengths[node]=distance
    for vtx in range(len(lengths)):
        if lengths[vtx]==0 or vtx in rwds:
            board[vtx]="*"
        elif edges[vtx]==set() or lengths[vtx]==".":
            board[vtx]="."
        else:
            
            if set(edges[vtx])&set(badRwds)==set(edges[vtx]):
                    maxVal=max([grf[-1][str(rwd)] for rwd in edges[vtx]])
                    directions=[((vtx+x) in edges[vtx] and str(vtx+x) in {*grf[-1].keys()} and grf[-1][str(vtx+x)]==maxVal) for x in [1,-1,width,-width]]
                    board[vtx]=getCharacter(directions)
                    
            else:
                if len(edges[vtx])==1 and list(edges[vtx])[0] in badRwds:
                    directions=[((vtx+x)==list(edges[vtx])[0])  for x in [1,-1,width,-width]]


                else:
                    minOptions=min([lengths[edge] for edge in set(edges[vtx])-set(badRwds)])
                    directions=[(vtx+x) in edges[vtx] and lengths[vtx+x]==minOptions and vtx+x not in badRwds for x in [1,-1,width,-width]]
            # if vtx==0:
            #     print(directions,minOptions,lengths,edges[vtx])
                # and set(getNeighborsOfVrtx(vtx,size,width))&set(badRwds)==set(badRwds)
                
            board[vtx]=getCharacter(directions)
            
            
    return board
        # if distance==0:
        #     board[node]="*"
        # nBrs=getNeighborsOfVrtx(node)
        # for i in nBrs:
        #     ...
            

parsedArgs=[]
for arg in range(len(args)):
    if re.search(r"^G(\d+)$", args[arg])!=None:
        parsedArgs.append(args[arg])
    if re.search(r"^(\d+)$",args[arg])!=None:
        parsedArgs.append((args[arg],arg))
    if re.search(r"^[Rr](\d+)$",args[arg])!=None:
        parsedArgs.append(args[arg])
    if (m:=re.search(r"^[Rr]:(\d+)$",args[arg]))!=None:
        parsedArgs.append(args[arg])
    if re.search(r"^[Rr](\d+):(\d+)$",args[arg])!=None:
        parsedArgs.append(args[arg])
    if re.search(r"^[Bb](\d+)$",args[arg])!=None:
        parsedArgs.append(args[arg])
    if re.search(r"^[Bb](\d+)([NSWE]+)$",args[arg])!=None:
        parsedArgs.append(args[arg])
if parsedArgs!=[]:
    grf=grfParse(parsedArgs)
    if grf[-1]==[]:
        print(strEdgesCMD("."*grf[0]["size"],grf[0]["width"]))
    else:
        maxNum=-999
        vtx=[]
        for i in grf[-1]:
            if grf[-1][i]>maxNum:
                maxNum=grf[-1][i]
        for i in grf[-1]:
            if grf[-1][i]==maxNum:
                vtx.append(int(i))
        badRwds=list(set(grf[2])-set(vtx))
        results,covered=bfs2(vtx,grf[1],set(),grf[2],badRwds)
        if grf[0]["opt"]==0:
            if {*range(grf[0]["size"])}-covered==set():
                policy=getPolicy(results,grf[2],badRwds,grf)
            else:
                results=updateResults(results,bfs2(badRwds,grf[1],covered,grf[2],badRwds)[0])
            # print(results)
        if grf[0]["opt"]==1:
            results,covered=bfs(vtx,grf[1],set(),grf[2],badRwds,grf)
        # print(results)
        # print(grf[1][27])
        # for i in badRwds:
        #     grf[1]=toDelete(grf[1],{i},{*range(grf[0]["size"])}-{i},grf[0]["size"])
        policy=getPolicy(results,grf[2],badRwds,grf)
        # if covered-{*range(grf[0]["size"])}==set():
        print(strEdgesCMD(policy,grf[0]["width"]))
        # else:

def main():
    ...

if __name__ == '__main__ ': main() 
#Ashwin Pulla 6 2024