import os
import csv
import tkinter
from tkinter import filedialog, simpledialog, messagebox

####################
# Helper functions #
####################
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


def compare_voltage_lists(voltage1, voltage2, tolerance=1e-4):
    """Compare two voltage lists with tolerance"""
    if len(voltage1) != len(voltage2):
        return False
    
    for v1, v2 in zip(voltage1, voltage2):
        if abs(v1 - v2) > tolerance:
            return False
    
    return True


def import_and_format_data(file_paths):
    all_voltage_data = []
    all_current_data = []
    
    # Extract data from all files
    for file_path in file_paths:
        voltage_data, current_data = extract_data_from_file(file_path)
        all_voltage_data.append(voltage_data)
        all_current_data.append(current_data)
    
    # Check that all voltage data arrays are the same as the one from the first selected file
    voltage_match = True
    reference_voltage = all_voltage_data[0]
    
    for i, voltage in enumerate(all_voltage_data[1:], 1):
        if len(voltage) != len(reference_voltage):
            print(f"Warning: File {i+1} has {len(voltage)} voltage points while the first file has {len(reference_voltage)} points.")
            voltage_match = False
        else:
            # Check if voltages are approximately equal using our custom function
            if not compare_voltage_lists(voltage, reference_voltage):
                print(f"Warning: Voltage values in file {i+1} do not match those in the first file.")
                voltage_match = False
    
    if not voltage_match:
        proceed = messagebox.askyesno("Voltage Mismatch", "The voltage data is not consistent across all files. Proceed anyway?")
        if not proceed:
            return None, None
    
    # If all checks pass, return the reference voltage and all current data
    return reference_voltage, all_current_data


def get_unique_filename(output_file_base):
    output_file = output_file_base + '.csv'
    
    # Check if the file exists
    if os.path.exists(output_file):
        overwrite = messagebox.askyesno("File Exists", f"The file '{output_file}' already exists. Do you want to overwrite it?")
        if overwrite:
            return output_file
        else:
            # Ask for a new filename
            while True:
                new_name = simpledialog.askstring('Output name', 'The file already exists. Enter a new file name:')
                if new_name:
                    new_file = new_name + '.csv'
                    if not os.path.exists(new_file):
                        return new_file
                    # If the new name also exists, the loop continues
                else:
                    # User canceled
                    return None
    
    return output_file


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
    
    print(f"Data successfully saved to {output_file}")


############################
# Main processing function #
############################
def process_lsv_files():
    # Initialize tkinter
    root = tkinter.Tk()
    root.withdraw()
    root.call('wm', 'attributes', '.', '-topmost', True)
    
    # Prompt user to select multiple files
    file_paths = filedialog.askopenfilenames(title="Select CSV files", filetypes=[("CSV files", "*.csv")])

    print(file_paths)
    
    if not file_paths:
        print("No files selected. Operation canceled.")
        return
    
    print(f"Selected {len(file_paths)} files.")
    
    # Import and format data
    voltage_data, all_current_data = import_and_format_data(file_paths)
    
    if voltage_data is None:
        print("Operation canceled due to voltage data mismatch.")
        return
    
    # Get output filename with validation
    output_file_base = simpledialog.askstring('Output name', 'Enter file name for output (without extension):')
    if not output_file_base:
        print("No output filename provided. Operation canceled.")
        return
    
    output_file = get_unique_filename(output_file_base)
    if output_file:
        save_to_csv(voltage_data, all_current_data, output_file)
    else:
        print("Operation canceled.")
