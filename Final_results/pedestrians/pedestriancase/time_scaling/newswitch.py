import matlab.engine
import numpy as np 
from timescalingex import timescalingex 
#from math import cos,sin,pi
import matplotlib.pyplot as plt
import matplotlib
# matplotlib.use("Agg")
import time
import matplotlib.animation as manimation
#stateRobo=[x0,y0,th,vn,wn]
FFMpegWriter = manimation.writers['ffmpeg']
metadata = dict(title='Movie Test', artist='Matplotlib',
                comment='Movie support!')
writer = FFMpegWriter(fps=15, metadata=metadata)

def mpccaller(x0,y0,xob,yob,th,na,mela,ob,vipas,wipas):
	#"-nojvm -nodisplay -nosplash"
	eng = matlab.engine.start_matlab("-nojvm -nodisplay -nosplash")
	eng.addpath(r'/home/raghu/Desktop/Iv_2019/Final_results/pedestrians/pedestriancase/mtlb')
	vlast,wlast,vsend,wsend,v_movx,v_movy,stateRobo,stateObst,oth,r_ob=eng.launch_iros(float(x0),float(y0),matlab.double(xob),matlab.double(yob),float(th),na,mela,ob,float(vipas),float(wipas), nargout=10)
	eng.quit()
	x_points_right=np.genfromtxt('/home/raghu/Desktop/Iv_2019/Final_results/pedestrians/pedestriancase/time_scaling/x_points_right.csv')
	x_points_left=np.genfromtxt('/home/raghu/Desktop/Iv_2019/Final_results/pedestrians/pedestriancase/time_scaling/x_points_left.csv')
	y_points_right=np.genfromtxt('/home/raghu/Desktop/Iv_2019/Final_results/pedestrians/pedestriancase/time_scaling/y_points_right.csv')
	y_points_left=np.genfromtxt('/home/raghu/Desktop/Iv_2019/Final_results/pedestrians/pedestriancase/time_scaling/y_points_left.csv')
	x_points_midleft=np.genfromtxt('/home/raghu/Desktop/Iv_2019/Final_results/pedestrians/pedestriancase/time_scaling/x_points_midleft.csv')
	y_points_midleft=np.genfromtxt('/home/raghu/Desktop/Iv_2019/Final_results/pedestrians/pedestriancase/time_scaling/y_points_midleft.csv')
	# stateRobo=np.hstack(stateRobo)
	# stateObst=np.hstack(stateObst)
	
	vsend = np.array(vsend)
	vsend = np.transpose(vsend)
	wsend = np.array(wsend)
	wsend = np.transpose(wsend)
	stateRobo=stateRobo[0]
	c=[];v=[];t=[]
	for i in stateObst:
		for j in i:
			c.append(j)
		v.append(c)
		c=[]
	stateObst=v
	for r in r_ob:
		t.append(np.float32(r))
	r_ob=list(t[0])
	return vlast,wlast,vsend,wsend,v_movx,v_movy,stateRobo,stateObst,x_points_right,y_points_right,x_points_left,y_points_left,oth,r_ob,x_points_midleft,y_points_midleft


def tscc(stateRobo,stateObst,vl,wl,x_points_right,y_points_right,x_points_left,y_points_left,v_movx,v_movy,oth,r_ob):
	#storing output arguments
	#calling timescaling 


	# np.asarray(stateRobo)
	# print('after np',type(stateRobo))
	# print('after list',type(stateRobo))
	velocity,omega,deltT,stateRobo,stateObst,cumxp,cumyp,cumxob,cumyob,cum_vel,cum_om,yaw,cumscale = timescalingex(list(stateRobo),list(stateObst),vl,wl,x_points_right,y_points_right,x_points_left,y_points_left,v_movx,v_movy,oth,r_ob)
	finalscale=np.array([])
	finalscale=np.concatenate((finalscale,cumscale),axis=0)
	np.savetxt('scalepedes.csv',finalscale)
	return velocity,omega,deltT,stateRobo,stateObst,cumxp,cumyp,cumxob,cumyob,cum_vel,cum_om,yaw

