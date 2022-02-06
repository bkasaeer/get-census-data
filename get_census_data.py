import pandas as pd
import censusdata
import os
import pandas as pd
import itertools
import argparse
import numpy as np 

def create_state_fips_dict():
    """this function creates the US state FIPS code dictionary! It stores the data as a CSV file within 
    the data folder upon the first call of the function. For every future run, it first attempts to 
     retrieve data from the local drive if it is not deleted! """
    file = os.path.join(os.getcwd(), 'data/state_fips.csv')
    if not os.path.isfile(file):
        fips_df = pd.read_html('https://www.nrcs.usda.gov/wps/portal/nrcs/detail/?cid=nrcs143_013696')[0]
        fips_df = fips_df.dropna()[['Name','FIPS']]
        fips_df['FIPS'] = fips_df.FIPS.astype(int).astype(str).str.zfill(2)
        fips_df.to_csv(file, index = False)
    else:
        fips_df = pd.read_csv(file, dtype = str)
    return dict(zip(fips_df.Name,fips_df.FIPS)) 

def create_data_api_table():
    """this function creates the ACS-5 2019 API data table! It stores the data as a CSV file within 
    the data folder upon the first call of the function. For every future run, it first attempts to 
     retrieve data from the local drive if it is not deleted!"""
    file = os.path.join(os.getcwd(), 'data/data_api_table.csv')
    if not os.path.isfile(file):
        api_df = pd.read_html('https://api.census.gov/data/2019/acs/acs5/variables.html')[0]
        api_df.to_csv(file, index = False)
    else:
        api_df = pd.read_csv(file)
    return api_df

def postprocess_df(df):
    """this function will post process the census raw data and add some new fields!"""
    #Create age groups with corresponding census APIs! This value is not gender specific and 
    #calculate as % of the total population within the geography (e.g., tract)
    age_grps = ["pct_age_under_5",'pct_age_5to9','pct_age_10to14','pct_age_15to17',
            'pct_age_18to21','pct_age_22to64','pct_age_65&over']
    grp_apis = [[3,27], [4,28], [5,29],[6,30], [7,8,9,31,32,33], list(range(
        10,20)) + list(range(34,44)), list(range(20,26)) + list(range(44,50))]
    for i,age_grps in enumerate(age_grps):
        df[age_grps] = 100*df[['B01001_%sE'%str(x).zfill(3) for x in grp_apis[i]]].sum(
            axis = 1)/df["B01001_001E"].replace(0,np.nan)
    #the following fields are calculated from existing census APIs! 
    df["pct_work_remote"] = 100*df['B08301_021E']/df['B08301_001E'].replace(0,np.nan)            # work remotely (%)
    df["pct_use_pub_trans"] = 100*df['B08301_010E']/df['B08301_001E'].replace(0,np.nan)          # using public transportation (%)
    df["income_per_capta"] = df['B19301_001E'].replace(0,np.nan)                                 # income per capita (USD)
    df["pct_labor_force"] = 100*df['B23025_002E']/df['B23025_001E'].replace(0,np.nan)            # labor force (%)
    #df["pct_unemployed"] = 100*df['B27011_008E']/df['B27011_001E'].replace(0,np.nan)            # unemployed (%) -- gives blank records!
    df["pct_unemployed"] = 100*df['B23025_005E']/df['B23025_002E'].replace(0,np.nan)             # unemployed (%)
    #df["pct_income_below_poverty"] = 100*df['B17020_002E']/df['B17020_001E'].replace(0,np.nan)  # below poverty (%)-- gives blank records!
    df["pct_income_below_poverty"] = 100*df['B29003_002E']/df['B29003_001E'].replace(0,np.nan)   # below poverty (%)
 

    df["pct_below_bsc"] = 100-(100*df[[x for x in ['B15002_%sE'%str(x).zfill(3) for x in [
    2,15,16,17,18,19,32,33,34,35]] if all(x!=n for n in ['B15002_002E','B15002_019E'])]].sum(
        axis = 1))/(df[['B15002_002E','B15002_019E']]).sum(axis = 1).replace(0, np.nan)             # below bachelors degree (%)
    df["pct_no_insurance"]=(100*df[['B27010_017E','B27010_033E','B27010_050E','B27010_066E']].sum(
        axis = 1))/df['B27010_001E'].replace(0,np.nan)                                           # has no insurance (%)
    df["pct_internet_no_subscr"] = 100*df['B28002_012E']/df['B28002_001E'].replace(
        0, np.nan)                                                                        # has internet without subscription (%)
    df["pct_no_internet"] = 100*df['B28002_013E']/df['B28002_001E'].replace(0, np.nan)      # no internet access (%)
    df["pct_has_a_computer"] = 100*df['B28003_002E']/df['B28003_001E'].replace(0, np.nan)       # has a computer (%)
    df["pct_has_computer_w_diapup_subscr"] = 100*df['B28003_003E']/df['B28003_001E'].replace(
        0, np.nan)                                                              # has computer and dialup subscription (%)
    df["pct_computer_no_internet_subscr"] = 100*df['B28003_005E']/df['B28003_001E'].replace(
        0, np.nan)                                                              # has computer but no internet subscription (%)
    #Commute data appears as None in some states! Needs to be fixed later!
    #df["pct_above3_yrs_enrolled_school"] = 100*(df['B14002_003E']+df['B14002_027E'])/df[
    #    'B14002_001E'].replace(0,np.nan)                                       # above three years old enrolled in school (%)
    #df['pct_commute_over_45mins'] = 100*(df['B08012_011E']+df['B08012_012E']+df[
    #    'B08012_013E'])/df['B08012_001E'].replace(0,np.nan)                    # commute to work above 45 minutes (%)
    #df['pct_commute_over_60mins'] = 100*(df['B08012_012E']+df['B08012_013E'])/df[
    #    'B08012_001E'].replace(0,np.nan)                                       # commute to work above 45 minutes (%)
    #df['pct_commute_over_90mins'] = 100*df['B08012_013E']/df['B08012_001E'].replace(
    #    0,np.nan) 
    #make sure income per capita is always positive! 
    df.loc[df.income_per_capta < 0,'income_per_capta'] = np.nan
    return df

