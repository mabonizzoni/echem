import os      # file operations
import re      # regular expressions
import csv     # comma-separated file handling
import tkinter # dialog boxes
from tkinter import filedialog, simpledialog, messagebox

####################
# Helper functions #
####################
def extract_data_from_file(file_path):
    """Extract linear scan voltammetry data from a comma-separated CSV file. Returns voltage, current for that file."""
    with open(file_path, 'r') as file:
        lines = file.readlines()
        
        # Find the line with 'Potential/V, Current/A'. Note the space after the comma.
        start_index = 0
        for i, line in enumerate(lines):
            if 'Potential/V, Current/A' in line:
                start_index = i + 1  # Advance the index by one more line to skip the blank line after the 'Potential/V, Current/A' header.
                break
             
        # Extract voltage and current data from the lines using the start
        voltage_data = []
        current_data = []
        for line in lines[start_index:]:
            if line.strip():  # Strip() removes whitespace so, if no data is present, an empty string is returned, which is falsey in Python. So this skips any blank lines.
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
    """Calls data extractor on all files in input, checks that voltages are all same, returns all extracted data formatted in a table"""
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


def get_unique_filename():
    """
    Prompts user for a file name, checks if it exists, and handles overwrite confirmations.
    Returns a valid output filename with .csv extension or None if canceled.
    """
    # Initial prompt for filename
    output_file_base = simpledialog.askstring('Output name', 'Enter file name for output (without extension):')
    if not output_file_base:
        print("No output filename provided. Operation canceled.")
        return None
    
    output_file = output_file_base + '.csv'
    
    # Check if the file exists
    if os.path.exists(output_file):
        overwrite = messagebox.askyesno("File Exists", f"The file '{output_file}' already exists. Do you want to overwrite it?")
        if overwrite:
            # Use the existing filename
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
                    print("No alternative filename provided. Operation canceled.")
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
    root.withdraw() # do now show a framework
    root.call('wm', 'attributes', '.', '-topmost', True) # make sure the dialogs are visible on top of the current window
    
    # Prompt user to select multiple files
    # Note: The files are NOT returned in the order in which they were selected!
    file_paths = filedialog.askopenfilenames(title="Select CSV files", filetypes=[("CSV files", "*.csv")])
 
    if not file_paths:
        print("No files selected. Operation canceled.")
        return
    
    print(f"Selected {len(file_paths)} files.")

    def extract_number(file_path):
        # Extract just the filename from the full path
        filename = os.path.basename(file_path)
        
        # Find all numbers in parentheses using regular expressions (regex)
        # \( and \) match literal parentheses
        # (\d+) captures one or more digits between the parentheses
        # the r defines a raw string, in which backslashes are interpreted as literals, and not as escape characters
        # this is handy when specifying regular expressions which often include many backslashes
        # findall() returns all non-overlapping matches as a list of strings
        matches = re.findall(r'\((\d+)\)', filename)
        
        # If matches were found, return the last one as an integer
        # Otherwise return infinity to place the file at the end when sorting
        return int(matches[-1]) if matches else float('inf')
    # end of extract_number
  
    # Sort file paths based on the extracted experiment numbers from the filenames
    sorted_file_paths = sorted(file_paths, key=extract_number)

    # Import and format data
    voltage_data, all_current_data = import_and_format_data(sorted_file_paths)
    
    if voltage_data is None:
        print("Operation canceled due to voltage data mismatch.")
        return
    
    # Get output filename with validation
    output_file = get_unique_filename()
    root.update()  # It avoids hung tkinter dialog boxes on MacOS; not needed in Windows
    if output_file:
        save_to_csv(voltage_data, all_current_data, output_file)
    else:
        print("Operation canceled.")