def dummyobs(x,y):
	n=100
	dobx=[];doby=[]
	vi=0.3
	for i in range(len(x)):
		x0=x[i]
		y0=y[i]
		x1=[];y1=[]
		if i!=0:
			vi = 0.15
		for k in range(n):
			x1.append(x0+k*vi)
			y1.append(y0)
		dobx.append(x1)
		doby.append(y1)	
	# print(dobx,doby)
	return dobx,doby

def plotter(prex,prey,prox,proy,cum_vel,cum_om,stateObst,x_points_right,y_points_right,x_points_left,y_points_left,rob,thl,yaw,x_points_midleft,y_points_midleft):
    fig2=plt.figure()
    yaw=yaw*180/3.14
    with writer.saving(fig2, "writer_test.mp4", 100):
	    for i in range(len(prex)):
	    	h = 3
	    	w = 2.5

	    	# for du in range(len(dobx)):
	    	# 	rect3 = plt.Rectangle((dobx[du][i],doby[du][i]),h,w,color='blue')
	    	# 	ax=plt.gca()
	    	# 	ax.add_artist(rect3)

	    	plt.plot(x_points_right,y_points_right,linestyle='solid',color='black')
	    	plt.fill_between(x_points_right,0,y_points_right,facecolor=(0.5,0.5,0.5))
	    	plt.fill_between(x_points_left,1000,y_points_left,facecolor=(0.5,0.5,0.5))
	    	# plt.plot((x_points_left+x_points_right)/2 ,(y_points_left+y_points_right)/2-3 ,linestyle='--',color='black')
	    	plt.plot(x_points_left,y_points_left,linestyle='solid',color='black')
	    	# plt.plot(x_points_midleft,y_points_midleft,linestyle='--',color='black')
	    	plt.plot(prex,prey,label='robot',linestyle=':')
	    	
	    	for oi in range(len(stateObst)):
	    		#plt.plot(prox[oi],proy[oi],label='obstacle')
	    		plt.plot(prox[oi][i],proy[oi][i],label='obstacle')
	    	circle1 = plt.Rectangle((prex[i]-h/2,prey[i]-w/2),h,w,angle=yaw[i],color='r')
	    	ax = plt.gca()
	    	ax.add_artist(circle1)
	    	
	    	for mi in range(len(stateObst)):
	    		rect2 = plt.Rectangle((prox[mi][i]-h/2,proy[mi][i]-w/2),h,w,angle=0,color='black')
	    		if mi >=1:
	    			if mi%2==0:
	    				rect2 = plt.Circle((prox[mi][i]-h/2,proy[mi][i]-w/2),rob[mi]+0.3,angle=yaw[i],color='blue')
	    			else:
	    				rect2 = plt.Circle((prox[mi][i]-h/2,proy[mi][i]-w/2),rob[mi]+0.3,angle=yaw[i],color='g')
	    		ax = plt.gca()
	    		ax.add_artist(rect2)
	    		ax.axis('equal')
	    		ax.axis('equal')

	    	
	    	# plt.plot(prex[i],prey[i],marker='o',markersize=10)
	    	#plt.plot(prox[i],proy[i],marker='s',markersize=10)
	    	plt.draw()
	    	axes = plt.gca()
	    	axes.set_xlim(100, 150)
	    	axes.set_ylim(205, 210)
	    	time.sleep(0.0005)
	    	plt.pause(1e-17)
	    	writer.grab_frame()
	    	plt.cla()
	    # plt.close(fig)
	    plt.close(fig2)
	    fig3 = plt.figure(3)
	    plt.plot(cum_vel)
	    plt.xlabel('DeltaT')
	    plt.ylabel('Scaled Linear velocities')
	    plt.savefig('Velocityplot.png')
	    plt.axis((0,30,0,7))
	    plt.show(block=False)
	    time.sleep(1)
	    plt.close(fig3)
	    fig4 = plt.figure(4)
	    plt.plot(cum_om)
	    plt.xlabel('DeltaT')
	    plt.ylabel('Scaled Angular velocities')
	    plt.savefig('omegaplot.png')
	    plt.show(block=False)
	    time.sleep(1)
	    plt.close(fig4)
	    np.savetxt('cum_vel_pedestrian.csv',cum_vel)
	    np.savetxt('cum_om_pedestrian.csv',cum_om)
	   
    return


