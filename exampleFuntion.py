def fourierTransform(imageName,std=2.5):
    hdu_list = fits.open(imageName)
    data = hdu_list[0].data
    kernel = Gaussian2DKernel(stddev=std)
    fftData = convolve_fft(data,kernel)
    hdu_list[0].data = fftData
    hdu_list.writeto(fourierImageName,overwrite=True)
    return fourierImageName

def sextractor(imageName): #,sextractoryDir=sextractoryDir,cataloguename=catalogue):
    os.chdir(sextractoryDir)
    subprocess.call(['sex',imageName])
    table = Table.read(catalogue,format='ascii.sextractor')
    return table
