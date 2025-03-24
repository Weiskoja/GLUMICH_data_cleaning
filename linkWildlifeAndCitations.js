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
  const data = readJsonFile(filePath);  // Assumes this is a function you have
  if (!data) return;

  data.forEach((item) => {
    if (item["Ref_location"] && typeof item["Ref_location"] === "object") {
      const newRefArray = [];

      // Convert each key/value in the old Ref_location object
      // into an array element with { type, refId, locations }.
      Object.entries(item["Ref_location"]).forEach(([key, rawLocations]) => {
        // Ensure rawLocations is an array so we can iterate
        const locationsArray = Array.isArray(rawLocations)
          ? rawLocations
          : [rawLocations];

        // Split any slash-delimited strings into multiple locations
        const processedLocations = [];
        locationsArray.forEach((loc) => {
          if (typeof loc === "string" && loc.includes("/")) {
            // Split on "/", trim whitespace
            const splitLocs = loc.split("/").map((str) => str.trim());
            processedLocations.push(...splitLocs);
          } else {
            // Push the original item if no slash
            processedLocations.push(loc);
          }
        });

        // Decide if this reference points to the database or is plain text
        if (citationMap[key]) {
          newRefArray.push({
            type: "database",
            refId: citationMap[key], 
            locations: processedLocations,
          });
        } else {
          newRefArray.push({
            type: "plaintext",
            refId: key,
            locations: processedLocations,
          });
        }
      });

      // Replace the original object with the new array structure
      item["Ref_location"] = newRefArray;
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