import pandas as pd
import random
from faker import Faker

fake = Faker()

def generate_data(n=10000):
    data = []
    for _ in range(n):
        email = fake.email()
        phone = fake.phone_number()
        credit_score = random.randint(300, 850)
        age_group = random.choice(['18-25', '26-35', '36-50', '51+'])
        family_background = random.choice(['Single', 'Married', 'Married with Kids'])
        income = random.randint(100000, 1000000)
        comments = random.choice([
            'urgent need to buy', 'just browsing', 'want to buy soon',
            'not interested', 'need home loan', 'job relocation'
        ])

        if 'urgent' in comments or 'soon' in comments or 'relocation' in comments:
            intent = 1  
        else:
            intent = 0 

        data.append([
            email, phone, credit_score, age_group,
            family_background, income, comments, intent
        ])

    df = pd.DataFrame(data, columns=[
        'Email', 'Phone', 'CreditScore', 'AgeGroup',
        'FamilyBackground', 'Income', 'Comments', 'Intent'
    ])

    df.to_csv('data/leads_dataset.csv', index=False)
    print("✅ Dataset generated and saved to data/leads_dataset.csv")

if __name__ == "__main__":
    generate_data()