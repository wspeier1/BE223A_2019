# BE 224B Final Project - 19 Spring

Localization of cortical electrodes from intraoperative fluoroscopy

Student name: Yannan Lin

## Getting Started

### Prerequisites

- Python 3.6
    - Download Python from their website: https://www.python.org/downloads/
    - Dependencies
        - mayavi, opencv, math, numpy, nibabel, PIL, matplotlib
        
#### Mayavi installation 

##### 1. Install Anaconda
- Download and install [Anaconda](https://www.anaconda.com/download/). 
- Enter Anaconda Navigator and initialize a new virtual environment with specification on Python 3.6
##### 2. Install mayavi
- Add conda to environment path 
- run "conda install mayavi" to install the package

### Running the program
- Step 1
Run the imports and functions section in the script
    - Line 7 to line 176

- Step 2
Run the block of code related to reading in images and volume data and removing NAN
    - Line 179 to line 236

- Step 3 
Run each block of code for each subject.
    - Example: Subject 1
    - 1. Run ### step 1 ### to read in the coordinates of the landmarks 
        - Line 343 to line 251
    - 2. Run ### step 2 ### to preprocess the fluoroscopic image
        - Line 255
    - 3. Run ### step 3 ### to align the fluoroscopy with the CT using landmarks 
        - Line 259 to line 291
    - 4. Run ### step 4 ### to plot the electrodes on the fluoroscopic image 
        - Line 297 to line 331
    - 5. Run ### step 5 ### to get the electrode coordinates in the 3D space 
        - Line 336 to line 347
    - 6. Run ### step 6 ### to visualize the electrodes on the cortical surface using the 1st projection algorithm 
        - Line 353 to line 377
    - 7. Run ### step 6 ### to visualize the electrodes on the cortical surface using the 2nd projection algorithm 
        - Line 380 to line 404
         
- Step 4 
 Run the rest of the code for each subject according to the steps specified in Step 3.
 Line 413 to line 975
  
- Note:
1. To avoid overlaying of mayavi scenes, please only run one block of code each time as instructed.

### Author:
Yannan Lin (allyn1982@ucla.edu)

