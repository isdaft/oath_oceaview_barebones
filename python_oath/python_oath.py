from numpy import printoptions
from excel_gen import excel_gen, print_to_json
from get_token import get_token
from fetch_all_data import fetch_all_data, fetch_historical_data
from config import URL, CONTEXT, CONTEXT_SENSOR_HISTORY
from processing.process_data import process_data
from excel_gen import excel_gen_files
import requests
import json
from datetime import datetime
import pandas as pd







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


def main1():
    
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
    print("Main: Generate Excel File from Payload")
    #excel_gen(payload)  
    #
    print_to_json(payload)  



if __name__ == "__main__":
    main()
