import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd
import random
from datetime import datetime
import time

# ==========================================
# CONFIGURATION: NH-8 SPECIFIC LOCATIONS
# ==========================================
# Real-world locations along the National Highway 8 (Delhi to Jaipur)
LOCATIONS = [
    'Shiv Murti (Delhi Start)', 
    'Gurgaon Toll Plaza', 
    'Manesar IMT', 
    'Bawal Industrial Area', 
    'Neemrana Flyover', 
    'Behror Midway', 
    'Kotputli Cut', 
    'Paota', 
    'Shahpura', 
    'Amer Fort Entry (Jaipur)'
]

SEVERITIES = ['Minor', 'Moderate', 'Severe', 'Fatal']
WEATHER_NH8 = ['Clear (Sunny)', 'Smog/Haze', 'Heavy Rain', 'Dust Storm']

# Global DataFrame to store live incoming data stream
live_data = pd.DataFrame(columns=['Time', 'Location', 'Severity', 'Weather', 'Vehicle_Speed'])

# Setup the plot figure
# We use a 2-row layout: Top for Severity Count, Bottom for Speed vs Casualty correlation
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 9))
plt.subplots_adjust(hspace=0.6)
fig.suptitle('LIVE MONITORING: NH-8 (DELHI-JAIPUR) HIGHWAY', fontsize=16, fontweight='bold')

# ==========================================
# 1. LIVE DATA SIMULATION MODULE
# ==========================================
def fetch_sensor_data():
    """
    Simulates receiving data from IoT sensors placed along NH-8.
    """
    now = datetime.now().strftime('%H:%M:%S')
    
    # Weighted probabilities: Fatal accidents are rarer than Minor ones
    severity_weights = [0.65, 0.25, 0.08, 0.02] 
    severity = random.choices(SEVERITIES, weights=severity_weights, k=1)[0]
    
    # Simulate Vehicle Speed based on location (Highways have higher speeds)
    speed = random.randint(40, 120)
    if severity == 'Fatal':
        speed = random.randint(100, 160) # High speed correlation
    
    location = random.choice(LOCATIONS)
    
    # Weather impact
    weather = random.choice(WEATHER_NH8)
    
    record = {
        'Time': now,
        'Location': location,
        'Severity': severity,
        'Weather': weather,
        'Vehicle_Speed': speed
    }
    return record

# ==========================================
# 2. UPDATE FUNCTION (ANIMATION LOOP)
# ==========================================
def animate(i):
    global live_data
    
    # 1. Ingest Data Packet
    new_record = fetch_sensor_data()
    
    # Console Alerts (Simulating a Control Room View)
    if new_record['Severity'] == 'Fatal':
        print(f"🔴 [CRITICAL ALERT] Fatal Crash at {new_record['Location']} | Speed: {new_record['Vehicle_Speed']}km/h")
    elif new_record['Severity'] == 'Severe':
        print(f"🟠 [WARNING] Severe accident at {new_record['Location']}. Ambulance dispatched.")
    else:
        print(f"🟢 [INFO] {new_record['Time']}: Minor incident at {new_record['Location']}.")

    # 2. Update DataFrame
    # Using concat as per modern pandas requirements
    new_df = pd.DataFrame([new_record])
    live_data = pd.concat([live_data, new_df], ignore_index=True)
    
    # Keep window to last 25 records to keep graphs readable
    if len(live_data) > 25:
        display_data = live_data.tail(25)
    else:
        display_data = live_data

    # 3. Visualization 1: Accident Count by Location (Top High-Risk Zones)
    ax1.clear()
    # Count accidents per location in the current window
    loc_counts = display_data['Location'].value_counts().head(5) # Top 5 active spots
    
    # Color logic
    colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#c2c2f0']
    
    ax1.barh(loc_counts.index, loc_counts.values, color=colors)
    ax1.set_title('Live Active Hotspots (Last 25 Incidents)')
    ax1.set_xlabel('Number of Incidents')
    ax1.invert_yaxis() # Highest count on top

    # 4. Visualization 2: Vehicle Speed Scatter Plot
    ax2.clear()
    
    # Map severity to color for the scatter plot
    color_map = {'Minor': 'green', 'Moderate': 'blue', 'Severe': 'orange', 'Fatal': 'red'}
    colors_mapped = [color_map[x] for x in display_data['Severity']]
    
    ax2.scatter(display_data['Time'], display_data['Vehicle_Speed'], c=colors_mapped, s=100, edgecolors='black')
    
    # Create a custom legend manually
    from matplotlib.lines import Line2D
    custom_lines = [Line2D([0], [0], color=c, lw=0, marker='o', markersize=10) for c in color_map.values()]
    ax2.legend(custom_lines, color_map.keys(), loc='upper right')
    
    ax2.set_title('Real-Time Speed vs. Severity Monitor')
    ax2.set_ylabel('Vehicle Speed (km/h)')
    ax2.set_xlabel('Time Stamp')
    
    # Rotate timestamps
    plt.setp(ax2.get_xticklabels(), rotation=45, ha="right")
    
    # Add grid
    ax2.grid(True, linestyle='--', alpha=0.7)

# ==========================================
# 3. MAIN EXECUTION
# ==========================================
if __name__ == "__main__":
    print("=================================================")
    print("   NH-8 HIGHWAY LIVE ACCIDENT MONITORING SYSTEM   ")
    print("   Connecting to Sensors at Shiv Murti, Manesar, Kotputli...")
    print("=================================================\n")
    
    # Run animation: Update every 1000ms (1 second)
    ani = animation.FuncAnimation(fig, animate, interval=1000)
    
    # Show the GUI window
    plt.tight_layout()
    plt.show()