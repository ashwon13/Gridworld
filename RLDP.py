import sys; args = sys.argv[1:]
#Ashwin Pulla 3/30/2024
import re
import math

#Reference functions

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
            
        elif (slicePos:=i.find(":"))!=-1 and (partition:=i.find(":",i.find(":")+1))==-1:
            start,stop=i[:slicePos],i[slicePos+1:]
            if start=="": start=0
            if stop=="": stop=size+1
            start,stop=int(start),int(stop)
            if E==False:
                vtxIndexes=vtxIndexes|(set([x for x in range(size)][start:stop]))
            else:
                for j in [x for x in range(size)][start:stop]: vtxIndexes.append(j)
        else:
            start,stop,third=i[:slicePos],i[slicePos+1:partition],i[partition+1:]
            if third=="": third=1
            third=int(third)
            if third<0 and start=="":
                start=None
            if third<0 and stop=="":
                stop=None
            if start=="": start=0
            if stop=="": stop =size+1
            if start!=None: start=int(start)
            if stop!=None: stop=int(stop)
            if E==False:
                vtxIndexes=vtxIndexes|(set([x for x in range(size)][start:stop:third]))
            else:
                selected=[x for x in range(size)][start:stop:third]
                for j in selected:vtxIndexes.append(j)
    
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
def parseBRTOptions(strOptions):
    brtParseB,brtParseR,brtParseT=re.search(r"(B(?!B))",strOptions),re.search(r"(R\d*(?!.*R\d*))",strOptions),re.search(r"(T(?!T))",strOptions)
    return [i.group(1) for i in [brtParseR,brtParseB,brtParseT] if i!=None]
def parseRwd(BRTOptions,graph):
    rwd=["R" in i for i in BRTOptions]
    if True in rwd:
        vtxRwd=0
        for option in BRTOptions:
            if "R" in option:
                if option[1:]!="":
                    vtxRwd=int(option[1:])
                else:
                    vtxRwd=graph["rwd"]
        return vtxRwd
    else:
        return None


def addEdges(vtxPairs,edges,mngmt,edgeProps,rwd,size):
    if mngmt=="!":
        for vtxPair in vtxPairs:
            added=set()
            x=vtxPair[0]
            edges[x]=edges[x]-{vtxPair[1]}
            if type(edgeProps[x])==set:
                    edgeProps[x]=[{str(z):z} for z in edges[x]]
            if len(added)!=0:
                for w in added: edgeProps[x].append({str(w):w})
    elif mngmt=="+":
        for vtxPair in vtxPairs:
            added=set()
            x=vtxPair[0]
            if vtxPair[1] not in edges[x]:
                edges[x]=edges[x]|{vtxPair[1]}
                added.add(vtxPair[1])
            if type(edgeProps[x])==set:
                edgeProps[x]=[{str(z):z} for z in edges[x]]
            if len(added)!=0:
                for w in added: edgeProps[x].append({str(w):w})
            if rwd!=None:  
                for edge in edgeProps[x]:
                    for j in edge.copy().keys():
                        if str(vtxPair[1])==j and vtxPair[1] in added:
                            edge["rwd"]=rwd
    elif mngmt=="*":
        for vtxPair in vtxPairs:
            added=set()
            x=vtxPair[0]
            if vtxPair[1] not in edges[x]:edges[x]=edges[x]|{vtxPair[1]};added.add(vtxPair[1])
            if type(edgeProps[x])==set:
                edgeProps[x]=[{str(z):z} for z in edges[x]]
            if len(added)!=0:
                for w in added: edgeProps[x].append({str(w):w})
            if rwd!=None:
                for edge in edgeProps[x]:
                    for j in edge.copy().keys():
                        if str(vtxPair[1])==j:
                            edge["rwd"]=rwd
    elif mngmt=="~":
        for vtxPair in vtxPairs:

            added=set()
            deleted=[]
            x=vtxPair[0]
            if vtxPair[1] in edges[x]: 
                edges[x]=edges[x]-{vtxPair[1]}
                deleted.append(vtxPair[1])
            
            elif vtxPair[1] not in edges[x]: edges[x]=edges[x]|{vtxPair[1]};added.add(vtxPair[1])
            toDelete=[]
            if type(edgeProps[x])==set:
                edgeProps[x]=[{str(z):z} for z in edges[x]]
            elif len(deleted)!=0:    
                for edge in range(len(edgeProps[x])):
                    if deleted[0] in edgeProps[x][edge].values():
                        toDelete.append(edge)
                toDelete=[edgeProps[x][i] for i in toDelete]
                for i in toDelete: edgeProps[x].remove(i)
                toDelete=[]
            elif len(added)!=0:
                for w in added: edgeProps[x].append({str(w):w})

            if rwd !=None:
                for edge in edgeProps[x]:
                    for j in edge.copy().keys():
                        if str(vtxPair[1])==j:
                            edge["rwd"]=rwd
        return edges,edgeProps
             
    elif mngmt=="@":
        for vtxPair in vtxPairs:
            added=set()
            x=vtxPair[0]
            if type(edgeProps[x])==set:
                edgeProps[x]=[{str(z):z} for z in edges[x]]
            if rwd!=None:     
                for edge in edgeProps[x]:
                    for j in edge.copy().keys():
                        if str(vtxPair[1])==j:
                            edge["rwd"]=rwd
    return edges,edgeProps
