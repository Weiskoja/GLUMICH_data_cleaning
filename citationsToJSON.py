import csv

def read_csv_to_dict(filename, null_values=("", "NULL", "null", "NaN", "nan", "NA", "na", "N/A", "n/a", "None", "none", " ", "\t")):
    """
    Reads a CSV file and converts it to a list of dictionaries.
    Handles null values (including blank and space-only cells) by converting them to None.

    Parameters:
        filename (str): Path to the CSV file.
        null_values (tuple): Strings to interpret as null (converted to None) after stripping.

    Returns:
        list[dict]: A list of dictionaries representing each row.
    """
    data = []
    with open(filename, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            cleaned_row = {}
            for key, value in row.items():
                val_str = str(value).strip() if value is not None else ""
                cleaned_row[key] = None if val_str in null_values else value
            data.append(cleaned_row)
    return data

def write_dict_to_json(data, json_file_path):
    """
    Writes a dictionary to a JSON file.
    
    :param data: Dictionary to write to the JSON file.
    :param json_file_path: Path to the output JSON file.
    """
    import json
    
    with open(json_file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

def clean_thing(thing):
    """
    Cleans the key by stripping whitespace and converting to lowercase.
    
    :param"
    """
    import re
    try:
        # Decode escaped Unicode sequences (e.g., "\u00f6") into actual characters
        decoded_thing = thing.encode('utf-8').decode('unicode_escape')
        
        # If you want to drop non-ASCII characters, uncomment this:
        decoded_thing = re.sub(r'[^\x00-\x7F]+', '', decoded_thing)
        decoded_thing = decoded_thing.replace('\n', '')
        return decoded_thing.strip()
    except:
        return thing

def main():
    # Read the CSV file and convert it to a list of dictionaries
    data = read_csv_to_dict('data-wrangling/working/Citations.csv')

    for row in data:
        # List comprehension to clean keys and values 
        cleaned_row = {clean_thing(k): clean_thing(v) for k, v in row.items()}
        row.clear()
        row.update(cleaned_row)


    # Write the list of dictionaries to a JSON file
    write_dict_to_json(data, 'data-wrangling/done/Citations.json')

    print("Data has been converted to JSON format.")

if __name__ == "__main__":
    main()