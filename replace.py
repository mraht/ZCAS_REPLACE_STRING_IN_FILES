# Version: 24.11.2023-001

import logging
import os
import re

def info(msg):
    logging.info(msg)
    print(msg)

def error(msg):
    logging.error(msg)
    print(msg)

def replace(m, oldNamespace, newNamespace):
    newStr = re.sub(oldNamespace, newNamespace, m.group(), flags = re.IGNORECASE)
    return newStr.lower() if m.group().islower() else newStr.upper()

def inputPathToFiles():
    pathToFiles = ''
    while pathToFiles == '':
        pathToFiles = input("Path to file(s): ")
        if pathToFiles == 'quit' or pathToFiles[0] == 'exit':
            exit()
        elif not os.path.isdir(pathToFiles):
            pathToFiles = ''
            print("Entered folder doesn't exist.")
    return pathToFiles

def inputSearchPattern():
    searchPattern = ''
    while searchPattern == '':
        searchPattern = input("Search pattern: ").lower()
        if searchPattern == 'quit' or searchPattern == 'exit':
            exit()
    return searchPattern

def inputReplacement():
    replacement = ''
    while replacement == '':
        replacement = input("Replacement string: ").lower()
        if replacement == 'quit' or replacement == 'exit':
            exit()
    return replacement

def buildExcludeFiles():
    excludedObjects     = None
    if os.path.exists('exclude.csv'):
        with open('exclude.csv', 'r', encoding="utf8") as f:
            excludedObjects = f.read().split(';')
    return excludedObjects

def execute():
    logging.basicConfig(level=logging.DEBUG, filename="log.txt", filemode="a+",
                        format="%(asctime)-15s %(levelname)-8s %(message)s")

    info('************************************* ZCAS_RENAME_DEV_OBJECTS **************************************')
    print(f"Enter 'quit' or 'STRG+C' to quit\n")

    pathToFiles    = inputPathToFiles()
    searchPattern  = inputSearchPattern()
    replacement    = inputReplacement()

    excludedObjects = buildExcludeFiles()

    info('****************************************************************************************************')

    for filenames in os.walk(pathToFiles):
        for index, file in enumerate(filenames[2]):
            print('%-50s' % file + f': {round((index / len(filenames[2])) * 100, 2)}%',"\r", end=' ')
            filePath = os.path.join(pathToFiles, file)

            exclude = False
            for excludedObject in excludedObjects:
                if excludedObject in file:
                    exclude = True
                    break
            if exclude:
                info(f'Excluded {file} from processing')
                continue

            with open (filePath, 'r+', encoding="utf8") as f:
                try:
                    content = f.read()
                    newContent = content
                        
                    tmpContent = re.sub(f'(?i){searchPattern}', lambda m: replace(m, searchPattern, replacement), newContent, flags = re.MULTILINE)
                    if tmpContent != newContent:
                        info(f'>> Occurrences of "{searchPattern}" replaced by "{replacement}" in {file}')
                    newContent = tmpContent
                
                    if content != newContent:
                        f.seek(0)
                        f.write(newContent)
                        f.truncate()

                except BaseException:
                    error(f'Error: Renaming objects in file {file} failed.')

    info(f'Replacing \'{searchPattern}\'  =>  \'{replacement}\' was successful.\n')
    return True

runApp = True
while runApp == True:
    runApp = execute()
