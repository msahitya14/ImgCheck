# ImgCheck
This is a app written in python with PyQT5 GUI. It can be used to open images by placing the folder in the same directory as the images, create a excel sheet easily and saving it to maintain data about the image.

Use pip install -r requirements.txt to install the required libraries - PyQT5 and pandas.

If you can successfully install PyQT5 using pip, use the following:
  For debian/linux:
    sudo apt-get install python3-pyqt5
  Using anaconda:
    conda install -c anaconda pyqt

Download this repository, and place it in the same directory containing your images.
Run the python file imagecheck.py.

On Linux : python3 imagecheck.py



*Instructions*:

Button -- 'A'  ===== Used to navigate to the the previous image


Button -- 'D'  ===== Used to navigate to the next image


Button -- 'S'  ===== Used to Zoom Out the image


Button -- 'W'  ===== Used to Zoom Into the image


You can Pan using your mouse to left right buttons when the scroll bar appears.


Saving:

The sheet gets automatically created in the same directory as the script with the date in its name. It updates after every image if the approve or deny button is pressed. It resets every session, so make sure you make a copy.

Alternatively, you can fill in a filename in the app and press save to save your progress - Example in the field - "Newimages" : It will be saved as "Newimage_image_approval.xlsx" in the same folder as the script.
