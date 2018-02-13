import numpy as np
import time as t
import scipy.optimize as scip 
import pylab as pl

# epsilon is the threshold for the newtons method
def newtonmethod(x_o,epsilon):
		count = 0 
		tolerance = epsilon 
		x = x_o
		x_last = x_o
		while np.abs(x-x_last)>tolerance or count == 0 :
			if count == 69:
				return np.nan
			x_last = x
			x = x_last - (np.log(x_last**2)/(2/x_last))
			count += 1



		return count,x,epsilon,x_o


iterations = []
X = []
x_o = np.linspace(10**(-4),2.5,100)
x_o = np.append(x_o,1)
x_o.sort()
for x in x_o:
	a,b,c,d = newtonmethod(x,0.0001)
	iterations.append(a)
	X.append(d)
	#print(b)

pl.plot(X,iterations)
pl.xlabel("Inital x_o")
pl.ylabel("Number of iterations")
pl.title("Number of iterations with respect to x_o with a tolerance of 10e-4")
pl.ylim(-1,10)
pl.xlim(-0.1,2.5)
fullFileName= "/Users/Scott/Desktop/PHYS_313/assgt6_THOMAS_NICASTRO-Fig01.png"
pl.savefig(fullFileName)
#pl.show()
pl.clf()
# we chose that intial range so we can find only one root

# we will compare the times with x_o = 2.5

time1 =[]

for i in range(0,10000):
	t0 = t.clock()
	a,b,c,d = newtonmethod(0.01,0.0001)
	# time returns seconds
	t1 = t.clock()
	dt = (t1-t0)*10**(6) # convert seconds to micro seconds
	time1.append(dt)

#pl.hist(time1,bins=70)
#pl.xlabel("Run Time [Micro Seconds]")
#pl.ylabel("Counts")
#pl.title("Run Time for Home Brew Newtons Method")
#pl.xlim(30,50)
#pl.show()

time2 = []
def func(x):
	return np.log(x**2)

def func2(x):
	return 2/x


for i in range(0,10000):
	t0 = t.clock()
	scip.newton(func,0.01,fprime = func2,tol = 0.0001)
	# time returns seconds
	t1 = t.clock()
	dt = (t1-t0)*10**(6) # convert seconds to micro seconds
	time2.append(dt)

pl.hist(time2,bins=50,label='Run Time for Scipy',histtype= "step")
pl.hist(time1,bins=50,label = 'Run Time for Home Brew Newtons Method',histtype= "step")
pl.xlabel("Run Time [Micro Seconds]")
pl.ylabel("Counts")
pl.title("Run Time comparing Scipy and Home Brew")
#pl.legend()
pl.xlim(30,80)
fullFileName= "/Users/Scott/Desktop/PHYS_313/assgt6_THOMAS_NICASTRO-Fig02.png"
pl.savefig(fullFileName)
pl.show()

# scipy runs faster becasue it's code is written in C
