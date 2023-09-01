# Functions required for notebook 3_data_aggregation.ipynb

# Imports
import pandas as pd
import numpy as np

from globals.global_vars import url, header, coordinate_description, lat, lon, start_year, end_year, sensing_interval, products, bands, above_below_left_right


def half_time_interval(df_data, type):
    """
    Decreases the time-interval by 2.
    :param: df_data: dataframe with numeric index from 0 to len(df_data.index), string-dates in a column, and pixels as columns.
    :returns: the new dataframe, which is reduced.
    """
    
    # Define the new dataframe
    df_data_new = pd.DataFrame()

    # Counter for regular copying of dataframe
    counter = 0

    # Iterate through the dataframe rows, increase by 2
    for i in range(0, len(df_data.index), 2):
        
        # Regularly copy dataframe, to avoid fragmentation
        if counter == 100:
            df_data_new = df_data_new.copy()
            counter = 0

        # Define indices
        index = df_data['date'][i]

        # Store the mean of two rows in the first date
        if type == 'mean':
            df_data_new[index] = df_data.loc[i:i+1].mean(numeric_only=True).to_frame().copy()
        # But, max-value in fire column
        elif type == 'max':
            df_data_new[index] = df_data.loc[i:i+1].max(numeric_only=True).to_frame().copy()
        else:
            raise ValueError('"type" has an unexpected value, choose between "max" and "mean"')
        
        # Increment counter
        counter +=1
    
    # Return the transpose, to get the column and rows right 
    df_data_new = df_data_new.transpose()

    return df_data_new

def double_time_interval(df_data, new_index):
    """
    Increases the the time-interval by 2.
    :param: df_data: dataframe with numeric index from 0 to len(df_data.index), string-dates in a column, and pixels as columns.
    :param: new_index: the index of the new time interval.
    :returns: the new dataframe, which is reduced.
    """
    
    # Define the new dataframe
    df_data_new = pd.DataFrame()

    # Counter for regular copying of dataframe
    counter = 0

    # Iterate through the dataframe rows, increase by 2
    for i in range(0, len(df_data.index)):
        
        # Regularly copy dataframe, to avoid fragmentation
        if counter == 49:
            df_data_new = df_data_new.copy()
            counter = 0

        # Define indices
        index_self = df_data['date'][i]
        index_other = new_index[1+2*i]

        # Store the mean of two rows in the first date
        df_data_new[index_self] = df_data.loc[i, ].to_frame().copy()
        df_data_new[index_other] = df_data.loc[i, ].to_frame().copy()
        
        # Increment counter
        counter +=1
    
    # Return the transpose, to get the column and rows right 
    df_data_new = df_data_new.transpose()

    return df_data_new



def resolution_decrement(df_data, current_dimension, desired_dimension):
    """
    Takes a dataframe, it's current dimension and the dimension that it will be converted to.
    :param: df_data: dataframe with a larger number of pixels than desired. Every column is one pixel.
    :param: current_dimension: the dimension of the input dataframe.
    :param: desired_dimension: the dimension that the dataframe will be converted to.
    :returns: the aggregated dateframe with the desired dimension
    """

    date_index = df_data['date']

    # Calculate the reduction factor
    reduction = int((current_dimension-1) / (desired_dimension-1))

    # New data frames
    df_data_agg = pd.DataFrame()

    # Copy the dataframe every 100 iterations
    counter = 0

    # Iterate through every _row_ of the pixel, of disired dimension
    for i_row in range(0, desired_dimension):
        
        # Base-index based on row, for high resolution dataframe
        i_row_hi = current_dimension * reduction * i_row
        
        # Iterate through every _column_ of the pixel, of disired dimension
        for i_col in range(0, desired_dimension):
            
            # Copy dataframe regularly
            if counter <= 100:
                df_data_agg = df_data_agg.copy()
                counter = 0
            counter += 1

            # desired index of the pixel
            index = i_row * desired_dimension + i_col

            # Index of higher resolution:
            index_hi = i_row_hi + reduction * i_col

            # Check for multiples of 21
            if (i_row+1 == desired_dimension) and (i_col+1 == desired_dimension):
                df_data_agg[f'{index}'] = df_data[f'{index_hi}']
            
            elif i_row+1 == desired_dimension:  # only merge adjacent in _column_
                df_data_agg[f'{index}'] = (df_data[f'{index_hi}'] + 
                                        df_data[f'{index_hi+1}']) / 2
        
            elif i_col+1 == desired_dimension:  # only merge adjacent in _row_
                df_data_agg[f'{index}'] = (df_data[f'{index_hi}'] + 
                                        df_data[f'{index_hi+current_dimension+1}']) / 2

            # Merge pixels of 4, if not a multiple of 21
            elif index_hi < current_dimension**2:
                df_data_agg[f'{index}'] = (df_data[f'{index_hi}'] + 
                                        df_data[f'{index_hi+1}'] + 
                                        df_data[f'{index_hi+current_dimension}'] + 
                                        df_data[f'{index_hi+current_dimension+1}']) / 4
                
            # Something is wrong if none of the above are satisfied
            else:
                raise ValueError
            
            df_data_agg['date'] = date_index
            
    return df_data_agg