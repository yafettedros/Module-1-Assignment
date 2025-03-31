import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import random
from datetime import datetime

# Make sure results are the same every time
random.seed(42)
np.random.seed(42)

# Lists for random data
classes = ['Waterbabies', 'Aquatots', 'Preschool']
days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
time_slots = ['9:00 AM', '10:00 AM', '12:00 PM', '2:00 PM', '4:00 PM', '5:00 PM']

# Create fake class data
data = []
for i in range(300):
    class_type = random.choice(classes)
    day = random.choice(days)
    time = random.choice(time_slots)
    capacity = random.choice([8, 10, 12])
    
    # Set realistic enrollment numbers
    if time in ['9:00 AM', '10:00 AM']:
        enrollment = random.randint(7, capacity)
    elif time in ['4:00 PM', '5:00 PM']:
        enrollment = random.randint(8, capacity)
    else:
        enrollment = random.randint(1, capacity // 2)

    data.append([class_type, day, time, capacity, enrollment])

# Put data into a table
df = pd.DataFrame(data, columns=['Class Type', 'Day', 'Time', 'Max Capacity', 'Enrollment'])

# Clean time column
df['Time'] = pd.to_datetime(df['Time'], format='%I:%M %p').dt.time

# Add enrollment rate column
df['Enrollment Rate (%)'] = (df['Enrollment'] / df['Max Capacity']) * 100

# Save the cleaned dataset
df.to_csv("swim_class_data_cleaned.csv", index=False)

# Group by time and get average enrollment rate
time_group = df.groupby('Time')['Enrollment Rate (%)'].mean()

# Make a clean bar chart
time_labels = [t.strftime('%I:%M %p') for t in time_group.index]
plt.figure(figsize=(10, 5))
plt.bar(time_labels, time_group.values)
plt.title('Average Enrollment Rate by Time Slot')
plt.xlabel('Time Slot')
plt.ylabel('Enrollment Rate (%)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("bar_chart_enrollment_rate_clean.png")
plt.close()

# Make a heatmap showing average enrollment by day and time
heatmap_data = df.pivot_table(index='Day', columns='Time', values='Enrollment Rate (%)', aggfunc='mean')
plt.figure(figsize=(12, 6))
sns.heatmap(heatmap_data, annot=True, fmt=".1f", cmap='YlGnBu')
plt.title('Heatmap of Enrollment Rate by Day and Time')
plt.tight_layout()
plt.savefig("heatmap_enrollment_rate.png")
plt.close()

print("Done! Files saved:")
print("- swim_class_data_cleaned.csv")
print("- bar_chart_enrollment_rate_clean.png")
print("- heatmap_enrollment_rate.png")

