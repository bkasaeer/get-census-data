# get-census-data
## About this Project

This code provides a high-level API to obtain a series of key socioeconomic and 
internet connectivity parameters from 5-year estimates of American Community Survey 
(ACS-5) for the two most recent years: 2018 or 2019. The censusdata package is used 
to pull data from the Census database. This work enables the user to obtain data in a pandas dataframe
and a local CSV file stored in the data folder for all future usages. The retrieved data is 
processed to have a GEOID for each geographic unit or each row of the dataset! In addition, 
a series of calculated fields are added to the final output which are found to be key for many 
data science projects. See the example Jupyter Notebook for more details about capabilities of 
this code. A summary of these fields include: 

* **pct_work_remote**: percent population that work from home (%)
* **pct_use_pub_trans**: percent population that use public transportation (%)
* **income_per_capita**: income per capita (USD)
* **pct_work_remote**: percent population that work from home (%)
* **pct_labor_force**: percent population in labor force (%)
* **pct_unemployed**: percent population in labor force that are unemployed (%)
* **pct_income_below_poverty**: percent population with income below US national poverty (%)
* **pct_below_bsc**: percent population with education below bachelors (%)
* **pct_no_insurance**: percent population with no insurance (%)
* **pct_internet_no_subscr**: percent population with internet but no internet subscription (%)
* **pct_no_internet**: percent population with no internet access (%)
* **pct_has_a_computer**: percent population with computer (%)
* **pct_has_computer_w_diapup_subscr**: percent population with computer and dialup internet subscription (%)
* **pct_computer_no_internet_subscr**: percent population with computer and no internet subscription (%)

## Prerequisites
* You need to obtain an API key from [US Census website](https://api.census.gov/data/key_signup.html) 
* `censusdata`
* `numpy`
* `pandas`

## Run
### Run Using the Windows Command Line
use this method it you would like to get the data in your local drive in a CSV format.
* `git clone https://github.com/bkasaeer/get-census-data`
* `set CENSUS_KEY=ENTER_YOUR_KEY_HERE`
* Example 1 (use default values, i.e. 2019 data for all US counties): `python get_census_data.py $CENSUS_KEY$`
* Example 2: `python get_census_data.py %CENSUS_KEY% --state_name "Rhode Island" --geo_level "block group" --year 2018` 
### Run From a Development Environment
see the example Jupyter Notebook (https://github.com/bkasaeer/get-census-data/blob/main/get_data_example.ipynb).

## References: 
* https://github.com/jtleider/censusdata
* https://www.census.gov/data/developers.html
* https://www.census.gov/programs-surveys/acs/
* https://www.census.gov/programs-surveys/geography/guidance/geo-identifiers.html
* https://api.census.gov/data/2019/acs/acs5/variables.html
* https://www.nrcs.usda.gov/wps/portal/nrcs/detail/?cid=nrcs143_013696
* https://en.wikipedia.org/wiki/Federal_Information_Processing_Standard_state_code
