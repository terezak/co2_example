import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime
from collections import defaultdict

DB_FILE = 'co2_data.db'

def fetch_data():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT timestamp, co2 FROM co2_readings WHERE co2 IS NOT NULL')
        rows = cursor.fetchall()
    return rows

def compute_daily_averages(timestamps, co2_values):
    daily_data = defaultdict(list)
    for ts, value in zip(timestamps, co2_values):
        date = ts.date()
        daily_data[date].append(value)
    daily_avg = {date: sum(v) / len(v) for date, v in daily_data.items()}
    return daily_avg

def find_worst_day(daily_avg):
    worst_day = max(daily_avg, key=daily_avg.get)
    worst_value = daily_avg[worst_day]
    return worst_day, worst_value

def compute_hourly_averages(timestamps, co2_values):
    hourly_data = defaultdict(list)
    for ts, value in zip(timestamps, co2_values):
        hour = ts.hour
        hourly_data[hour].append(value)
    hourly_avg = {hour: sum(v) / len(v) for hour, v in hourly_data.items()}
    return hourly_avg


def plot_all(timestamps, co2_values, daily_avg, worst_day, hourly_avg):
    fig, axs = plt.subplots(2, 2, figsize=(14, 8))
    fig.suptitle("Analýza CO₂ dat", fontsize=16)

    # --- 1. Časová řada ---
    axs[0, 0].plot(timestamps, co2_values, color='green', marker='.', linestyle='-')
    axs[0, 0].set_title("Vývoj koncentrace CO₂")
    axs[0, 0].set_xlabel("Čas")
    axs[0, 0].set_ylabel("CO₂ [ppm]")
    axs[0, 0].grid(True)

    # --- 2. Denní průměry ---
    dates = sorted(daily_avg.keys())
    values = [daily_avg[d] for d in dates]
    axs[0, 1].plot(dates, values, marker='o', linestyle='-', color='blue')
    axs[0, 1].set_title("Denní průměr koncentrace CO₂")
    axs[0, 1].set_xlabel("Datum")
    axs[0, 1].set_ylabel("Průměr CO₂ [ppm]")
    axs[0, 1].grid(True)

    if worst_day in daily_avg:
        axs[0, 1].plot(worst_day, daily_avg[worst_day], marker='s', markersize=8, color='red', label="Nejhorší den")
        axs[0, 1].legend()

    # --- 3. Shrnutí textem ---
    axs[1, 0].axis('off')
    summary_text = f"📊 Nejvyšší denní průměr:\n\n🗓️  {worst_day}\n📈 {daily_avg[worst_day]:.2f} ppm"
    axs[1, 0].text(0.05, 0.6, summary_text, fontsize=12, verticalalignment='top')

    # --- 4. Průměr CO₂ podle hodin ---
    hours = sorted(hourly_avg.keys())
    avg_by_hour = [hourly_avg[h] for h in hours]
    axs[1, 1].plot(hours, avg_by_hour, marker='o', linestyle='-', color='purple')
    axs[1, 1].set_title("Průměr CO₂ podle denní hodiny")
    axs[1, 1].set_xlabel("Hodina dne")
    axs[1, 1].set_ylabel("CO₂ [ppm]")
    axs[1, 1].grid(True)
    axs[1, 1].set_xticks(range(0, 24, 1))

    fig.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()

def main():
    rows = fetch_data()
    if not rows:
        print("Žádná data k zobrazení.")
        return

    timestamps = [datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S") for row in rows]
    co2_values = [row[1] for row in rows]

    daily_avg = compute_daily_averages(timestamps, co2_values)
    hourly_avg = compute_hourly_averages(timestamps, co2_values)
    worst_day, worst_value = find_worst_day(daily_avg)

    plot_all(timestamps, co2_values, daily_avg, worst_day, hourly_avg)


if __name__ == "__main__":
    main()
