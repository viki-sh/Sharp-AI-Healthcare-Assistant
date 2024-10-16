import openai

def extract_key_info_from_gpt_response(response):
    """ 
    Extract structured data like name, age, and symptoms from GPT's response. 
    This function assumes the GPT response contains natural language information about a person.
    """
    structured_prompt = f"Extract and return in a structured format: Name, Age, Symptoms from the following response: {response}"
    
    extracted_response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": structured_prompt}
        ]
    )
    
    return extracted_response.choices[0].message['content']

def save_to_csv(data, file_path="patient_data.csv"):
    """ 
    Saves the extracted data to a CSV file 
    """
    import csv
    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([data['name'], data['age'], data['symptoms']])

if __name__ == "__main__":
    # Example response from GPT (for testing purposes, replace with actual response)
    example_response = "The patient named John, aged 30, is experiencing headaches and fever."
    
    # Extract the information
    extracted_info = extract_key_info_from_gpt_response(example_response)
    print(f"Extracted Info: {extracted_info}")
    
    # Simulated data extraction (this would be replaced by actual structured data)
    data = {"name": "John", "age": 30, "symptoms": "headaches, fever"}
    
    # Save the extracted info to CSV
    save_to_csv(data)
