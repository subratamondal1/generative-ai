from pathlib import Path

import docx


def list_docx_files(folder_path):
    path = Path(folder_path)
    return [file.name for file in path.glob(pattern="*.docx") if file.is_file()]


def split_docx(file_path):
    doc = docx.Document(file_path)
    full_text = "\n".join([para.text for para in doc.paragraphs])
    return full_text.split("****")


files: list[str] = list_docx_files(folder_path="./ca-fo-p1-c1")


def create_documents(file_path: str):
    sections = split_docx(file_path=file_path)
    sections = [section.strip() for section in sections]
    sections.remove(sections[0])
    course_name = sections[0]
    sections.remove(course_name)
    chapter_name = sections[0]
    sections.remove(chapter_name)
    print(course_name)
    print(chapter_name)
    print(len(sections))
    print(sections)


create_documents(file_path="./ca-fo-p1-c1/CA-FO-P1-C1-Unit 1-Ashok.docx")
