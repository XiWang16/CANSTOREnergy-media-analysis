import PyPDF2, spacy, os, re
CREDIT_TEXT = "CREDIT: " # Text that precedes the listing of author(s) for pieces other than Letters to the Editor
KEYWORDS = ["Hamilton", "energy"]
LETTER = "letter"
DEFAULT_TYPE = "article"

# load the en_core_web_trf model, which prioritizes accuracy
# the alternative is en_core_web_sm, which prioritizes speed
nlp = spacy.load("en_core_web_trf")

def process_pdfs_in_directory(directory):
    """Process all PDF files in the given directory."""
    for filename in os.listdir(directory):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(directory, filename)
            print(f"Processing {pdf_path}")
            texts = extract_text_from_pdf(pdf_path)
            
            # Get title 
            title = extract_title(texts[0])
            
            # Get author(s)
            authors = extract_authors(texts)
                
def extract_text_from_pdf(pdf_path):
    """Extract text from each page of the PDF."""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        texts = [reader.pages[page_num].extract_text() for page_num in range(len(reader.pages))]
    return texts

def extract_title(text):
    """
    Extract the title of the news piece that contains the keywords in the KEYWORDS list.
    This will work for all of News Articles, Opinion Pieces, Letters to the Editor, and Information Briefs.
    """
    lines = text.split('\n')
    title = None
    
    # Find the first non-empty line
    for line in lines:
        stripped_line = line.strip()
        if stripped_line:
            title = stripped_line
            break
    
    if title and title.lower() != "readers write":
        print(f"Article Title: {title}")
    else:  # the piece is a Letter to the Editor
        title = find_standalone_phrase(text)
        if title is not None:
            print(f"Letter to the Editor Title: {title}")
        else:
            print("No title found for the Letter to the Editor.")
    
    return title

def find_standalone_phrase(text, search_before=True):
    """Find the last standalone phrase before or after the paragraph in which any keyword in KEYWORDS occurred."""
    # Split the document into paragraphs
    paragraphs = text.split('\n\n')
    
    # Compile a regex pattern to find any keyword in the KEYWORDS list, ignoring case
    keyword_pattern = re.compile(r'\b(?:' + '|'.join(KEYWORDS) + r')\b', re.IGNORECASE)
    
    for i, paragraph in enumerate(paragraphs):
        if keyword_pattern.search(paragraph):
            if search_before:
                # Find the last standalone phrase preceding this paragraph
                for j in range(i - 1, -1, -1):
                    # Split the paragraph into lines
                    lines = paragraphs[j].split('\n')
                    for line in reversed(lines):
                        # Check if the line is a standalone phrase (not a complete sentence)
                        if line and not re.search(r'[.!?]$', line.strip()):
                            return line.strip()
            else:
                # Find the first standalone phrase following this paragraph
                for j in range(i + 1, len(paragraphs)):
                    # Split the paragraph into lines
                    lines = paragraphs[j].split('\n')
                    for line in lines:
                        # Check if the line is a standalone phrase (not a complete sentence)
                        if line and not re.search(r'[.!?]$', line.strip()):
                            return line.strip()
            break
    return None

def extract_authors(text, content_type=DEFAULT_TYPE):
    """
    Extract the authors of the news piece.
    If the type is "letter", use the find_standalone_phrase function to find the author.
    Otherwise, use the CREDIT_TEXT to locate the authors.
    """

    if content_type == LETTER:
        # Use find_standalone_phrase to find the author
        author_line = find_standalone_phrase(text, False)
        if author_line:
            authors = author_line.extract_person_entities(author_line)
    else:
        # Use CREDIT_TEXT to locate the authors
        credit_index = text.find(CREDIT_TEXT)
        if credit_index != -1:
            credit_text = text[credit_index + len(CREDIT_TEXT):]
            lines = credit_text.split('\n')
            for line in lines:
                stripped_line = line.strip()
                if stripped_line:
                    authors = author_line.extract_person_entities(stripped_line)
                    break

    # Remove duplicates
    authors = list(set(authors))

    if authors:
        print(f"Authors: {', '.join(authors)}")
    else:
        print("No authors found.")

    return authors

def extract_person_entities(text):
    """
    Extract entities with the "PERSON" label from the given text.
    
    Args:
    text (str): The text to process.
    
    Returns:
    list: A list of entities with the "PERSON" label.
    """
    # Process the text with spaCy
    doc = nlp(text)
    
    # Extract entities with the "PERSON" label
    person_entities = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
    
    return person_entities

if __name__ == "__main__":
    directory = '.'  # the directory that contains the PDF files
    process_pdfs_in_directory(directory)
################################################################################


################### Attempts to use NLTK for text analysis ###################
# import nltk
# from nltk.corpus import movie_reviews
# from nltk import FreqDist
# fids = movie_reviews.fileids()
# # print(fids)
# fd = FreqDist(movie_reviews.words('pos/cv869_23611.txt'))
################################################################################



############## Attempts to use PyPDF2 for text preprocessing ##############
