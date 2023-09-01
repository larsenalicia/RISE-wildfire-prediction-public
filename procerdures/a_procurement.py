# Functions required for notebook 1_data_procurement.ipynb


# IMPORTS
# External imports
import requests
import json
import datetime
import pandas as pd

# Internal imports
from globals.global_vars import url, header, coordinate_description, lat, lon, start_year, end_year, sensing_interval, products, bands, above_below_left_right


def print_globals_of_interest():
    """
    Prints the global variables necessary for 1_data_procurement.ipynb
    """
    print(f"""
    GLOBAL VARIABLES

    Set-up 
        url = {url}
        header = {header}

    Parameters  
        lat = {lat}
        lon = {lon}
        products = {products}
        bands = {bands}
        above_below = {above_below_left_right}
        left_right = {above_below_left_right}
    """)

def get_dates(data_points_in_year, product):
    """
    Retrieves all the dates in the time_period in between the years specified in globals.py, between Feb and Nov.
    :param: data_points_in_year: the number of data points that a product collects over a year.
    :param: product: the product code name of interest.
    :returns: the modis dates of interest and the real dates of interst.
    """
    
    # The numer of years between the given start and end years
    time_period = (end_year + 1) - start_year   
    
    # Calculating the number of data points: based on the the sensing interval of the instrument and the time-period (years) of interest
    data_points_in_time_interval = time_period * data_points_in_year

    # Get response from https
    response = requests.get(f'https://modis.ornl.gov/rst/api/v1/{product}/dates?latitude={lat}&longitude={lon}', headers=header)

    # Check the available dates
    dates: list = json.loads(response.text)['dates']
    modis_dates: list = [i['modis_date'] for i in dates]
    #calendar_dates = [i['calendar_date'] for i in dates]
    
    # Get the dates within time interval of interest
    dates_mod = modis_dates[modis_dates.index(f'A{start_year}001'):modis_dates.index(f'A{start_year}001') + data_points_in_time_interval]
    dates_real = [(datetime.datetime(int(date[1:5]), 1, 1) + datetime.timedelta(int(date[5:]))).strftime('%Y-%m-%d') for date in dates_mod]

    # Filter dates on time period 1 Feb - 1 Nov
    index_not_of_interest = [dates_real.index(date) for date in dates_real if ((int(date.split('-')[1]) == 1) or 
                                                                                (int(date.split('-')[1]) == 11) or
                                                                                (int(date.split('-')[1]) == 12))]

    # New dates, only the ones of interest
    dates_mod = [date for date in dates_mod if dates_mod.index(date) not in index_not_of_interest]
    dates_real = [date for date in dates_real if dates_real.index(date) not in index_not_of_interest]

    return dates_mod, dates_real


def print_parameters_of_interest():
    """
    Prints the parameters used in the data retrieval in 1_data_procurement.ipynb.
    """
    print(f'''
    CONSTANTS
        latitude = {lat}
        longitude = {lon}
        kmAboveBelow = {above_below_left_right}
        kmLeftRight = {above_below_left_right}

    VARIABLES
        product: products[i]
        band = bands[j]
        startDate = dates_mod[k]
        endDate = dates_mod[k]
    ''')



def data_retrival(product_key, band, dates_mod, dates_real):
    """
    Retrieves the data and writes it to a CSV file.
    
    """
    # Define the product code
    product = products[product_key]

    # Initialize list to store the returned data
    data = []

    # Iterate through the list of dates and submit subset requests for each date:
    for dt in dates_mod:
        try:
            # Join LST request parameters to URL string and submit request
            response = requests.get("".join([
                url, product, "/subset?",
                "latitude=", str(lat),
                "&longitude=", str(lon),
                "&band=", str(band),
                "&startDate=", str(dt),
                "&endDate=", str(dt),
                "&kmAboveBelow=", str(above_below_left_right),
                "&kmLeftRight=", str(above_below_left_right)
            ]), headers=header)

            data.append( json.loads(response.text)['subset'][0]['data'] )
        except:
            pass
    
    # Error control  
    if len(data) == len(dates_real):
        df_data = pd.DataFrame(data, index=dates_real)
    elif len(data) < len(dates_real):
        difference = len(dates_real) - len(data)
        dates_real_short = dates_real[: len(dates_real) - difference]
        df_data = pd.DataFrame(data, index=dates_real_short)
    else:
        raise ValueError('The length of the data is longer than the index')

    # Store the data as a CSV
    df_data.to_csv(f'data/procurement/{product_key}/{product}_{band}_{start_year}-{end_year}_{coordinate_description}.csv')

    print(f'✅ {product_key} {band}')

