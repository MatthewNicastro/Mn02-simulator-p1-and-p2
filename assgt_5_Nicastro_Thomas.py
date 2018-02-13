from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plot
import matplotlib.lines as mlines
import random as rn
import math as m
import numpy as np

#Attinuation length of Mn54 is 27*10**(-6)m
#All lengths and position in meters
#All velocities in meters per seconds
#Time is seconds 
class source(object):
    #Initializes variables for the class
    def __init__(self, length, height, atten_len, n):
        self.side_m = length/2 
        self.height_m = height/2
        self.n = n
        self.atten_len_m = atten_len
        self.test = "Working"

        #Randomly generates x, y, z uniformly
        self.x_m = [rn.uniform(-self.side_m, self.side_m) for i in range(0, self.n)]
        self.y_m = [rn.uniform(-self.side_m, self.side_m) for i in range(0, self.n)]
        self.z_m = [rn.uniform(-self.height_m, self.height_m) for i in range(0, self.n)]

        #Randomly generates phi and theta uniformly foor velocity
        theta = [rn.uniform(0.0,2*np.pi) for i in range(0, self.n)]
        phi = [np.arccos(rn.uniform(-1,1)) for i in range(0, self.n)]

        #Converts phi and theta to x, y, z velocity
        self.vecx_m_s = np.sin(phi)*np.cos(theta)
        self.vecy_m_s = np.sin(phi)*np.sin(theta)
        self.vecz_m_s = np.cos(phi)

        self.lens_m = []

        self.topA_m = []
        self.sideA_m = []
        self.topA_m_s = []
        self.sideA_m_s = []

        self.name = "/Users/zbit12/Desktop/School/Phys_313/Assignement_5/"

    #Creates a 2D histogram with parameters
    def hist2D(self, first, second, bins, frsN, lsN, obj, name):
        plot.clf()
        plot.hist2d(first, second, bins = bins, cmap = "Blues")
        plot.xlabel(frsN)
        plot.ylabel(lsN)
        plot.title("%s Vs %s 2D histogram of %s" %(frsN, lsN, obj))
        cbar = plot.colorbar()
        cbar.ax.set_ylabel("Counts")
        plot.savefig(self.name+name)
        plot.show()
        

    #Calculates the time it takes for a line to intersect a plane
    def time(self, v_m_s, pos_m, plpos_m):
        return (plpos_m - pos_m)/v_m_s

    #Calculates the magnitude of the distance using velocity and time
    def magn(self, vecx_m_s, vecy_m_s, vecz_m_s, t_s):
        return np.sqrt((vecx_m_s*t_s)**2 + (vecy_m_s*t_s)**2 + (vecz_m_s*t_s)**2)
    
    def newPos(self, x_m, y_m, z_m, v_x_m_s, v_y_m_s, v_z_m_s, t_s):
        nx_m = v_x_m_s * t_s + x_m
        ny_m = v_y_m_s * t_s + y_m
        nz_m = v_z_m_s * t_s + z_m
        return [nx_m, ny_m, nz_m]

    #Finds direction of the component of the vector
    def posneg(self, v_m_s):
        if v_m_s >= 0:
            return True
        else:
            return False
        
    #Checks the direction of the component
    #Calculates the time it would take to intersect the plane
    #Chooses the min time the appends the magnitude to the lens list
    #Appends the xrays going towards the detector into 4 lists 2 for the xrays position out of the sides and the top
    #and two for the velocity again for the sides and the top
    def sideInt(self):
        for i in range(0, self.n):
            if self.posneg(self.vecx_m_s[i]):
                t_x_s = self.time(self.vecx_m_s[i], self.x_m[i], self.side_m)
            else:
                t_x_s = self.time(self.vecx_m_s[i], self.x_m[i], -self.side_m)
                
            if self.posneg(self.vecy_m_s[i]):
                t_y_s = self.time(self.vecy_m_s[i], self.y_m[i], self.side_m)
            else:
                t_y_s = self.time(self.vecy_m_s[i], self.y_m[i], -self.side_m)
                
            if self.posneg(self.vecz_m_s[i]):
                t_z_s = self.time(self.vecz_m_s[i], self.z_m[i], self.height_m)                
            else:
                t_z_s = self.time(self.vecz_m_s[i], self.z_m[i], -self.height_m)
                
            t_s = min(t_x_s, t_y_s, t_z_s)
            self.lens_m.append(self.magn(self.vecx_m_s[i], self.vecy_m_s[i], self.vecz_m_s[i], t_s))

            if(self.vecz_m_s[i] > 0 and t_s == t_x_s):
                self.sideA_m.append(self.newPos(self.x_m[i], self.y_m[i], self.z_m[i], self.vecx_m_s[i], self.vecy_m_s[i], self.vecz_m_s[i], t_s))
                self.sideA_m_s.append([self.vecx_m_s[i], self.vecy_m_s[i], self.vecz_m_s[i]])

            elif(self.vecz_m_s[i] > 0 and t_s == t_y_s):
                self.sideA_m.append(self.newPos(self.x_m[i], self.y_m[i], self.z_m[i], self.vecx_m_s[i], self.vecy_m_s[i], self.vecz_m_s[i], t_s))
                self.sideA_m_s.append([self.vecx_m_s[i], self.vecy_m_s[i], self.vecz_m_s[i]])

            elif(self.vecz_m_s[i] > 0 and t_s == t_z_s):
                self.topA_m.append(self.newPos(self.x_m[i], self.y_m[i], self.z_m[i], self.vecx_m_s[i], self.vecy_m_s[i], self.vecz_m_s[i], t_s))
                self.topA_m_s.append([self.vecx_m_s[i], self.vecy_m_s[i], self.vecz_m_s[i]])

    #Generates a histogram for the distribution of lengths
    def hist1D(self, name, lens):
        bins = np.linspace(0, 0.03, 50)
        plot.hist(lens, bins = bins, facecolor = 'green')
        plot.xlabel("Lengths [m]")
        plot.ylabel("Count")
        plot.title("Dist. of lengths [m]")
        plot.savefig(self.name+name)
        plot.show()

