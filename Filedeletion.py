import os
import time

def delete_jpg_within_last_24_hours(folder_path):
    # 24 hours in seconds
    time_interval = 24 * 60 * 60
    current_time = time.time()

    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".png"):
            file_path = os.path.join(folder_path, filename)
            try:
                file_mtime = os.path.getmtime(file_path)
                if current_time - file_mtime <= time_interval:
                    os.remove(file_path)
                    print(f"Deleted (recent): {file_path}")
            except Exception as e:
                print(f"Error handling file {file_path}: {e}")


folder_to_clean = "C:/Users/ARPIT/OneDrive/Desktop/Cheating-Surveillance-System-main/log"  
Response = input("DO YOU WANT TO KEEP THE SNAPSHOTS (Y/N): ")
if Response == 'Y':
    delete_jpg_within_last_24_hours(folder_to_clean)
else:
    print("THE SNAPSHOTS ARE STORED IN LOG FOLDER")