def getPairs(vslcs,direction,size,width):
    pairs=set()
    for i in vslcs:
        if "N" in direction and i-width>=0:
            pairs.add((i,i-width))
        if "S" in direction and i+width<size:
            pairs.add((i,i+width))
        if "E" in direction and (i+1)//width==i//width:
            pairs.add((i,i+1))
        if "W" in direction and (i-1)//width==i//width:
            pairs.add((i,i-1))
    return pairs
def rectify(edges,edgProps):
    if edgProps==None:
        return edgProps
    for vtx in range(len(edges)):
        copy=[]
        if type(edgProps[vtx])==set:
            edgProps[vtx]=edges[vtx]
        if type(edgProps[vtx])==list:
            for edge in edgProps[vtx]:

                if int(list(set(edge.keys())-{"rwd"})[0]) in edges[vtx] and edges[vtx]!=set():
                    copy.append(edge)
            edgProps[vtx]=copy
    return edgProps
def grfParse(args):
    graphDatastruct=[]
    graph={}
    edges=[]
    vtxProps=[]
    edgeProps=[]

    for arg in args:
        gDirective=re.search(r"^G([NG]?)(\d+)(W\d+)?(R\d+)?$", arg)
        vDirective=re.search(r"^(V)([^BRT]*)([R(\d+)BT]*)$",arg)
        edgDirective1=re.search(r"^E([\!\+\*\~\@]*)([^~=NESW]*)([~=])([^~=NESWRT]*)([R(\d+)T]*)$",arg)
        edgDirective2=re.search(r"^E([\!\+\*\~\@]*)([^~=NESW]*)([NESW]+)+([~=])([R(\d+)T]*)$",arg)
        if gDirective!=None:
            graph["type"]=gDirective.group(1)
            graph["size"]=int(gDirective.group(2))

            if gDirective.group(3) not in [None]:
                graph["width"]=int(gDirective.group(3)[1:])
            if graph["size"]==0:
                graph["type"]="N"
            if gDirective.group(3)==None:
                graph["width"]=findWidth(graph["size"])
            if gDirective.group(4)==None:
                graph["rwd"]=12
            else:
                graph["rwd"]=int(gDirective.group(4)[1:])
            if graph["type"]!="N" and graph["width"]!=0:
                edges=nativeEdges(graph["size"],graph["width"])
                vtxProps=[{} for i in range(len(edges))]
                edgeProps=[i for i in edges]
            graphDatastruct.append(graph)
        if vDirective!=None:
            vslcs=vDirective.group(2)
            brtOptions=parseBRTOptions(vDirective.group(3))

            W=parseVslices(vslcs,graph["size"],False)
            
            V={v for v in range(graph["size"])}
            X=V-W
            if "B" in brtOptions:
                updatedEdges=toDelete(edges.copy(),W,X,graph["size"])
                toRecover=toAdd(edges.copy(),W,X,graph["size"],graph["width"])
                diff=[toRecover[i]-edges[i] if toRecover[i]!=set() else edges[i] for i in range(len(toRecover))]
                edges=updatedEdges
                edges=[edges[i]|diff[i] if diff[i]!=set() else edges[i] for i in range(len(edges))]
                edgeProps=rectify(edges,edgeProps)
            rwd=["R" in i for i in brtOptions]
            vtxRwd=0
            for option in brtOptions:
                if "R" in option:
                    if option[1:]!="":
                        vtxRwd=int(option[1:])
                    else:
                        vtxRwd=graph["rwd"]
            if True in rwd:
                if vtxProps==[]:
                    vtxProps=[{} for i in range(graph["size"])]
                for edge in W:
                    vtxProps[edge]["rwd"]=vtxRwd
        if edgDirective1!=None:
            mngmt=edgDirective1.group(1)
            if mngmt=="":
                mngmt="~"
            vslcs1=edgDirective1.group(2)
            direction=edgDirective1.group(3)
            vslcs2=edgDirective1.group(4)
            rwdOptions=edgDirective1.group(5)
            if rwdOptions!="":
                rwdOptions=parseBRTOptions(rwdOptions)
                rwd=parseRwd(rwdOptions,graph)
            else:
                rwd=None
            vslcs1=parseVslices(vslcs1,graph["size"],True)
            vslcs2=parseVslices(vslcs2,graph["size"],True)
            vtxPairs={i for i in zip(vslcs1,vslcs2)}
            if direction=="=":
                vtxPairs={(i[0],i[1]) for i in vtxPairs}| {(j[1],j[0]) for j in vtxPairs}
            edges,edgeProps=addEdges(vtxPairs,edges,mngmt,edgeProps,rwd,graph["size"])
        if edgDirective2!=None:
            mngmt=edgDirective2.group(1)
            if mngmt=="":
                mngmt="~"
            vslcs=edgDirective2.group(2)
            directions=edgDirective2.group(3)
            directed=edgDirective2.group(4)
            rwdOptions=edgDirective2.group(5)
            if rwdOptions!="":
                rwdOptions=parseBRTOptions(rwdOptions)
                rwd=parseRwd(rwdOptions,graph)
            else:
                rwd=None
            vslcs=parseVslices(vslcs,graph["size"],True)
            vtxPairs=getPairs(vslcs,directions,graph["size"],graph["width"])
            if directed=="=":
                vtxPairs={(i[0],i[1]) for i in vtxPairs}| {(j[1],j[0]) for j in vtxPairs}
            edges,edgeProps=addEdges(vtxPairs,edges,mngmt,edgeProps,rwd,graph["size"])


    graphDatastruct.append(edges)
    graphDatastruct.append(vtxProps)
    graphDatastruct.append([i for i in range(len(vtxProps)) if vtxProps[i]!={}])
    graphDatastruct.append(edgeProps)
    return graphDatastruct
