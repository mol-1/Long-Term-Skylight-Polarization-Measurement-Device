# -*- coding: utf-8 -*-

#code adapted from an example from astropy python package to get sun ephemerids and plot a nice figure

import time
import sys
import numpy as np
import matplotlib.pyplot as plt
from astropy.visualization import astropy_mpl_style, quantity_support
plt.style.use(astropy_mpl_style)
quantity_support()

# Import the packages necessary for finding coordinates and making
# coordinate transformations

import astropy.units as u
from astropy.time import Time
from astropy.coordinates import SkyCoord, EarthLocation, AltAz, HADec

# Use `astropy.coordinates.EarthLocation` to provide the location of La Timone (Marseille, France)
#Luminy : 43.233856735452754, 5.443703565986805
luminy = EarthLocation(lat=43.233856735452754*u.deg, lon=5.443703565986805*u.deg, height=390*u.m)
timone = EarthLocation(lat=43.286990365824785*u.deg, lon=5.403361407820939*u.deg, height=390*u.m)


######################################################################
# Use  `~astropy.coordinates.get_sun` to find the location of the Sun 

from astropy.coordinates import get_sun

#from astropy.utils.iers import IERS_B_FILE
from astropy.utils.iers import IERS_A_URL_MIRROR

class ephemerides:
    '''
    self.timone stores location on earth of La Timone observation site
    '''
    def __init__(self):
        self.luminy = EarthLocation(lat=43.233856735452754*u.deg, lon=5.443703565986805*u.deg, height=390*u.m)
        self.timone = EarthLocation(lat=43.286990365824785*u.deg, lon=5.403361407820939*u.deg, height=390*u.m)
        self.utcoffset = 2*u.hour  # Difference between local and UTC hour - 2h on summer like when this database was released, and 1h on winter
        
        self.aujourdhui=str(Time.now().datetime.date())
        self.midday = Time(self.aujourdhui+' 12:00:00') - self.utcoffset
        
    def getHADecSoleil(self,chainetps=None):
        '''
        Return Hour Angle and Declinaison at a specified French local summer time (UTC+2)
        '''
        if chainetps is None:
            Times_now=Time.now()
        else:
            chaineheure=chainetps.split("T")[1][0:-1].split("-")
            heure_image=Time(chainetps.split("T")[0]+'T'+chaineheure[0]+":"+chaineheure[1]+":"+chaineheure[2])
            Times_now=Time(heure_image,format='isot')
        self.times_now=Times_now-self.utcoffset# Add an UTC offset to go from french local to UTC time
        self.frame_now = HADec(obstime=self.times_now, location=self.timone)
        self.sunaltazs_now = get_sun(self.times_now).transform_to(self.frame_now)
        return (self.sunaltazs_now.ha.degree,90-self.sunaltazs_now.dec.degree)
        
    def getAltAzSoleil(self,chainetps=None):
        '''
        Return Sun Zenith Angle and Azimut at a specified French local summer time (UTC+2)
        '''
        if chainetps is None:
            Times_now=Time.now()
        else:
            chaineheure=chainetps.split("T")[1][0:-1].split("-")
            heure_image=Time(chainetps.split("T")[0]+'T'+chaineheure[0]+":"+chaineheure[1]+":"+chaineheure[2])
            Times_now=Time(heure_image,format='isot')
        self.times_now=Times_now-self.utcoffset#Time.now()#-utcoffset#-8*u.hour

        self.frame_now = AltAz(obstime=self.times_now, location=self.timone)
        self.sunaltazs_now = get_sun(self.times_now).transform_to(self.frame_now)
        return (self.sunaltazs_now.az.degree,90-self.sunaltazs_now.alt.degree)

    

    
    def traceAzELSoleil(self,chainetps=None,Ax=None):
        '''
        Plot Sun Zenith Angle and Azimut at a specified French local summer time (UTC+2) on a plot with whole day trajectory.
        '''
        if Ax is None:
            Ax=plt.subplot(221) #plt.gca()
        if chainetps is None:
            Times_now=Time.now()
        else:
            chaineheure=chainetps.split("T")[1][0:-1].split("-")
            heure_image=Time(chainetps.split("T")[0]+'T'+chaineheure[0]+":"+chaineheure[1]+":"+chaineheure[2])
            Times_now=Time(heure_image,format='isot')

        Times_now.format='isot'
        self.times_now=Times_now-self.utcoffset#Time.now()#-utcoffset#-8*u.hour

        
        self.ax=Ax


        self.frame_now = AltAz(obstime=self.times_now, location=self.timone)
        self.sunaltazs_now = get_sun(self.times_now).transform_to(self.frame_now)
       
        self.aujourdhui=str(self.times_now.datetime.date())


        self.midday = Time(self.aujourdhui+' 12:00:00') - self.utcoffset

        
        self.delta_midday = np.linspace(-2, 10, 100)*u.hour
        
        self.diff=(self.times_now-self.midday).value*24
        self.delta_midday = np.linspace(-12, 12, 1000)*u.hour
        self.times_JourJ = self.midday+ self.delta_midday #- self.utcoffset
        self.frame_JourJ = AltAz(obstime=self.times_JourJ, location=self.timone)
        self.sunaltazs_JourJ = get_sun(self.times_JourJ).transform_to(self.frame_JourJ)
        
        
        
        
        ##############################################################################
        # Make a beautiful figure illustrating nighttime and the altitudes of the Sun over that time:
               
        self.ax.plot(self.delta_midday, self.sunaltazs_JourJ.alt, color='r', label='Elevation',zorder=2)
        self.ax2=self.ax.twinx()
        self.ax2.plot(self.delta_midday, self.sunaltazs_JourJ.az, color='g', label='Azimut',zorder=1)

        self.ax.fill_between(self.delta_midday, 0*u.deg, 90*u.deg,
                         self.sunaltazs_JourJ.alt < -0*u.deg, color='0.5', zorder=0)
        self.ax.fill_between(self.delta_midday, 0*u.deg, 90*u.deg,
                         self.sunaltazs_JourJ.alt < -18*u.deg, color='k', zorder=0)

        
        self.ax.set(title="Sun Position - "+str(self.midday).split()[0])
        self.ax.set_xlim(-12*u.hour, 12*u.hour)
        self.ax.set_xticks((np.arange(13)*2-12)*u.hour)#,np.arange(13)*2%12)
        self.ax.set_xticklabels(np.arange(13)*2)
        self.ax.set_yticks((np.arange(0,80,10))*u.deg)
        self.ax2.set_yticks((np.arange(0,360,45))*u.deg)
        #plt.xtickslabels()
        self.ax.set_ylim(0*u.deg, 80*u.deg)
        self.ax2.set_ylim(0*u.deg, 360*u.deg)
        self.ax.set_xlabel('Local Hour')
        self.ax.set_ylabel('')
        self.ax2.set_ylabel('')
        
        self.legende1=self.ax.legend(loc="upper left")
        self.legende2=self.ax2.legend(loc="upper right").set_zorder(13)
        self.legende1.remove()
        self.ax2.add_artist(self.legende1)

        
        self.props = dict(boxstyle='round', facecolor='wheat', alpha=0.9)
        self.texte1=self.ax.text(0.05,0.85, str(round(self.sunaltazs_now.alt.degree,2))+" °" , transform=self.ax.transAxes, fontsize=14,
                horizontalalignment='left',
                verticalalignment='top', bbox=self.props,zorder=11)
        self.texte2=self.ax2.text(0.95,0.85, str(round(self.sunaltazs_now.az.degree,2))+" °" , transform=self.ax.transAxes, fontsize=14,
                horizontalalignment='right',
                verticalalignment='top', bbox=self.props,zorder=10)
        self.texte1.remove()
        self.ax2.add_artist(self.texte1)
        self.texte_heure="UTC : "+str(self.times_now.value)#.time())
        self.texteh=self.ax2.text(0.5,0.9, self.texte_heure , transform=self.ax.transAxes, fontsize=14,
                horizontalalignment='center',
                verticalalignment='top', bbox=self.props,zorder=10)
        self.pltSoleilAz=self.ax2.scatter(self.diff,self.sunaltazs_now.az.degree,c = 'tab:orange',marker = 'o',alpha = 0.8,s=200)
        self.ptSoleilAlt=self.ax.scatter(self.diff,self.sunaltazs_now.alt.degree,c = 'tab:orange',marker = 'o',alpha = 0.8,s=200)
        #return (ax,ax2,midday,texte1,texte2,texteh,ptSoleilAlt,pltSoleilAz)
