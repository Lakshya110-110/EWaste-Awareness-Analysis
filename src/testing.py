import pandas as pd
import numpy as np

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import seaborn as sns

from scipy.stats import chi2_contingency

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (
     accuracy_score,
     confusion_matrix,
     classification_report
)

#---------- Load Dataset ---------

df = pd.read_excel("brm.xlsx")

#---------- View Data ----------

print("\nFIRST 5 ROWS\n")
print(df.head())

print("\nCOLUMN NAMES\n")
print(df.columns)

print("\nDATASET INFO\n")
print(df.info())

#---------- Check Null Values ---------

print("\nNULL VALUES\n")
print(df.isnull().sum())

#---------- CLean Data --------------

df.dropna(inplace=True)
df.drop_duplicates(inplace=True)

print("\nDATASET SHAPE AFTER CLEANING\n")
print(df.shape)

#--------- Visualization ------------

plt.figure(figsize=(6,5))
sns.countplot(x=df['2. Gender'])
plt.title("Gender Distribution")
plt.savefig("gender_distribution.png")
plt.close()

#---------- Label Encoding -----------

le = LabelEncoder()

for col in df.columns:
     df[col] = le.fit_transform(df[col].astype(str))

print("\nENCODED DATA\n")
print(df.head())

#------------ Correlation Heatmap -----------

plt.figure(figsize=(14,10))
sns.heatmap(df.corr(), annot=True, cmap='coolwarm')
plt.title("Correlation Heatmap")

plt.savefig("heatmap.png")
plt.close()

#----------- Hypothesis Testing --------------

table = pd.crosstab(
     df['2. Gender'],
     df['4. Have you heard about e-waste? ']
)

print("\nCONTINGENCY TABLE\n")
print(table)

#----------- Chi Square Test ------------------

chi2, p, dof, expected = chi2_contingency(table)

print("\nCHI-SQUARE TEST RESULTS\n")
print("Chi-Square Value:", chi2)
print("P-value:", p)
print("Degrees of Freedom:", dof)

#----------- Hypothesis Decision -------------

alpha = 0.05

if p < alpha:
     print("\nReject Null Hypothesis")
     print("Gender and Awareness are dependent")
else:
     print("\nFail to Reject Null Hypothesis\n")
     print("Gender and Awareness are independent")

#------------ Second hypothesis testing ----------

table2 = pd.crosstab(
     df['2. Gender'],
     df['10.Do you own unused/old electronic devices?']
)

print("\nSECOND CONTINGENCY TABLE\n")
print(table2)

#----------- Second Chi Square Test ----------

chi2_2, p2, dof2, expected2 = chi2_contingency(table2)

print("\nSECOND CHI-SQUARE TEST RESULTS\n")
print("Chi-Square Value:", chi2_2)
print("P-value:", p2)
print("Degrees of Freedom:", dof2)

#------------ Second Hypothesis Decision ----------

alpha = 0.05

if p2 < alpha:
     print("\nReject Null Hypothesis")
     print("Gender and E-waste ownership are dependent")
else:
     print("\nFail to Reject Null Hypothesis")
     print("Gender and E-waste ownership are independent")
#------------ Machine Learning ---------------

x = df[[
     '1. Age Group',
     '2. Gender',
     '3. Education Level'
]]

y = df['4. Have you heard about e-waste? ']

#------------ Train Test Split ----------------

x_train, x_test, y_train, y_test = train_test_split(
     x,
     y,
     test_size=0.2,
     random_state=42
)

#------------ Random Forest Model --------------

model = RandomForestClassifier(
     n_estimators=100,
     random_state=42
)

model.fit(x_train,y_train)

#------------- Predictions ----------------

y_pred = model.predict(x_test)

#------------ Accuracy ---------------------

accuracy = accuracy_score(y_test, y_pred)

print("\nMODEL ACCURACY\n")
print("Accuracy:", accuracy)

#------------- Classification Report -----------

print("\nCLASSIFICATION REPORT\n")

print(classification_report(y_test, y_pred, zero_division=0))

#------------- Confusion Matrix -----------------

cm = confusion_matrix(y_test, y_pred)

plt.figure(figsize=(6,5))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')

plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.savefig("confusion_matrix.png")
plt.close()

#---------------- Feature Importance -------------

importance = model.feature_importances_

features = x.columns

plt.figure(figsize=(7,5))
plt.bar(features, importance)
plt.title("Feature Importance")
plt.xlabel("Features")
plt.ylabel("Importance")
plt.savefig("feature_importance.png")
plt.close()

#------------- Final Insights -----------------

print("\nFINAL INSIGHTS\n")

print("""
1. Chi-Square Test was used to determine whether
   Gender and E-Waste Awareness are statistically related.

2. Random Forest Classification was used to predict
   awareness levels using demographic variables.

3. Feature Importance identified the most influential
   factor affecting awareness.

4. This project combines hypothesis testing and
   machine learning for behavioral analysis.
""")