def grfGProps(grf):
    if grf[0]["type"]!="N":
        return {"rwd":grf[0]["rwd"],"width":grf[0]["width"]}
    else:
        return {"rwd":grf[0]["rwd"]}
def findWidth(size):
    min=999
    for i in range(math.ceil(size**0.5),size):
        if (size%i)==0 and i<min :
            min=i
    if min!=999:
        return min
    else:
        return size

def argmax(args,v):
    # print(v)

    if "" in v:
        while "" in v:
            v[v.index("")]=-5
    args=list(args)
    maxN=max(v)
    return [args[i] for i in range(len(v)) if v[i]==maxN ]

def grfFindOptimalPolicy(grf):
    pairs=set()
    edgeProps=grf[-1]
    for vtx in range(len(grf[-1])):
        if type(edgeProps[vtx])==list:
            for x in edgeProps[vtx]:
                rwd=0
                if len(x.keys())==1:
                    rwd=0
                else:
                    rwd=x["rwd"]
                pairs=pairs|{((vtx,int(list(x.keys())[0]),rwd))}
    size=grf[0]["size"]
    edges=grf[1]
    policy=edges
    value=grfValuePolicy(grf,policy,0.999,0,pairs)
    currentPolicy=grfPolicyFromValuation(grf,value,pairs)
    print("Initial",value,currentPolicy)
    count=0
    x=0
    while count<2:
        # print(count)
        if False not in [{*policy[i]}== {*currentPolicy[i]} for i in range(len(policy))]:
            count+=1
        policy=currentPolicy
        newValue=grfValueOneStep(grf,value,policy,0.995,size,pairs)
        currentPolicy=grfPolicyFromValuation(grf,newValue)
        # print(x)
        x+=1
        value=newValue
    # print(newValue)
    # print("valuation2", newValue)
    if "" not in value:
        currentPolicy=[set() if value[i]<=0 else currentPolicy[i] for i in range(size)]
    return currentPolicy

