import os

def increment_filename(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            
            if file.endswith(".mp4"):
                i =0
                try:
                    base, ext = os.path.splitext(file)
                    num = int(base)
                    new_name = f"{num + 1}{ext}"
                    os.rename(os.path.join(root, file), os.path.join(root, new_name))
                    print(f"Renamed {file} to {new_name}")
                except ValueError:
                    print(f"Skipping {file}, as it does not have a numeric name")

if __name__ == "__main__":
    base_directory = os.path.join(os.getcwd(), './')
    increment_filename(base_directory)