#New class that extends the source class
class detector(source):
    #Class constructor initializes variables
    def __init__(self, side, height, distance, source_side, source_height, xraypos, xrayv, sxraypos, sxrayv, n, atten_len):
        self.side_m = side/2
        self.height_m = height
        self.side_source_m = source_side
        self.height_source_m = source_height
        self.dist_m = distance
        self.distOfD_l_m = self.dist_m+self.height_source_m
        self.distOfD_t_m = self.dist_m+self.height_source_m + (self.height_m*2)

        self.xraypos_m = xraypos
        self.xrayv_m_s = xrayv
        self.sxraypos_m = sxraypos
        self.sxrayv_m_s = sxrayv
        
        self.n = n
        self.atten_len_m = atten_len

        #Generates the x, y, z for the detector
        self.x_m = [rn.uniform(-self.side_m, self.side_m) for i in range(0, self.n)]
        self.y_m = [rn.uniform(-self.side_m, self.side_m) for i in range(0, self.n)]
        self.z_m = [rn.uniform(-self.height_m, self.height_m) for i in range(0, self.n)]

        self.name = "/Users/zbit12/Desktop/School/Phys_313/Assignement_5/"
    
    #Calculates the positio of the xray
    def position(self, pos_m, t_s, v_m_s):
        return v_m_s * t_s + pos_m

    #Checks if the xray has been detected 
    def Detect(self, side_m, xpos_m, ypos_m):
        if(-side_m <= xpos_m and xpos_m <= side_m):
            if(-side_m <= ypos_m and ypos_m <= side_m):
                return True
        return False

    #Checks if the xray 
    def Detectv2(self, side_m, pos_m, zpos_m):
        if(-side_m <= pos_m and pos_m <= side_m):
            if( self.distOfD_l_m <= zpos_m and zpos_m <= self.distOfD_t_m):
                return True
        return False
    
    #Returns the difference of the plane and the new point
    def difference(self, nz, height):
        return height - nz

    #checks if the particle gets detected
    def hitdetect(self, dist = None, side = None):
        if side == None:
            side = self.side_m
        
        if dist == None:
            dist = self.dist_m
            
        self.hit_m_m_s = []

        #Case 1 where detector is larger the the source
        #Calculates the time z then sees if the xray will hit the detector for both the source's top and the source's sides 
        if ((side*2)*(side*2) > (self.dist_m*2)*(self.dist_m*2)):
            for i in range(0, len(self.xrayv_m_s)):
                t_s = self.time(self.xrayv_m_s[i][2], self.xraypos_m[i][2], dist)
                xpos_m = self.position(self.xraypos_m[i][0], t_s, self.xrayv_m_s[i][0])
                ypos_m = self.position(self.xraypos_m[i][1], t_s, self.xrayv_m_s[i][1])
                if self.Detect(side, xpos_m, ypos_m):
                    self.hit_m_m_s.append([self.xrayv_m_s[i][0], self.xrayv_m_s[i][1], self.xrayv_m_s[i][2], xpos_m, ypos_m, self.distOfD_l_m])

            for i in range(0, len(self.sxraypos_m)):
                t_s = self.time(self.sxrayv_m_s[i][2], self.sxraypos_m[i][2], dist + self.difference(sxraypos_m[i][2]), sourceSide)
                xpos_m = self.position(self.sxraypos_m[i][0], t_s, self.sxrayv_m_s[i][0])
                ypos_m = self.position(self.sxraypos_m[i][1], t_s, self.sxrayv_m_s[i][1])
                if self.Detect(side, xpos_m, ypos_m):
                    self.hit_m_m_s.append([self.sxrayv_m_s[i][0], self.sxrayv_m_s[i][1], self.sxrayv_m_s[i][2], sxpos_m, sypos_m, self.distOfD_l_m])

        #Case 2 where detector is the same size as the source
        #Calculates the time z then sees if the xray will hit the detector for both the source's top 
        elif ((side*2)*(side*2) == (self.dist_m*2)*(self.dist_m*2)):
            for i in range(0, len(self.xrayv_m_s)):
                t_s = self.time(self.xrayv_m_s[i][2], self.xraypos_m[i][2], dist)
                xpos_m = self.position(self.xraypos_m[i][0], t_s, self.xrayv_m_s[i][0])
                ypos_m = self.position(self.xraypos_m[i][1], t_s, self.xrayv_m_s[i][1])
                if self.Detect(side, xpos_m, ypos_m):
                    self.hit_m_m_s.append([self.xrayv_m_s[i][0], self.xrayv_m_s[i][1], self.xrayv_m_s[i][2], xpos_m, ypos_m, self.distOfD_l_m])

        #Case 3 where detector is smaller then the source
        #Calculates the time z then sees if the xray will hit the detector's sides and the base of the detector for the source's top
        else:
            for i in range(0, len(self.xrayv_m_s)):
                t_s = self.time(self.xrayv_m_s[i][2], self.xraypos_m[i][2], dist)
                xpos_m = self.position(self.xraypos_m[i][0], t_s, self.xrayv_m_s[i][0])
                ypos_m = self.position(self.xraypos_m[i][1], t_s, self.xrayv_m_s[i][1])

                #Checks if the particle will hit the base of the detector
                if self.Detect(side, xpos_m, ypos_m):
                    self.hit_m_m_s.append([self.xrayv_m_s[i][0], self.xrayv_m_s[i][1], self.xrayv_m_s[i][2], xpos_m, ypos_m, self.distOfD_l_m])

                #Checks if the particle will hit the sides of the detector for this case
                else:
                    if xpos_m < -side and self.xrayv_m_s[i][0] > 0:
                        t_s = self.time(self.xrayv_m_s[i][0], xpos_m, -side)
                        ypos_m = self.position(self.xraypos_m[i][1], t_s, self.xrayv_m_s[i][1])
                        zpos_m = self.position(dist, t_s, self.xrayv_m_s[i][2])
                        if(self.Detectv2(side, ypos_m, zpos_m)):
                            self.hit_m_m_s.append([self.xrayv_m_s[i][0], self.xrayv_m_s[i][1], self.xrayv_m_s[i][2], -side, ypos_m, ypos_m])
                            
                    elif xpos_m > side and self.xrayv_m_s[i][0] < 0:
                        t_s = self.time(self.xrayv_m_s[i][0], xpos_m, side)
                        ypos_m = self.position(self.xraypos_m[i][1], t_s, self.xrayv_m_s[i][1])
                        zpos_m = self.position(dist, t_s, self.xrayv_m_s[i][2])
                        if(self.Detectv2(side, ypos_m, zpos_m)):
                            self.hit_m_m_s.append([self.xrayv_m_s[i][0], self.xrayv_m_s[i][1], self.xrayv_m_s[i][2], side, ypos_m, zpos_m])

                    elif ypos_m < -side and self.xrayv_m_s[i][1] > 0:
                        t_s = self.time(self.xrayv_m_s[i][1], ypos_m, -side)
                        xpos_m = self.position(self.xraypos_m[i][0], t_s, self.xrayv_m_s[i][0])
                        zpos_m = self.position(dist, t_s, self.xrayv_m_s[i][2])
                        if(self.Detectv2(side, xpos_m, zpos_m)):
                            self.hit_m_m_s.append([self.xrayv_m_s[i][0], self.xrayv_m_s[i][1], self.xrayv_m_s[i][2], xpos_m, -side ,zpos_m])

                    elif ypos_m > side and self.xrayv_m_s[i][1] < 0:
                        t_s = self.time(self.xrayv_m_s[i][1], xpos_m, -side)
                        xpos_m = self.position(self.xraypos_m[i][0], t_s, self.xrayv_m_s[i][0])
                        zpos_m = self.position(dist, t_s, self.xrayv_m_s[i][2])
                        if(self.Detectv2(side, xpos_m, zpos_m)):
                            self.hit_m_m_s.append([self.xrayv_m_s[i][0], self.xrayv_m_s[i][1], self.xrayv_m_s[i][2], xpos_m, side, zpos_m])

    #Finds out where the xray will leave the detector                       
    def sideInt(self):
        self.lens_m = []
        for i in range(0, len(self.hit_m_m_s)):
            if self.hit_m_m_s[i][0] > 0:
                t_x_s = self.time(self.hit_m_m_s[i][0], self.hit_m_m_s[i][3], self.side_m)
            else:
                t_x_s = self.time(self.hit_m_m_s[i][0], self.hit_m_m_s[i][3], -self.side_m)
            if self.hit_m_m_s[i][1] > 0:
                t_y_s = self.time(self.hit_m_m_s[i][1], self.hit_m_m_s[i][4], self.side_m)
            else:
                t_y_s = self.time(self.hit_m_m_s[i][1], self.hit_m_m_s[i][4], -self.side_m)
            t_z_s = self.time(self.hit_m_m_s[i][2], self.distOfD_l_m, self.height_m+self.distOfD_l_m)
            t_s = min(t_x_s, t_y_s, t_z_s)
            self.lens_m.append(self.magn(self.hit_m_m_s[i][0], self.hit_m_m_s[i][1], self.hit_m_m_s[i][2], t_s))

    #Calculates if the xray will be detected by the detector
    def absorbingphoton(self, atten_len):
        prob = [rn.uniform(0,1) for j in range(0,len(self.lens_m))]
        escapeornot = []
        for i in range(len(self.lens_m)):
            prob_unscathed = np.e**(-self.lens_m[i]/atten_len)
            # if prob is higher then prob_unscathed, the x-ray escapes
                    
            if prob_unscathed > prob[i]:
                escapeornot.append(True) #the particle doesn't get absorbed
            else:
                escapeornot.append(False)     #the particle gets absorbed 
                        
        return escapeornot

    #Finds ratio of escaped photons 
    def fractionofabsorbingphotons(self, escapingphoton):
        absorbed = []
        for x in escapingphoton:
            if not x:
                absorbed.append(x)
        # number photons that get absorbed is our photons_absorbed 
        photons_absorbed = len(absorbed)
        Ratio = float(photons_absorbed)/float(self.n)
        return Ratio

    #calculates the dependance of lamba over the length
    def dependance(self, name):
        # Since dependancy of lambda/h is just a number, we will just vary lambda
        # since attenuation length of Mn source is just 27*10**(-6), choose a range below for atten_len
        x = np.linspace(0.00000000001,1,1500)
        atten_len = np.linspace(0.00000000001,1,1500)
        y=[]  #empty array to populate with escape ratios
        # iterate through every possible lambda by calling our fractionofescapingphotons function
        for i in range(1500):
            y.append(self.fractionofabsorbingphotons(self.absorbingphoton(atten_len[i]))) 

        # plotting the dependance of lambda/h 
        plot.clf()
        plot.plot(x,y)
        plot.title("Dependance of absorbed Photons with lambda/h")
        plot.xlabel("Lambda/H [Unitless]")
        plot.ylabel("Ratio of absorbed photons [Unitless]")
        plot.savefig(self.name+name)
        plot.show()

    # loops through the whole code varying d and graphing the dependance on it
    def dependance_on_d(self, name):
        d_m = np.linspace(self.height_source_m, 0.1, 1000)
        y = []
        for i in range(len(d_m)):
            self.hitdetect(d_m[i])
            self.sideInt()
            y.append(self.fractionofabsorbingphotons(self.absorbingphoton(self.atten_len_m)))

        # plotting the dependance of d 
        plot.clf()
        plot.plot(d_m,y)
        plot.title("Dependance of absorbed Photons with d [m]")
        plot.xlabel("d [m]")
        plot.ylabel("Ratio of absorbed photons [Unitless]")
        plot.savefig(self.name+name)
        plot.show()

    # loops through the whole code varying a and graphing the dependance on it
    # gives divides by zero error warning for the start of the division on ln 331 so just skips the zero
    def dependance_on_a(self, name):
        a_m = np.linspace(0, 0.1, 200)
        x = (self.side_source_m*2)/a_m
        y = []
        for i in range(len(a_m)):
            self.hitdetect(None, a_m[i])
            self.sideInt()
            y.append(self.fractionofabsorbingphotons(self.absorbingphoton(self.atten_len_m)))

        # plotting the dependance of a
        plot.clf()
        plot.plot(x,y)
        plot.title("Dependance of absorbed Photons with side[m]")
        plot.xlabel("a/A [Unitless]")
        plot.ylabel("Ratio of absorbed photon [Unitless]")
        plot.savefig(self.name+name)
        plot.show()

