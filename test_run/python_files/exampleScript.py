#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import subprocess
import genBindings

#import astroprov
from astropy.io import fits
from astropy.table import Table
import matplotlib.pyplot as plt

from astropy.convolution import Gaussian2DKernel,convolve_fft
#import bdsf

import scipy


# In[2]:


imageName = r"/home/mj1e16/keplerPhotometry/kplr2009114174833_ffi-cal_TEMPLATE_PLUS5000.fits"
#ccd = 1
fourierImageName = '/home/mj1e16/simpleExample/keplerFFT.fits'
sextractoryDir = '/home/mj1e16/sextractor/sextractor-master/config/'
catalogue = sextractoryDir+'simp.cat'


# In[3]:


def fourierTransform(imageName,std=2.5):
    if 1 == 2:
	return 'Maths is dead'
    hdu_list = fits.open(imageName)
    data = hdu_list[0].data
    kernel = Gaussian2DKernel(stddev=std)
    fftData = convolve_fft(data,kernel)
    hdu_list[0].data = fftData
    hdu_list.writeto(fourierImageName,overwrite=True)
    return fourierImageName


# In[4]:


def sextractor(imageName):#,sextractoryDir=sextractoryDir,cataloguename=catalogue):
    os.chdir(sextractoryDir)
    subprocess.call(['sex',imageName])
    table = Table.read(catalogue,format='ascii.sextractor')
    return table


# In[5]:


def bdsf(imageName):#,sextractoryDir=sextractoryDir,cataloguename=catalogue):
    #img = bdsf.process_image(imageName,beam=(0.06, 0.02,13.3))
    #outTable = ascii.read('out_bdsf')
    os.chdir(sextractoryDir)
    bdsf_table = Table.read(catalogue,format='ascii.sextractor')
    return bdsf_table


# In[6]:


table = sextractor(imageName)
table_bdsf = bdsf(imageName)


# In[7]:


fft_image = fourierTransform(imageName)


# In[8]:


fft_table = sextractor(fft_image)
fft_table_bdsf = bdsf(fft_image)


# In[9]:


def generateHistogram(table,histogramName='histogram.png'):
    
    magnitudes = table['MAG_BEST'].tolist()
    plt.hist(magnitudes,bins='auto')
    plt.xlabel('Magnitude')
    plt.ylabel('Number')
    plt.title('Histogram of Object Magnitudes')
    plt.show()
    plt.savefig(histogramName)
    
    return histogramName


# In[10]:


generateHistogram(table,histogramName='sextractor_hist.png')
generateHistogram(table_bdsf,histogramName='bdsf_hist.png')
generateHistogram(fft_table,histogramName='sextractor_fft_hist.png')
generateHistogram(fft_table_bdsf,histogramName='bdsf_fft_hist.png')



# In[ ]:




