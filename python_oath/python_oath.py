from numpy import printoptions
from excel_gen import excel_gen, generate_excel_from_limits, print_to_json
from get_token import get_token
from fetch_all_data import fetch_all_data, fetch_historical_data
from fetch_audit import fetch_and_process_audit_trail
from comm_loss import fetch_and_process_comm_loss
from config import URL, CONTEXT, CONTEXT_SENSOR_HISTORY
from processing.process_data import process_data
from excel_gen import excel_gen_files, generate_excel_from_limits, excel_gen_equipment_names
import requests
import json
from datetime import datetime
import pandas as pd
from filter_nulls_gaps import filter_nulls_gaps
from pypdf import PdfWriter
import os
#import ghostscriptaaaaaaaa





def main2tr():
    
   
    # Prepare an empty list to store the rows
    rows = []
    incorrect_equipments = []
    equipments_and_calibrations = []
    for sublist in resource:
        for item in sublist:
            # Prepare a row as a dictionary
            print(item)
            row = {
                'Name': item['name'],
                'Inventory Code': item['inventoryCode'],
                'Type': item['type'],
                'Topology Name': item['topology']['name']
            }
            # Append the row to the list
            rows.append(row)



    with open('C:\\Users\\ashbyb\\Documents\\Alarm_Script\\alarmsFilter_20240412_163749\\fetched_sensors.json', 'r') as f:
        sensors = json.load(f)
        
    for row in rows:
    # Loop through each sensor
        row['sensors'] = []
        for sensor in sensors:
            # If the sensor's equipment name matches the row's name
            if 'Equipment' in sensor and sensor['Equipment'] is not None and sensor['Equipment'].get('Name') is not None and sensor['Equipment'].get('Name') == row['Name']:

                type_mapping = {
                    1: "C",
                    2: "RH%",
                    3: "CO2%"
                }
                correct_values_mapping = {
                    "C": [-1.0, 42.0],
                    "RH%": [45.0, 99.0],
                    "CO2%": [3.0, 7.0]
                }
                if 'Calibration' not in sensor:
                    sensor['Calibration'] = {}
                # Do something with the sensor
                # Create a new dictionary with only the desired keys and values
                #new_sensor = {key: (sensor.get(key) if sensor.get(key) is not None else 'null') for key in ['Id', 'Name', 'ProbeSerialNumber', 'Number', 'Type', 'PhysicalParameter', 'Inventory Code']}
                new_sensor = {
                    'ProbeSerialNumber': sensor.get('ProbeSerialNumber', 'null'),
                    'Number': sensor.get('Number', 'null'),
                    'Type': sensor.get('Type', 'null'),
                    'PhysicalParameter': type_mapping.get(sensor.get('PhysicalParameter', 'null')),
                    'DataLoggerName': sensor.get('Connection', {}).get('DataLogger', {}).get('Name', 'null') if sensor.get('Connection') is not None else 'null',
                    'InventoryCode': sensor.get('Connection', {}).get('DataLogger', {}).get('InventoryCode', 'null') if sensor.get('Connection') is not None else 'null',
                    #'IncorrectLevel1Limits': [],
                    'Calibration': sensor.get('Calibration', {}).get('CertificateDate', 'null') if sensor.get('Calibration') is not None else 'null'
                    
                }
                # last_data_logging = sensor.get('LastDataLogging', {})
                # if last_data_logging:
                #     for limit in last_data_logging.get('Limits', []):
                #         if limit.get('Level') == 1.0:
                #             # Check if the Level1Limits values are correct, but only for Cytomat Incubator equipments
                #             if row['Type'] == "Cytomat Incubator":
                #                 correct_values = correct_values_mapping.get(new_sensor['PhysicalParameter'])
                #                 if correct_values is not None and limit['Value'] not in correct_values:
                #                     incorrect_limit = {key: limit[key] for key in ['Id', 'Value', 'Delay', 'Level']}
                #                     new_sensor['IncorrectLevel1Limits'].append(incorrect_limit)

                # Append the new sensor to the row's 'sensors' list if it has incorrect limits
                #if new_sensor['IncorrectLevel1Limits']:
                 #   row['sensors'].append(new_sensor)
                 #   incorrect_equipments.append(row)
                    
                row['sensors'].append(new_sensor) 



    # Prepare an empty list to store the rows
    excel_rows = []

    for equipment in rows:
        # Prepare a row as a dictionary
        for sensor in equipment['sensors']:
            row = {
                'Name': equipment['Name'],
                'Inventory Code': equipment['Inventory Code'],
                'Type': equipment['Type'],
                'Topology Name': equipment['Topology Name'],
                'Calibration': sensor['Calibration'] 
            }

            # Loop through each sensor
            #for sensor in equipment['sensors']:
                # Add the Level1Limits values to the row
                #for i, limit in enumerate(sensor['IncorrectLevel1Limits']):
                #    row[f"{sensor['PhysicalParameter']} Level 1 Value ({i+1})"] = limit['Value']

            # Append the row to the list
            excel_rows.append(row)

    # Create a DataFrame from the list of rows
    df = pd.DataFrame(excel_rows)

    # Write the DataFrame to an Excel file
    df.to_excel('C:\\Users\\ashbyb\\Downloads\\all-eq_with_calbshssip3.xlsx', index=False)


        

        

    # mismatched_equipments = []

    # for equipment in rows:
    #     true_name = equipment['Name']
    #     for sensor in equipment['sensors']:
    #         if sensor['DataLoggerName'] != true_name:
    #             if equipment not in mismatched_equipments:
    #                 mismatched_equipments.append(equipment)
    #             break  
    # # Create a DataFrame from the list of rows
    # df = pd.DataFrame(rows)

    # with open('C:\\Users\\ashbyb\\Documents\\output_mis.json', 'w') as f:
    #     json.dump(mismatched_equipments, f, indent=4)
    # print("Number of mismatched equipments: ", len(mismatched_equipments))
    # print("Total number of equipments: ", len(rows))

    # Write the DataFrame to an Excel file
    #df.to_excel('C:\\Users\\ashbyb\\Downloads\\output+ship_equip_info244-3.xlsx', index=False)

    # cytomat_incubators = []

    # for equipment in rows:
    #     if equipment['Type'] == "Cytomat Incubator":
    #         for sensor in equipment['sensors']:
    #             for limit in sensor['Level1Limits']:
    #                 if limit['Value'] != -1 and limit['Value'] != 42:
    #                     cytomat_incubators.append(equipment)
    #                     break  # No need to check other limits for this sensor

    # # Print the cytomat_incubators to a new JSON file
    # with open('C:\\Users\\ashbyb\\Documents\\cytomat_incubators_offlimits.json', 'w') as f:
    #     json.dump(cytomat_incubators, f, indent=4)


def main():
    
    # generate token
    print("Main: Generating Token")
    token = get_token()
    
    # get the data from the api
    print("Main: Fetch All Data From API")
    data = fetch_all_data(URL, token, CONTEXT)

    # process the data
    print("Main: Process Payload")
    payload = process_data(data, token)
    
    # generate excel file with processed data
    #print("Main: Generate Excel File from Payload")
    #generate_excel_from_limits(payload, 'C:\\Users\\ashbyb\\Downloads\\unit_limits_incorrect5.xlsx')
    #excel_gen(payload)  

    # take in the payload, then print to a json file and return the file name and location
    with open('C:\\Users\\ashbyb\\Downloads\\py_historical_data_75b_j111.json', 'w') as f:
        json.dump(payload, f, indent=4)
    # filter nulls and gaps from a json file
    filter_nulls_gaps('C:\\Users\\ashbyb\\Downloads\\py_historical_data_75b_j111.json')

def main_test_readings():
    payload_file = 'C:\\Users\\ashbyb\\Downloads\\readings_gap.json'
    filter_nulls_gaps(payload_file)

def main11():
    print("Main: Generating Token")
    token = get_token()
    
    print("Main: Fetch All Data From API")
    data = fetch_all_data(URL, token, CONTEXT)
    
    print("Main: Process Payload")
    payload = process_data(data, token)
    
    #print("excel gen")
    #excel_gen_equipment_names(payload)
    #audit_results = fetch_and_process_audit_trail('MRK0307600, 3004, 2W220, ENV. CH.', token)
    #print(f"{audit_results}")

def main282_biomek():
    
    import os
    import re

    def find_snippets(directory, search_term):
        # Initialize a list to hold filenames
        filenames = []
        # Initialize a dictionary to hold sections
        sections_dict = {}

        # Walk through the directory
        for root, dirs, files in os.walk(directory):
            for file in files:
                # Check if the file is a .log file
                if file.endswith('.log'):
                    # Open the file
                    with open(os.path.join(root, file), 'r') as log_file:
                        # Read the file content
                        content = log_file.read()
                        # Split the content into sections
                        sections = re.split(r'\n\s*\n', content)
                        # Check each section for the search term
                        for section in sections:
                            if search_term in section:
                                print(f"adding {file} to RESULTS.")
                                
                                # Add the filename to the list
                                if file not in filenames:
                                    filenames.append(file)
                                # Add the section to the dictionary
                                if file not in sections_dict:
                                    sections_dict[file] = []
                                sections_dict[file].append(section)

        # Open the output file
        with open('C:\\Users\\ashbyb\\Downloads\\Span8_FoundFileList.txt', 'w') as output_file:
            # Write the filenames to the output file
            output_file.write('Files:\n')
            for filename in filenames:
                output_file.write(f'{filename}\n')
            output_file.write('\n')

            # Write the sections to the output file
            for filename, sections in sections_dict.items():
                output_file.write(f'Filename: {filename}\n')
                for section in sections:
                    output_file.write(f'{section}\n\n')

        # Call the function with the directory and search term


def main_biomek_script():
    
    import os
    import re
    
    folder = "C:\\Users\\ashbyb\\OneDrive - Merck Sharp & Dohme LLC\\Desktop\\Biomek_logs_MRK6032083_29May2024\\"

    def find_files_and_methods(directory, search_term):
        # Initialize a list to hold filenames
        details_filenames = []
        # Initialize a dictionary to hold methods
        methods_dict = {}
        usernames_dict = {}
        # Initialize a list to hold the final objects
        final_objects = []
        pod2_counts = {}
        # Walk through the directory
        for root, dirs, files in os.walk(directory):
            for file in files:
                # Check if the file is a Details .log file and contains the search term
                if file.startswith('Details') and file.endswith('.log'):
                    with open(os.path.join(root, file), 'r') as log_file:
                        lines = log_file.readlines()
                        content = ''.join(lines)
                        if search_term in content:
                            details_filenames.append(file)
                            # Read the second line
                            if len(lines) > 1:
                                second_line = lines[1]
                            
                            # Extract the username
                                username = second_line.split('=')[1].strip()
                                usernames_dict[file] = username

        # Create the Span8 filenames list
        span8_filenames = [filename.replace('Details', 'Span8Pipetting') for filename in details_filenames]
        span8_t_filenames = [filename.replace('Details', 'Span8Transfer') for filename in details_filenames]
        unified_t_filenames = [filename.replace('Details', 'UnifiedPipetting') for filename in details_filenames]
        unified_p_filenames = [filename.replace('Details', 'UnifiedTransfer') for filename in details_filenames]
        pipetting_filenames = [filename.replace('Details', 'Pipetting') for filename in details_filenames]
        
        all_filenames = span8_filenames + span8_t_filenames + unified_t_filenames + unified_p_filenames + pipetting_filenames
        

        # Walk through the directory again
        for root, dirs, files in os.walk(directory):
            for filename in all_filenames:
                if filename in files:
                    # Open the file
                    with open(os.path.join(root, filename), 'r') as log_file:
                        content = log_file.read()
                        # Count the number of instances of "Pod2"
                        pod2_counts[filename] = content.count('Pod2')
                        # Read the first line
                        first_line = log_file.readline().strip()
                        # Extract the method
                        method_name = content.split('\n')[0].split('=')[1].strip() if '=' in content.split('\n')[0] else None
                        methods_dict[filename] = method_name

        # Build the final objects list
        for details_filename in details_filenames:
            final_objects.append({
                'Details filename': details_filename,
                'Logged in User': usernames_dict.get(details_filename),
                'Span8 method': methods_dict.get(details_filename.replace('Details', 'Span8Pipetting')),
                'Span8 Pod2 count >= 2': pod2_counts.get(details_filename.replace('Details', 'Span8Pipetting'), 0) >= 2,
                'Span8_t method': methods_dict.get(details_filename.replace('Details', 'Span8Transfer')),
                'Span8_t Pod2 count >= 2': pod2_counts.get(details_filename.replace('Details', 'Span8Transfer'), 0) >= 2,
                'Unified_t method': methods_dict.get(details_filename.replace('Details', 'UnifiedPipetting')),
                'Unified_t Pod2 count >= 2': pod2_counts.get(details_filename.replace('Details', 'UnifiedPipetting'), 0) >= 2,
                'Unified_p method': methods_dict.get(details_filename.replace('Details', 'UnifiedTransfer')),
                'Unified_p Pod2 count >= 2': pod2_counts.get(details_filename.replace('Details', 'UnifiedTransfer'), 0) >= 2,
                'Pipetting method': methods_dict.get(details_filename.replace('Details', 'Pipetting')),
                'Pipetting Pod2 count >= 2': pod2_counts.get(details_filename.replace('Details', 'Pipetting'), 0) >= 2
            })

        return final_objects

    # Call the function with the directory and search term
    final_objects = find_files_and_methods(folder, 'Span8')

    # Print the final objects
    for obj in final_objects:
        print(obj)
    df = pd.DataFrame(final_objects)
    df.to_excel('C:\\Users\\ashbyb\\Downloads\\output_py_biomek_span8_logs_scrape.xlsx', index=False)

def mai1n():


    def compress_pdf(input_file, output_file):
        args = [
            "ps2pdf", # actual value doesn't matter
            "-dNOPAUSE", "-dBATCH", "-dSAFER",
            "-sDEVICE=pdfwrite",
            "-dCompatibilityLevel=1.4",
            "-dPDFSETTINGS=/screen", # lowest quality
            "-sOutputFile=" + output_file,
            input_file
        ]

        encoding = 'utf8'
        args = [a.encode(encoding) for a in args]

        ghostscript.Ghostscript(*args)

    def compress_pdfs_in_dir(directory):
        for filename in os.listdir(directory):
            if filename.endswith(".pdf"):
                input_file = os.path.join(directory, filename)
                output_file = os.path.join(directory, "compressed_" + filename)
                compress_pdf(input_file, output_file)

    # Usage
    compress_pdfs_in_dir("C:\\Users\\ashbyb\\OneDrive - Merck Sharp & Dohme LLC\\Documents\\2023_\\lg_file")
    

   # writer = PdfWriter(clone_from="C:\\Users\\ashbyb\OneDrive - Merck Sharp & Dohme LLC\\Documents\\2023_\\27-Sep-2023-PM_UPLC.pdf")
        
if __name__ == "__main__":
    main()
