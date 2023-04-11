import pickle
import pandas as pd

model = pickle.load(open('random_forest.sav', 'rb'))

data = pd.read_csv('output.csv', delimiter=',')

