import os
import openai
from PIL import Image
import pytesseract
import time
import pandas as pd
import csv
import re

#----------------------------------------------------------------#
#This is a script written by Riley Herbst.
#----------------------------------------------------------------#


# Set your OpenAI GPT-3 API key
openai.api_key = "Enter API Key"

# Function to extract text from an image using Tesseract OCR
def extract_text_from_image(image_path):
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        return text
    except Exception as e:
        print(f"Error extracting text from {image_path}: {str(e)}")
        return ""

# Function to categorize text using GPT-3 with retry on rate limit error
def categorize_text_with_gpt3(text):
    prompt = f"Categorize the following text:\n\n{text}\n\nInto Categories of:Taxon,Family,Collector,Collection,Number,Date,Locality,Location,Habitat and Extra Information"
    
    # Retry on rate limit error with a longer fixed delay
    while True:
        try:
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                temperature=0.7,
                max_tokens=150,
            )
            categories = response['choices'][0]['text'].strip().split(",")
            return categories
        except openai.error.RateLimitError as e:
            # Sleep for a longer duration and then retry
            print("Rate limit exceeded. Waiting for 300 seconds.")
            time.sleep(300)  # Sleep for 5 minutes

# Function to extract information from text
def extract_info_from_text(text):
    # Define regex patterns for extracting information
    regex_patterns = {
        'Image': r'Image: (.+)',
        'Taxon': r'Taxon: (.+)',
        'Family': r'Family: (.+)',
        'Collector': r'Collector: (.+)',
        'Collection Number': r'Collection: (.+)',
        'Date': r'Date: (.+)',
        'Locality': r'Locality: (.+)',
        'Location': r'Location: (.+)',
        'Habitat': r'Habitat: (.+)',
        'Extra Information': r'Extra Information: (.+)',
    }

    result = {}
    
    # Extract information using regex patterns
    for key, pattern in regex_patterns.items():
        match = re.search(pattern, text)
        result[key] = match.group(1) if match else ''

    return result

# Process the text file and extract information
def process_text_file(file_path):
    try:
        with open(file_path, 'r') as file:
            contents = file.read()
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return []

    entries = re.split(r'Image: ', contents)[1:]  # Split entries based on the image marker

    data = []
    for entry in entries:
        entry_info = extract_info_from_text('Image: ' + entry)
        data.append(entry_info)

    return data

# Export extracted information to CSV
def export_to_csv(data, csv_file_path):
    fields = list(data[0].keys())

    with open(csv_file_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()
        writer.writerows(data)

if __name__ == "__main__":
    # Path to the folder containing JPG images
    #THIS IS YOUR INITIAL FOLDER FOR IMAGES THIS IS WHERE YOU START
    image_folder = "FOLDER FOR IMAGES PLEASE CHANGE ME"  # Update with your image folder path

    # Create a text file to store the output
    #CHANGE ME TO WHAT YOU WANT OR DONT I DONT CARE
    output_text_file = open("output.txt", "w")

    # Iterate through each file in the folder
    for filename in os.listdir(image_folder):
        if filename.endswith(".jpg") or filename.endswith(".jpeg"):
            image_path = os.path.join(image_folder, filename)
            text = extract_text_from_image(image_path)
            
            if text:
                categories = categorize_text_with_gpt3(text)
                
                print(f"\nImage: {filename}")
                print("Parsed:")
                output_text_file.write(f"\nImage: {filename}\nOutput:\n")
                
                for category in categories:
                    print(category)
                    output_text_file.write(category + "\n")

    # Close the text file
    output_text_file.close()

    print(f"Output written to {output_text_file}")

    # Process the generated text file and extract information
    #YOU NEED TO CHANGE THESE AS WELL!
    #MAKE SURE THAT THE INPUT FILE PATH IS THE SAME AS THE OUTPUT THAT YOU INITALLY GENERATE. 
    # JUST MAKE IT THE SAME AS WHAT YOU HAVE ON LINE 107
    #MAKE SURE ITS NOT JUST THE NAME YOU NEED THE PATHS 
    input_file_path = "C:\\Users\\riley\\OneDrive\\Desktop\\CodeForMe\\python\\output16.txt"
    #SPREADSHEET OUTPUT NAME IT WHATEVER YOU LIKE AND PUT IT WHEREVER YOU LIKE 
    output_csv_file_path = "C:\\Users\\riley\\OneDrive\\Desktop\\CodeForMe\\python\\textout4.csv"

    extracted_data = process_text_file(input_file_path)
    if extracted_data:
        export_to_csv(extracted_data, output_csv_file_path)
        print(f"Data exported to '{output_csv_file_path}'.")
        print(f"All Done!")
