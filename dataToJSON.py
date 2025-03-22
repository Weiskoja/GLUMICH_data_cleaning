import csv

def read_csv_to_dict(filename, null_values=("", "NULL", "null", "NaN", "nan")):
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

        
def process_indicator_field(data_dict, key, value, list_of_keys, category_name):
    """
    Process fields that act as indicators (x or 1) and group them into a category list.
    
    :param data_dict: Dictionary to update
    :param key: Field name
    :param value: Value to process
    :param category_name: Name of the category list to add this key to if it's an indicator
    :return: Updated dictionary
    """
    try:
        newvalue = int(value)
    except:
        newvalue = value

    if key in list_of_keys:
        if (isinstance(newvalue, str) and newvalue.lower() == 'x') or newvalue == 1:
            try:
                data_dict[category_name].append(key)
            except KeyError:
                data_dict[category_name] = [key]
            return True
    return False



def process_slash_separated_field(data_dict, key, value):
    """
    Process fields that contain slash-separated values.
    
    :param data_dict: Dictionary to update
    :param key: Field name
    :param value: Value to process
    :return: Updated dictionary
    """
    if value is None:
        return
    newData = value.split("/")
    cleanedData = [x.strip() for x in newData]
    data_dict[key] = cleanedData


def clean_thing(thing):
    """
    Cleans the key by stripping whitespace and converting to lowercase.
    
    :param"
    """
    try:
        return thing.strip()
    except:
        return None
    


def main():


    data = read_csv_to_dict("data-wrangling/working/FishCleanTest.csv")
    cleaned_data = []
    for row in data:
        new_dict = {}
        new_dict['category'] = 'fish'
        for key, value in row.items():
            cleanValue = clean_thing(value)
            cleanKey = clean_thing(key)
            if "\ufeff" in cleanKey:
                cleanKey = cleanKey.replace("\ufeff", "")
            added = False

            if cleanKey == "CommonName":
                process_slash_separated_field(new_dict, cleanKey, cleanValue)
                cleaned_data.append(new_dict)
                added = True
            if cleanKey == "GroupFine":
                process_slash_separated_field(new_dict, cleanKey, cleanValue)
                cleaned_data.append(new_dict)
                added = True
            if cleanKey == "AlternateNames":
                process_slash_separated_field(new_dict, cleanKey, cleanValue)
                added = True
            lakes = ["Erie", "Ontario", "Michigan", "Huron", "Superior"]
            if cleanKey in lakes:
                added = True
            if process_indicator_field(new_dict, cleanKey, cleanValue, lakes, 'lakes'):
                added = True
            if cleanKey == "St. Mary's River":
                pass
            rivers = ["St. Mary's River", "Huron Erie Corridor", "Niagara River"]
            if cleanKey in rivers:
                added = True
            if process_indicator_field(new_dict, cleanKey, cleanValue, rivers, 'rivers'):
                added = True
            domain = ["Benthic", "Littoral", "Limnetic", "Tribs/Wetlands", "Aerial/ Terrestrial"]
            if cleanKey in domain:
                added = True
            if process_indicator_field(new_dict, cleanKey, cleanValue, domain, 'domain'):
                added = True

            if added == False:
                if cleanValue == "X" or cleanValue == 1:
                    new_dict[cleanKey] = True
                else:
                    new_dict[cleanKey] = cleanValue
    write_dict_to_json(cleaned_data, "data-wrangling/done/Fish.json")
    print("Done")
if __name__ == "__main__":
    main()