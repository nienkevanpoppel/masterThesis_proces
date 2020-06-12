import json
import re
import pandas as pd
from male_words import masculine_words
from female_words import feminine_words
from superlatives import superlative_words
from relationship import relationship_words
import os
import glob

class CalculateBias:
    def __init__(self):
        self

    def returnBias(self, text):
        if(text):
            file="/job_vacancies/{}".format(text)
            path=os.getcwd()+file
            with open(path, 'r') as vacancyFile: 
                data = vacancyFile.read()
                masculine_matches = []
                feminine_matches = []

                #masculine words list
                for item in masculine_words:
                    #this regex method is necessary as I want the full word the predefined words match on
                    # for example: if it finds 'domina', I want to use the full word (dominant) to search for a synonym
                    # to prevent the API from crashing
                    pattern = "\\w*" + item +"\\w*"
                    matchObj = re.search(pattern, data)
                    if(matchObj != None):
                        matchedWord = matchObj.group(0)
                        masculine_matches.append(matchedWord)
                    
                #superlative words list
                for item in superlative_words:
                    pattern = "\\w*" + item +"\\w*"
                    matchObj = re.search(pattern, data)
                    if(matchObj != None):
                        matchedWord = matchObj.group(0)
                        masculine_matches.append(matchedWord)
                
                for item in feminine_words:
                    pattern = "\\w*" + item +"\\w*"
                    matchObj = re.search(pattern, data)
                    if(matchObj != None):
                        matchedWord = matchObj.group(0)
                        feminine_matches.append(matchedWord)
                
                #relationship-related words list
                for item in relationship_words:
                    pattern = "\\w*" + item +"\\w*"
                    matchObj = re.search(pattern, data)
                    if(matchObj != None):
                        matchedWord = matchObj.group(0)
                        feminine_matches.append(matchedWord)

                classification= 'neutral'
                if (len(masculine_matches) > len(feminine_matches)):
                    classification = 'masculine-biased'
                elif (len(masculine_matches) < len(feminine_matches)):
                    classification = 'feminine-biased'
                #add data to dataframe
                return(classification)

        