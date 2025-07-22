import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.preprocessing import LabelEncoder
import joblib

df = pd.read_csv('data/leads_dataset.csv')

le_age = LabelEncoder()
le_family = LabelEncoder()

df['AgeGroup'] = le_age.fit_transform(df['AgeGroup'])
df['FamilyBackground'] = le_family.fit_transform(df['FamilyBackground'])

X = df[['CreditScore', 'AgeGroup', 'FamilyBackground', 'Income']]
y = df['Intent']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = GradientBoostingClassifier()
model.fit(X_train, y_train)

joblib.dump(model, 'model/model.pkl')
print("✅ Model trained and saved to model/model.pkl")