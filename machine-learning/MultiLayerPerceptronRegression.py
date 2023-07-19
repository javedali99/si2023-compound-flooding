import os
import numpy as np
import csv
import pandas as pd
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import MinMaxScaler

# Specify the folder path containing the CSV files
folder_path = '/mh1/fyarveysi/SummerInstitude/PythonCode/CSVsFolder'

# Get a list of all CSV files in the folder
csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]

# Initialize results dictionary
results = {}

# Initialize importances list
importances_list = []

# Iterate over CSV files
for csv_file in csv_files:
    # Read the CSV file into a pandas DataFrame (X: features, y: target variable)
    data = pd.read_csv(os.path.join(folder_path, csv_file), delimiter=',')
    X = data.drop(['FloodDepth'], axis=1)  # Adjust the column name for the target variable
    y = data['FloodDepth']  # Adjust the column name for the target variable
    
    # Apply min-max normalization to the features
    scaler = MinMaxScaler()
    X = scaler.fit_transform(X)
    
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)    
     
    
    # Create an SVR model with a linear kernel
    # Create an MLP regressor
    mlp_model = MLPRegressor(hidden_layer_sizes=(10, 10), activation='relu', solver='adam', random_state=5)
    
    # Perform cross-validation and calculate mean squared error
    cv_scores = cross_val_score(mlp_model, X_train, y_train, cv=10, scoring='neg_mean_squared_error')
    avg_cv_score = -cv_scores.mean()
    
    # Train the model
    mlp_model.fit(X_train, y_train)
    
          
    # Get feature importances
    importances = np.abs(mlp_model.coefs_[0]).mean(axis=0)

    # Append the importances to the importances_list
    importances_list.append(importances)

    print(importances_list)
    
    
    # Predict the target variable for the test set
    y_pred = mlp_model.predict(X_test)
       
    # Calculate R-squared score (coefficient of determination) on the test set
    r2 = r2_score(y_test, y_pred)
    
    # Calculate Root Mean Square Error (RMSE)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    
    # Calculate the mean of the observed values
    observed_mean = np.mean(y_test)

    # Calculate the KGE
    KGE = 1 - np.sqrt((np.mean(y_pred) / np.mean(y_test) - 1) ** 2 +(np.std(y_pred) / np.std(y_test) - 1) ** 2 + (np.corrcoef(y_test, y_pred)[0, 1] - 1) ** 2)

    # Create a new entry in the results dictionary for the current file name
    results[csv_file] = {
        'file_name': csv_file,
        'feature_importances': importances_list,
        'r_squared': r2,
        'rmse': rmse,
        'kge': KGE,
        'avg_cv_score': avg_cv_score}
     

# Save feature importance, R-squared score, and average mean squared error results to a single CSV file
output_file = 'feature_importance_results_MPL_10.csv'
with open(output_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)

    # Write the header row
    header = ['GEOID', 'Precipitation_importance', 'Surge_importance', 'Discharge_importance', 'R-squared', 'RMSE', 'KGE', 'Avg_cv_score']
    writer.writerow(header)

    # Write the data rows
    for result in results.values():
        row = [
            result['file_name'],
            result['feature_importances'][0],
            result['feature_importances'][1],
            result['feature_importances'][2],
            result['r_squared'],
            result['rmse'],
            result['kge'],
            result['avg_cv_score']
        ]
        writer.writerow(row)                        




