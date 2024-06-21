


def excel_gen(payload):
    import pandas as pd

    # Prepare an empty list to store the rows
    excel_rows = []

    for equipment in payload:
        # Prepare a row as a dictionary
        for sensor in equipment['sensors']:
            row = {
                'Name': equipment['Name'],
                'Inventory Code': equipment['Inventory Code'],
                'Type': equipment['Type'],
                'Topology Name': equipment['Topology Name'],
                'Calibration': sensor['Calibration'],
                'HistoricalData': sensor['HistoricalData']
            }

            # Add the historical data to the row
            if 'HistoricalData' in sensor:
                for i, item in enumerate(sensor['HistoricalData']):
                    row[f"Item {i+1} ID"] = item['id']
                    row[f"Item {i+1} Value"] = item['value']

            # Append the row to the list
            excel_rows.append(row)

    # Create a DataFrame from the list of rows
    df = pd.DataFrame(excel_rows)

    # Write the DataFrame to an Excel file
    df.to_excel('C:\\Users\\ashbyb\\Downloads\\py_eq_proc_out3.xlsx', index=False)


def excel_gen_files(comparedFiles):
    import pandas as pd

    # Unpack the dictionaries from comparedFiles
    matching_status, non_matching_rows_tester, non_matching_rows_sap = comparedFiles

    # Create a DataFrame from the matching_status list of dictionaries
    df_matching_status = pd.DataFrame(matching_status)

    # Write the DataFrame to an Excel file
    with pd.ExcelWriter('C:\\Users\\ashbyb\\Downloads\\py_compare_files.xlsx') as writer:
        df_matching_status.to_excel(writer, sheet_name='Matching Status', index=False)
        non_matching_rows_sap.to_excel(writer, sheet_name='Matching SAP SN', index=False)

def print_to_json(payload):
    import json
    
    
    
    #filtered_data_sensW_Hist = [item for item in data['sensors'] if item['HistoricalData']]
    filtered_data_sensW_Hist = [item for item in payload if 'HistoricalData' in item['sensors']]
    
    filtered_json_sensW_Hist = json.dumps(filtered_data_sensW_Hist, indent=4)
    
    save_location = 'C:\\Users\\ashbyb\\Downloads\\py_historical_data_608_2.json'
    
    with open(save_location, 'w') as json_file:
        json.dump(filtered_json_sensW_Hist, json_file, indent=4)
    
    return save_location

        
def generate_excel_from_limits(data, file_path):
    import pandas as pd
    import json

    # Flatten the data into a list of dictionaries
    rows = []
    #data = json.loads(data)
    for equipment in data:
        for sensor in equipment['sensors']:
            for level, value in sensor['IncorrectLimits']:
                # Prepare a row as a dictionary
                row = {
                    'Equipment Name': equipment['Name'],
                    'Equipment Id': equipment['Id'],
                    'Equipment Inventory Code': equipment['Inventory Code'],
                    'Equipment Type': equipment['Type'],
                    'Equipment Topology Name': equipment['Topology Name'],
                    'Sensor Id': sensor['Id'],
                    'Sensor ProbeSerialNumber': sensor['ProbeSerialNumber'],
                    'Sensor Type': sensor['PhysicalParameter'],
                    'Incorrect Limit Level': level,
                    'Incorrect Limit Value': value,
                }
                # Append the row to the list
                rows.append(row)

    # Convert the list of dictionaries to a DataFrame
    df = pd.DataFrame(rows)

    # Write the DataFrame to an Excel file
    df.to_excel(file_path, index=False)       

def excel_gen_equipment_names(rows):
    import pandas as pd

    # Create a DataFrame from the list of rows
    df = pd.DataFrame(rows)

    # Write the DataFrame to an Excel file
    df.to_excel('C:\\Users\\ashbyb\\Downloads\\SHIP_prev_equipment_names_3.xlsx', index=False)