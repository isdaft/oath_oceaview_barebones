
from datetime import datetime, timedelta
import json
import pandas as pd
import xlsxwriter
import pytz

def convert_utc_to_est(utc_datetime):
    utc_datetime = utc_datetime.replace(tzinfo=pytz.UTC)
    est_datetime = utc_datetime.astimezone(pytz.timezone('US/Eastern'))
    return est_datetime

def filter_nulls_gaps(payload_file):
    
    with open(payload_file, 'r') as f:
        data = json.load(f)
        # Create an empty DataFrame to store the data

    null_columns = ['Id', 'ProbeSerialNumber', 'DataLoggerName', 'NullInstances','ReadingInterval', 'FirstDate', 'LastDate']
    largegap_columns = ['DataLoggerName', 'ProbeSerialNumber', 'PhysicalParameter', 'prev_date', 'date', 'delta']
    excel_rows_null = []
    excel_rows_large_gap =[]
    for equipment in data:
        for sensor in equipment['sensors']:   
            
            null_count = 0
            null_duration = timedelta()
            first_date = None
            last_date = None
            prev_date = None
            null_instances = []
            large_gap_instances = [] 
            
            if sensor['PhysicalParameter'] is not None:
                
                if 'HistoricalData' in sensor and not sensor['HistoricalData']:
                    #
                    # If the sensor has no historical data, add a row with null values
                    excel_rows_null.append({'Id': sensor['Id'], 'ProbeSerialNumber': sensor['ProbeSerialNumber'], 'DataLoggerName': sensor['DataLoggerName'], 'NullInstances': 'null', 'FirstDate': 'null', 'LastDate': 'null'})
                else:
                    
                    if sensor['ReadingInterval'] is not None:
                        
                        readingInterval = sensor['ReadingInterval'] // 60
                   

                        for reading in sensor['HistoricalData']:

                            date_string = reading['date']
                            if len(date_string) == 28:  # Check if date string has extra precision
                                date_string = date_string[:-2] + 'Z'  # Remove the last digit before 'Z'
                            date = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%fZ")
                            date = convert_utc_to_est(date)
                            date = date.replace(tzinfo=None)
            
                            if first_date is None or date < first_date:
                                first_date = date
                                first_date = first_date.replace(tzinfo=None)
                            if last_date is None or date > last_date:
                                last_date = date
                                last_date = last_date.replace(tzinfo=None)
                            if reading['value'] is None:
                                if prev_date is not None and (prev_date - date <= timedelta(minutes=readingInterval)):
                                #if prev_date is not None and (prev_date - date <= timedelta(minutes=5)) or (prev_date - date <= timedelta(minutes=10)):

                                    null_count += 1
                                    null_duration += timedelta(minutes=(prev_date - date).total_seconds() / 60)
                            
                                else:
                                    if null_count > 0:
                                        null_instances.append(null_duration)
                                    
                                    null_count = 1
                                    null_duration = timedelta()
                            else:
                           
                                if null_count > 0:
                                    null_instances.append(null_duration)
                                #read value > 0
                                if prev_date is not None:
                                    #
                                    print(f"[{sensor['DataLoggerName']}][{sensor['ProbeSerialNumber']}][{sensor['PhysicalParameter']}] prev_date: {prev_date}, date: {date}, delta?: {prev_date - date}")    
                                    if (prev_date - date > timedelta(minutes=readingInterval)):
                                        print(f"[{sensor['DataLoggerName']}][{sensor['ProbeSerialNumber']}][{sensor['PhysicalParameter']}] prev_date: {prev_date}, date: {date}, delta?: {prev_date - date}")
                                        #print("greater than 10 minutes"
                                        delta = str(prev_date - date)
                                        #large_gap_instances.append((prev_date, date))
                                        #large_gap_instances.append({'DataLoggerName': sensor['DataLoggerName'], 'ProbeSerialNumber': sensor['ProbeSerialNumber'], 'PhysicalParameter': sensor['PhysicalParameter'], 'prev_date': prev_date, 'date': date, 'delta': delta})
                                        #excel_rows.append({'Id': sensor['Id'], 'ProbeSerialNumber': sensor['ProbeSerialNumber'], 'DataLoggerName': sensor['DataLoggerName'], 'NullInstances': null_instances_str,'LargeGapInstances': large_gap_instances_str, 'FirstDate': first_date, 'LastDate': last_date})
                                        excel_rows_large_gap.append({
                                            'DataLoggerName': sensor['DataLoggerName'], 
                                            'ProbeSerialNumber': sensor['ProbeSerialNumber'], 
                                            'PhysicalParameter': sensor['PhysicalParameter'], 
                                            'prev_date': prev_date, 
                                            'date': date, 
                                            'delta': delta
                                        })
                                        null_count = 0
                            
                                null_count = 0
                                null_duration = timedelta()
                
                
                            prev_date = date
                        if null_count > 0:
                            null_instances.append(null_duration)
            
                    
                        # Convert the durations to a human-readable format
                        null_instances_str = [str(int(td.total_seconds() // 3600)) + " hours " + str(int((td.total_seconds() % 3600) // 60)) + " minutes " + str(int(td.total_seconds() % 60)) + " seconds" for td in null_instances]
                            # Add the data to the DataFrame
                        excel_rows_null.append({'Id': sensor['Id'], 'ProbeSerialNumber': sensor['ProbeSerialNumber'], 'DataLoggerName': sensor['DataLoggerName'],'ReadingInterval': sensor['ReadingInterval'], 'NullInstances': null_instances_str, 'FirstDate': first_date, 'LastDate': last_date})
                        #excel_rows_large_gap.append({'Id': sensor['Id'], 'ProbeSerialNumber': sensor['ProbeSerialNumber'], 'DataLoggerName': sensor['DataLoggerName'], 'LargeGapInstances': large_gap_instances})
                        #.append({'Id': sensor['Id'], 'ProbeSerialNumber': sensor['ProbeSerialNumber'], 'DataLoggerName': sensor['DataLoggerName'], 'NullInstances': null_instances_str, 'FirstDate': first_date, 'LastDate': last_date})
                   
                        print(f"Id: {sensor['Id']}, ProbeSerialNumber: {sensor['ProbeSerialNumber']}, DataLoggerName: {sensor['DataLoggerName']}, PhysicalParam: {sensor['PhysicalParameter']}, NullInstances: {null_instances_str}, FirstDate: {first_date}, LastDate: {last_date}")
    

    
                    
    writer = pd.ExcelWriter('C:\\Users\\ashbyb\\Downloads\\75b_junesafepoint12_gaps_nulls.xlsx', engine='xlsxwriter')
    pd.DataFrame(excel_rows_null, columns=null_columns).to_excel(writer, sheet_name='Null Instances', index=False)
    pd.DataFrame(excel_rows_large_gap, columns=largegap_columns).to_excel(writer, sheet_name='Large Gap Instances', index=False)

                   #Close the Pandas Excel writer and output the Excel file.
    writer.close()   


