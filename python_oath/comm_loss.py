

def fetch_and_process_comm_loss( token):
    from fetch_all_data import fetch_comm_loss
    from config import BASE_URL, CONTEXT_CM
    from datetime import datetime
    # Initialize the results list if it's not provided
    
    # Fetch the audit trail for the equipment
    
    results = fetch_comm_loss(BASE_URL, token, CONTEXT_CM)
    print(f"{results}")
    for result in results:
        if isinstance(result, dict):
            # Check if the 'device' key is in the result and is a dictionary
            if 'device' in result and isinstance(result['device'], dict):
                # Check if the 'name' key is in the device
                if 'name' in result['device']:
                    print(f"Comm Loss: {result['device']['name']}")
    
    return results




