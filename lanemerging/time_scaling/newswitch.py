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

def mpccaller(x0,y0,xob,yob,th,na,mela,ob,vipas,wipas,mpv,mpw):
	#"-nojvm -nodisplay -nosplash"
	eng = matlab.engine.start_matlab("-nojvm -nodisplay -nosplash")
	eng.addpath(r'/home/raghu/Desktop/Iv_2019/Results_videos/lanemerging/mtlb')
	vlast,wlast,vsend,wsend,v_movx,v_movy,stateRobo,stateObst,oth,r_ob=eng.launch_iros(float(x0),float(y0),matlab.double(xob),matlab.double(yob),float(th),na,mela,ob,vipas,wipas, nargout=10)
	eng.quit()
	x_points_right=np.genfromtxt('/home/raghu/Desktop/Iv_2019/Results_videos/lanemerging/mtlb/x_points_right.csv')
	x_points_left=np.genfromtxt('/home/raghu/Desktop/Iv_2019/Results_videos/lanemerging/mtlb/x_points_left.csv')
	y_points_right=np.genfromtxt('/home/raghu/Desktop/Iv_2019/Results_videos/lanemerging/mtlb/y_points_right.csv')
	y_points_left=np.genfromtxt('/home/raghu/Desktop/Iv_2019/Results_videos/lanemerging/mtlb/y_points_left.csv')
	# x_points_midleft=np.genfromtxt('/home/raghu/Desktop/Iv_2019/Results_videos/lanemerging/time_scaling/x_points_midleft.csv')
	# y_points_midleft=np.genfromtxt('/home/raghu/Desktop/Iv_2019/Results_videos/lanemerging/time_scaling/y_points_midleft.csv')
	# stateRobo=np.hstack(stateRobo)
	# stateObst=np.hstack(stateObst)

	vsend = np.array(vsend)
	vsend = np.transpose(vsend)
	print('mpc returns',np.shape(vsend))
	# vsend[0]=0

	# if len(mpv)==0:
	# 	kali = 1
	# else:
	# 	kali=0
	mpv = np.append(mpv,vsend)
	# if kali !=1:
	# 	print('vsend obtained is',vsend[0])
	# 	mpv[len(vsend)]=0
	wsend = np.array(wsend)
	wsend = np.transpose(wsend)
	mpw= np.append(mpw,wsend)
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
	return vlast,wlast,vsend,wsend,v_movx,v_movy,stateRobo,stateObst,x_points_right,y_points_right,x_points_left,y_points_left,oth,r_ob,mpv,mpw


def tscc(stateRobo,stateObst,vl,wl,x_points_right,y_points_right,x_points_left,y_points_left,v_movx,v_movy,oth,r_ob):
	#storing output arguments
	#calling timescaling 


	# np.asarray(stateRobo)
	# print('after np',type(stateRobo))
	# print('after list',type(stateRobo))
	velocity,omega,deltT,stateRobo,stateObst,cumxp,cumyp,cumxob,cumyob,cum_vel,cum_om,yaw = timescalingex(list(stateRobo),list(stateObst),vl,wl,x_points_right,y_points_right,x_points_left,y_points_left,v_movx,v_movy,oth,r_ob)
	# finalscale=np.array([])
	# finalscale=np.concatenate((finalscale,cumscale),axis=0)
	# np.savetxt('scalepedes.csv',finalscale)
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

