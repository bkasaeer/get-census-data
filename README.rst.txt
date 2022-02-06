# About this Project

This package provide a high-level API to obtain a series of key socioeconomic and 
internet connectivity parameters from 5-year estimates of American Community Survey 
(ACS-5) for the two most recent years: 2018 or 2019. The package is using 
the censusdata package and enables the user to simply obtain data in a pandas dataframe
and a local CSV file stored in the data folder for all future usages. The retrieved data is 
processed to have a GEOID for each geographic unit or each row of the dataset! In addition, 
a series of calculated fields are added to the final output which are found to be key for many 
data science projects. See the example Jupyter Notebook for more details about capabilities of 
this package. 

# Prerequisites
* You need to obtain an API key from US Census website: [CENSUS_KEY](https://api.census.gov/data/key_signup.html) 
* `[censusdata](https://github.com/jtleider/censusdata)`
* `numpy`
* `pandas`

# Run
## Run Using the Windows Command Line
use this method it you would like to get the data in your local drive in a CSV format.
* `git clone https://github.com/bkasaeer/get_us_census_data`
* `set CENSUS_KEY ENTER_YOUR_KEY_HERE`
* Example 1 (use default values, i.e. 2019 data for all US counties): `python get_census_data.py $CENSUS_KEY$`
* Example 2: `python get_census_data.py %CENSUS_KEY% --state_name "Rhode Island" --geo_level "block group --year 2018"` 
## Run From a Development Environment
see the example [Jupyter Notebook] (https://github.com/bkasaeer/get_us_census_data/blob/master/get_data_example.ipynb).

# References: 
* https://github.com/jtleider/censusdata
* https://www.census.gov/data/developers.html
* https://www.census.gov/programs-surveys/acs/
* https://www.census.gov/programs-surveys/geography/guidance/geo-identifiers.html
* https://api.census.gov/data/2019/acs/acs5/variables.html
* https://www.nrcs.usda.gov/wps/portal/nrcs/detail/?cid=nrcs143_013696
* https://en.wikipedia.org/wiki/Federal_Information_Processing_Standard_state_code