## main code begins here ##
#mpccaller(x0,y0,xob,yob,th,na,mela,ob)
#call mpc to get the velocities and omega values
vipas =5
wipas =0.1
vlast,wlast,vgot,wgot,v_movx,v_movy,stateRobo,stateObst,x_points_right,y_points_right,x_points_left,y_points_left,oth,r_ob,x_points_midleft,y_points_midleft=mpccaller(109,210,[135],[210],0,10,1,1,vipas,wipas)
stateRobo[3]=vgot[0]
stateRobo[4]=wgot[0]
# dobx,doby=dummyobs([145,175,102],[216,209,222])
#MPC only can plot mpc velocities properly as we are sending velocites once in 1 second
#xp,yp,x_ob,y_ob,tht = plotter(vgot,wgot,0.2,0,0,0,15,0,v_movx,v_movy,n_ob)
# stateRobo=[0,0,0,0.01,0]
# #The velocities and omegas obtained from MPC are passed to tscc

prex=np.array([])
prey=np.array([])
prox=[]
proy=[] 
cumyaw =np.array([])
finalvel=np.array([])
finalom=np.array([])
simulationtime=10
while(simulationtime):
	if (stateRobo[0] == 109):
		# stateObst.append([115,217,1.57,-1])
		# stateObst.append([115,200,1.57,1])
		# stateObst.append([112,217,1.57,-1])
		# stateObst.append([113,200,1.57,1])
		stateObst.append([130,217,1.57,-1])
		stateObst.append([131,200,1.57,1])
		stateObst.append([132,217,1.57,-1])
		stateObst.append([133,200,1.57,1])
		stateObst.append([134,217,1.57,-1])
		stateObst.append([135,200,1.57,1])
		obsta=1
	velocity,omega,deltT,stateRobo,stateObst,cumxp,cumyp,cumxob,cumyob,cum_vel,cum_om,yaw=tscc(stateRobo,stateObst,vgot,wgot,x_points_right,y_points_right,x_points_left,y_points_left,v_movx,v_movy,oth,r_ob)
	
	#accumuliation and plotting
	prex=np.concatenate((prex,cumxp),axis=0)
	prey=np.concatenate((prey,cumyp),axis=0)
	cumyaw=np.concatenate((cumyaw,yaw),axis=0)
    
	if len(prox)==0 :
		for li in range(len(stateObst)):
			prox.append(cumxob[li])
			proy.append(cumyob[li])

	# elif( len(prox)<len(stateObst)):
	# 	for li in range(len(prox)):
	# 		prox[li]=prox[li]+cumxob[li]
	# 		proy[li]=proy[li]+cumyob[li]
	# 	for ki in range(len(stateObst)-len(prox)):
	# 		mi = len(prox)
	# 		prox.append(cumxob[mi])
	# 		proy.append(cumyob[mi])
	else:
		for li in range(len(stateObst)):
			prox[li]=prox[li]+cumxob[li]
			proy[li]=proy[li]+cumyob[li]
	
	finalvel=np.concatenate((finalvel,cum_vel),axis=0)
	finalom=np.concatenate((finalom,cum_om),axis=0)
	# print(finalom)
	xob=[];yob=[]
	xl = stateRobo[0];yl = stateRobo[1]
	thl=stateRobo[2]
	for i in range(len(stateObst)):
		xob.append(stateObst[i][0])
		yob.append(stateObst[i][1])

	plotter(prex,prey,prox,proy,finalvel,finalom,stateObst,x_points_right,y_points_right,x_points_left,y_points_left,r_ob,thl,cumyaw,x_points_midleft,y_points_midleft)
	vipas = stateRobo[3]
	wipas = stateRobo[4]
	print('before',stateObst)
	if obsta==1:
		del stateObst[1:]
	print('after',stateObst)

	vlast,wlast,vgot,wgot,v_movx,v_movy,stateRobo,stateObst,x_points_right,y_points_right,x_points_left,y_points_left,oth,r_ob,x_points_midleft,y_points_midleft=mpccaller(xl,yl,xob,yob,thl,10,1,1,vipas,wipas)
	simulationtime-=1

print('The end')