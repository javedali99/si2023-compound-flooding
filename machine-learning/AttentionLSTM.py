import os
import numpy as np
import csv
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from keras.models import Sequential
from keras.layers import LSTM, Dense, Activation, Bidirectional, Layer
from keras.optimizers import Adam
from keras.callbacks import EarlyStopping
from sklearn.preprocessing import MinMaxScaler
import keras.backend as K


# Custom Attention layer
class AttentionLayer(Layer):
    def __init__(self):
        super(AttentionLayer, self).__init__()

    def build(self, input_shape):
        self.W = self.add_weight(name='att_weight', shape=(input_shape[-1], 1), initializer='normal')
        self.b = self.add_weight(name='att_bias', shape=(input_shape[1], 1), initializer='zeros')
        super(AttentionLayer, self).build(input_shape)

    def call(self, inputs):
        e = K.squeeze(K.dot(inputs, self.W) + self.b, axis=-1)
        a = K.softmax(e, axis=1)
        weighted_input = inputs * K.expand_dims(a, axis=-1)
        return K.sum(weighted_input, axis=1)

    def compute_output_shape(self, input_shape):
        return input_shape[0], input_shape[2]


# Specify the folder path containing the CSV files
folder_path = '/mh1/fyarveysi/SummerInstitude/PythonCode/CSVsFolder'

# Get a list of all CSV files in the folder
csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]

# Initialize results dictionary
results = {}

# Define LSTM model parameters
n_features = None  # Set the number of input features
n_steps = None  # Set the number of time steps
n_units = 64  # Set the number of LSTM units
n_epochs = 100  # Set the number of training epochs
batch_size = 32  # Set the batch size

# Iterate over CSV files
for csv_file in csv_files:
    # Read the CSV file into a pandas DataFrame (X: features, y: target variable)
    data = pd.read_csv(os.path.join(folder_path, csv_file), delimiter=',')
    X = data.drop(['FloodDepth'], axis=1).values  # Adjust the column name for the target variable
    y = data['FloodDepth'].values  # Adjust the column name for the target variable
    
    # Apply min-max normalization to the features
    scaler = MinMaxScaler()
    X = scaler.fit_transform(X)
    
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    
    # Reshape the input data for LSTM (samples, time steps, features)
    n_features = X_train.shape[1]
    n_steps = X_train.shape[0]
    X_train = X_train.reshape((n_steps, 1, n_features))
    X_test = X_test.reshape((X_test.shape[0], 1, n_features))
    
    # Create the Attention LSTM model
    model = Sequential()
    model.add(Bidirectional(LSTM(n_units, return_sequences=True), input_shape=(1, n_features)))
    model.add(AttentionLayer())
    model.add(Dense(1))
    model.add(Activation('linear'))
    
    # Compile the model
    optimizer = Adam()
    model.compile(loss='mean_squared_error', optimizer=optimizer)
    
    # Train the model
    early_stopping = EarlyStopping(patience=10, verbose=1)
    model.fit(X_train, y_train, epochs=n_epochs, batch_size=batch_size, callbacks=[early_stopping])
    
    # Predict on the test set
    y_pred = model.predict(X_test)
    
    # Calculate R-squared
    r2 = r2_score(y_test, y_pred)
    
    # Calculate Root Mean Square Error (RMSE)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    
    # Calculate KGE
    y_test = np.reshape(y_test, (-1,))
    y_pred = np.reshape(y_pred, (-1,))
    kge = 1 - np.sqrt((np.mean(y_pred) / np.mean(y_test) - 1) ** 2 +(np.std(y_pred) / np.std(y_test) - 1) ** 2 +(np.corrcoef(y_test, y_pred)[0, 1] - 1) ** 2)


        
    
    # Get the attention weights
    attention_weights = K.eval(model.layers[1].weights[0])
    importances = np.mean(attention_weights, axis=0)  # Calculate mean along the first axis
    
    
    # Append the importances to the importances_list
    importances_list.append(importances)

    print(importances_list)
    
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
    
    
    

