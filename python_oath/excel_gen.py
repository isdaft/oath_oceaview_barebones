
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
    
    data = json.loads(payload)
    
    filtered_data_sensW_Hist = [item for item in data['sensors'] if item['HistoricalData']]
    
    filtered_json_sensW_Hist = json.dumps(filtered_data_sensW_Hist, indent=4)
    
    with open('C:\\Users\\ashbyb\\Downloads\\py_hist_null2.json', 'w') as json_file:
        json.dump(payload, json_file, indent=4)
        
        
