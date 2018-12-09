def make_three_dig_zip(x):
    while len(x) < 5:
        x = '0'+x
    return x[:3]

def clean_census(df_census):
    # get only first 3 digits of zip code
    df_census['zip_3_digit'] = (df_census['Zip'].astype(str).apply(make_three_dig_zip))

    # Calculate the total number of males and females
    df_census['Female'] = df_census['Female_0to9_Years'] + df_census['Female_10to19_Years'] + df_census['Female_20to29_Years'] + df_census['Female_30to39_Years'] + df_census['Female_40to49_Years'] + df_census['Female_50to59_Years'] + df_census['Female_60to69_Years'] + df_census['Female_70p_Years']
    df_census['Male'] = df_census['Male_0to9_Years'] + df_census['Male_10to19_Years'] + df_census['Male_20to29_Years'] + df_census['Male_30to39_Years'] + df_census['Male_40to49_Years'] + df_census['Male_50to59_Years'] + df_census['Male_60to69_Years'] + df_census['Male_70p_Years']

    # Calculate the total number of older adults (>60)
    df_census['Old'] = df_census['Female_60to69_Years'] + df_census['Female_70p_Years'] + df_census['Male_60to69_Years'] + df_census['Male_70p_Years']

    # Calculate the percent of race,gender,and age variables for each three digit zip code
    protected_classes  = ['White',
                          'Black',
                          'Native',
                          'Asian',
                          'Islander',
                          'Hispanic',
                          'Male',
                          'Female',
                          'Old'
                         ]
    pop_by_zip = df_census.groupby('zip_3_digit')[protected_classes].apply(lambda x : x.sum())

    #get proportions
    pop_by_zip['Total'] = pop_by_zip.sum(axis = 1)
    return pop_by_zip.div(pop_by_zip['Total'].values, axis = 0)
