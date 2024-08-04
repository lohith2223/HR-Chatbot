import PyPDF2
import re
import google.generativeai as genai
import os

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text

# Function to clean text
def clean_text(text):
    # Remove non-alphabetic characters, symbols, and numbers
    cleaned_text = re.sub(r'[^a-zA-Z\s]', '', text)
    # Convert to lowercase
    cleaned_text = cleaned_text.lower()
    # Remove extra whitespaces
    cleaned_text = ' '.join(cleaned_text.split())
    return cleaned_text

# Extract and clean text from PDF files
pdf_files = ["/content/Employee Manuals.pdf", "/content/FAQ.pdf", "/content/HRPolicy.pdf"]
all_cleaned_text = ""

for pdf_file in pdf_files:
    raw_text = extract_text_from_pdf(pdf_file)
    cleaned_text = clean_text(raw_text)
    all_cleaned_text += cleaned_text + " "

# Remove any trailing whitespace
all_cleaned_text = all_cleaned_text.strip()

# Configure Gemini API
genai.configure(api_key='AIzaSyCU40DkMBOwXFzI6VHXmOHgHxR78-1hG5M')

# Initialize the GenerativeModel
model = genai.GenerativeModel(model_name='gemini-pro')

def get_response(question):
    # Generate content based on the question and stored text
    response = model.generate_content(f"{all_cleaned_text}\n\n{question}")
    return response.text.strip()

# FAQ dictionary
faqs = {
    "leave policy": "Employees are entitled to 6 leaves per month, with a maximum of 30 leaves per year.",
    "work hours": "Standard work hours are 9 AM to 5 PM, Monday to Friday.",
    "dress code": "Business casual attire is required in the office.",
    "benefits": "We offer health insurance, 401(k), and annual performance bonuses."
}

def view_faqs():
    print("FAQs:")
    for question, answer in faqs.items():
        print(f"Q: {question.capitalize()}")
        print(f"A: {answer}\n")

def hr_chatbot():
    print("Welcome to the HR Chatbot!")

    while True:
        print("\nWhat would you like to do?")
        print("1. View FAQ")
        print("2. Ask a question")
        print("3. Quit")

        choice = input("Enter your choice (1-3): ")


        if choice == '1':
            view_faqs()
        elif choice == '2':
            question = input("What's your question? ")
            response = get_response(question)
            print(f"Bot: {response}")
        elif choice == '3':
            print("Thank you for using the HR Chatbot. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    hr_chatbot()