def plotter(prex,prey,prox,proy,cum_vel,cum_om,stateObst,x_points_right,y_points_right,x_points_left,y_points_left,rob,thl,yaw,mpv,mpw):
    fig2=plt.figure()
    yaw=yaw*180/3.14
    # y_points_left[31:]=y_points_left[31:]-6;
    with writer.saving(fig2, "writer_test.mp4", 100):
	    for i in range(len(prex)):
	    	h = 5
	    	w = 3

	    	# for du in range(len(dobx)):
	    	# 	rect3 = plt.Rectangle((dobx[du][i],doby[du][i]),h,w,color='blue')
	    	# 	ax=plt.gca()
	    	# 	ax.add_artist(rect3)
	    	
	    	xlmark = np.genfromtxt('/home/raghu/Desktop/Iv_2019/Results_videos/lanemerging/time_scaling/xlmark.csv')
	    	ylmark = np.genfromtxt('/home/raghu/Desktop/Iv_2019/Results_videos/lanemerging/time_scaling/ylmark.csv')
	    	

	    	plt.plot(xlmark+6,ylmark+3,linestyle='--',color='black')
	    	plt.plot(x_points_right,y_points_right-7,linestyle='solid',color='black')
	    	plt.fill_between(x_points_right,-1000,y_points_right-7,facecolor=(0.8,0.8,0.8))
	    	plt.fill_between(x_points_left,1000,y_points_left+3,facecolor=(0.8,0.8,0.8))
	    	# plt.plot((x_points_left+x_points_right)/2 ,(y_points_left+y_points_right)/2 ,linestyle='--',color='black')
	    	# plt.plot(x_points_left[:27],y_new_left,marker='*',color='blue',)
	    	plt.plot(x_points_left,y_points_left+3,linestyle='solid',color='black')

	    	# plt.plot(x_points_midleft,y_points_midleft,linestyle='--',color='black')
	    	plt.plot(prex-h/2,prey-w/2,label='robot',linestyle='--',color='blue')
	    	
	    	for oi in range(len(stateObst)):
	    		# plt.plot(prox[oi],proy[oi],label='obstacle')
	    		plt.plot(prox[oi][i],proy[oi][i],label='obstacle')
	    	# if yaw[i]<=0.2:
	    	# 	circle1 = plt.Rectangle((prex[i]-h/2,prey[i]-w/2),h,w,angle=yaw[i],color='r')
	    	# else:

	    	circle1 = plt.Rectangle((prex[i],prey[i]),h,w,angle=yaw[i],color='r')
	    	ax = plt.gca()
	    	ax.add_artist(circle1)
	    	
	    	for mi in range(len(stateObst)):
	    		rect2 = plt.Rectangle((prox[mi][i]-h/2,proy[mi][i]-w/2),h,w,angle=0,color='black')
	    		if mi >=3:
	    			if (mi%2==0):
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
	    	axes.set_xlim(0, 100)
	    	axes.set_ylim(0, 15)
	    	time.sleep(0.0005)
	    	plt.pause(1e-17)
	    	writer.grab_frame()
	    	plt.cla()
	    # plt.close(fig)
	    plt.close(fig2)
	    fig3 = plt.figure(3)
	    plt.plot(cum_vel,label='tscc velo')
	    plt.plot(mpv,label='mpc velocity')
	    plt.xlabel('DeltaT')
	    plt.ylabel('Scaled Linear velocities')
	    plt.savefig('Velocityplot.png')
	    plt.legend()
	    plt.show(block=False)
	    time.sleep(1)
	    plt.close(fig3)
	    fig4 = plt.figure(4)
	    plt.plot(cum_om,label='tscc velo')
	    plt.plot(mpw,label = 'mpc velo')
	    plt.xlabel('DeltaT')
	    plt.ylabel('Scaled Angular velocities')
	    plt.savefig('omegaplot.png')
	    plt.legend()
	    plt.show(block=False)
	    time.sleep(1)
	    plt.close(fig4)
	    np.savetxt('cum_vel_4obs.csv',mpv)
	    np.savetxt('cum_om_4obs.csv',cum_om)
	   
    return


## main code begins here ##
#mpccaller(x0,y0,xob,yob,th,na,mela,ob)
#call mpc to get the velocities and omega values
mpv= np.array([])
mpw =np.array([])
vipas=0.01;wipas=0
vlast,wlast,vgot,wgot,v_movx,v_movy,stateRobo,stateObst,x_points_right,y_points_right,x_points_left,y_points_left,oth,r_ob,mpv,mpw=mpccaller(1,0,[-5,42,30],[33,33,25],0.785,10,1,1,vipas,wipas,mpv,mpw)

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
	if stateRobo[0]==1250:
		stateObst.append([20,10,2.355,1])
		stateObst.append([0,20,2.355,-1])
		stateObst.append([20,12,1.57,-1])
		stateObst.append([0,18,1.57,1])
		# stateObst.append([119,217,1.57,-1])
		# stateObst.append([120,200,1.57,1])
		# stateObst.append([121,217,1.57,-1])
		# stateObst.append([122,200,1.57,1])
		# stateObst.append([123,217,1.57,-1])
		# stateObst.append([124,200,1.57,1])
	velocity,omega,deltT,stateRobo,stateObst,cumxp,cumyp,cumxob,cumyob,cum_vel,cum_om,yaw=tscc(stateRobo,stateObst,vgot,wgot,x_points_right,y_points_right,x_points_left,y_points_left,v_movx,v_movy,oth,r_ob)
	
	#accumuliation and plotting
	prex=np.concatenate((prex,cumxp),axis=0)
	prey=np.concatenate((prey,cumyp),axis=0)
	cumyaw=np.concatenate((cumyaw,yaw),axis=0)
    
	if len(prox)==0:
		for li in range(len(stateObst)):
			prox.append(cumxob[li])
			proy.append(cumyob[li])
	else:
		for li in range(len(stateObst)):
			prox[li]=prox[li]+cumxob[li]
			proy[li]=proy[li]+cumyob[li]
	# if simulationtime==9:
	# 	cum_vel[0]=0
	finalvel=np.concatenate((finalvel,cum_vel),axis=0)
	finalom=np.concatenate((finalom,cum_om),axis=0)
	# print(finalom)
	xob=[];yob=[]
	xl = stateRobo[0];yl = stateRobo[1]
	thl=stateRobo[2]
	for i in range(len(stateObst)):
		xob.append(stateObst[i][0])
		yob.append(stateObst[i][1])
	print('simulation time is',simulationtime)	
	
	np.savetxt('lmx.csv',prex)
	np.savetxt('lmy.csv',prey)
	plotter(prex,prey,prox,proy,finalvel,finalom,stateObst,x_points_right,y_points_right,x_points_left,y_points_left,r_ob,thl,cumyaw,mpv,mpw)
	vipas = stateRobo[3]
	wipas = stateRobo[4]
	vlast,wlast,vgot,wgot,v_movx,v_movy,stateRobo,stateObst,x_points_right,y_points_right,x_points_left,y_points_left,oth,r_ob,mpv,mpw=mpccaller(xl,yl,xob,yob,thl,10,1,1,float(stateRobo[3]),float(stateRobo[4]),mpv,mpw)
	simulationtime-=1

print('The end')