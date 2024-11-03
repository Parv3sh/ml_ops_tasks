import os
import json

results_dir = './results'
best_trial = None
best_mse = float('inf')

for file_name in os.listdir(results_dir):
    if file_name.endswith('.json'):
        with open(os.path.join(results_dir, file_name), 'r') as f:
            result = json.load(f)
            if result['mse'] < best_mse:
                best_mse = result['mse']
                best_trial = result

print("Best hyperparameters found:")
print(best_trial)
