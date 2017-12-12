#rasterfile -> The raster image that has to be simulated
#classificata -> A classification map of rasterfile in 10 classes
#num -> number of simulated maps you want to have
#pos_out -> output filder
#out_name -> output filename
def image_creator(rasterfile,classificata,num,pos_out,out_name):
    import numpy as np
    import gdal
    import os
    import math
    for iii in range(0,num):

        print "Generazione immagine ", iii+1 , " in corso"
        gdal.AllRegister()
        # Prendo i driver del GeoTiff
        driver = gdal.GetDriverByName("GTiff")
        driver.Register()

        rasterfile_nbands = rasterfile.RasterCount
        rasterfile_3Darray = np.empty((rasterfile.RasterYSize, rasterfile.RasterXSize, rasterfile.RasterCount))

        # RasterYsize righe
        # RasterXsize colonne
        #gdal.AllRegister()
        # Prendo i driver di ENVI
        #driver = gdal.GetDriverByName("ENVI")
        #driver.Register()


        classificata_array = classificata.ReadAsArray(0, 0, classificata.RasterXSize, classificata.RasterYSize)
        # ReadAsArray vuole prima le colonne e poi le righe
        indclass1 = np.nonzero(classificata_array == 1)
        indclass2 = np.nonzero(classificata_array == 2)
        indclass3 = np.nonzero(classificata_array == 3)
        indclass4 = np.nonzero(classificata_array == 4)
        indclass5 = np.nonzero(classificata_array == 5)
        indclass6 = np.nonzero(classificata_array == 6)
        indclass7 = np.nonzero(classificata_array == 7)
        indclass8 = np.nonzero(classificata_array == 8)
        indclass9 = np.nonzero(classificata_array == 9)
        indclass10 = np.nonzero(classificata_array == 10)

        indlist = [indclass1, indclass2, indclass3, indclass4, indclass5, indclass6, indclass7, indclass8, indclass9,
                   indclass10]

        matsd = np.empty((10, rasterfile_nbands))

        for i in range(0, 10):
            for jj in range(0, (rasterfile_nbands)):
                # print i,jj
                rasterfile_band = rasterfile.GetRasterBand(jj + 1)
                rasterfile_array = rasterfile_band.ReadAsArray(0, 0, rasterfile.RasterXSize, rasterfile.RasterYSize)
                matsd[i, jj] = np.std(rasterfile_array[indlist[i]])
                if math.isnan(matsd[i, jj]):
                    matsd[i, jj] = 999

        # np.asscalar(np.random.normal(mean, std, 1))
        nnn = 0
        for k in range(0, (rasterfile_nbands)):
            rasterfile_band = rasterfile.GetRasterBand(k + 1)
            rasterfile_array = rasterfile_band.ReadAsArray(0, 0, rasterfile.RasterXSize, rasterfile.RasterYSize)
            for i in range(0, rasterfile.RasterYSize):
                for j in range(0, rasterfile.RasterXSize):
                    nnn = nnn + 1
                    # print rasterfile_array[i,j], "valore iniziale"
                    classe = classificata_array[i, j]
                    # print classe , "classe"
                    sd = matsd[classe - 1, k]
                    # print sd, "std della classe"
                    rasterfile_array[i, j] = np.asscalar(np.random.normal(rasterfile_array[i, j], sd, 1))
                    # print rasterfile_array[i, j], "valore finale"
                    rasterfile_3Darray[i, j, k] = rasterfile_array[i, j]
                    percentuale = (float(nnn) / float(rasterfile_3Darray.size)) * 100
            print "percentuale", int(percentuale)

        pos02 = pos_out
        os.chdir(pos02)
        driver.Register()  # l'ho ripetuto ma non dovrebbe servire
        cols = rasterfile.RasterXSize  # numero colonne
        rows = rasterfile.RasterYSize  # numero righe
        bands = rasterfile.RasterCount  # numero bande
        # estraggo il datatype dal file originale
        banda1 = rasterfile.GetRasterBand(1)
        datatype = banda1.DataType

        out_name2 = out_name + "_"
        iiis = str(iii)
        num_len = len(iiis)

        for ii in range(0, 4 - num_len):
            iiis = str(0) + iiis

        out_name2 = out_name2 + iiis
        iiis=None
        # creo un file GeoTiff vuoto (NB mentre l'array ragiona in Righe e Colonne GDAL ragiona in colonne e righe)
        out_rasterfile = driver.Create(out_name2, cols, rows, bands, datatype)
        out_name2=None
        # estraggo il sistema di riferimento dal file originale e lo inserisco in quello nuovo
        geoTransform = rasterfile.GetGeoTransform()
        out_rasterfile.SetGeoTransform(geoTransform)
        proj = rasterfile.GetProjection()
        out_rasterfile.SetProjection(proj)

        # riempio le bande del nuovo file con le bande dell'array 3D che avevo creato
        for i in range(1, (rasterfile_nbands + 1)):
            out_rasterfile.GetRasterBand(i).WriteArray(rasterfile_3Darray[:, :, (i - 1)], 0, 0)
        print "ciclo scrivi file finito"
        # il comando FlushCache scrive effettivamente tutto quello che ho richiesto sul file richiesto
        out_rasterfile.FlushCache()

    rasterfile_array=None
    rasterfile_nbands=None
    rasterfile_3Darray=None
    rasterfile_band=None
    out_rasterfile=None
    print "Immagine ", iii+1, " generata"
    return