def grfValueOneStep(grf,previous, policy,gamma,size,pairs):
    width,size=grf[0]["width"],grf[0]["size"]
    if width==0 or grf[0]["type"]=="N":
        x=["" if i not in grf[-2] else grf[-3][i]["rwd"] for i in range(size)]
        return x
    value=previous.copy()
    for vtx in range(size):
        if vtx not in grf[-2]:
            if policy[vtx]==set():
                value[vtx]=0
            else:    
                listToAdd=[previous[x] for x in policy[vtx]]
                if pairs!=None:
                    for x in pairs:
                        if x[0]==vtx and x[1] in policy[vtx] and x[2]!=0:
                            listToAdd.remove(previous[x[1]])
                            listToAdd.append(x[2])
                        
                valueVtx=((sum(listToAdd))/len(listToAdd))
                value[vtx]=round((valueVtx*(gamma>0.5)*gamma)+((valueVtx-gamma)*(gamma<0.5)),4)
               
                for x in pairs:
                    if x[0]==vtx and x[1]==x[0] and x[2]!=0:
                        value[vtx]=x[2]
    
            
    return value
def grfValuePolicy(grf,policy,gamma,option=1,pairs=None):
    if pairs==None:
        pairs=getEdgePairs(grf)
    size,width=grf[0]["size"],grf[0]["width"]
    if width==0 or grf[0]["type"]=="N":
        x=["" if i not in grf[-2] else grf[-3][i]["rwd"] for i in range(size)]
        return x

    value=[0]*size
    for i in grf[-2]:
        value[i]=grf[-3][i]["rwd"]
    previous,policy=value.copy(),[{*i} for i in policy]
    print("preevious",previous)
    value=grfValueOneStep(grf,previous,policy,gamma,size,pairs)
    print(value)
    if option==0:
        return value
    count=0
    while abs(sum(value)-sum(previous))>0.01*size and False in [value[i]==previous[i] for i in range(0,len(value))]:
        count+=1
        previous=value.copy()
        value=grfValueOneStep(grf,previous,policy,gamma,size,pairs)
        # print(value)
    value=["" if x==0 else x for x in value ]
    return value

def getEdgePairs(grf):
    pairs=set()
    edgeProps=grf[-1]
    for vtx in range(len(grf[-1])):
        if type(edgeProps[vtx])==list:
            for x in edgeProps[vtx]:
                rwd=0
                if len(x.keys())==1:
                    rwd=0
                else:
                    rwd=x["rwd"]
                pairs=pairs|{((vtx,int(list(x.keys())[0]),rwd))}

    return pairs
def grfPolicyFromValuation(grf,values,pairs=None):
    if pairs==None:
        pairs=set()
        edgeProps=grf[-1]
        for vtx in range(len(grf[-1])):
            if type(edgeProps[vtx])==list:
                for x in edgeProps[vtx]:
                    rwd=0
                    if len(x.keys())==1:
                        rwd=0
                    else:
                        rwd=x["rwd"]
                    pairs=pairs|{((vtx,int(list(x.keys())[0]),rwd))}
    # print("paris",pairs)
    width=grf[0]["width"]
    size=grf[0]["size"]
    grfType=grf[0]["type"]
    if width==0 or grf[0]["type"]=="N":
        x=[[] if i not in grf[-2] else [] for i in range(size)]
        return x
    policy=[00]*size
    edges=grf[1]
    for vtx in range(size):
        if edges[vtx]==set() or values[vtx]=="" :
            directions=[]
        else:
           
            valuesArg=[]
            if pairs!=None:
                for x in edges[vtx]:
                    counted=False
                    for y in pairs:
                        if y[0]==vtx and y[1] ==x and y[2]!=0:
                            # print(valuesArg,y)
                            valuesArg.append(y[2])
                            counted=True
                    if counted==False:
                        valuesArg.append(values[x])
            
            
            else:
                valuesArg=[values[x] for x in edges[vtx] ]
            # print("AWODJAOIWHD",valuesArg, valuesArg, edges[vtx])
            directions=argmax(edges[vtx],valuesArg)
            directions=[i for i in directions if i in edges[vtx]]
            
        # directions=[(vtx+x in directions)*(vtx+x) for x in [1,-1,size,-size]]
        policy[vtx]=set(directions)
        if vtx in grf[-2]:
            policy[vtx]=set()
        # policy[vtx]=getCharacter(directions)
    return policy
