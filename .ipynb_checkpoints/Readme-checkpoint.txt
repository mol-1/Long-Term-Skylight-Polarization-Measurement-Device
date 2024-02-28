This is the Readme file to explain processing code associated with our database of skylight polarization images taken at La Timone, Marseille, France. Processing codes are here to calibrate it, reduce image size, and process data to get Angle and Degree of Polarization. It can also help to explain data structure provided.



Database download : 

POUGHON, Leo, 2024, "1 Month-long skylight polarization images dataset", Recherche Data Gouv, 
https://doi.org/10.57745/610QTS

Associated publications, please cite them when using our code and database  :

https://ieeexplore.ieee.org/document/10325176
https://hal.science/hal-04267766

Associated Github : 

https://github.com/mol-1/Long-Term-Skylight-Polarization-Measurement-Device



Léo Poughon et al. 2021-2024
Licence : CC-BY-SA




For code execution, please update the paths in the beginning of each jupyter notebook to match with your own system and install libs specified in requirements.txt. 
You can download all timestamped ".npy"  (like 2022-08-02_raw.npy) in a local "PolarizedDatabase" folder, others numpy files in a calib folder in "PolarizedDatabase/calib" folder,  and eventually the "ManipeResultatsRed.tar.gz" archive in a "ManipeResultats" folder. All codes (jupyter notebooks and python files) should be located in a PolarizedDatabaseCode folder.

This code was executed with python 3.9.6. For parts where processing is parallelized, please ajust the "num_processes" variable to the amount of cores available to your system (in linux you can use "nproc" command in terminal)




Workflow :

ManipeResultats folder -> 1-calibration_orientation_fisheye_with_sun_redac.ipynb -> PolarizedDatabase/calib folder 
                       -> 2_reduction_to_PolarizedDatabase.ipynb -> PolarizedDatabase folder
                       
PolarizedDatabase folder -> 2_b_PolarizedDatabase_Manual_Annotation.ipynb -> PolarizedDatabase folder
                       
PolarizedDatabase folder -> 3_calculation_PolarizedDatabaseProcessed.ipynb -> PolarizedDatabaseProcessed folder

PolarizedDatabaseProcessed folder -> 4_Database_Use_example.ipynb 





    First a "ManipeResultats" folder was obtained from the system described in the paper. It contain several "acquisitions" and each acquisition is composed of several images taken with auto and fixed exposure time, named after as "image_type" ranging from 0 to 10, with images less than 5 are auto exposure one and 5 and above fixed exposures of growing values with number. As these data are heavy, only three days days are provided on the public in an archive, named "ManipeResultatsRed" 

    The notebook "1-calibration_orientation_fisheye_with_sun_redac.ipynb" explains how the calibration is done and generate files in specified "calib" path in another folder "PolarizedDatabase/calib". It compares sun position detected on sensor on clear day with ephemerids and keeps best calibration. It creates following files in calib folder :

 
dist_center.npy  -> distorsion center of optic, obtained with Scaramuzza's Matlab camera calibration toolbox
lat_lon.npy  -> local position of camera, hard coded in code


f.npy  -> estimated focal lenght of optic, in pixels (~520 pixels * 3.45 um -> ~1.8mm)
orientation_pixels_ENU.npy  -> each pixels rays incidence angles in East-North-Up frame
rotation.npy  -> rotation value between camera and ENU frames, ZXY euler angles
rot_mat.npy -> rotation matrix








    The notebook 2-reduction_to_PolarizedDatabase.ipynb takes data from "ManipeResultats" folder, crop images and reduce their size to 16 bits (in reality, 12 bits range from IMX250MYR sensor on PHX050S-QC camera, bitshifted to 4 bytes). It creates following files in calib folder :

params_crop.npy
alpha_crop.npy
theta_crop.npy


It also creates files with images grouped for each day on numpy files like "2022-07-29_raw.npy" in PolarizedDatabase folder. These images are associated with exposure time (in µs), timestamp, and image_type (numbers corresponding to fixed or auto exposure values) variables.




    The notebook 2_b_PolarizedDatabase_Manual_Annotation.ipynb can help user to define custom annotations for a choosen day, annotation associated to each image "group" (grouped by "acquisition" : 1 acquisition each 10 minutes in our case) and to create corresponding lists containing timestamps and corresponding annotation.

For example, one can choose "c" for highly cloudy sky, "h" for hazy sky, "n" for normal (clear) sky etc.


    Finally, code from 3_calculation_PolarizedDatabaseProcessed.ipynb is the only one really usefull to execute for final database user, the two previous ones are useful to understand how the PolarizedDatabase database was made and this third one allows to create locally a PolarizedDatabaseProcessed.
    
    It take each image, and generate AOP and DOP images from it for each color, and a simulation of equivalent rayleigh image. Eaach one are registered in folders, and a .csv file is created for each day to give Image_folder_path, Timestamp, Hour_Local, Minute_Local, Second_Local, Date, Sun_azimuth, Sun_zenith_angle, Sun_hour_angle, Sun_declination, Camera_exposure_time, and Image_type.
    
    In each Image_folder_path, one can find (and use) :
    
    AOP_B.npy  AOP_Gb.npy  AOP_Gr.npy  AOP_R.npy  AOP_s.npy, AOP values for R, Gb, Gr, B, and rayleigh simulation values,
    DOP_B.npy  DOP_Gb.npy  DOP_Gr.npy  DOP_R.npy  DOP_s.npy  DOP values for R, Gb, Gr, B, and rayleigh simulation values,
    (where 'B', 'Gb', 'Gr', and 'R' correspond to color bayer filters on sensors : 'B' is blue, 'Gb' and 'Gr' are green filters next to blue and red ones, and 'R' red one. 's' correspond to rayleigh simuation.)
    
    expo.npy  for exposure
    fig.png  for processed figure
    image.npy  for raw image
    time.npy for timestamp
    
    
    

Once the processed database is done, one can use it, like in the example provided on 4_Database_Use_example.ipynb to train a simple neural network able to estimate sun's elevation in an image (courtesy of Thomas Kronland-Martinet for this last code)




centroide_images.py, ephemeride.py and rayleigh.py are additionnal functions used by our notebook.
For rayleigh sky simulation, it is recommended to use 'OpenSky" simulator that is more rigorous. Future versions of the present work may use it instead of rayleigh.py file.

https://github.com/MoutenetA/OpenSky


