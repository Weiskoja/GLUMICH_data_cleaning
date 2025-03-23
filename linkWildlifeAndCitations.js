import { MongoClient } from 'mongodb';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { dirname } from 'path';

// Get current directory path in ESM
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// MongoDB connection configuration
const mongoURL = 'mongodb://root:glumich@localhost:27017/glumich-db?authSource=admin';
const dbName = 'glumich-db';
const citationsCollection = 'Citations';

// Paths for wildlife data files
const wildlifeDataPath = 'data-wrangling/done/';
const wildlifeFiles = ['Fish.json', 'Algae.json', 'Benthos.json', 'Herps.json', 'Zooplankton.json'];

// Function to read JSON file
const readJsonFile = (filePath) => {
    try {
        const data = fs.readFileSync(filePath, 'utf8');
        return JSON.parse(data);
    } catch (error) {
        console.error(`Error reading ${filePath}:`, error);
        return null;
    }
};

// Function to write JSON file
const writeJsonFile = (filePath, data) => {
    try {
        fs.writeFileSync(filePath, JSON.stringify(data, null, 2), 'utf8');
        console.log(`Successfully updated ${filePath}`);
    } catch (error) {
        console.error(`Error writing ${filePath}:`, error);
    }
};

const processFile = (filePath, citationMap) => {
    const data = readJsonFile(filePath);  // Fixed function name from readJson to readJsonFile
    if (!data) return;

    data.forEach((item) => {
        // Check if Ref_location exists and is an object
        if (item["Ref_location"] && typeof item["Ref_location"] === 'object') {
            const updatedRefs = {};
            // Iterate through each location and its reference
            Object.entries(item["Ref_location"]).forEach(([reference, location]) => {
                // If reference exists and has a citation ID mapping, use it
                // Otherwise keep the original reference
                if (reference && citationMap[reference]) {
                    updatedRefs[citationMap[reference]] = location;
                } else {
                    updatedRefs[reference] = location;
                }
            });
            // Replace the original Ref_location with the updated references
            item["Ref_location"] = updatedRefs;
        }
    });
    return data;
};

// Wrap the main execution in an async function
const main = async () => {
    let client;
    try {
        // Connect to MongoDB
        client = new MongoClient(mongoURL);
        await client.connect();
        console.log('Connected to MongoDB');

        const db = client.db(dbName);
        const citations = await db.collection(citationsCollection).find({}).toArray();
        console.log(`Retrieved ${citations.length} citations from MongoDB`);

        const citationMap = {};
        citations.forEach(citation => {
            citationMap[citation["In-text citations"]] = citation._id;
        });

        wildlifeFiles.forEach(file => {
            const filePath = path.join(wildlifeDataPath, file);
            const data = processFile(filePath, citationMap);
            if (data) {
                writeJsonFile(filePath, data);
            }
        });
    } catch (error) {
        console.error('Error:', error);
    } finally {
        if (client) await client.close();
    }
};

// Execute the main function
main();