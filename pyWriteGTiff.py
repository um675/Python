def pyWriteGTiff(rasterfile,out_name):
    import numpy as np
    import gdal
    gdal.AllRegister()
    # Prendo i driver del GeoTiff
    driver = gdal.GetDriverByName("GTiff")
    driver.Register()

        # la apro in GDAL
    #rasterfile = gdal.Open(rasterfile_nome)
    # conto le bande
    rasterfile_nbands = rasterfile.RasterCount
    # creo un array vuoto con le dimensioni del raster che ho importato
    rasterfile_3Darray = np.empty((rasterfile.RasterYSize, rasterfile.RasterXSize, rasterfile.RasterCount))

    # riempio l'array con i valori delle bande del raster
    # NOTA BENE range(1:8) crea un vettore di 7 elementi da 1 a 7

    for i in range(1, (rasterfile_nbands + 1)):
        rasterfile_band = rasterfile.GetRasterBand(i)
        rasterfile_array = rasterfile_band.ReadAsArray(0, 0, rasterfile.RasterXSize, rasterfile.RasterYSize)
        rasterfile_array[rasterfile_array == -1.6999999999999999e+308] = np.nan
        rasterfile_3Darray[:, :, (i - 1)] = rasterfile_array
    print "ciclo NaN_natore finito"

    driver.Register()  # l'ho ripetuto ma non dovrebbe servire
    cols = rasterfile.RasterXSize  # numero colonne
    rows = rasterfile.RasterYSize  # numero righe
    bands = rasterfile.RasterCount  # numero bande
    # estraggo il datatype dal file originale
    banda1 = rasterfile.GetRasterBand(1)
    datatype = banda1.DataType

    # creo un file GeoTiff vuoto (NB mentre l'array ragiona in Righe e Colonne GDAL ragiona in colonne e righe)
    out_rasterfile = driver.Create(out_name, cols, rows, bands, datatype)
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
    return "file pronto"

