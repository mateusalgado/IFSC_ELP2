"""Completa os dois ramos de sinal com busca em grade e obstáculos da placa B."""
from pathlib import Path
import json, math, heapq
import numpy as np
from router import Router, HV_NETS  # barreira: free &= xx < 80.5 (trilha 0,5 mm -> borda 80,75 <= 81,2)
HERE=Path(__file__).parent
F=HERE/'rotas.json'
data=json.loads(F.read_text())
r=Router()
grid=0.4
xx,yy=np.meshgrid(np.arange(0,82,grid),np.arange(0,90,grid))
h,w=xx.shape
layers=['F.Cu','B.Cu']
def search(net,ref,end,record):
    track=0.5
    free=np.ones((2,h,w),dtype=bool)
    via=np.ones((h,w),dtype=bool)
    def block(obs,mask,rad):
        mask &= obs > rad*rad
    def squared(ax,ay,bx,by):
        dx,dy=bx-ax,by-ay
        q=np.clip(((xx-ax)*dx+(yy-ay)*dy)/(dx*dx+dy*dy),0,1) if dx or dy else 0
        return (xx-ax-q*dx)**2+(yy-ay-q*dy)**2
    for ob in r.pads:
        if ob['net']==net:continue
        margin=1 if ob['net'] in HV_NETS else .30
        ds=(xx-ob['x'])**2+(yy-ob['y'])**2
        block(ds,free,ob['r']+margin+.25+.22)
        block(ds,via,ob['r']+margin+.60+.22)
    for ob in data['tracks']:
        if ob['net']==net:continue
        ds=squared(ob['x1'],ob['y1'],ob['x2'],ob['y2'])
        margin=1 if ob['net'] in HV_NETS else .30
        block(ds,free[layers.index(ob['layer'])],ob['w']/2+margin+.25+.22)
        block(ds,via,ob['w']/2+margin+.60+.22)
    for ob in data['vias']:
        if ob['net']==net:continue
        ds=(xx-ob['x'])**2+(yy-ob['y'])**2
        margin=1 if ob['net'] in HV_NETS else .30
        block(ds,free,ob['d']/2+margin+.25+.22);block(ds,via,ob['d']/2+margin+.60+.22)
    free &= (xx>1.5)&(xx<80.5)&(yy>1.5)&(yy<88)
    pa=next(ob for ob in r.pads if ob['ref']+'.'+ob['num']==ref)
    pb=next(ob for ob in r.pads if ob['ref']+'.'+ob['num']==end)
    def node(p):return int(round(p['x']/grid)),int(round(p['y']/grid))
    A,B=node(pa),node(pb)
    queue=[]; dist={}; parent={}
    for lay in (0,1):
        state=(*A,lay)
        if free[lay,A[1],A[0]]:
            dist[state]=0;heapq.heappush(queue,(0,0,state))
    while queue:
        _,g,state=heapq.heappop(queue)
        if g!=dist[state]:continue
        x,y,k=state
        if (x,y)==B:break
        options=[(x+dx,y+dy,k,math.hypot(dx,dy)*(1 if k==0 else 2.2)) for dx,dy in [(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]]
        if via[y,x]:options.append((x,y,1-k,20))
        for nx,ny,nk,cost in options:
            if not(0<=nx<w and 0<=ny<h and free[nk,ny,nx]):continue
            child=(nx,ny,nk); ng=g+cost
            if ng>=dist.get(child,1e20):continue
            dist[child]=ng;parent[child]=state
            heapq.heappush(queue,(ng+math.hypot(nx-B[0],ny-B[1]),ng,child))
    else: raise ValueError((net,ref,end,'sem caminho'))
    chain=[state]
    while chain[-1] in parent:chain.append(parent[chain[-1]])
    chain.reverse()
    seq=[(pa['x'],pa['y'],chain[0][2])]+[(round(x*grid,4),round(y*grid,4),k) for x,y,k in chain]+[(pb['x'],pb['y'],chain[-1][2])]
    pts=[]
    for v in seq:
        if pts and pts[-1]==v:continue
        if len(pts)>1 and pts[-2][2]==pts[-1][2]==v[2]:
            a,b=pts[-2:]; cross=(b[0]-a[0])*(v[1]-b[1])-(b[1]-a[1])*(v[0]-b[0])
            if abs(cross)<1e-6:pts.pop()
        pts.append(v)
    for a,b in zip(pts,pts[1:]):
        if a[2]!=b[2]:
            data['vias'].append(dict(net=net,x=a[0],y=a[1],d=1.2,drill=.5))
        else:data['tracks'].append(dict(net=net,layer=layers[a[2]],x1=a[0],y1=a[1],x2=b[0],y2=b[1],w=track))
    record.append([net,ref,end])
if __name__=='__main__' and 'ramos_B' not in data:
    done=[]
    search('/DRV','U1.6','R7.1',done)
    search('/CS','R11.1','C3.1',done)
    data['ramos_B']=done
    F.write_text(json.dumps(data,indent=1),'utf8')
    print(done)

