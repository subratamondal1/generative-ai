from pathlib import Path

import docx


# Function to list all .docx files in a given folder
def list_docx_files(folder_path, file_extension=".docx"):
    path = Path(folder_path)
    # Using glob to find files that match the pattern *[file_extension]
    return [file.name for file in path.glob(f"*{file_extension}") if file.is_file()]


# Example: Listing all .docx files in the folder "./ca-fo-p1/Chapter 2"
files = list_docx_files(folder_path="./ca-fo-p1/Chapter 2")
print("List of .docx files:", files)


# Function to read a .docx file, join paragraph texts, and split it by "****"
def split_docx(file_path):
    doc = docx.Document(file_path)
    # Join all paragraphs with newline character
    full_text = "\n".join([para.text for para in doc.paragraphs])
    # Split the full text by the separator "****"
    return full_text.split("****")


# Specify the DOCX file to work on
file_path = "./ca-fo-p1-c1/CA-FO-P1-C1-Unit 1-Ashok.docx"
# Split the document into sections using the defined function
sections = split_docx(file_path=file_path)
# Remove any leading/trailing whitespace from each section
sections = [section.strip() for section in sections]

# Debug prints to check the number of sections and their content
print("Number of sections found:", len(sections))
print("Sections:", sections)

# Remove the first section (assumed to be unwanted metadata/header)
sections.remove(sections[0])

# Extract the collection name and chapter name based on the new order of sections
collection_name = sections[0]
print("Collection Name:", collection_name)
chapter_name = sections[1]
print("Chapter Name:", chapter_name)

# Remove the already extracted collection name and chapter name from sections
sections.remove(collection_name)
sections.remove(chapter_name)


# This function encapsulates the document processing steps and returns:
# - course_name: the first remaining section after removing the header.
# - chapter_name: the subsequent section.
# - sections: the list of the rest of the content sections.
def create_documents(file_path: str):
    # Split the document into sections
    sections = split_docx(file_path=file_path)
    # Remove extra whitespace
    sections = [section.strip() for section in sections]
    # Remove the first section (e.g., header or title)
    sections.remove(sections[0])

    # Assume the first section now is the course name
    course_name = sections[0]
    sections.remove(course_name)

    # Next, assume the first section is the chapter name
    chapter_name = sections[0]
    sections.remove(chapter_name)

    # Return the course name, chapter name, and the remaining sections
    return course_name, chapter_name, sections


# Use the helper function to get the structured document parts
course_name, chapter_name, sections = create_documents(file_path=file_path)

# Debug prints for course name, chapter name, and remaining sections
print("Course Name:", course_name)
print("Chapter Name:", chapter_name)
print("Number of remaining sections:", len(sections))
print("Remaining sections:", sections)
