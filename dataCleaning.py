import pandas as pd
import pathlib

#directory stuff to make organization easier

workingDirectory = pathlib.Path.cwd()

parentDir = workingDirectory.parent

# print(workingDirectory, parentDir)
print("Working Directory: ", workingDirectory)
print("Parent Directory: ", parentDir)
dataDirectory = f'{parentDir}/data/'

file = pd.ExcelFile(f"{dataDirectory}GLWL_wAlgae_oneRowHeader_working_17Oct2022.xlsx")

dataWriteDir_InProcess= f'{workingDirectory}/data-wrangling/working'

dataWriteDir_Wrangled= f'{workingDirectory}/data-wrangling/done'

progress_path = pathlib.Path(dataWriteDir_InProcess).mkdir(parents=True, exist_ok=True)
finish_path = pathlib.Path(dataWriteDir_Wrangled).mkdir(parents=True, exist_ok=True)


def glumichDataPrecleanRead(file, dataDirectory):
    """
    take in the raw file and create dataframe for each sheet.
    Saved as csv in a seperate directory, for wrangling later
    """
    animal_dataframes = {}

    for frame in file.sheet_names[2:]:
        animal_dataframes[frame] = pd.read_excel(file,frame)
    
    for frame in animal_dataframes.items():
        frame[1].to_csv(f'{dataDirectory}/{frame[0]}.csv',index=False)

    return animal_dataframes


def cleanCitationFrame():
    """TODO: CITATIONS CLEANING"""

def cleanAnimals(dataDirectory, fileName):
    """TODO: write to import frame for each, and then add to 'master' frame once done"""
    frame = pd.read_csv(f'{dataDirectory}/{fileName}.csv')
    frame['Category'] = fileName.lower()
    #print(frame.head())


def main():
    frames = glumichDataPrecleanRead(file, dataWriteDir_InProcess)
    #print(frames.keys())
    #for animal in frames.keys():
        #cleanAnimals(dataWriteDir_InProcess, animal)


if __name__ == "__main__":
    main()