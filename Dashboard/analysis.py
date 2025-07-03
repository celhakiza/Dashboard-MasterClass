#import packages

import pandas as pd
data = pd.read_csv('data/Dataset_1.csv',low_memory=False)
#print(data)
age = "23"
age = int(age)

names_list = ["Peter","Pacifique","Jane"]
names_tuples = ("Peter","Pacifique","Jane")
names_dict = {
    "Name":"Celestin",
    "age":20,
    "Gender":"Male"
}

print(names_dict)
print(names_list)

print(data.columns)
print(data.dtypes)
print(data.head())

print(data.columns)

n_male = len(data[data['gender'].str.lower()=='male'])
n_female = len(data[data['gender'].str.lower()=='female'])
both_sexes = n_male + n_female

print(f"Males:{n_male} \n Females:{n_female}\n Both sexes: {both_sexes}")
data['education_level'] = data['education_level'].fillna('Not educated')
education_level = data.groupby('education_level').agg(
    nbr = ("student_id","count"),
    avg_income = ("monthly_income_rwf","mean"),
).reset_index()

print(education_level)