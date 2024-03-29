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

# Function to update the database CSV file with a timestamp, full file path, weight, total area, actual weight, and position
def update_database(history_path, timestamp, full_file_path, weight, total_area, actual_weight, position, file_name):
    # Check if the history file exists
    try:
        df_history = pd.read_csv(history_path)
    except FileNotFoundError:
        # If the file doesn't exist, create a new dataframe
        df_history = pd.DataFrame(columns=['File', 'Timestamp', 'Weight', 'TotalArea', 'ActualWeight', 'Position', 'File_name'])

    # Check if the file has columns
    if df_history.empty or 'File' not in df_history.columns or 'Timestamp' not in df_history.columns:
        df_history = pd.DataFrame(columns=['File', 'Timestamp', 'Weight', 'TotalArea', 'ActualWeight', 'Position', 'File_name'])

    # Append the new record to the dataframe
    new_record = {'File': full_file_path, 'Timestamp': timestamp, 'Weight': weight, 'TotalArea': total_area, 'ActualWeight': actual_weight, 'Position': position, 'File_name': file_name}
    df_history = pd.concat([df_history, pd.DataFrame([new_record])], ignore_index=True)

    # Save the updated dataframe to the CSV file
    df_history.to_csv(history_path, index=False)

# Define positions outside the block to make it accessible throughout the script
positions = ['left upper corner', 'right upper corner', 'left middle', 'right middle', 'left bottom corner', 'right bottom corner']

# Menu to ask the user what they need
print("What do you need?")
print("1. Weigh a weight")
print("2. Retrieve an entry")

user_choice = input("Enter the corresponding number for your choice: ")

if user_choice == '1':
    # Weigh a weight

    # Prompt the user for the actual weight
    actual_weight = float(input("What is the actual weight? (in Kg): "))

    # Prompt the user for the position of the weights
    print("Select the position of the weights:")
    for i, pos in enumerate(positions, start=1):
        print(f"{i}. {pos}")

    selected_position_index = int(input("Enter the corresponding number for the position: "))
    selected_position = positions[selected_position_index - 1]

    # Get the full file path of the CSV file in the same folder as the PyCharm project
    file_name = '1.628kgnew11.csv'  # Replace with your actual file name
    full_file_path = os.path.join(os.path.dirname(__file__), file_name)

    # Load your data and skip the first 12 columns and the first row
    df = pd.read_csv(full_file_path, skiprows=1, usecols=list(range(12, 1036))).replace(0, np.nan)

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

    # Update the history with the current file path, timestamp, weight, total area, actual weight, and position
    current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    update_database(history_path, current_timestamp, full_file_path, weight, total_area, actual_weight, selected_position, file_name)

elif user_choice == '2':

    # Prompt the user for the actual weight
    actual_weight = float(input("Enter the actual weight for retrieval (in Kg): "))

    # Prompt the user for the position of the weights
    print("Select the position of the weights:")
    for i, pos in enumerate(positions, start=1):
        print(f"{i}. {pos}")

    selected_position_index = int(input("Enter the corresponding number for the position: "))
    selected_position = positions[selected_position_index - 1]

    # Load the history file
    try:
        df_history = pd.read_csv(history_path)
    except FileNotFoundError:
        print("History file not found.")
        exit()

    # Filter entries based on user input
    filtered_entries = df_history[
        (df_history['ActualWeight'] == actual_weight) & (df_history['Position'] == selected_position)]

    if not filtered_entries.empty:
        # Display the retrieved entries
        print("\nRetrieved Entries:")
        for index, row in filtered_entries.iterrows():
            print(f"Timestamp: {row['Timestamp']}")
            print(f"File Path: {row['File']}")
            print(f"Weight: {row['Weight']} Kg")
            print(f"Total Area: {row['TotalArea']} square meters")
            print(f"Actual Weight: {row['ActualWeight']} Kg")
            print(f"Position: {row['Position']}")
            print("\n")
    else:
        print("No entries found for the given criteria.")
else:
    print("Invalid choice. Please select a valid option.")

# Identify the column with the highest average value
highest_column_index = np.argmax(average_values)

# Get the 20 multiples of the number of rows
multiples_of_rows = np.arange(20) * len(df)

# Identify the column with the highest average value
highest_column_index = np.argmax(average_values)

# Get the 20 multiples of the number of rows
multiples_of_rows = np.arange(20) * len(df)

# Plotting the graph using the data from the file_name CSV file
plt.figure(figsize=(10, 6))
for i in range(20):
    plt.plot(df.iloc[i * len(df):(i + 1) * len(df), highest_column_index].values, marker='o', label=f'Row Multiple {i + 1}')

plt.title(f'Highest Value Column ({highest_column_index}) Against 20 Multiples of Rows')
plt.xlabel('Column Index')
plt.ylabel('Column Value')
plt.legend()
plt.grid(True)
plt.show()
