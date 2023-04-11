import pickle
import pandas as pd
import sklearn
import os
from dotenv import dotenv_values

import mysql.connector

def predict_insert(raw):
    config = dotenv_values(".env")

    model = pickle.load(open('random_forest.sav', 'rb'))

    data = raw.drop('ip', axis=1)

    pred = model.predict(data)

    mydb = mysql.connector.connect(
        host=config['DB_HOST'],
        user=config['DB_USERNAME'],
        password=config['DB_PASSWORD'],
        database=config['DB_DATABASE'],
    )

    cursor = mydb.cursor()

    i = 0
    while i in range(len(pred)):
        if pred[i] == 1:
            sql = "INSERT INTO bots (ip) VALUES (%s)"
            val = [raw.loc[i]['ip']]
            cursor.execute(sql, val)
            mydb.commit()
        i += 1
