# might want to put the different processing functions that I accumulate
# over time into here
# process_data could just be overarching area where i can turn on and off
# what I apply to the raw api data and return as a payload for file generation
import pandas as pd
import json
from datetime import datetime
from config import BASE_URL, CONTEXT_SENSOR_HISTORY
from fetch_all_data import fetch_historical_data

def process_data(data, token):
    
    
    def combineEquipSensors(data, token):
        try:
            rows = []
    
            for sublist in data:
                for item in sublist:
                    # Prepare a row as a dictionary
                    print(item)
                    row = {
                        'Name': item['name'],
                        'Id': item['id'],
                        'Inventory Code': item['inventoryCode'],
                        'Type': item['type'],
                        'Topology Name': item['topology']['name']
                    }
                    # Append the row to the list
                    rows.append(row)
                
            with open('C:\\Users\\ashbyb\\Documents\\Alarm_Script\\alarmsFilter_20240501_142604\\fetched_sensors.json', 'r') as f:
                sensors = json.load(f)
        
            for row in rows:
            # Loop through each sensor
                row['sensors'] = []
                for sensor in sensors:
                    # If the sensor's equipment name matches the row's name
                    if 'Equipment' in sensor and sensor['Equipment'] is not None and sensor['Equipment'].get('Name') is not None and sensor['Equipment'].get('Name') == row['Name']:

                        equipment_id = row['Id']
                        sensor_id = sensor['Id']
                        # this should fetch historical data and place in this equipment's object. will be large.
                        historical_data = fetch_historical_data(BASE_URL, token, CONTEXT_SENSOR_HISTORY, equipment_id, sensor_id)
                        if 'HistoricalData' not in sensor:
                            sensor['HistoricalData'] ={}
                        
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
                        #new_sensor = {key: (sensor.get(key) if sensor.get(key) is not None else 'null') for key in ['Id', 'Name', 'ProbeSerialNumber', 'Number', 'Type', 'PhysicalParameter', 'Inventory Code']}
                        new_sensor = {
                            'Id': sensor.get('Id', 'null'),
                            'ProbeSerialNumber': sensor.get('ProbeSerialNumber', 'null'),
                            'Number': sensor.get('Number', 'null'),
                            'Type': sensor.get('Type', 'null'),
                            'PhysicalParameter': type_mapping.get(sensor.get('PhysicalParameter', 'null')),
                            'DataLoggerName': sensor.get('Connection', {}).get('DataLogger', {}).get('Name', 'null') if sensor.get('Connection') is not None else 'null',
                            'InventoryCode': sensor.get('Connection', {}).get('DataLogger', {}).get('InventoryCode', 'null') if sensor.get('Connection') is not None else 'null',
                            #'IncorrectLevel1Limits': [],
                            'Calibration': sensor.get('Calibration', {}).get('CertificateDate', 'null') if sensor.get('Calibration') is not None else 'null',
                            'HistoricalData': historical_data
                    
                        }
                
                    
                        row['sensors'].append(new_sensor)
                    
            return rows
        
        except Exception as e:
            print(f"error {e}")
            return none
    
    combinedESRet = combineEquipSensors(data, token)    

    def compare_files(master_file, tester_file, sap_file):
        # Read the excel files
        df_master = pd.read_excel(master_file)
        df_tester = pd.read_excel(tester_file)
        df_sap = pd.read_excel(sap_file)

        # Extract the 'MRK Column' values from the master file
        master_mrks = df_master['MRK Column'].values

        # Find the rows in the tester file that match the 'MRK Column' values from the master file
        matching_rows = df_tester[df_tester['MRK Column'].isin(master_mrks)]
        
        # Find the rows in the tester file that don't match the 'MRK Column' values from the master file
        non_matching_rows_tester = df_tester[~df_tester['MRK Column'].isin(master_mrks)]

        # Find the rows in the SAP file that don't match the 'MRK Column' values from the master file
        non_matching_rows_sap = df_sap[~df_sap['Serial Number'].isin(master_mrks)]

        matching_status = []
        # For each matching row, split the combined column and check the accuracy of the parts
        for index, row in matching_rows.iterrows():
           
            # Split the combined column into parts
            parts = str(row['Combined Column']).split(',')
            # Remove leading/trailing whitespaces
            df_master['MRK Column'] = df_master['MRK Column'].str.strip()
            df_tester['MRK Column'] = df_tester['MRK Column'].str.strip()

            # Convert to a consistent case (e.g., upper case)
            df_master['MRK Column'] = df_master['MRK Column'].str.upper()
            df_tester['MRK Column'] = df_tester['MRK Column'].str.upper()

            # Replace NaN values with a specific value (e.g., 'Unknown')
            df_master['MRK Column'] = df_master['MRK Column'].fillna('Unknown')
            df_tester['MRK Column'] = df_tester['MRK Column'].fillna('Unknown')
            
            df_master['Serial Number'] = df_master['Serial Number'].astype(str)
            df_sap['Serial Number'] = df_sap['Serial Number'].astype(str)
            # Check the data type of 'Serial Number'
            if isinstance(row['Serial Number'], str):
                # If it's already a string, no need to convert
                pass
            elif isinstance(row['Serial Number'], pd.Series):
                # If it's a pandas Series, use astype to convert
                row['Serial Number'] = row['Serial Number'].astype(str)
            else:
                # If it's another type (like int or float), use str to convert
                row['Serial Number'] = str(row['Serial Number'])

            df_master['Serial Number'] = df_master['Serial Number'].astype(str).str.replace('-', '').str.replace(' ', '')
            filtered_df = df_master[df_master['MRK Column'] == row['MRK Column']]
            df_master['Serial Number'] = df_master['Serial Number'].astype(str)
            if not filtered_df.empty:
                master_row = filtered_df.iloc[0]
                master_row['Serial Number'] = master_row['Serial Number'].replace('-','').replace(' ','')
            else:
                print(f"No matching row in df_master for MRK Column value {row['MRK Column']}")
                
            # Get the corresponding row in the SAP file
            # Get the corresponding row in the SAP file
            matching_sap_rows = df_sap[df_sap['Serial Number'] == row['Serial Number']]
            if not matching_sap_rows.empty:
                sap_row = matching_sap_rows.iloc[0]
            else:
                # Handle the case where no matching row was found
                # For example, you could skip this iteration of the loop
                non_matching_rows_sap = pd.concat([non_matching_rows_sap, row])
                sap_row = None  # Or any other default value

            # Check the accuracy of the 'MRK', 'Nickname', and 'Room' parts
            status = {
                'MRK_tester_master': row['MRK Column'] == master_row['MRK Column'] or f"MRK mismatch: tester file {row['MRK Column']} vs master file {master_row['MRK Column']}",
                'MRK_Combi_master': parts[0] == master_row['MRK Column'] or f"MRK mismatch: tester file {parts[0]} vs master file {master_row['MRK Column']}",
                'Serial Number_tester_sap': sap_row is not None and row['Serial Number'] == sap_row['Serial Number'] or f"Serial Number mismatch: tester file {row['Serial Number']} vs SAP file {sap_row['Serial Number'] if sap_row is not None else 'None'}",
# 'Serial Number_tester_sap': row['Serial Number'] == sap_row['Serial Number'] or f"Serial Number mismatch: tester file {row['Serial Number']} vs SAP file {sap_row['Serial Number']}",
                'Serial Number_tester_master': row['Serial Number'] == master_row['Serial Number'] or f"Serial Number mismatch: tester file {row['Serial Number']} vs master file {master_row['Serial Number']}",
                'Nickname_combi_sap': sap_row is not None and len(parts) > 1 and parts[1] == sap_row['Nick Name'] or f"Nickname mismatch: tester file {parts[1] if len(parts) > 1 else 'None'} vs SAP file {sap_row['Nick Name'] if sap_row is not None else 'None'}",
#'Nickname_combi_sap': sap_row is not None and parts[1] == sap_row['Nick Name'] or f"Nickname mismatch: tester file {parts[1]} vs SAP file {sap_row['Nick Name'] if sap_row is not None else 'None'}",
#'Nickname_combi_sap': parts[1] == sap_row['Nick Name'] or f"Nickname mismatch: tester file {parts[1]} vs SAP file {sap_row['Nick Name']}",
                'Room_combi_sap': sap_row is not None and len(parts) > 2 and parts[2] == sap_row['Room'] or f"Room mismatch: tester file {parts[2] if len(parts) > 2 else 'None'} vs SAP file {sap_row['Room'] if sap_row is not None else 'None'}"
#'Room_combi_sap': sap_row is not None and parts[2] == sap_row['Room'] or f"Room mismatch: tester file {parts[2]} vs SAP file {sap_row['Room'] if sap_row is not None else 'None'}"
#'Room_combi_sap': parts[2] == sap_row['Room'] or f"Room mismatch: tester file {parts[2]} vs SAP file {sap_row['Room']}"
            }
            print(f"Appending status for row {index}")
            # Add the status to the list
            matching_status.append(status)
            print(f"Appended status for row {index}. Total statuses: {len(matching_status)}")

        # Return the matching rows for further analysis if needed
        # Return the matching status and the non-matching rows
        return matching_status, non_matching_rows_tester, non_matching_rows_sap
    
    
        
    
    #p = "C:\\Users\\ashbyb\\Documents\\Oceaview\\"
    #master_file = p+ "master_file.xlsx"
    #tester_file= p + "tester_file.xlsx"
    #sap_file = p + "sap_file.xlsx"
    #comparedFiles = compare_files(master_file, tester_file, sap_file)
    
    
    return combinedESRet
