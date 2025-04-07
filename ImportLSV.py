import os
import csv
import tkinter as tk
import tkinter.filedialog
#from tkinter import Tk

###########################
# Define helper functions #
###########################

def extract_data_from_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        
        # Find the line with 'Potential/V,Current/A'
        start_index = 0
        for i, line in enumerate(lines):
            if 'Potential/V, Current/A' in line:
                start_index = i + 1  # Skip the next blank line
                break
             
        # Extract voltage and current data
        voltage_data = []
        current_data = []
        for line in lines[start_index:]:
            if line.strip():  # Skip any blank lines
                potential, current = line.strip().split(',')
                voltage_data.append(float(potential))
                current_data.append(float(current))
                
        return voltage_data, current_data

def import_and_format_data(file_paths):
    all_voltage_data = None
    all_current_data = []

    for file_path in file_paths:
        voltage_data, current_data = extract_data_from_file(file_path)
        
        if all_voltage_data is None:
            all_voltage_data = voltage_data
        
        all_current_data.append(current_data)
    
    return all_voltage_data, all_current_data

def save_to_csv(voltage_data, all_current_data, output_file):
    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        
        # Write header
        header = ['Potential'] + [f'Current_{i+1}' for i in range(len(all_current_data))]
        writer.writerow(header)
        
        # Write data rows
        for i in range(len(voltage_data)):
            row = [voltage_data[i]] + [current[i] for current in all_current_data]
            writer.writerow(row)

####################
# Start processing #
####################

# Prompt user to select multiple files for import using tkinter to generate a dialog box
root = tk.Tk()
root.withdraw()
root.call('wm', 'attributes', '.', '-topmost', True) # Needed to make sure the dialog is not hidden in the background
file_paths = tk.filedialog.askopenfilenames(title="Select CSV files", filetypes=[("CSV files", "*.csv")])

# Import and format data
voltage_data, all_current_data = import_and_format_data(file_paths)

# Save formatted data to a new CSV file
output_file = tkinter.simpledialog.askstring('', 'Enter file name for output:') + '.csv'
save_to_csv(voltage_data, all_current_data, output_file)
