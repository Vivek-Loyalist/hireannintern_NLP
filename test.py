import re
import fitz
import boto3

# Create a session using your AWS credentials
# session = boto3.Session(
#     aws_access_key_id='AKIAYSHIUCYP5VPIETBH',
#     aws_secret_access_key='uwEdNMY7OqECH+rBY1TaxMgJmrYx0vq8Zmfke4Op',
#     region_name='ca-central-1'
# )

session = boto3.Session(
    aws_access_key_id='AKIAWTDAAMMFRCMP56VN',
    aws_secret_access_key='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',
    region_name='ca-central-1'
)


# Specify the S3 bucket name
bucket_name = 'hireanintern-resume'

# Initialize variables to track the latest object and timestamp
latest_object = None
latest_timestamp = None

# List objects in the bucket
s3 = session.client('s3')
objects = s3.list_objects_v2(Bucket=bucket_name)

# Iterate through the objects to find the latest one
if 'Contents' in objects:
    for obj in objects['Contents']:
        if 'Key' in obj and obj['LastModified']:
            if latest_timestamp is None or obj['LastModified'] > latest_timestamp:
                latest_timestamp = obj['LastModified']
                latest_object = obj

# Check if a latest object was found
if latest_object:
    resume_object_key = latest_object['Key']

    # Local file path for the text file on your machine
    job_file_path = r'/Users/vivekgurram/Desktop/Final_Project/Final-Project/artificial_intelligence/job.txt'  # Replace with the actual path

    # Local file path where the resume PDF will be saved
    resume_file_path = r'/Users/vivekgurram/Desktop/Final_Project/Final-Project/artificial_intelligence/resume1.pdf'

    # Download the latest resume PDF from Amazon S3
    s3.download_file(bucket_name, resume_object_key, resume_file_path)

    # Function to extract text from a PDF file using PyMuPDF (Fitz)
    def extract_text_from_pdf(file_path):
        pdf_text = ""
        try:
            pdf_document = fitz.open(file_path)
            for page_num in range(pdf_document.page_count):
                page = pdf_document.load_page(page_num)
                pdf_text += page.get_text()
        except Exception as e:
            print(f"An error occurred while extracting text from PDF: {e}")
        return pdf_text

    # Function to read the content of a text file
    def read_text_file(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            print(f"File not found at {file_path}")
            return ""
        except Exception as e:
            print(f"An error occurred: {e}")
            return ""

    # Read the content of the job description text file
    job_contents = read_text_file(job_file_path)

    if job_contents:
        # Extract words from the resume PDF and job description text file
        def extract_words(text):
            words = re.findall(r'\b\w+\b', text)
            return set(words)

        resume_contents = extract_text_from_pdf(resume_file_path)
        resume_words = extract_words(resume_contents)
        job_words = extract_words(job_contents)

        # Calculate Jaccard similarity between words
        word_similarity = (len(resume_words.intersection(job_words)) / len(resume_words.union(job_words))) * 100

        # Print the word similarity as a numeric value
        print(word_similarity)
    else:
        print("Unable to compare. Check your file paths and file contents.")
else:
    print(f"No objects found in the '{bucket_name}' bucket.")



# import re
# import fitz
# import boto3

# # Create a session using your AWS credentials
# session = boto3.Session(
#     aws_access_key_id='AKIAYSHIUCYP5VPIETBH',
#     aws_secret_access_key='uwEdNMY7OqECH+rBY1TaxMgJmrYx0vq8Zmfke4Op',
#     region_name='ca-central-1'
# )

# # Specify the S3 bucket name
# bucket_name = 'hireanintern'

# # Initialize variables to track the latest object and timestamp
# latest_object = None
# latest_timestamp = None

# # List objects in the bucket
# s3 = session.client('s3')
# objects = s3.list_objects_v2(Bucket=bucket_name)

# # Iterate through the objects to find the latest one
# if 'Contents' in objects:
#     for obj in objects['Contents']:
#         if 'Key' in obj and obj['LastModified']:
#             if latest_timestamp is None or obj['LastModified'] > latest_timestamp:
#                 latest_timestamp = obj['LastModified']
#                 latest_object = obj

# # Check if a latest object was found
# if latest_object:
#     resume_object_key = latest_object['Key']

#     # Local file path for the text file on your machine
#     job_file_path = r'/Users/vivekgurram/Desktop/Final_Project/Final-Project/artificial_intelligence/job.txt'  # Replace with the actual path

#     # Local file path where the resume PDF will be saved
#     resume_file_path = r'/Users/vivekgurram/Desktop/Final_Project/Final-Project/artificial_intelligence/resume1.pdf'

#     # Download the latest resume PDF from Amazon S3
#     s3.download_file(bucket_name, resume_object_key, resume_file_path)

#     # Function to extract text from a PDF file using PyMuPDF (Fitz)
#     def extract_text_from_pdf(file_path):
#         pdf_text = ""
#         try:
#             pdf_document = fitz.open(file_path)
#             for page_num in range(pdf_document.page_count):
#                 page = pdf_document.load_page(page_num)
#                 pdf_text += page.get_text()
#         except Exception as e:
#             print(f"An error occurred while extracting text from PDF: {e}")
#         return pdf_text

#     # Function to read the content of a text file
#     def read_text_file(file_path):
#         try:
#             with open(file_path, 'r', encoding='utf-8') as file:
#                 return file.read()
#         except FileNotFoundError:
#             print(f"File not found at {file_path}")
#             return ""
#         except Exception as e:
#             print(f"An error occurred: {e}")
#             return ""

#     # Read the content of the job description text file
#     job_contents = read_text_file(job_file_path)

#     if job_contents:
#         # Extract words from the resume PDF and job description text file
#         def extract_words(text):
#             words = re.findall(r'\b\w+\b', text)
#             return set(words)

#         resume_contents = extract_text_from_pdf(resume_file_path)
#         resume_words = extract_words(resume_contents)
#         job_words = extract_words(job_contents)

#         # Calculate Jaccard similarity between words
#         word_similarity = (len(resume_words.intersection(job_words)) / len(resume_words.union(job_words))) * 100

#         # Print the word similarity as a numeric value with two decimal places
#         print(f"Jaccard Similarity: {word_similarity:.2f}%")
#     else:
#         print("Unable to compare. Check your file paths and file contents.")
# else:
#     print(f"No objects found in the '{bucket_name}' bucket.")
