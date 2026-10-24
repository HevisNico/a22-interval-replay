"""Exploratory b-only disorder and analytic adjoints. Not a certificate."""
import json,math
from pathlib import Path
import numpy as np
from scipy.optimize import minimize
A=math.log(4);K=.5;LM=math.log(1.25)/.02;LE=A/.15;G=np.array([.3,1.2,.3])

def h(x):return A/(A-K)*(np.exp(-K*x)-np.exp(-A*x))
def dh(x):return A/(A-K)*(A*np.exp(-A*x)-K*np.exp(-K*x))
def root(g,x,start):
 f=np.mean(x,axis=-1)+start
 for _ in range(12):
  v=f[...,None]-x
  f-=(np.sum(g*h(v),axis=-1)-.9)/np.sum(g*dh(v),axis=-1)
 return f

def step(x,b,derivatives=False):
 z=np.stack([np.roll(x,1),x,np.roll(x,-1)],axis=-1)
 f=root(G,z,.6666)
 R=(math.log(2.5)+b*(f+1)+.1*np.sum(8+z+.02,axis=-1)-.024+.3/LM)/(b+.3)
 d=R[:,None]-z-9.1;e=.8*np.exp(-LE*d)
 gamma=np.clip(e-.2,0,.6);g=G*np.exp(gamma)
 out=root(g,z,.27)
 if not derivatives:return out-out.mean()
 raw=G*dh(f[:,None]-z);t=raw/raw.sum(axis=-1)[:,None]
 rp=(b[:,None]*t+.1)/(b[:,None]+.3)
 r1=g*dh(out[:,None]-z);den=r1.sum(axis=-1);weights=r1/den[:,None]
 c=g*h(out[:,None]-z)*LE*e*((d>0)&(d<.15))/den[:,None]
 jac=weights-c+c.sum(axis=-1)[:,None]*rp
 db=c.sum(axis=-1)*(f+1-R)/(b+.3)
 return out-out.mean(),jac,db

def forward(controls,record=False):
 x=np.zeros(12);hist=[]
 for row in controls:
  x=step(x,.08+1e-5*row)
  if record:hist.append(x.tolist())
 return x,hist

def objective(c,n):
 c=c.reshape(n,12);x=np.zeros(12);tape=[]
 for row in c:
  x,j,db=step(x,.08+1e-5*row,True);tape.append((j,db))
 loss=-(x[0]-x[6]);adj=np.zeros(12);adj[0]=-1;adj[6]=1;grad=[]
 for j,db in reversed(tape):
  adj-=adj.mean();grad.append(adj*db*1e-5)
  adj=adj*j[:,1]+np.roll(adj*j[:,0],-1)+np.roll(adj*j[:,2],1)
 return loss,np.array(grad[::-1]).ravel()

def main():
 rows=[]
 for n in [6,12,24,63]:
  control=np.tile(np.array([-1]*6+[1]*6),(n,1));x,hist=forward(control,True)
  rows.append({'family':'half-ring fixed b','layers':n,'controls':control.astype(int).tolist(),'diameter':float(np.ptp(x)),'history':hist})
  print(json.dumps({'fixed_layers':n,'diameter':float(np.ptp(x))}),flush=True)
 # Gradients checked on a smooth interior point, away from clipping boundaries.
 rng=np.random.default_rng(20261025);c=rng.uniform(-.1,.1,(6,12));f,g=objective(c,6)
 errors=[]
 for k in [0,7,21,39,65]:
  cp=c.ravel().copy();cm=cp.copy();cp[k]+=1e-4;cm[k]-=1e-4
  numeric=(objective(cp,6)[0]-objective(cm,6)[0])/2e-4
  errors.append(abs(numeric-g[k]))
 if max(errors)>2e-8:raise RuntimeError('adjoint check failed')
 for n in [12,24,63]:
  for seed in [0,1]:
   init=np.tile(np.array([-1]*6+[1]*6),(n,1)).astype(float) if seed==0 else rng.uniform(-1,1,(n,12))
   opt=minimize(lambda c:objective(c,n),init.ravel(),jac=True,bounds=[(-1,1)]*(12*n),method='L-BFGS-B',options={'maxiter':200,'ftol':1e-12,'gtol':1e-9,'maxls':30})
   controls=opt.x.reshape(n,12);x,hist=forward(controls,True)
   rec={'family':'adversarial b only','layers':n,'seed':seed,'success':bool(opt.success),'message':str(opt.message),'controls':controls.tolist(),'diameter':float(np.ptp(x)),'objective_gap':float(x[0]-x[6]),'history':hist}
   rows.append(rec);print(json.dumps({k:rec[k] for k in ['family','layers','seed','success','diameter']}),flush=True)
   (Path(__file__).parent/'results/disorder_search.json').write_text(json.dumps({'status':'EXPLORATORY_ONLY','gradient_check_max_absolute_error':max(errors),'results':rows},indent=2)+'\n')
if __name__=='__main__':main()
