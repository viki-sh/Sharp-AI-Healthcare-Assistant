import csv

def save_to_csv(data, file_path="patient_data.csv"):
    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([data['name'], data['age'], data['symptoms']])