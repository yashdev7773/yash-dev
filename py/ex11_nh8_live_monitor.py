import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd
import random
from datetime import datetime
import warnings

# Suppress warnings for cleaner output
warnings.filterwarnings("ignore")

# ==========================================
# CONFIGURATION & SETUP
# ==========================================
# Specific locations along NH-8 (Delhi to Jaipur stretch)
LOCATIONS = [
    'Gurgaon Toll Plaza', 'Manesar IMT', 'Bilaspur Chowk', 
    'Dharuhera Cut', 'Neemrana Flyover', 'Behror Midway', 
    'Kotputli Cut', 'Paota Village', 'Shahpura', 'Amer Fort Entry'
]

# Severity levels for accidents
SEVERITY = ['Minor', 'Moderate', 'Severe', 'Fatal']
# Weather conditions affecting NH-8
WEATHER = ['Clear', 'Smog', 'Heavy Rain', 'Dust Storm']

# Global buffer to store the last 50 live records for visualization
live_data_buffer = pd.DataFrame(columns=['Time', 'Location', 'Speed', 'Severity'])

# ==========================================
# MODULE 1: SENSOR SIMULATION (Data Ingestion)
# ==========================================
def fetch_sensor_data():
    """
    Simulates receiving a data packet from an IoT sensor on the highway.
    In a real project, this would be an API call or Database read.
    """
    now = datetime.now().strftime('%H:%M:%S')
    location = random.choice(LOCATIONS)
    
    # Simulate correlation: Higher speeds often lead to higher severity
    speed = random.randint(40, 160)
    
    # Weighted random choice for severity based on speed
    if speed > 120:
        sev = random.choices(SEVERITY, weights=[0.1, 0.2, 0.4, 0.3])[0]
    else:
        sev = random.choices(SEVERITY, weights=[0.7, 0.2, 0.1, 0.0])[0]
        
    return {
        'Time': now,
        'Location': location,
        'Speed': speed,
        'Severity': sev
    }

# ==========================================
# MODULE 2: VISUALIZATION ENGINE
# ==========================================
def animate(i):
    """
    This function is called automatically every 1000ms (1 second) by Matplotlib.
    It clears the charts and redraws them with the newest data.
    """
    global live_data_buffer
    
    # 1. Fetch new data
    new_packet = fetch_sensor_data()
    
    # 2. Append to buffer (using pd.concat instead of append)
    new_row = pd.DataFrame([new_packet])
    live_data_buffer = pd.concat([live_data_buffer, new_row], ignore_index=True)
    
    # Keep only last 25 records to keep the graph "moving"
    if len(live_data_buffer) > 25:
        live_data_buffer = live_data_buffer.iloc[1:]
        
    # 3. Check for Alerts (Console Log)
    if new_packet['Severity'] == 'Fatal':
        print(f"🔴 [CRITICAL ALERT] Fatal Crash at {new_packet['Location']} | Speed: {new_packet['Speed']}km/h")
    else:
        print(f"🟢 [INFO] {new_packet['Time']}: Minor incident at {new_packet['Location']}.")

    # 4. Clear Axes for Redraw
    ax1.clear()
    ax2.clear()
    
    # --- CHART 1: Live Active Hotspots (Bar Chart) ---
    # Count accidents per location in the current buffer
    counts = live_data_buffer['Location'].value_counts().head(5)
    ax1.barh(counts.index, counts.values, color='#FF6B6B')
    ax1.set_title(f"Live Active Hotspots (Last 25 Incidents)", fontsize=14, fontweight='bold')
    ax1.set_xlabel("Number of Incidents")
    
    # --- CHART 2: Speed vs Severity Correlation (Scatter Plot) ---
    # Map severity to colors
    colors = live_data_buffer['Severity'].map({
        'Minor': 'green', 'Moderate': 'yellow', 'Severe': 'orange', 'Fatal': 'red'
    })
    
    ax2.scatter(live_data_buffer['Speed'], live_data_buffer['Location'], c=colors, s=100, edgecolors='black')
    ax2.set_title("Real-Time Vehicle Speed vs. Location Analysis", fontsize=14, fontweight='bold')
    ax2.set_xlabel("Vehicle Speed (km/h)")
    ax2.set_xlim(0, 180) # Fixed x-axis for stability
    ax2.grid(True, linestyle='--', alpha=0.6)

# ==========================================
# MAIN EXECUTION
# ==========================================
if __name__ == "__main__":
    print("--- STARTING NH-8 LIVE TRAFFIC MONITORING SYSTEM ---")
    print("Press Ctrl+C in terminal to stop.")
    
    # Setup the Layout
    fig = plt.figure(figsize=(14, 8))
    fig.suptitle('NH-8 HIGHWAY LIVE ACCIDENT ANALYSIS DASHBOARD', fontsize=16, color='darkblue')
    
    # Create 2 subplots (Top and Bottom)
    ax1 = fig.add_subplot(2, 1, 1) # Top: Bar Chart
    ax2 = fig.add_subplot(2, 1, 2) # Bottom: Scatter Plot
    
    # Adjust layout spacing
    plt.subplots_adjust(hspace=0.4)
    
    # Start Animation (Interval = 1000ms = 1 second)
    ani = animation.FuncAnimation(fig, animate, interval=1000)
    
    # Auto-fit to screen (Maximize window)
    manager = plt.get_current_fig_manager()
    try:
        manager.window.state('zoomed') # Works on Windows
    except:
        try:
            manager.full_screen_toggle() # Works on Linux/Mac
        except:
            pass # Default size
            
    plt.show()