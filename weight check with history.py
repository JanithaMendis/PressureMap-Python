import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import os

# Function to display a matrix with values annotated in each cell
def display_matrix_with_annotations(matrix, title):
    fig, ax = plt.subplots(figsize=(15, 15))  # Increased figure size for larger cells
    cax = ax.matshow(matrix, cmap='binary')  # Using 'binary' colormap for black and white

    # Annotating each cell with the integer value
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            ax.text(j, i, f'{int(matrix[i, j])}', va='center', ha='center', color='blue', fontsize=8)

    plt.title(title)
    plt.axis('off')
    fig.colorbar(cax)
    plt.show()

# Creating a file path for updating the history
history_path = 'readings_history.csv'  # Using CSV instead of Excel

# Function to update the database CSV file with a timestamp and full file path
def update_database(history_path, timestamp, full_file_path, weight, total_area):
    # Check if the history file exists
    try:
        df_history = pd.read_csv(history_path)
    except FileNotFoundError:
        # If the file doesn't exist, create a new dataframe
        df_history = pd.DataFrame(columns=['File', 'Timestamp', 'Weight', 'TotalArea', 'File_name'])

    # Check if the file has columns
    if df_history.empty or 'File' not in df_history.columns or 'Timestamp' not in df_history.columns:
        df_history = pd.DataFrame(columns=['File', 'Timestamp', 'Weight', 'TotalArea', 'File_name'])

    # Append the new record to the dataframe
    new_record = {'File': full_file_path, 'Timestamp': timestamp, 'Weight': weight, 'TotalArea': total_area, 'File_name': file_name}
    df_history = pd.concat([df_history, pd.DataFrame([new_record])], ignore_index=True)

    # Save the updated dataframe to the CSV file
    df_history.to_csv(history_path, index=False)

# Get the full file path of the CSV file in the same folder as the PyCharm project
file_name = '2.428kgnew_2.csv'  # Replace with your actual file name
full_file_path = os.path.join(os.path.dirname(__file__), file_name)

# Load your data
df = pd.read_csv(full_file_path).replace(0, np.nan)

# Calculate the average of each column, ignoring null values and zeros
average_values = df.mean(axis=0, skipna=True)

# Convert the average values to a numeric format and reshape to a 32x32 matrix
matrix_average = pd.to_numeric(average_values, errors='coerce').fillna(0).values[:1024].reshape(32, 32)

# Flip the matrix around the x-axis
flipped_matrix = np.flipud(matrix_average)

# Display the flipped matrix with annotations
display_matrix_with_annotations(flipped_matrix, 'Flipped Average Matrix of All Columns (Excluding Zeros)')

# Dimensions of the matrix square values
dimension_1 = 46 / 32  # in cm
dimension_2 = 50 / 32  # in cm

# Calculate area in square meters
area = dimension_1 * dimension_2 * 0.0001  # Convert cm^2 to m^2

# Convert mmHg to N/m^2
mmHg_to_N_per_m2 = 133.322

# Calculate total force
total_force = np.sum(flipped_matrix) * area * mmHg_to_N_per_m2

# Calculate weight in Kg
weight = total_force / 9.81

print(f"Weight: {weight:.4f} Kg")

# Initialize total area
total_area = 0

# Iterate through each cell in the matrix
for i in range(flipped_matrix.shape[0]):
    for j in range(flipped_matrix.shape[1]):
        if flipped_matrix[i, j] != 0:
            # If the matrix value is non-zero, add the corresponding area to the total
            total_area += dimension_1 * dimension_2 * 0.0001  # Convert cm^2 to m^2

print(f"Total Area with Non-Zero Values: {total_area:.6f} square meters")

# Update the history with the current file path, timestamp, weight, and total area
current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
update_database(history_path, current_timestamp, full_file_path, weight, total_area)
