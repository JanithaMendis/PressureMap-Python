import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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

# Load your data
df = pd.read_csv('1kg3.1.24.csv')  # Update with your actual file path

# Replace zeros with NaN
df_replaced = df.replace(0, np.nan)

# Calculate the average of each column, ignoring null values and zeros
average_values = df_replaced.mean(axis=0, skipna=True)

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