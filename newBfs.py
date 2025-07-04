def bfs(vtxRwds,edges,size,width):
    queue=vtxRwds.copy()
    marked=[False]*size
    visited=[]
    temp=[]
    while queue:
        v=queue.pop(0)
        
        if not marked[v]:
            marked[v]=True
            visited.append(v)
            if v in vtxRwds:
                temp.append([v])
            
            for neighbors in edges[v]:
                    
                if not marked[neighbors]:

                    queue.append(neighbors)
                    temp.append((neighbors,v))
    final=[]
    return v