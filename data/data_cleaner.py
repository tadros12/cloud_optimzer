import pandas as pd
import ast

def extract_and_clean_google_trace(input_file="borg_traces_data.csv", output_file="clean_google_jobs.csv", target_jobs=1000):
    print(f"Reading raw data from {input_file}...")
    try:
        df = pd.read_csv(input_file, nrows=5000)
    except FileNotFoundError:
        print(f"Error: Could not find {input_file}.")
        return

    clean_jobs = []
    job_id_counter = 0
    
    for index, row in df.iterrows():
        val = row.get('resource_request', None)
        if pd.isna(val):
            continue
            
        try:
            if isinstance(val, (int, float)):
                cpu_val = float(val)
            elif isinstance(val, str):
                parsed_dict = ast.literal_eval(val)
                cpu_val = parsed_dict.get('cpus', 0.0)
            else:
                continue
            
            if cpu_val > 0:
                clean_jobs.append({
                    'job_id': job_id_counter,
                    'workload_cu': round(cpu_val, 4) 
                })
                job_id_counter += 1
                
        except Exception:
            continue 
            
        if len(clean_jobs) >= target_jobs:
            break
            
    clean_df = pd.DataFrame(clean_jobs)
    clean_df.to_csv(output_file, index=False)
    print(f"✅ Success! Cleaned and saved {len(clean_df)} jobs to '{output_file}'.")

# Run the cleaner
extract_and_clean_google_trace()