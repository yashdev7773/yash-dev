import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd
import random
from datetime import datetime
import time

# ==========================================
# CONFIGURATION & GLOBAL STATE
# ==========================================
# These lists simulate the "Live Data Feed" coming from sensors/cameras
LOCATIONS = ['Highway-404', 'Main St', '4th Avenue', 'Rural Route 9', 'City Center']
SEVERITIES = ['Minor', 'Moderate', 'Severe', 'Fatal']
WEATHER = ['Clear', 'Rain', 'Fog', 'Snow']

# Global DataFrame to store live incoming data
live_data = pd.DataFrame(columns=['Time', 'Location', 'Severity', 'Weather', 'Casualties'])

# Setup the plot
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
plt.subplots_adjust(hspace=0.5)

# ==========================================
# 1. LIVE DATA SIMULATION MODULE
# ==========================================
def fetch_live_data():
    """
    Simulates receiving a single data packet from a traffic sensor or API.
    In a real project, this would be an API call or IoT sensor reading.
    """
    now = datetime.now().strftime('%H:%M:%S')
    
    # Weighted random choice to make 'Fatal' rare
    severity_weights = [0.6, 0.3, 0.08, 0.02] 
    severity = random.choices(SEVERITIES, weights=severity_weights, k=1)[0]
    
    casualties = 0
    if severity == 'Fatal':
        casualties = random.randint(1, 4)
    elif severity == 'Severe':
        casualties = random.randint(0, 2)

    record = {
        'Time': now,
        'Location': random.choice(LOCATIONS),
        'Severity': severity,
        'Weather': random.choice(WEATHER),
        'Casualties': casualties
    }
    return record

# ==========================================
# 2. UPDATE FUNCTION (THE "LIVE" ENGINE)
# ==========================================
def animate(i):
    global live_data
    
    # 1. Ingest Data
    new_record = fetch_live_data()
    
    # Check for ALERT condition
    if new_record['Severity'] == 'Fatal':
        print(f"⚠️  ALERT: FATAL ACCIDENT DETECTED AT {new_record['Location']}! Dispatching Help...")
    elif new_record['Severity'] == 'Severe':
        print(f"⚠️  WARNING: Severe accident at {new_record['Location']}.")
    else:
        print(f"[{new_record['Time']}] Normal traffic flow. Minor incident at {new_record['Location']}.")

    # 2. Append to DataFrame (using concat instead of append for newer pandas versions)
    new_df = pd.DataFrame([new_record])
    live_data = pd.concat([live_data, new_df], ignore_index=True)
    
    # Keep only last 20 records for the "Live" window to keep graph readable
    if len(live_data) > 20:
        display_data = live_data.tail(20)
    else:
        display_data = live_data

    # 3. Update Graph 1: Severity Counts (Live Bar Chart)
    ax1.clear()
    severity_counts = display_data['Severity'].value_counts()
    colors = {'Minor': 'green', 'Moderate': 'yellow', 'Severe': 'orange', 'Fatal': 'red'}
    bar_colors = [colors.get(x, 'blue') for x in severity_counts.index]
    
    ax1.bar(severity_counts.index, severity_counts.values, color=bar_colors)
    ax1.set_title('Live Accident Severity Distribution (Last 20 Events)')
    ax1.set_ylabel('Count')

    # 4. Update Graph 2: Casualties over Time (Live Line Chart)
    ax2.clear()
    ax2.plot(display_data['Time'], display_data['Casualties'], color='darkred', marker='o', linestyle='-')
    ax2.set_title('Real-Time Casualty Monitoring')
    ax2.set_xlabel('Time')
    ax2.set_ylabel('Number of Casualties')
    
    # Rotate x-axis labels to prevent overlap
    plt.setp(ax2.get_xticklabels(), rotation=45, ha="right")

# ==========================================
# 3. MAIN EXECUTION
# ==========================================
if __name__ == "__main__":
    print("--- STARTING LIVE ROAD ACCIDENT MONITORING SYSTEM ---")
    print("Waiting for sensor data...")
    
    # Update the graph every 1000 milliseconds (1 second)
    ani = animation.FuncAnimation(fig, animate, interval=1000)
    
    plt.show()