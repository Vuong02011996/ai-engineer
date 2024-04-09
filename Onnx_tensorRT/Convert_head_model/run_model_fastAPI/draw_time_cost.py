import matplotlib
matplotlib.use('tkagg')
import matplotlib.pyplot as plt
import pandas as pd
# Read DataFrame from text file
loaded_df = pd.read_csv('model_head_100.txt')

# Convert DataFrame back to array
loaded_array = loaded_df['Values'].tolist()

print("Loaded array:", loaded_array)

# loaded_array = loaded_array[100:len(loaded_array)]

plt.plot(range(len(loaded_array)), loaded_array, marker='o', linestyle='-')
plt.show()
