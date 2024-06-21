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