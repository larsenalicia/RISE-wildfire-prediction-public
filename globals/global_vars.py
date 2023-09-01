# Global variables determining location, size and time period for analysis

# Random state
random_state = 42

# Set up
url = "https://modis.ornl.gov/rst/api/v1/"
header = {'Accept': 'application/json'} # Use following for a csv response: header = {'Accept': 'text/csv'}

# Place if interest
coordinates: tuple = (67.236412, 21.956056) 
coordinate_description = 'nilivara'
lat = coordinates[0]
lon = coordinates[1]

# Determines the size
above_below_left_right = 100

# Time period
start_year = 2018
end_year = 2022
time_period = end_year - start_year

sensing_interval = None

# Data points in a year, depening on sening interval
data_points_in_year_8 = 46
data_points_in_year_16 = 23

data_points_in_time_interval_8 = time_period * data_points_in_year_8
data_points_in_time_interval_16 = time_period * data_points_in_year_16

date_indices = {
    8: data_points_in_time_interval_8, 
    16: data_points_in_time_interval_16
}

types: dict = {
    'lst': 'mean',
    'lsr': 'mean',
    'evi': 'mean',
    'fire': 'max'}

# Modis products
products: dict = { 
    'lst': 'MOD11A2',
    'lsr': 'MOD09A1',
    'evi': 'MOD13Q1',
    'fire': 'MOD14A2'}

alternative_mapping: dict = {
    'nir': 'lsr',
    'swir': 'lsr'}

# Product_names
product_names = ['lst', 'nir', 'swir', 'evi', 'fire']

# Bands per product
bands: dict = {
    'MOD11A2': ['LST_Day_1km', 'QC_Day'],
    'MOD09A1': ['sur_refl_b02', 'sur_refl_b06', 'sur_refl_qc_500m'],
    'MOD13Q1': ['250m_16_days_EVI', '250m_16_days_VI_Quality'],
    'MOD14A2': ['FireMask']}

time_intervals: dict = {
    'MOD11A2': 8,
    'MOD09A1': 8,
    'MOD13Q1': 16,
    'MOD14A2': 8}

# Original dimension in pixels
space_resolution: dict = { 
    'lst': 1,
    'nir': 0.5,
    'swir': 0.5,
    'evi': 0.25,
    'fire': 1}

def dimension(key):
    """ Takes a string key and calculates it's dimension in pixels.
    """
    return int((2 * above_below_left_right) / space_resolution[key]) + 1


# Original dimension in pixels
original_dimensions: dict = { 
    'lst': dimension('lst'),
    'nir': dimension('nir'),
    'swir': dimension('swir'),
    'ndmi': dimension('swir'),
    'evi': dimension('evi'),
    'fire': dimension('fire')}