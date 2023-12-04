# BorderRegion_KDE
This program imports, handles, organizes, and visualizes data about mobility patterns over European national borders.
The primary analysis is a Kernel Density Estimation (KDE) of mobility across country borders. Several variations and calculations to the program are further discussed in the *Usage* part. This program can be helpful in understanding transnational locations as well as provide insight into movement trends.

## Installation
**This program has dummy data which you can try if it works as it should on your computer. For that, I have added a *.env* file and *OutputFolder* so that everything is set up for you to test the program with the dummy data. The dummy data works only currently for the KDE plot and not for the H3 to geo conversion. To test the program with the dummy data, follow the installation steps below, everything else should have been already taken care of.**

To install this program you need to 

**1. Navigate to a proper directory in your command line.**

**2. Clone the GitHub repository with the command below:**
```
git clone https://github.com/DigitalGeographyLab/BorderRegion_KDE.git
```
**3. Install Poetry if you don't have it installed already. More about installing Poetry [here](https://python-poetry.org/docs/)**

**4. Navigate into the BorderRegion_KDE folder.**

**5. Use Poetry to install all project dependencies with the command below, make sure you're inside the git repository in your command line:**
```
poetry install
```
**6. Use Poetry to active the virtual environment with this command:**
```
poetry shell
```
**7. After everything is installed and set upped, navigate to the *src* file and execute the program with one of the following commands:**
```
python index.py 
```
```
python3 index.py
```
   

## Usage

This section will give a brief explanation of what files the program consists of and what they do as well as guidance of how the program can be used. 
 
### The options and order of things

##### TO BE UPDATED SOON!

### How and where to start
 
##### TO BE UPDATED SOON!

#### N.B. *There might be some minor changes that the user has to do in the code in case the user has input data with different column names or filenames. In case the user already has a dataset with geographical coordinates, it can jump straight to the distance calculation and onward* 

### Referencing
If you use this script in your research or project, or develop it further, please refer back to us using this:

Söderholm, M., Aagesen, H., Väisänen, T., & Järv, O (2023) BoderRegion_KDE