def get_census_data(key, state_name = 'All', year = 2019, geo_level = 'county'):
    """Downloads American Community Survery (ACS) 5-year socioeconomic data for a specified geographic level
        Args:
            state_name (str): US state name, e.g. Rhode Island. The defauilf is All meaning all US states! 
            year (int): The year of ACS data. This fuction supports both 2018 & 2019 (default)
            geo_level (str): The desired geographic level for the data. It can be county, tract, or block group   

        Returns:
            pandas dataframe: US nationwide dataset for the specified time and geographic level. Also, returns 
            a backup CSV file from the data for all future runs of the function. 
        Examples:: 
            # Pull data on Rhode Island block groups from the 2018 ACS-5 estimates.
            python get_census_data.py %CENSUS_KEY% --state_name "Rhode Island" --geo_level "block group --year 2018
            See the get_data_example.ipynb for data retrieval in the development environment.
        """
    #create a list of APIs and add some important parameters to it!
    names = []
    names.append(['B01001_%sE'%str(x).zfill(3) for x in range(1, 50)])    # population per age group
    names.append(['B08301_021E','B08301_001E'])                          # work from home
    names.append(['B08301_010E'])                                        # public transporation use
    names.append(['B19301_001E'])                                        # per capita income (USD)
    names.append(['B23025_001E','B23025_002E'])                          # labor force
    #names.append(['B27011_008E','B27011_001E'])                         # unemployment --gives blank records 
    names.append(['B23025_005E'])                                        # unemployment
    #names.append(['B17020_001E','B17020_002E'])                         # below poverty --gives blank records 
    names.append(['B29003_001E','B29003_002E'])                          # below poverty

    
    names.append(['B15002_%sE'%str(x).zfill(3) for x in [
        2, 15, 16, 17, 18, 19, 32, 33, 34, 35]])                                  # education
    names.append(['B27010_%sE'%str(x).zfill(3) for x in [
        1, 17, 33, 50, 66]])                                                 # insurance coverage
    names.append(['B14002_001E','B14002_003E','B14002_027E'])            # school enrolement
    #names.append(['B08012_001E','B08012_011E','B08012_012E',
    #              'B08012_013E'])                                        # travel time to work --gives blank records 
    names.append(['B28002_001E','B28002_012E','B28002_013E',
            'B28003_001E','B28003_002E','B28003_003E',
            'B28003_005E','B28001_003E','B28001_004E',
            'B28001_006E','B28001_008E','B28001_011E',
            'B28002_003E','B28002_006E','B28002_007E',
            'B28002_010E','B19049_001E','B25010_001E',
            'B01001_001E'])                                              # internet access 
    #flatten the list of lists
    names = list(itertools.chain(*names))
    #create a fips state table 
    fips_dict = create_state_fips_dict()
    #define a file name and location for the final product
    final_file = 'data/%s_%s_%s.csv'%(state_name,'_'.join(geo_level.split()), year)
    #if geo_level is county, use below to download data:
    if geo_level == 'county':
        #first try to read from local file before jumping into Census API!
        try:
            df = pd.read_csv(final_file, dtype = {'GEOID' : str})
        except:
            df = censusdata.download('acs5', year, censusdata.censusgeo([('county', '*')]),
                                        names, key = key)
            df['GEOID'] = [''.join([g[1] for g in x.geo]) for x in df.index]
            postprocess_df(df).to_csv(final_file,index = False)
        if state_name != 'All':
            df = df[df.GEOID.str[:2] == fips_dict[state_name]]
                
    #if geo_level is tract or block group use below route:
    else:
        try:
            #first try to see if the full dataset is locally available!
            df = pd.read_csv(final_file, dtype = {'GEOID' : str})
        except:      
            if state_name != 'All':
                state_fips = fips_dict[state_name]
                #create a dictionary of counties within the specifies parameters!
                counties = censusdata.geographies(censusdata.censusgeo([(
                    'state', state_fips), ('county', '*')]), 'acs5', year, key = key)
                #download all the required data for counties from census using above APIs
                dfs = [censusdata.download('acs5', year, censusdata.censusgeo(
                    [('state', state_fips), ('county', v.geo[1][1]), (
                        geo_level, '*')]), names, key = key) for k,v in counties.items()]
                #merge counties together in one dataframe
                df = pd.concat(dfs)
                df['GEOID'] = [''.join([g[1] for g in x.geo]) for x in df.index]
                postprocess_df(df).to_csv(final_file, index = False) 
            
            else:
                #first try to see if the full dataset is locally available!
                try:
                    df = pd.read_csv(final_file, dtype = {'GEOID' : str})
                except:
                    print('start retreiving data for all US states!')
                    states_df = []
                    #censusdata won't appear to give data for four below territories!
                    fips_dict = {k:v for k, v in fips_dict.items() if all(x != k for x in ['60','66','69','78'])}
                    fips_dict = {'x':'50','Y':'72'}
                    for state,fips in fips_dict.items():
                        state_file = 'data/%s_%s_%s.csv'%(state,'_'.join(geo_level.split()), year)
                        #try to get the data locally first! If doesnt exist, get from Census!
                        try:
                            states_df.append(pd.read_csv(state_file, dtype = {'GEOID' : str}))
                            print('data for %s was read from memory!'%state)
                        except: 
                            #create a dictionary of counties within the specifies parameters!
                            counties = censusdata.geographies(censusdata.censusgeo([(
                                'state', fips), ('county', '*')]), 'acs5', year, key = key)
                            state_data = [censusdata.download('acs5', year, censusdata.censusgeo(
                            [('state', fips), ('county', v.geo[1][1]), (
                                geo_level, '*')]), names, key = key) for k,v in counties.items()]
                            #create a full fips code for the corrrsponding geography
                            df = pd.concat(state_data)
                            df['GEOID'] = [''.join([g[1] for g in x.geo]) for x in df.index]
                            postprocess_df(df).to_csv(state_file, index = False)
                            states_df.append(df)
                            print('%s level data for %s for %s was downloded using census API\
                                and stored locally!'%(geo_level, state, year))
                
                    print('data for all states was downloaded!')    
                    df = pd.concat(states_df)
    
                
    return df.reset_index(drop = True) 

def parse_args():
    """parses arguments from command line to use by the main function!"""
    parser=argparse.ArgumentParser(description="get census data for a specified geographic level and year")
    parser.add_argument("key" , type = str, help = 'use your census API key here. It can be obtained here: \
        https://api.census.gov/data/key_signup.html')
    parser.add_argument("--state_name", type = str, default = 'All', help = 'US state name! Use All to get \
        nationwide data!')
    parser.add_argument("--year", type = int, default = 2019, help = 'specify the year of ACS5 data!')
    parser.add_argument("--geo_level", type = str, default = 'county', help = 'specify the geographic level! \
        Can be county(default), tract, or block group!')
    args=parser.parse_args()

    print("the inputs are:")
    for arg in vars(args):
        print("{} is {}".format(arg, getattr(args, arg)))

    return args

def main():
    inputs=parse_args()
    get_census_data(inputs.key,inputs.state_name,inputs.year,inputs.geo_level)

if __name__ == '__main__':
    main()
