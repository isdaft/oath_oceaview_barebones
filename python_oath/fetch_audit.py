

def fetch_and_process_audit_trail(equipment_name, token, results=None, counter=0):
    from fetch_all_data import fetch_audit_equipment
    from config import BASE_URL, CONTEXT_AUDIT
    from datetime import datetime
    counter += 1
    print(f"Entering recursion level {counter} for equipment {equipment_name}")
    # Initialize the results list if it's not provided
    if results is None:
        results = []

    # Fetch the audit trail for the equipment
    
    audit_trail = fetch_audit_equipment(BASE_URL, token, CONTEXT_AUDIT, equipment_name)
    

    # Loop through the audit trail
    # Loop through the audit trail
    for audit_list in audit_trail:
        # Check if the audit_list is a list
        if isinstance(audit_list, list):
            # Loop through the audit list
            #print(f"audit list count: {len(audit_list)}")
            for audit in audit_list:
                # Check if the audit is a dictionary
                if isinstance(audit, dict):
                    # If this audit's id is the same as the last one we processed, skip it
                    if any(result['audit_id'] == audit['id'] for result in results):
                        #  check if the total amount of changes = 1 , which is common when its usually the last name change, last page.
                        #  is there going to be any other case where this is true?
                        # audit['changes] len = 1
                        continue

                    # Check if the 'changes' key is in the audit and is a list
                    if 'changes' in audit and isinstance(audit['changes'], list):
                        # Loop through the changes
                        #
                        
                        previous_date = None 
                        
                        for change in audit['changes']:
                            # Check if the change is a dictionary
                            if isinstance(change, dict):
                                # Check if the 'name' key is in the change and is 'Name'
                                if change.get('name') == 'Name':
                                    # Extract the old and new values
                                    old_equipment_name = change.get('oldValue', [None])[0]
                                    new_value = change.get('newValue', [None])[0]
                                    date_str = audit.get('date')
                                    date_str = date_str[:-2] + 'Z'  # remove the last digit before 'Z'
                                    formatted_date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%fZ')
                                    # Add the result to the list
                                    print(f"adding {old_equipment_name} to RESULTS.")
                                    results.append({
                                        'equipment_id': equipment_name,
                                        'old_name': old_equipment_name,
                                        'new_name': new_value,
                                        'previous_date': previous_date,
                                        'date': formatted_date,
                                        'audit_id': audit['id']
                                    })
                                    print(f"Equipment {equipment_name} changed name from {old_equipment_name} to {new_value}")

                                    previous_date = formatted_date

                                    # If an old value was found, fetch the audit trail for the old name
                                    if old_equipment_name is not None:
                                        
                                        results_length_before = len(results)
                                        print(f"Searching for audit trail for {old_equipment_name}")
                                        equipment_name = old_equipment_name
                                        fetch_and_process_audit_trail(equipment_name, token, results=results, counter=counter)
                                        results_length_after = len(results)
                                        
                                        if results_length_before == results_length_after:
                                        # Check if there are any audits left in audit_list
                                            if any(audit['id'] not in [result['audit_id'] for result in results] for audit in audit_list):
                                                print(f"No new 'old values' found for {equipment_name}, but there are still audits left to process.")
                                            else:
                                                print(f"No new 'old values' found for {equipment_name}, and no audits left to process.")
                                                

    print(f"Exiting recursion level {counter} for equipment {equipment_name}")
    return results




