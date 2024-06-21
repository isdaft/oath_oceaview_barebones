# might want to put the different processing functions that I accumulate
# over time into here
# process_data could just be overarching area where i can turn on and off
# what I apply to the raw api data and return as a payload for file generation
import pandas as pd
import json
from datetime import datetime
from config import BASE_URL, CONTEXT_SENSOR_HISTORY
from fetch_all_data import fetch_historical_data
from fetch_audit import fetch_and_process_audit_trail
from excel_gen import print_to_json

def process_data(data, token):
    
    def check_limits(limits, equipment_type, physical_param):

        #is not a door sensor
        #"PhysicalParameter": 12,
        print(f"Checking Limits")
        #equipment_type = "-70C"
        correct_values_70C = {
            1.0: [-85.0, -55.0],
            2.0: [-50.0],
            3.0: [-45.0],
        }
        #equipment_type = "-80C"
        correct_values_80C = {
            1.0: [-95.0, -65.0],
            2.0: [-60.0],
            3.0: [-55.0],
        }
        #equipment_type = "-20C"
        correct_values_20C = {
            1.0: [-35.0, -5.0],
            2.0: [-40.0, 0.0],
            3.0: [5.0],
        }
        #equipment_type = "4C"
        correct_values_4C = {
            1.0: [2.0,8.0],
            2.0: [0.0,10.0],
            3.0: [15.0],
        }
        #equipment_type = "Incubator"
        correct_values_INC_C = {
            1.0: [35.0, 45.0],
            2.0: [30.0, 50.0],
            3.0: [25.0],
        }
        correct_values_INC_CO2 = {
            1.0: [3.0, 7.0],
            2.0: [1.0, 9.0],
        }
        correct_values_INC_RH = {
            1.0: [45.0, 99.0],
            2.0: [35.0],
        }
        
        # Map the equipment types to the correct values
        # sensor type = C
        equipment_type_mapping = {
            "-70C": correct_values_70C,
            "-80C": correct_values_80C,
            "-20C": correct_values_20C,
            "4C": correct_values_4C,
            "Incubator_C": correct_values_INC_C,
            "Incubator_CO2%": correct_values_INC_CO2,
            "Incubator_RH%": correct_values_INC_RH,
            # Add other equipment types here...
        }
        if equipment_type == "Incubator" and physical_param:
            equipment_type += f"_{physical_param}"
        # Get the correct values for the given equipment type
        print(f"equipment type  =  {equipment_type}")
        correct_values = equipment_type_mapping.get(equipment_type)
        
        if correct_values is None:
            return []

        # If the equipment type is not recognized, return an error
        

        incorrect_values = []
        value = None
        for limit in limits:
            
            level = limit["Level"]
            value = limit["Value"]
            print(f"..{limit} , {value}..")
            if level not in correct_values or value not in correct_values[level]:
                # Add the level and value to the list of incorrect values
                incorrect_values.append((level, value))
                print(f"not correct valyue: {value}, or limit {limit}")
        for level in correct_values:
            if level not in [limit["Level"] for limit in limits]:
                # Add the missing level to the list of incorrect values
                incorrect_values.append((level, "Missing Level"))
                print(f"missing level {level}")
        return incorrect_values

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
                
            with open('C:\\Users\\ashbyb\\Documents\\Alarm_Script\\alarmsFilter_20240612_104713\\fetched_sensors.json', 'r') as f:
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
                            3: "CO2%",
                            12: "Door"
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
                            'ReadingInterval': sensor.get('LastDataLogging', {}).get('ReadingInterval', 'null') if sensor.get('LastDataLogging') is not None else 'null',
                            'PhysicalParameter': type_mapping.get(sensor.get('PhysicalParameter', 'null')),
                            'DataLoggerName': sensor.get('Connection', {}).get('DataLogger', {}).get('Name', 'null') if sensor.get('Connection') is not None else 'null',
                            'InventoryCode': sensor.get('Connection', {}).get('DataLogger', {}).get('InventoryCode', 'null') if sensor.get('Connection') is not None else 'null',
                            'Calibration': sensor.get('Calibration', {}).get('CertificateDate', 'null') if sensor.get('Calibration') is not None else 'null',
                            'HistoricalData': historical_data
                    
                        }
                
                    
                        row['sensors'].append(new_sensor)
                    
            return rows
        
        except Exception as e:
            print(f"error {e}")
            return none

    def combineEquipSensors_Limits(data, token):
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
                
            with open('C:\\Users\\ashbyb\\Documents\\Alarm_Script\\alarmsFilter_20240510_101451\\fetched_sensors.json', 'r') as f:
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
                            3: "CO2%",
                            12: "Door"
                        }
                        
                        print(f"EQUIPMENTNAME:  {row['Name']}")
                        print(f"SensorEqName: {sensor['Equipment'].get('Name')}")
                        print(f"Sensor Type Map Physical P-- {type_mapping.get(sensor.get('PhysicalParameter'))}")
                        
                        incorrect_limits = []
                        
                        if sensor.get('PhysicalParameter') != 12:
                            Limits = sensor.get('LastDataLogging', {}).get('Limits', [])
                        
                            incorrect_limits = check_limits(Limits, sensor['Equipment'].get('Type'),type_mapping.get(sensor.get('PhysicalParameter')))
                        
                        #new_sensor = {key: (sensor.get(key) if sensor.get(key) is not None else 'null') for key in ['Id', 'Name', 'ProbeSerialNumber', 'Number', 'Type', 'PhysicalParameter', 'Inventory Code']}
                        new_sensor = {
                            'Id': sensor.get('Id', 'null'),
                            'ProbeSerialNumber': sensor.get('ProbeSerialNumber', 'null'),
                            #'Number': sensor.get('Number', 'null'),
                            #'Type': sensor.get('Type', 'null'),
                            'PhysicalParameter': type_mapping.get(sensor.get('PhysicalParameter', 'null')),
                            #'DataLoggerName': sensor.get('Connection', {}).get('DataLogger', {}).get('Name', 'null') if sensor.get('Connection') is not None else 'null',
                            'IncorrectLimits': incorrect_limits
                        }
                        #print(f"appending sensor, incorrect limits = {incorrect_limits}")
                    
                        row['sensors'].append(new_sensor)
                    
            return rows
        
        except Exception as e:
            print(f"error {e}")
            return None
    
    #combinedESRet = combineEquipSensors_Limits(data, token)    

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
    
    #def fetch_prev_equip_names(data, token):
        eq_n_d = []
        


        return  eq_n_d
    

        from fetch_all_data import fetch_audit_equipment
        from config import BASE_URL, CONTEXT_AUDIT

        # Initialize the results list if it's not provided
        if results is None:
            results = []

        # Fetch the audit trail for the equipment
        audit_trail = fetch_audit_equipment(BASE_URL, token, CONTEXT_AUDIT, equipment_name)

        # Loop through the audit trail
        for audit in audit_trail:
            # Check if the audit is about a name change
            for change in audit.get('changes', []):
                if change.get('name') == 'Name':
                    # Extract the old and new values
                    old_equipment_name = change.get('oldValue', [None])[0]
                    new_value = change.get('newValue', [None])[0]

                    # Add the result to the list
                    results.append({
                        'equipment_id': equipment_name,
                        'old_name': old_equipment_name,
                        'new_name': new_value,
                        'date': audit.get('date')
                    })

                    # If an old value was found, fetch the audit trail for the old name
                    if old_equipment_name is not None:
                        fetch_and_process_audit_trail(equipment_name, old_equipment_name, token, results)

        return results

    #for searching previous equipment names
    def equipment_names(data, token):
        rows = []
        for sublist in data:
            for item in sublist:
                # Prepare a row as a dictionary
                print(f"Searching...Equipment: {item['name']}")
                equipment_names = fetch_and_process_audit_trail(item['name'], token)

                
                for equipment in equipment_names:
                    row = {
                        'Name': item['name'],
                        'AuditTrail_SearchName': equipment['equipment_id'],
                        'OldName': equipment['old_name'],
                        'NewName': equipment['new_name'],
                        'PreviousDate': equipment['previous_date'],
                        'Date': equipment['date']
                    }

                    # Append the row to the list
                    rows.append(row)
        return rows
    #p = "C:\\Users\\ashbyb\\Documents\\Oceaview\\"
    #master_file = p+ "master_file.xlsx"
    #tester_file= p + "tester_file.xlsx"
    #sap_file = p + "sap_file.xlsx"
    #comparedFiles = compare_files(master_file, tester_file, sap_file)
    #eq_names = equipment_names(data, token)
    final_data = []
    final_data = combineEquipSensors(data, token)
    


    return final_data