def gridFromEdges(edges,width,size):
        dictOfSymbols={"<":[0,1,1,1],"J":[0,1,0,1],"W":[0,1,0,0],"7":[0,1,1,0],"N":[0,0,0,1],"^":[1,1,0,1],"+":[1,1,1,1],"v":[1,1,1,0],"S":[0,0,1,0],"L":[1,0,0,1],"E":[1,0,0,0],"r":[1,0,1,0], ">":[1,0,1,1], "-":[1,1,0,0],"|":[0,0,1,1],".":[0,0,0,0]}
        gridRepresentation=""
        for i in range(len(edges)):
            bearing=[(i+1 in edges[i])*((i+1)<size)*(i//width==(i+1)//width),(i-1 in edges[i])*((i-1)>=0)*((i-1)//width==i//width),(i+width) in edges[i], (i-width) in edges[i]]
            gridRepresentation+=list(dictOfSymbols.keys())[list(dictOfSymbols.values()).index(bearing)]
        return gridRepresentation
def getCharacter(direction):
    dictOfSymbols={"F":[0,1,1,1],"M":[0,1,0,1],"L":[0,1,0,0],"E":[0,1,1,0],"U":[0,0,0,1],"N":[1,1,0,1],"+":[1,1,1,1],"T":[1,1,1,0],"D":[0,0,1,0],"V":[1,0,0,1],"R":[1,0,0,0],"S":[1,0,1,0], "W":[1,0,1,1], "-":[1,1,0,0],"|":[0,0,1,1],".":[0,0,0,0]}
    gridRepresentation=list(dictOfSymbols.keys())[list(dictOfSymbols.values()).index(direction)]
    return gridRepresentation
def getJmps(grf,size,width):
    vslcs=[]
    oneDirection=[]
    biDirection=[]
    jmp=""
    option=True
    for i in range(size):
        
        diff=grf[1][i]-{i+1,i-1,i+width,i-width}
        if (i+1)//width !=i//width and i+1 in grf[1][i]:
            diff=diff|{(i+1)}
        if (i-1)//width !=i//width and i-1 in grf[1][i]:
            diff=diff|{(i-1)}
        diff=list(diff)
            

        if diff !=set():
            for k in diff:
                vslcs.append((i,k))
    for edge in range(len(vslcs)):
        for edge2 in range(0,len(vslcs)):
            if vslcs[edge2][1]==vslcs[edge][0] and vslcs[edge2][0]==vslcs[edge][1] and edge2!=edge and vslcs[edge] not in biDirection:
                biDirection.append(vslcs[edge2])
    oneDirection=list(set(vslcs)-set(biDirection))
    vslcs1=[]
    vslcs2=[]
    for pair in biDirection:
        vslcs1.append(pair[1])
        vslcs2.append(pair[0])
    vslcs1Direc=[]
    vslcs2Direc=[]
    for pair in oneDirection:
        vslcs1Direc.append(pair[0])
        vslcs2Direc.append(pair[1])
    if len(vslcs1)!=0:
        jmp+=str(vslcs1)[1:-1].replace(" ","")+"="+str(vslcs2)[1:-1].replace(" ","")+";"
    if len(vslcs1Direc)!=0:
        jmp+=str(vslcs1Direc)[1:-1].replace(" ","")+"~"+str(vslcs2Direc)[1:-1].replace(" ","")+";"


    if len(biDirection)!=0 or len(oneDirection):
        return jmp[:-1]
    
    else:
        return None
def grfStrEdges(grf):
    if grf[0]["type"]=="N":
        return ""
    elif grf[0]["width"]==0:
        return ""
    else:
        if len(grf)<1:
            return gridFromEdges(grf[1],grf[0]["width"],grf[0]["size"])
        else:
            jmps=getJmps(grf,grf[0]["size"],grf[0]["width"])
            
            if jmps==None:
                return gridFromEdges(grf[1],grf[0]["width"],grf[0]["size"])
            else:
                return gridFromEdges(grf[1],grf[0]["width"],grf[0]["size"])+"\n"+"Jumps: "+jmps



def grfSize(grf):
    return grf[0]["size"]
def strEdges(grf):
    # print(grf[3])
    strE=""
    edgesOption=False
    for vtx in grf[-1]:

        if type(vtx)==list:
            edgesOption=True
    if edgesOption==False:
        return ""
    else:
        edges=grf[1]
        rectifiedEdgProps=rectify(edges,grf[-1])
      
        for vtx in range(len(edges)):
            for edge in grf[-1][vtx]:
                if type(grf[-1][vtx])==list:
                    if "rwd" in edge.keys():
                        actualEdge=list(set(edge.keys())-{"rwd"})[0]
                        # print(actualEdge)
                        strE+="("+f"{vtx}"+","+f"{actualEdge}"+"): "+"rwd:"+str(edge["rwd"])+"\n"
        return strE[:-1]


def grfStrProps(grf):
    vertices=[i for i in range(len(grf[2])) if grf[2][i]!={}]
    vtxSgmt=""
    for v in vertices:
        vtxSgmt+=f"{v}:"+str(grfVProps(grf,v))+"\n"
    edgSgmt=strEdges(grf)
    return str(grfGProps(grf))+"\n"+vtxSgmt+edgSgmt



def grfVProps(grf,vtxIdx):
    isEmpty=[i=={} for i in grf[2]]
    if False not in isEmpty:
        return {}
    else:
        return grf[2][vtxIdx]
def grfNbrs(grf,vtxIdx):
    if grf[1]==[]:
        return []
    else:
        return grf[1][vtxIdx]
def grfEProps(grf,vtx1,vtx2):
    edgesOption=False
    for vtx in grf[-1]:
        if type(vtx)==list:
            edgesOption=True
    if edgesOption==False:
        return {}
    elif type(grf[-1][vtx1])==set:
        return {}
    else:
        for edges in grf[-1][vtx1]:
            for j in edges.copy().keys():
                if str(vtx2) ==j and "rwd" in edges.keys():
                    return {"rwd":edges["rwd"]}
        else:
            return {}
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

#Cmd line arguments
parsedArgs=[]
for arg in args:
    if re.search(r"^G([NG]?)(\d+)(W\d+)?(R\d+)?$", arg)!=None:
        parsedArgs.append(arg)
    if re.search(r"^(V)([^BRT]*)([R(\d+)BT]*)$",arg)!=None:
        parsedArgs.append(arg)
    if re.search(r"^E([\!\+\*\~\@]*)([^~=NESW]*)([~=])([^~=NESWRT]*)([R(\d+)T]*)$",arg)!=None:
        parsedArgs.append(arg)
    if re.search(r"^E([\!\+\*\~\@]*)([^~=NESW]*)([NESW]+)+([~=])([R(\d+)T]*)$",arg)!=None:
        parsedArgs.append(arg)
if parsedArgs!=[]:
    grf=grfParse(parsedArgs)
    if grf[0]["type"]!="N" and grf[0]["width"]!=0:
        strBoard2d=strEdgesCMD(grfStrEdges(grf),grf[0]["width"])
        print("Graph:")
        print(strBoard2d)
    print("Rewards:")
    print(grfStrProps(grf))

    # print("Valuation:",values)
    # if values==[]:
    #     print("Policy: ",[])
    # else: 
        # policy=grfPolicyFromValuation(grf,values)
        # print("Policy:",policy)
    # valuationT=[19.96, 19.95, 19.96, 19.97, 19.98, 19.99, 19.98, 19.97, 19.96, 6.96, 6.97, 6.98, 19.97, 19.96, 19.96, 19.97, 19.98, 19.98, 19.97, 19.96, 6.96, 6.97, 6.98, 6.99, 19.98, 19.97, 19.97, 19.98, 19.99, 19.98, 19.98, 19.97, 6.97, 6.98, 6.99, 7.0, 19.99, 19.98, 19.97, 19.97, 19.98, 19.98, 19.99, 19.98, 19.97, 6.97, 6.98, 6.99, 19.98, 19.97, 19.96, 19.96, 19.97, 19.97, 19.98, 19.97, 19.96, 6.96, 6.97, 6.98]
    # print("THIS IS IMPORTANT",grfPolicyFromValuation(grf,valuationT))
    x=grfFindOptimalPolicy(grf)

    v=grfValuePolicy(grf,x,0.99)
    print("Valuation:",v)
    print("Optimal Policy:")
    print(x)
def main():
    graph = grfParse(args)
    edgesStr = grfStrEdges(graph)
    processEdges=strEdgesCMD(edgesStr,grf[0]["width"])
    print(processEdges)
    propsStr = grfStrProps(graph)

if __name__ == '__main__ ': main() 
#Ashwin Pulla 6 2024