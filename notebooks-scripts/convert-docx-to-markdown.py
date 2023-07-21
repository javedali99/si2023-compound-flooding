"""
Description: This script converts a Microsoft Word (.docx) document to Markdown format. The conversion is carried out
paragraph by paragraph, where each paragraph's text is extracted and a newline character is appended at the end to
denote a paragraph in Markdown. Currently, text styling (like bold or italic) is not supported in the conversion. 
The final Markdown text is saved into an 'output.md' file.

Author: Javed Ali (javed.ali@ucf.edu)

Date: July 21, 2023

"""

# Import the Document class from the docx module.
from docx import Document


# This function converts a docx paragraph to markdown.
def convert_paragraph(paragraph):
    """
    Convert a docx paragraph to markdown.

    This function extracts the text from a paragraph in a docx file and adds a newline character at the end.

    Args:
        paragraph (docx.text.paragraph.Paragraph): The docx paragraph to be converted.

    Returns:
        str: The text of the paragraph in markdown format.
    """
    # This function currently doesn't handle elements like bold or italic text.
    # The text from the paragraph is extracted and a newline character is added at the end to create a markdown paragraph.
    return paragraph.text + "\n"


# This function converts a docx file to markdown.
def docx_to_md(path_to_docx):
    """
    Convert a docx file to markdown.

    This function opens a docx file, converts each paragraph to markdown using the convert_paragraph function, and concatenates them.

    Args:
        path_to_docx (str): The path to the docx file to be converted.

    Returns:
        str: The content of the docx file in markdown format.
    """
    # Open the docx file.
    document = Document(path_to_docx)

    # Initialize an empty string to store the markdown content.
    markdown = ""

    # Iterate over each paragraph in the document.
    for paragraph in document.paragraphs:
        # Convert the paragraph to markdown and add it to the markdown content.
        markdown += convert_paragraph(paragraph)

    # Return the markdown content.
    return markdown


# Path to the .docx file to be converted.
path_to_docx = "docs/Report draft_ Compound flooding NY City.docx"

# Convert the .docx file to markdown.
markdown = docx_to_md(path_to_docx)

# Write the markdown content to a file.
# The 'w' mode is used to overwrite the file if it already exists.
with open("output.md", "w") as f:
    f.write(markdown)
