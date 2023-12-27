#ONE HOT ENCODING FOR CITIES :

import pandas as pd

def one_hot_encode_city(csv_file, city_column):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file)
    df.drop(columns=['url'], inplace=True)

    # Perform one-hot encoding for the specified city column
    df_encoded = pd.get_dummies(df, columns=[city_column], prefix=city_column)

    return df_encoded

# Example usage:
input_csv_path = 'plots-dataset.csv'
city_column_name = 'city'

encoded_df = one_hot_encode_city(input_csv_path, city_column_name)

# Export the DataFrame with one-hot encoding to a new CSV file
output_csv_path = 'plots-dataset-v3.csv'
encoded_df.to_csv(output_csv_path, index=False)


#BINARY ENCODING FOR LOCATIONS :

import pandas as pd
import category_encoders as ce

def binary_encode_location(csv_file, location_column, start_suffix=1):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file)
    loc = df['location']

    # Create a BinaryEncoder instance
    encoder = ce.BinaryEncoder(cols=[location_column], return_df=True)

    # Fit-transform the 'location' column
    df_encoded = encoder.fit_transform(df)

    # Rename the binary columns with the desired suffix
    binary_columns = [f"{location_column}_{i}" for i in range(len(encoder.get_feature_names_out()))]
    new_column_names = {old_name: f"{location_column}_{start_suffix + i}"
                        for i, old_name in enumerate(binary_columns)}

    df_encoded.rename(columns=new_column_names, inplace=True)

    df_encoded['location'] = loc

    return df_encoded

# Example usage:
input_csv_path = 'plots-dataset-v3.csv'
location_column_name = 'location'
start_suffix = 1

encoded_df = binary_encode_location(input_csv_path, location_column_name, start_suffix)

# Export the DataFrame with binary encoding to a new CSV file
output_csv_path = 'plots-dataset-new.csv'
encoded_df.to_csv(output_csv_path, index=False)

