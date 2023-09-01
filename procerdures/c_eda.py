# Functions required for notebook 4_exploratory_data_analysis.ipynb

def stats(df_data, column):

    mean = df_data[column].mean()
    std = df_data[column].std()
    min = df_data[column].min()
    max = df_data[column].max()

    column = column.upper()

    print(f"""
    {column} STATISTICS
    -------------------------------------------
    Mean:                   {mean}
    Standard deviation:     {std}
    Minimal value:          {min}
    Maximal value:          {max}
    """)


def fire_stats(df_data, column):
    none = len(df_data[df_data[column] == 0].index)
    low_conf = len(df_data[df_data[column] == 1].index)
    mod_conf = len(df_data[df_data[column] == 2].index)
    high_conf = len(df_data[df_data[column] == 3].index)

    print(f"""
    FIRE STATISTICS
    ---------------------------------
    No fire:                   {none}
    Fire (low confidence):     {low_conf}
    Fire (nominal confidence): {mod_conf}
    Fire (high confidence):    {high_conf}
    """)