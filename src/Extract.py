import openai
import csv

# Hardcoded OpenAI API key
openai.api_key = ''  # Replace with your actual API key

def ask_gpt(message_history):
    """
    Function to interact with the OpenAI API using the conversation history.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",  # Use GPT-4 if available, otherwise GPT-3.5-turbo
        messages=message_history
    )
    return response['choices'][0]['message']['content']

def save_to_csv(data, file_path="patient_data.csv"):
    """
    Saves the extracted data to a CSV file.
    :param data: A dictionary with 'name', 'age', and 'symptoms'.
    :param file_path: The CSV file path (default is "patient_data.csv").
    """
    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([data.get('name'), data.get('age'), data.get('symptoms')])

if __name__ == "__main__":
    # Conversation history to be used by GPT
    conversation_history = [
        {"role": "system", "content": "You are a helpful medical assistant that can book appointments."},
        {"role": "assistant", "content": "Hello! How can I assist you today?"}
    ]

    # Step 1: Ask how the bot can help
    print("Bot: Hello! How can I assist you today?")
    user_input = input("You: ")
    conversation_history.append({"role": "user", "content": user_input})

    # Step 2: Check if the user wants to book an appointment
    if "appointment" in user_input.lower():
        print("Bot: Sure, I can book that appointment.")
        conversation_history.append({"role": "assistant", "content": "Sure, I can book that appointment."})

        # Step 3: Ask for the user's name
        print("Bot: May I have your name?")
        user_name = input("You (Name): ")
        conversation_history.append({"role": "user", "content": user_name})

        # Step 4: Ask for the user's age
        print("Bot: May I know your age?")
        user_age = input("You (Age): ")
        conversation_history.append({"role": "user", "content": user_age})

        # Step 5: Ask for the user's symptoms
        print("Bot: Please describe your symptoms.")
        user_symptoms = input("You (Symptoms): ")
        conversation_history.append({"role": "user", "content": user_symptoms})

        # Step 6: Confirm the booking details
        print(f"Bot: Thank you! I have your details as:\nName: {user_name}\nAge: {user_age}\nSymptoms: {user_symptoms}.")
        print("Bot: Your appointment will be booked shortly.")

        # Extract the relevant data (name, age, symptoms)
        extracted_data = {
            "name": user_name.strip(),
            "age": user_age.strip(),
            "symptoms": user_symptoms.strip()
        }

        # Save the extracted info to CSV
        save_to_csv(extracted_data)

        print("The information has been saved to 'patient_data.csv'.")

    else:
        # If the user does not want to book an appointment
        print("Bot: I'm here to assist with medical appointments and symptoms. How else can I help you?")
