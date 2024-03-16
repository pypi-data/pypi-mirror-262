# DataPipelinePackage

## To Install the Package
    From the internet for use elsewhere:
    $ pip install ecopipeline
    Install locally in an editable mode:
    Navigate to DataPipelinePackage directory and run the following command
    $ pip install -e .

## File Structure
    .
    ├── src
    ├   ├── docs 
    ├   ├   ├── 
    ├   └── ecopipeline
    ├       ├── extract.py               # functionality for extracting data from a file system
    ├       ├── transform.py             # functionality for cleaning data and calcualting derived values
    ├       ├── load.py                  # functionality for loading pandas dataframe into a mySQL database table
    ├       ├── unit_convert.py   
    ├       ├── config.py                # file containing all file paths 
    ├       ├── bayview.py               # Bayview site-specific functionality
    ├       └── lbnl.py                  # LBNL site-specific functionality
    ├── testing
    ├   ├── Bayview
    ├   ├    ├── Bayview_input
    ├   ├    ├── extract.py              
    ├   ├    ├   └── extract_test.py     # testing for extract functionality
    ├   ├    ├── transform.py
    ├   ├    ├   ├── pickles             # pickles used for bayview unit testing
    ├   ├    ├   └── transform_test.py   # testing for transform functionality
    ├   ├    └── load.py                 
    ├   ├        └── load_test.py        # testing for load functionality
    ├   └── LBNL
    ├       ├── extract.py
    ├       ├   └── extract_test.py
    ├       ├── transform.py 
    ├       ├   ├── LBNL-input           # LBNL input dataframes used as testing input
    ├       ├   ├── LBNL-output          # LBNL output dataframes used for crossreferencing our output to expected output
    ├       ├   ├── pickles              # pickles used for bayview unit testing
    ├       ├   └── transform_test.py
    ├       └── load.py
    ├           └── load_test.py
    ├── config.ini                       # file containing all configuration parameters
    └── README.md
 
## Purpose
This project was developed with the help of Ecotope, Inc. It containes seperate modular functionalities that, when combined, can extract, transfrom, and load data from incoming sensors. The main goal was to rewrite the existing R pipeline code with Python making the codebase more readable. In addition to that, scalability was taken into account during this project since this codebase will be used to create pipelines for different sites in the future. 

## Architecture
![Screenshot](ArchitectureDiagram.png)

### extract.py 
- loading data from a local file system
- extracting NOAA weather data from a FTP server

### transform.py 
- cleaning the data
    - rounding
    - removing outliers
    - renaming columns
    - filling missing values
- calculating dervived COP (coefficient of performance) values
- agreggating the data

### load.py
- establishing a connection to the database
- loading pandas dataframe into a table in the database

### config.ini
- database
    - user: username for host database connection 
    - password: password for host database connection
    - host: name of host 
    - database: name of database
- minute
    - table_name: name of table to be created in the mySQL database containing minute-by-minute data
- hour
    - table_name: name of table to be created in the mySQL database containing hour-by-hour data
- day
    - table_name: name of table to be created in the mySQL database containing day-by-day data
- input
    - directory: diretory of the folder containing the input files listed below
    - site_info: name of the site information csv
    - 410a_info: name of the 410a information csv
    - superheat_info: name of the superheat infomation csv
- output 
    - directory: diretory of the folder where any pipeline output should be written to
- data
    - directory: diretory of the folder from which extract loads the raw sensor data
## Unit Testing
To run Unit tests, run the following command in the terminal in the corresponding directory:
```bash
python -m pytest
```















