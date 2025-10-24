import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Function to load, convert, and smooth
def process_csv(filepath):
    df = pd.read_csv(filepath)

    # Convert MM:SS to seconds from start
    def time_to_seconds(time_str):
        minutes, seconds = map(int, time_str.split(':'))
        return minutes * 60 + seconds

    df['TimeSeconds'] = df['Time'].apply(time_to_seconds)
    start_time = df['TimeSeconds'].iloc[0]
    df['TimeFromStart'] = df['TimeSeconds'] - start_time

    # Convert Temperature column to float
    df['Temperature'] = df['Temperature'].astype(float)

    # Smooth by averaging per second
    smoothed = df.groupby('TimeFromStart')['Temperature'].mean().reset_index()
    return smoothed

# Process both CSVs
smoothed_A = process_csv('ExperimentA_1.csv')
smoothed_B = process_csv('ExperimentA_2.csv')  # change filename accordingly

# Plot both
plt.figure(figsize=(10,5))
plt.plot(smoothed_A['TimeFromStart'], smoothed_A['Temperature'], 
         marker='o', linestyle='-', color='blue', label='Unisolated termistor')
plt.plot(smoothed_B['TimeFromStart'], smoothed_B['Temperature'], 
       marker='s', linestyle='-', color='red', label='Isolated termistor')

plt.xlabel('Time from start (s)')
plt.ylabel('Temperature (°C)')
plt.title('Temperature vs Time')
plt.grid(True)

# Format x-axis as minutes:seconds
plt.gca().xaxis.set_major_formatter(
    ticker.FuncFormatter(lambda x, pos: f"{int(x//60)}:{int(x%60):02d}")
)

plt.legend()
plt.tight_layout()
plt.show()

