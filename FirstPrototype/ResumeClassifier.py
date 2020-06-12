import pandas as pd
import re 
import math
from sklearn.model_selection import train_test_split   
from sklearn.ensemble import RandomForestClassifier

def cleanData(df):
    df['person_skills'] = df['person_skills'].str.replace('[^A-Za-z0-9]+', ' ').str.lower()
    df['person_experience'] = df['person_experience'].str.replace('[^A-Za-z0-9]+', ' ').str.lower()
    df['person_education'] = df['person_education'].str.replace('[^A-Za-z0-9]+', ' ').str.lower()
    df['person_qualities'] = df['person_qualities'].str.replace('[^A-Za-z0-9]+', ' ').str.lower()

    for index,row in df.iterrows():
        for column in df[['person_skills', 'person_experience', 'person_qualities']]:
            no_digits = []
            # Iterate through the string, adding non-numbers to the no_digits list
            if(type(row[column]) == str):
                for i in row[column]:
                    if not i.isdigit():
                        no_digits.append(i)
            # Now join all elements of the list with '', 
            # which puts all of the characters together.
                result = ''.join(no_digits)
                df.loc[index,column] = result

    for index,row in df.iterrows():
        no_digits = []
        for i in row['person_education']:
            if not i.isdigit():
                        no_digits.append(i)
            # Now join all elements of the list with '', 
            # which puts all of the characters together.
            result = ''.join(no_digits)
            df.loc[index,'person_education'] = result

    return(df)

def findWord(s, w):
    return (' ' + w + ' ') in (' ' + s + ' ')

def findFemaleConfirmed(df):

    male_words=["men","mens","boy","boys"]
    female_words=["women", "womens", "girl", "girls", "woman", "womans"]

    for index,row in df.iterrows():  
        for column in df[['person_qualities', 'person_experience', 'person_education']]:
            print(column)
            if(pd.notna(row[column])):
                for item in female_words:
                    female_match = findWord(row[column],item)
                    if(female_match != False):
                        df.loc[index,'femaleConfirmed'] = 1
                for item in male_words:
                    male_match = findWord(row[column],item)
                    if(male_match != False):
                        df.loc[index,'maleConfirmed'] = 1
    return df           

def RandomForest(X_person,wantedColumns):
    df = pd.read_csv('resumesCleaned.csv', delimiter= ',')
    df.columns = ['person_name', 'person_gender', 'person_skills', 'person_experience', 'person_education', 'person_qualities', 'femaleConfirmed', 'maleConfirmed']
    df = pd.concat([df,df.person_qualities.str.get_dummies(' ')],axis=1)
    df = pd.concat([df,df.person_skills.str.get_dummies(' ')],axis=1)

    y = df['person_gender'] #We need to take out the gender as our Y-variable
    X = df[wantedColumns] 
    X = X.groupby(X.columns, axis=1).sum()
    X 

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1)
    train_data_features=X_train
    forest = RandomForestClassifier(n_estimators = 100, random_state=1) 
    forest = forest.fit(train_data_features, y_train)
    result = forest.predict(X_person)
    return result

class ResumeeClassifier:
    def __init__(self):
        self

    def classify(self, name, skills, experience, education, qualities):
        if(name is not None and skills is not None and experience is not None and education is not None and qualities is not None):
            data = {'person_name': [name], 'person_skills':[skills], 'person_experience':[experience], 'person_education': [education], 'person_qualities': [qualities]}
            personaldf = pd.DataFrame(data=data)
            personaldf = cleanData(personaldf)

            personaldf = pd.concat([personaldf,personaldf.person_qualities.str.get_dummies(' ')],axis=1)
            personaldf = pd.concat([personaldf,personaldf.person_skills.str.get_dummies(' ')],axis=1)

            newdf = findFemaleConfirmed(personaldf)
            wantedColumns = ['femaleConfirmed','people', 'independent', 'player', 'multi', 'information', 'learn', 'drive', 'experience', 'accounting', 'quality', 'efficient', 'well', 'produce', 'provide', 'challenging', 'learning', 'she', 'hardworking', 'her', 'excellence', 'complex', 'mature', 'organized', 'netball', 'interpersonal', 'time', 'basketball', 'soccer', 'football', 'leadership', 'driven', 'business', 'badminton', 'equity', 'analytical', 'his', 'investment', 'proven' , 'keen', 'leader', 'individual', 'sports', 'independently', 'he']
            for item in wantedColumns:
                if item not in newdf:
                    newdf[item] = 0
            
            X_person = newdf[wantedColumns]
            result = RandomForest(X_person, wantedColumns)
            print(result)
            if(result==1):
                return 'male'
            if(result==0):
                return 'female'
        else:
            return None
