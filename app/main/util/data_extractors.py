import cv2
import pytesseract
from pdf2image import convert_from_path
from langchain.document_loaders import YoutubeLoader
from dotenv import load_dotenv
from langchain import OpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import CharacterTextSplitter
import textwrap
from langchain.document_loaders import PyPDFLoader
# from langchain.text_splitter import RecursiveTextSplitter

#from app.main.util.context_generation_utilities import context_splitter
import os


load_dotenv
pytesseract.pytesseract.tesseract_cmd=r'C:\Program Files\Tesseract-OCR\tesseract'
# pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'
upload_images_directories = os.environ.get('IMAGES_UPLOAD')
upload_files_directories = os.environ.get('FILES_UPLOAD')

# DATA PROCESSING
def PDF_IMG_OCR(input_file):
    """
    Convert a PDF file to a list of strings, where each string is an OCR'd image of the PDF page.

    Args:
        input_file (str): The path to the PDF file.

    Returns:
        List[str]: A list of strings, where each string is an OCR'd image of the PDF page.
    """
    # # Convert PDF pages to images
    # pages = convert_from_path(upload_files_directories + input_file)
    # # Iterate over the pages and apply OCR using pytesseract and add the texts for each page in a list
    # texts = []
    # for i, page in enumerate(pages):
    #     text = pytesseract.image_to_string(page)
        
    #     texts.append(text)
    # return str(texts)
    loader = PyPDFLoader(upload_files_directories + input_file)
    text = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=10,length_function=len,is_separator_regex=False,)
    texts = text_splitter.split_text(str(text))
    # print(texts[1])
    

    return texts


def IMG_OCR(input_file):
    """
    This function takes in an image file as input and applies optical character recognition (OCR) to it using the Pytesseract library.

    Args:
        input_file (str): The path to the image file.

    Returns:
        str: The OCR output of the image file.
    """

    # Iterate over the pages and apply OCR using pytesseract and add the texts for each page in a list
   
    page = upload_images_directories + input_file
    img_cv = cv2.imread(page)

    img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
    text = pytesseract.image_to_string(img_rgb)
    
    return text


def XURL(url):
    """
    This function takes in a youtube video url as input and returns the transcript of the video.

    Args:
        url (str): The youtube video url.

    Returns:
        str: The transcript of the video.
    """
    video_url = url
    loader = YoutubeLoader.from_youtube_url(video_url)
    transcript = loader.load()
    return str(transcript[0])


# SUMMARIZATION CHAIN

def summarizationCHAIN(content):
    """Summarize the input text using the summarization chain.

    Args:
        content (str): The input text to be summarized.

    Returns:
        str: The summarized text.
    """
    openai_llm = OpenAI(openai_api_key = "openai api key",
    model_name="gpt-3.5-turbo-instruct", temperature=0.1
    ) 
    text_splitter = RecursiveCharacterTextSplitter()
    texts = text_splitter.create_documents([str(content)])

    chain = load_summarize_chain(openai_llm, chain_type="map_reduce", verbose=False)
    output_summary = chain.run(texts)
    wrapped_text = textwrap.fill(
        output_summary, break_long_words=False, replace_whitespace=False
    )
 
    return wrapped_text

def content_splitter(doc):
    """
    This function takes in a document as input and splits it into a list of smaller chunks.

    Args:
        doc (str): The document to be split.

    Returns:
        List[str]: A list of smaller chunks.
    """
    text_splitter = RecursiveCharacterTextSplitter()
    texts = text_splitter.create_documents([str(doc)])
    text_splitter = CharacterTextSplitter(chunk_size=200, chunk_overlap=0)
    texts = text_splitter.split_documents(texts)
    
    return texts



def whole_summary_generator(note):
    """
    This function takes in a note as input and returns the whole summary of the note.
    If the length of the note is greater than or equal to 1000 words, the function splits the note into two parts and returns the whole summary of both parts concatenated together.
    If the length of the note is less than 1000 words, the function summarizes the note using the summarization chain and returns the whole summary.

    Args:
        note (str): The note to be summarized.

    Returns:
        str: The whole summary of the note.
    """
    if len(str(note).split()) >= 1000:
       
        note1 = str(note).split()[0:int(len(str(note).split())/2)]
        note2 = str(note).split()[int(len(str(note).split())/2):]

        note1 = summarizationCHAIN(note1)
        note2 = summarizationCHAIN(note2)
        final_noteS = " ".join([str(note1), str(note2)])
        
        return str(final_noteS)
    note = summarizationCHAIN(str(note))
    note = str(note)

    return note

