import os
import pandas as pd
import datetime
import markdown

from settings import *

def getDateNow():
    return datetime.datetime.now().strftime("%Y%m%d%H%M%S")

def getCsvFiles():
    dict_df = {}
    for file in os.listdir(PATH_CSV):
        key = file.split('.')[0]
        dict_df[key] = pd.read_csv(f'{PATH_CSV}/{file}', nrows=5)
    return dict_df


def getMetaData():
    df_metaData = pd.read_csv('data/feature_definitions.csv')
    return df_metaData


def genDetail():

    dict_df = getCsvFiles()

    df_metaData = getMetaData()

    text = []
    for k in dict_df.keys():
        text.append(f"{PATH_CSV}/{k}.csv\n")
        for column in dict_df[k].keys():
            describe = df_metaData[df_metaData['Variable'] == column]
            if describe.empty:
                text.append(f"1. **{column}** -> NA\n")
                continue
            describe = describe['Description'].values[0]
            text.append(f"1. **{column}** -> {describe}\n")
        text.append(dict_df[k].to_html() + '\n')
        text.append('___\n')
    
    return text

def saveDetail(text, file_name):

    html_base = open('src/templates/base.html', 'r').readlines()
    html_base = "".join(html_base)

    text = markdown.markdown("\n".join(text))
    html_base = html_base.replace('TITLE', file_name)
    html_base = html_base.replace('BODY', text)
    with open(f'tmp/{file_name}.html', 'w') as f:
        f.write(html_base + '\n')

def genDetailByFile():

    dict_df = getCsvFiles()
    df_metaData = getMetaData()

    for df_name in dict_df.keys():
        tmp_df = pd.DataFrame()
        try:
            tmp_df = pd.read_csv(f'{PATH_CSV}/{df_name}.csv')
        except:
            print(f"Error reading {df_name}")
            continue
        
        text = []
        text.append(f"file: {df_name}\n")
        for k in tmp_df.keys():
            value_counts = tmp_df.value_counts(k)
            text.append(f"column: {k}\n")
            if df_metaData[df_metaData['Variable'] == k].empty:
                text.append(f"describe: NA\n")
            else:
                text.append(f"describe: {df_metaData[df_metaData['Variable'] == k]['Description'].values[0]}\n")
            text.append(f"    - null values: {tmp_df[k].isnull().sum()}\n")
            text.append(f"    - unique values: {value_counts.index.size}\n")
            text.append(f"{value_counts.reset_index().head(10).to_html()}\n")
            text.append(f"___\n")

        saveDetail(text, df_name)

def run():
    # saveDetail()
    genDetailByFile()