def main():
    n = 10000
    side = 0.01
    side2 = 0.01
    atten_len = 27*10**(-6)
    thickeness = 0.000000001
    thickness2 = 0.002
    distance = 0.002
    detectAtten = 22*10**(-5)
    bins = 30
    
    src = source(side, thickeness, atten_len, n)
    src.sideInt()
    detect = detector(side2, thickness2, distance, src.side_m, src.height_m, src.topA_m, src.topA_m_s, src.sideA_m, src.sideA_m_s, n, detectAtten)
##    detect.hist2D(detect.x_m, detect.y_m, bins, "X [m]", "Y [m]", "detector", "assgt05_Nicastro_Thomas_fig01")
##    detect.hist2D(detect.x_m, detect.z_m, bins, "X [m]", "Z [m]", "detector", "assgt05_Nicastro_Thomas_fig02")
##    detect.hist2D(detect.y_m, detect.z_m, bins, "Y [m]", "Z [m]", "detector", "assgt05_Nicastro_Thomas_fig03")
    detect.hitdetect()
    detect.sideInt()
    detect.hist1D("assgt05_Nicastro_Thomas_fig04", detect.lens_m)
    print("fraction of absorbed xrays for base case: "+str(detect.fractionofabsorbingphotons(detect.absorbingphoton(detect.atten_len_m))))
    detect.dependance("assgt05_Nicastro_Thomas_fig05")
    detect.dependance_on_d("assgt05_Nicastro_Thomas_fig06")
    detect.dependance_on_a("assgt05_Nicastro_Thomas_fig07")

main()

##How to plot log scale plot.yscale('log', nonposy='clip') for histogram
