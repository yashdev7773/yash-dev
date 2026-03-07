import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import random
from datetime import datetime, timedelta

# ==========================================
# 1. DATA GENERATION MODULE (MOCK DATA)
# ==========================================
def generate_mock_data(num_records=1000):
    """
    Generates a synthetic dataset for Road Accident Analysis.
    In a real scenario, this would be replaced by pd.read_csv('file.csv').
    """
    print("Generating mock dataset...")
    
    # Lists for random choice
    road_types = ['Highway', 'City Street', 'Rural Road', 'Intersection', 'Parking Lot']
    weather_conditions = ['Clear', 'Rainy', 'Foggy', 'Snowy', 'Stormy']
    light_conditions = ['Daylight', 'Dark - Lighted', 'Dark - Unlighted', 'Dusk', 'Dawn']
    severity_levels = ['Minor', 'Moderate', 'Severe', 'Fatal']
    vehicle_types = ['Car', 'Truck', 'Motorcycle', 'Bus', 'Bicycle']
    
    data = []
    
    start_date = datetime(2023, 1, 1)
    
    for _ in range(num_records):
        # Random date and time
        random_days = random.randint(0, 365)
        random_seconds = random.randint(0, 86400)
        date_time = start_date + timedelta(days=random_days, seconds=random_seconds)
        
        # Weighted severity based on conditions (simulating logic)
        weather = random.choice(weather_conditions)
        severity_weight = [0.6, 0.3, 0.08, 0.02] # Bias towards minor accidents
        
        if weather in ['Rainy', 'Snowy', 'Foggy']:
            severity_weight = [0.4, 0.4, 0.15, 0.05] # Higher chance of severe in bad weather
            
        severity = random.choices(severity_levels, weights=severity_weight, k=1)[0]
        
        record = {
            'Accident_ID': f'ACC{random.randint(10000, 99999)}',
            'Date': date_time.strftime('%Y-%m-%d'),
            'Time': date_time.strftime('%H:%M:%S'),
            'Hour': date_time.hour,
            'Road_Type': random.choice(road_types),
            'Weather': weather,
            'Light_Condition': random.choice(light_conditions),
            'Vehicle_Type': random.choice(vehicle_types),
            'Person_Age': random.randint(18, 85),
            'Speed_Limit': random.choice([30, 40, 50, 60, 80, 100, 120]),
            'Severity': severity
        }
        data.append(record)
        
    df = pd.DataFrame(data)
    print(f"Dataset generated with {num_records} records.")
    return df

# ==========================================
# 2. ANALYSIS MODULE
# ==========================================
def analyze_data(df):
    print("\n--- Starting Analysis ---")
    
    # Set plot style
    sns.set_style("whitegrid")
    plt.rcParams['figure.figsize'] = (10, 6)

    # Analysis 1: Accidents by Hour of Day
    print("Generating Chart: Accidents by Hour...")
    plt.figure()
    sns.histplot(df['Hour'], bins=24, kde=True, color='skyblue')
    plt.title('Distribution of Accidents by Hour of Day')
    plt.xlabel('Hour (0-23)')
    plt.ylabel('Number of Accidents')
    plt.savefig('accidents_by_hour.png')
    plt.show()

    # Analysis 2: Accidents by Weather Condition
    print("Generating Chart: Accidents by Weather...")
    plt.figure()
    sns.countplot(x='Weather', data=df, palette='viridis', order=df['Weather'].value_counts().index)
    plt.title('Accident Count by Weather Condition')
    plt.xlabel('Weather Condition')
    plt.ylabel('Count')
    plt.show()

    # Analysis 3: Severity vs Road Type (Heatmap Logic or Stacked Bar)
    print("Generating Chart: Severity vs Road Type...")
    plt.figure()
    ct = pd.crosstab(df['Road_Type'], df['Severity'])
    ct.plot(kind='bar', stacked=True, colormap='Reds', figsize=(10, 6))
    plt.title('Accident Severity by Road Type')
    plt.xlabel('Road Type')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
    
    # Analysis 4: Correlation Matrix (Numeric Data)
    print("Generating Correlation Matrix...")
    # Convert severity to numeric for correlation
    severity_map = {'Minor': 1, 'Moderate': 2, 'Severe': 3, 'Fatal': 4}
    df['Severity_Score'] = df['Severity'].map(severity_map)
    
    numeric_df = df[['Hour', 'Person_Age', 'Speed_Limit', 'Severity_Score']]
    corr = numeric_df.corr()
    
    plt.figure()
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title('Correlation Matrix of Numerical Features')
    plt.show()

# ==========================================
# 3. TEXT REPORT MODULE
# ==========================================
def generate_summary_stats(df):
    print("\n--- Summary Statistics ---")
    total_accidents = len(df)
    most_dangerous_hour = df['Hour'].mode()[0]
    most_common_cause = df['Weather'].mode()[0]
    fatal_count = len(df[df['Severity'] == 'Fatal'])
    
    print(f"Total Accidents Analyzed: {total_accidents}")
    print(f"Most Dangerous Hour of Day: {most_dangerous_hour}:00")
    print(f"Most Frequent Weather Condition: {most_common_cause}")
    print(f"Total Fatalities Recorded: {fatal_count}")
    print(f"Fatality Rate: {(fatal_count/total_accidents)*100:.2f}%")

# ==========================================
# MAIN EXECUTION
# ==========================================
if __name__ == "__main__":
    # 1. Load Data
    df = generate_mock_data(1500)
    
    # 2. Pre-process (Simulated Cleaning)
    # Check for nulls
    if df.isnull().sum().sum() > 0:
        df.dropna(inplace=True)
        
    # 3. Perform Analysis
    generate_summary_stats(df)
    analyze_data(df)
    
    print("\nAnalysis Complete. Charts have been generated.")