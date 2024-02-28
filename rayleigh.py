#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  1 22:02:26 2022

@author: leo
"""

# -- coding: utf-8 --
"""
Created on Wed Sep 29 10:33:08 2021

@author: U607402
"""
import numpy as np
from numpy import arctan2, sqrt
#import numexpr as ne
from scipy.spatial.transform import Rotation as R

import matplotlib.pyplot as plt
def average_angle(angle1,angle2):
    x=np.cos(angle1)+np.cos(angle2)
    y=np.sin(angle1)+np.sin(angle2)
    return np.arctan2(y,x)
def myprint(**kwargs):#namestr #https://stackoverflow.com/questions/592746/how-can-you-print-a-variable-name-in-python
    #print(kwargs.items())
    for k,v in kwargs.items():
        print("%s = %s" % (k, repr(v)))


#7312 IEEE SENSORS JOURNAL, VOL. 15, NO. 12, DECEMBER 2015



def cart2sph(x,y,z):
    azimuth = np.arctan2(y,x)
    elevation = np.arctan2(z,np.sqrt(x**2 + y**2))
    r = np.sqrt(x**2 + y**2 + z**2)
    return azimuth, elevation, r

def sph2cart(azimuth,elevation,r):
    x = r * np.cos(elevation) * np.cos(azimuth)
    y = r * np.cos(elevation) * np.sin(azimuth)
    z = r * np.sin(elevation)
    return x, y, z

def cart2sph2(x,y,z):
    """
    Entree : trois tableaux numpy avec les n coordonnées selon l'axe x, y et z de n vecteurs
    Sortie : deux tableaux numpy avec les n coordonnées en azimut et elevation, en radians, avec la convention elevation  à pi/2 si vecteur selon le plan x-y, et nulle selon z.
    """
    azimuth = np.arctan2(y,x)
    elevation = np.pi/2-np.arctan2(z,np.sqrt(x**2 + y**2))
    return azimuth, elevation


def sph2cart2(azimuth,elevation):
    """
    Entree : deux tableaux numpy avec les n coordonnées en azimut et elevation, en radians, avec la convention elevation  à pi/2 si vecteur selon le plan x-y, et nulle selon z.
    Sortie : trois tableaux numpy avec les n coordonnées selon l'axe x, y et z de n vecteurs
    """
    x = np.cos(np.pi/2-elevation) * np.cos(azimuth)
    y = np.cos(np.pi/2-elevation) * np.sin(azimuth)
    z = np.sin(np.pi/2-elevation)
    return x, y, z

def rebin(arr, new_shape): #https://scipython.com/blog/binning-a-2d-array-in-numpy/
        shape = (new_shape[0], arr.shape[0] // new_shape[0],
                 new_shape[1], arr.shape[1] // new_shape[1])
        return arr.reshape(shape).mean(-1).mean(1)
def simul_rayleigh_subplot(Psi_sun = -85,Theta_sun = 80,ax_aop=None,ax_dop=None,fig=None,Theta=None,Psi=None,rot_mat=None,limit_Zenith_Angle=np.pi*0.45,out_zone=0):#orientation_pixels_ENU=None):

    r=R.from_matrix(rot_mat) #get rotation function

    #Sun azimut (rad)
    Psi_sun = Psi_sun*np.pi/180;
    #Sun zenith angle
    Theta_sun = Theta_sun*np.pi/180;    
    
    xsi=np.arctan2(np.cos(Theta_sun)*np.sin(Theta)-np.sin(Theta_sun)*np.cos(Theta)*np.cos(Psi-Psi_sun),-np.sin(Psi-Psi_sun)*np.sin(Theta_sun))
    #Formulas from "model_pixel_sensors-14-14916" article
    Xsi=((xsi+Psi)%np.pi-np.pi/2)#*180/np.pi
    
    #Xsi[Theta>limit_Zenith_Angle]=out_zone #remove what is outside of field of view
    

    Xsi_0=np.cos(Xsi)**2
    Xsi_45=np.cos(Xsi-np.pi/4)**2
    Xsi_90=np.cos(Xsi-np.pi/2)**2
    Xsi_135=np.cos(Xsi-3*np.pi/4)**2
    
    Q=Xsi_0-Xsi_90 # I0-I90
    U=Xsi_45-Xsi_135 # I45-I135

    
    d=np.pi/180
    couleur=0
    Q_dofp=Xsi_0[((couleur//2)*2+0//2)::4,((couleur%2)*2+0%2)::4]-Xsi_90[((couleur//2)*2+3//2)::4,((couleur%2)*2+3%2)::4] # I0-I90
    U_dofp=Xsi_45[((couleur//2)*2+1//2)::4,((couleur%2)*2+1%2)::4]-Xsi_135[((couleur//2)*2+2//2)::4,((couleur%2)*2+2%2)::4] # I45-I135
    #AOP calculation with correction to get in right angle quadrant and use orientation. Supposes X and Y second and third rotations are null for simplification.
    ksi_dofp=(-(0.5*np.arctan2(U_dofp,Q_dofp))*180/np.pi-r.as_euler('ZXY')[0]/d+90)%180-90 
    
    
    
    # Here we want to calculate the "average angle" seen at the center of a macropixel. 
    # We know the orientations of each sub-pixel (theta, alpha). However, a simple average 
    # does not work for finding the "central" orientation. For instance, the "average" between 
    # two 2D vectors with angles 45° and 315° would "actually" be 0°, but the arithmetic mean of
    # the two angles is 180°. Here, we encounter the same problem when transitioning from -π to π 
    # with numerical artifacts. To avoid this, we convert back to Cartesian coordinates and use atan2.            
            
    
    alpha_0=Psi[((couleur//2)*2+0//2)::4,((couleur%2)*2+0%2)::4]
    alpha_90=Psi[((couleur//2)*2+3//2)::4,((couleur%2)*2+3%2)::4]
    alpha_45=Psi[((couleur//2)*2+1//2)::4,((couleur%2)*2+1%2)::4]
    alpha_135=Psi[((couleur//2)*2+2//2)::4,((couleur%2)*2+2%2)::4]
    alpha_mini=average_angle(average_angle(alpha_0,alpha_90),average_angle(alpha_45,alpha_135))    
    theta_0=Theta[((couleur//2)*2+0//2)::4,((couleur%2)*2+0%2)::4]
    theta_90=Theta[((couleur//2)*2+3//2)::4,((couleur%2)*2+3%2)::4]
    theta_45=Theta[((couleur//2)*2+1//2)::4,((couleur%2)*2+1%2)::4]
    theta_135=Theta[((couleur//2)*2+2//2)::4,((couleur%2)*2+2%2)::4]
    theta_mini=average_angle(average_angle(theta_0,theta_90),average_angle(theta_45,theta_135))
    
    Psi=alpha_mini#rebin(alpha,(alpha.shape[0]//4,alpha.shape[1]//4))
    Theta=theta_mini#rebin(theta,(theta.shape[0]//4,theta.shape[1]//4))    
    ksi_dofp[theta_mini>limit_Zenith_Angle]=out_zone

    [OMx,OMy,OMz]=sph2cart(Psi,np.pi/2-Theta,1);
    [m,n]=np.shape(OMx);

    #Zenith and azimut angle of the measurement vector OM

    OS= (sph2cart((Psi_sun),(np.pi/2-Theta_sun),1))

    
    OM=np.rollaxis(np.array([OMx,OMy,OMz]).transpose(),1)
    gammab=np.arccos(np.dot(OM,OS))
    DOP=np.square(np.sin(gammab)) / (1+np.square(np.cos(gammab)));
    DOP[Theta>limit_Zenith_Angle]=out_zone

    if ax_aop is not None:
        cmap_jet = plt.cm.jet  # You can use any colormap you prefer
        cmap_jet.set_bad('black', alpha=1.0)
        cmap_hsv = plt.cm.hsv  # You can use any colormap you prefer
        cmap_hsv.set_bad('black', alpha=1.0)
        pcm2=ax_aop.pcolormesh(ksi_dofp,cmap=cmap_hsv,vmin=-90.0, vmax=90.0)
        cbar=fig.colorbar(pcm2,ax=ax_aop)
        cbar.set_ticks([-90,-67.5,-45,-22.5,0,22.5,45,67.5,90])
        cbar.set_label("Angle of Polarization")
        ax_aop.set_title("Rayleigh Model AOP")#- Az : "+"%0.2f" % Psi_sun+" El : "+"%0.2f" % Theta_sun)
        
        pcm2d=ax_dop.pcolormesh(DOP,cmap=cmap_jet,vmin=0.0, vmax=1.0)
        cbard=fig.colorbar(pcm2d,ax=ax_dop)
        #cbard.set_ticks([-90,-67.5,-45,-22.5,0,22.5,45,67.5,90])
        cbard.set_label("Degree of Polarization")
        ax_dop.set_title("Rayleigh Model DOP ")#- Az : "+"%0.2f" % Psi_sun+" El : "+"%0.2f" % Theta_sun)
    
    return ksi_dofp,DOP #return simulated AOP and DOP
