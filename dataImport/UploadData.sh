#!/bin/bash
# filepath: /Users/ethansnyder/NOAA-GreatLakes/GLUMICH_data_cleaning/data-wrangling/done/temp.sh

# MongoDB connection string
MONGO_URI="mongodb://root:glumich@localhost:27017/glumich-db?authSource=admin"

# Counter for successful imports
IMPORT_COUNT=0

echo "Starting import of JSON files into MongoDB..."

# Import Wildlife files
echo "Importing Wildlife files..."
echo "-----------------------------------"
WILDLIFE_DIR="./Wildlife"
if [ -d "$WILDLIFE_DIR" ]; then
    for JSON_FILE in "$WILDLIFE_DIR"/*.json; do
        if [ -f "$JSON_FILE" ]; then
            FILENAME=$(basename "$JSON_FILE")
            echo "Importing $FILENAME into Wildlife collection..."
            
            # Run mongoimport command
            mongoimport --uri="$MONGO_URI" \
                --collection "Wildlife" \
                --file="$JSON_FILE" \
                --jsonArray
            
            # Check if import was successful
            if [ $? -eq 0 ]; then
                echo "✅ Successfully imported $FILENAME"
                ((IMPORT_COUNT++))
            else
                echo "❌ Failed to import $FILENAME"
            fi
            echo "-----------------------------------"
        fi
    done
else
    echo "❌ Wildlife directory not found at $WILDLIFE_DIR"
fi

# Import Citations file
echo "Importing Citations file..."
echo "-----------------------------------"
CITATIONS_FILE="./Citations.json"
if [ -f "$CITATIONS_FILE" ]; then
    echo "Importing $(basename "$CITATIONS_FILE") into Citations collection..."
    
    # Run mongoimport command
    mongoimport --uri="$MONGO_URI" \
        --collection "Citations" \
        --file="$CITATIONS_FILE" \
        --jsonArray
    
    # Check if import was successful
    if [ $? -eq 0 ]; then
        echo "✅ Successfully imported $(basename "$CITATIONS_FILE")"
        ((IMPORT_COUNT++))
    else
        echo "❌ Failed to import $(basename "$CITATIONS_FILE")"
    fi
    echo "-----------------------------------"
else
    echo "❌ Citations file not found at $CITATIONS_FILE"
fi

echo "Import complete! Successfully imported $IMPORT_COUNT JSON files."