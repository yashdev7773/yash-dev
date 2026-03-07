# nh8_live_analysis.py
"""
Live Road Accident Analysis - NH-8 (Delhi -> Mumbai)
Single-file demo app (Tkinter GUI). Uses:
- pandas for data handling
- matplotlib for charts embedded in Tkinter
- folium for interactive map (optional; opens in browser)
This file includes:
- CSV loader
- Simulated live feed generator (for demo)
- Basic analytics: counts by city, severity distribution, hourly time series
- GUI that auto-fits to screen and has Exit button
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for safe drawing to canvas
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time, os, webbrowser, datetime, io, random
try:
    import folium
    from folium.plugins import HeatMap
    FOLIUM_AVAILABLE = True
except Exception:
    FOLIUM_AVAILABLE = False

# -----------------------------------------------------------------------------
# Configuration / constants
NH8_CITIES = ["Delhi","Gurgaon","Jaipur","Ajmer","Udaipur","Ahmedabad","Vadodara","Surat","Mumbai"]
SIM_INTERVAL_SECONDS = 2  # how often simulated events arrive
DEFAULT_SEED = 42

# -----------------------------------------------------------------------------
# Helper utilities
def sample_event_generator(seed=DEFAULT_SEED):
    """Yield simulated accident events as dicts (infinite generator)."""
    rng = random.Random(seed)
    # Rough lat/lon centers for cities along NH-8 (approx)
    city_coords = {
        "Delhi": (28.7041,77.1025),
        "Gurgaon": (28.4595,77.0266),
        "Jaipur": (26.9124,75.7873),
        "Ajmer": (26.4499,74.6399),
        "Udaipur": (24.5854,73.7125),
        "Ahmedabad": (23.0225,72.5714),
        "Vadodara": (22.3072,73.1812),
        "Surat": (21.1702,72.8311),
        "Mumbai": (19.0760,72.8777)
    }
    id_counter = 100000
    while True:
        city = rng.choice(list(city_coords.keys()))
        lat_center, lon_center = city_coords[city]
        # small random jitter
        lat = lat_center + rng.uniform(-0.1,0.1)
        lon = lon_center + rng.uniform(-0.1,0.1)
        severity = rng.choices([1,2,3,4], weights=[50,30,15,5])[0]
        event = {
            "id": id_counter,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "latitude": round(lat,6),
            "longitude": round(lon,6),
            "city": city,
            "nearest_km_marker": None,
            "severity": severity,
            "type": rng.choice(["collision","single-vehicle","pedestrian","rollover","other"]),
            "vehicles_involved": rng.randint(1,5),
            "description": "Simulated event"
        }
        id_counter += 1
        yield event

def read_csv_to_df(path):
    """Read CSV to pandas DataFrame with required columns. Returns cleaned df."""
    df = pd.read_csv(path)
    # Basic validation and normalization
    expected = ["id","timestamp","latitude","longitude","city","nearest_km_marker","severity","type","vehicles_involved","description"]
    for col in expected:
        if col not in df.columns:
            df[col] = None
    # Parse timestamp
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    # Drop rows without coords
    df = df.dropna(subset=['latitude','longitude'])
    return df[expected]

# -----------------------------------------------------------------------------
# Analyzer class
class AccidentAnalyzer:
    def __init__(self):
        self.df = pd.DataFrame(columns=["id","timestamp","latitude","longitude","city","nearest_km_marker","severity","type","vehicles_involved","description"])
        # ensure timestamp dtype
        self.df['timestamp'] = pd.to_datetime(self.df['timestamp'], errors='coerce')

    def ingest_dataframe(self, new_df):
        """Append new events dataframe (drop duplicates by id)."""
        combined = pd.concat([self.df, new_df], ignore_index=True)
        combined = combined.drop_duplicates(subset=['id'])
        combined['timestamp'] = pd.to_datetime(combined['timestamp'], errors='coerce')
        self.df = combined.sort_values('timestamp').reset_index(drop=True)

    def ingest_event(self, event_dict):
        """Ingest a single event dict."""
        new_df = pd.DataFrame([event_dict])
        new_df['timestamp'] = pd.to_datetime(new_df['timestamp'], errors='coerce')
        self.ingest_dataframe(new_df)

    def total_count(self):
        return len(self.df)

    def counts_by_city(self):
        return self.df['city'].value_counts().reindex(NH8_CITIES).fillna(0).astype(int)

    def counts_by_severity(self):
        return self.df['severity'].value_counts().sort_index()

    def hourly_time_series(self, last_n_hours=24):
        """Return a time series (hour-level) for the past n hours."""
        if self.df.empty:
            now = pd.Timestamp.now()
            idx = pd.date_range(end=now, periods=last_n_hours, freq='H')
            return pd.Series(0, index=idx)
        now = pd.Timestamp.now()
        start = now - pd.Timedelta(hours=last_n_hours)
        df2 = self.df[(self.df['timestamp'] >= start) & (self.df['timestamp'] <= now)].copy()
        if df2.empty:
            idx = pd.date_range(start=start, end=now, freq='H')
            return pd.Series(0, index=idx)
        df2['hour'] = df2['timestamp'].dt.floor('H')
        s = df2.groupby('hour').size().reindex(pd.date_range(start=start, end=now, freq='H'), fill_value=0)
        return s

    def get_latest_event(self):
        if self.df.empty:
            return None
        row = self.df.iloc[-1]
        return row.to_dict()

# -----------------------------------------------------------------------------
# GUI Application
class NH8App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Live Road Accident Analysis - NH-8 (Demo)")
        # Auto-fit to screen (maximize)
        try:
            self.state('zoomed')  # Windows
        except Exception:
            self.attributes('-zoomed', True)  # Some Linux window managers
        # Create main layout panes
        self.protocol("WM_DELETE_WINDOW", self.on_exit)
        self.analyzer = AccidentAnalyzer()
        self.simulator = sample_event_generator(seed=DEFAULT_SEED)
        self.sim_thread = None
        self.sim_running = threading.Event()
        self.create_widgets()
        # initial plots empty
        self.update_ui()

    def create_widgets(self):
        # Top header frame
        header = ttk.Frame(self, padding=8)
        header.pack(side=tk.TOP, fill=tk.X)
        title_lbl = ttk.Label(header, text="Live Road Accident Analysis of NH-8 (Delhi → Mumbai)", font=("Times New Roman", 16, "bold"))
        title_lbl.pack(side=tk.LEFT)
        right_lbl = ttk.Label(header, text="Module: Dashboard", font=("Times New Roman", 12))
        right_lbl.pack(side=tk.RIGHT)

        # Main content frame
        content = ttk.Frame(self, padding=8)
        content.pack(fill=tk.BOTH, expand=True)

        # Left: stats
        left = ttk.Frame(content, width=350)
        left.pack(side=tk.LEFT, fill=tk.Y)
        self.stats_text = tk.Text(left, width=40, height=30, font=("Times New Roman", 11))
        self.stats_text.pack(fill=tk.BOTH, expand=True)

        # Right: charts
        right = ttk.Frame(content)
        right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        # Matplotlib figure placeholders
        self.fig1 = plt.Figure(figsize=(5,3))
        self.ax1 = self.fig1.add_subplot(111)
        self.canvas1 = FigureCanvasTkAgg(self.fig1, master=right)
        self.canvas1.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.fig2 = plt.Figure(figsize=(5,2))
        self.ax2 = self.fig2.add_subplot(111)
        self.canvas2 = FigureCanvasTkAgg(self.fig2, master=right)
        self.canvas2.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Bottom controls
        bottom = ttk.Frame(self, padding=8)
        bottom.pack(side=tk.BOTTOM, fill=tk.X)
        btn_load = ttk.Button(bottom, text="Load CSV", command=self.on_load_csv)
        btn_load.pack(side=tk.LEFT, padx=4)
        btn_start = ttk.Button(bottom, text="Start Simulation (Live)", command=self.on_start_sim)
        btn_start.pack(side=tk.LEFT, padx=4)
        btn_stop = ttk.Button(bottom, text="Stop Simulation", command=self.on_stop_sim)
        btn_stop.pack(side=tk.LEFT, padx=4)
        btn_map = ttk.Button(bottom, text="Show Map (Browser)", command=self.on_show_map)
        btn_map.pack(side=tk.LEFT, padx=4)
        btn_export = ttk.Button(bottom, text="Export Summary CSV", command=self.on_export)
        btn_export.pack(side=tk.LEFT, padx=4)
        btn_exit = ttk.Button(bottom, text="Exit", command=self.on_exit)
        btn_exit.pack(side=tk.RIGHT, padx=4)

    # --- UI callbacks ---
    def on_load_csv(self):
        path = filedialog.askopenfilename(title="Open CSV file", filetypes=[("CSV files","*.csv"),("All files","*.*")])
        if not path:
            return
        try:
            df = read_csv_to_df(path)
            self.analyzer.ingest_dataframe(df)
            messagebox.showinfo("Loaded", f"Loaded {len(df)} events from CSV")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load CSV: {e}")
        self.update_ui()

    def on_start_sim(self):
        if self.sim_thread and self.sim_thread.is_alive():
            messagebox.showinfo("Sim", "Simulation already running")
            return
        self.sim_running.set()
        self.sim_thread = threading.Thread(target=self._sim_loop, daemon=True)
        self.sim_thread.start()
        messagebox.showinfo("Sim", "Simulation started")
    
    def _sim_loop(self):
        # Insert simulated events periodically until stopped
        while self.sim_running.is_set():
            event = next(self.simulator)
            self.analyzer.ingest_event(event)
            # update UI from main thread: schedule via after
            self.after(100, self.update_ui)
            time.sleep(SIM_INTERVAL_SECONDS)

    def on_stop_sim(self):
        if self.sim_thread and self.sim_thread.is_alive():
            self.sim_running.clear()
            messagebox.showinfo("Sim", "Stopping simulation...")
        else:
            messagebox.showinfo("Sim", "No simulation running")

    def on_show_map(self):
        if not FOLIUM_AVAILABLE:
            messagebox.showwarning("Folium not installed", "Folium is not available. Install with: pip install folium")
            return
        # Build a folium map and open in browser
        df = self.analyzer.df
        if df.empty:
            messagebox.showinfo("Map", "No events to show on map")
            return
        # center map at mean coordinates
        center = [df['latitude'].mean(), df['longitude'].mean()]
        m = folium.Map(location=center, zoom_start=6)
        # add points
        for _, row in df.iterrows():
            folium.CircleMarker(
                location=(row['latitude'], row['longitude']),
                radius=4 + (0 if pd.isna(row['severity']) else int(row['severity'])),
                popup=f"ID:{row['id']} {row['timestamp']}\nCity:{row['city']}\nSeverity:{row['severity']}",
                color=None,
                fill=True
            ).add_to(m)
        # add heatmap
        heat_data = df[['latitude','longitude']].dropna().values.tolist()
        if heat_data:
            HeatMap(heat_data).add_to(m)
        path = os.path.join(os.getcwd(), "nh8_map.html")
        m.save(path)
        webbrowser.open("file://" + path)

    def on_export(self):
        if self.analyzer.df.empty:
            messagebox.showinfo("Export", "No events to export")
            return
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV","*.csv")])
        if not path:
            return
        self.analyzer.df.to_csv(path, index=False)
        messagebox.showinfo("Exported", f"Exported {len(self.analyzer.df)} events to {path}")

    def on_exit(self):
        # stop simulator thread
        try:
            self.sim_running.clear()
        except:
            pass
        self.destroy()

    # --- UI update functions ---
    def update_ui(self):
        # Update stats text
        s = []
        s.append(f"Total events: {self.analyzer.total_count()}")
        latest = self.analyzer.get_latest_event()
        s.append("\nLatest event:")
        if latest is not None:
            s.append(f"  ID: {latest['id']}")
            s.append(f"  Time: {latest['timestamp']}")
            s.append(f"  City: {latest['city']}")
            s.append(f"  Severity: {latest['severity']}")
            s.append(f"  Type: {latest['type']}")
        else:
            s.append("  None")
        s.append("\nCounts by City:")
        city_counts = self.analyzer.counts_by_city()
        for city, val in city_counts.items():
            s.append(f"  {city}: {val}")
        s.append("\nCounts by Severity:")
        sev_counts = self.analyzer.counts_by_severity()
        for sev, val in sev_counts.items():
            s.append(f"  {int(sev)}: {int(val)}")
        self.stats_text.delete("1.0", tk.END)
        self.stats_text.insert(tk.END, "\n".join(s))

        # Update chart 1: City counts bar
        self.ax1.clear()
        city_counts.plot(kind='bar', ax=self.ax1)
        self.ax1.set_title("Accidents by City")
        self.ax1.set_ylabel("Count")
        self.fig1.tight_layout()
        self.canvas1.draw()

        # Update chart 2: Hourly time series
        self.ax2.clear()
        ts = self.analyzer.hourly_time_series(last_n_hours=24)
        if ts is not None:
            ax = ts.plot(ax=self.ax2)
            self.ax2.set_title("Accidents in last 24 hours (hourly)")
            self.ax2.set_xlabel("Hour")
            self.ax2.set_ylabel("Count")
            self.fig2.tight_layout()
            self.canvas2.draw()

# -----------------------------------------------------------------------------
# If run as main, start app
def main():
    app = NH8App()
    app.mainloop()

if __name__ == "__main__":
    main()
