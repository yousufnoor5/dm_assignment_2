#Giving categories to low,medium, high locations :

import pandas as pd

# Read the CSV file into a DataFrame
df = pd.read_csv('plots-dataset-new.csv')

# Set the display option to show float values with standard decimal notation
pd.set_option('display.float_format', '{:.2f}'.format)

# Group by unique area values and get the lowest, highest, and average rate for each area
aggregated = df.groupby('area')['price'].agg(['min', 'max', 'mean']).reset_index()

# Rename the columns so that they're easier to understand upon merging back
aggregated.columns = ['area', 'area_min', 'area_max', 'area_mean']

# Merge the aggregated DataFrame back to the original DataFrame
df = df.merge(aggregated, on='area')

# Define a function to categorize the location type based on the price relative to the min, max, and mean
def categorize_location_type(row):
    if row['price'] < row['area_mean']:
        return 'Low'  # Low
    elif row['price'] < row['area_max']:
        return 'Medium'  # Medium
    else:
        return 'High'  # High

# Apply the function to create a new 'Location_Type' column
df['location_type'] = df.apply(categorize_location_type, axis=1)

# Drop unnecessary columns if you want to keep only the 'area', 'price', and 'location_type' columns
df = df.drop(columns=['area_min', 'area_max', 'area_mean'])

# Display the result
print(df.head())

df.to_csv('new_plots.csv', index=False)


#One hot encoding for these categories


import pandas as pd

def one_hot_encode_city(csv_file, city_column):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file)
    # df.drop(columns=['url'], inplace=True)

    # Perform one-hot encoding for the specified city column
    df_encoded = pd.get_dummies(df, columns=[city_column], prefix=city_column)

    return df_encoded

# Example usage:
input_csv_path = 'new_plots.csv'
city_column_name = 'location_type'

encoded_df = one_hot_encode_city(input_csv_path, city_column_name)

# Export the DataFrame with one-hot encoding to a new CSV file
output_csv_path = 'plots-dataset-final.csv'
encoded_df.to_csv(output_csv_path, index=False)

