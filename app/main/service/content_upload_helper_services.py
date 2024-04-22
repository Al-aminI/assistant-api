from werkzeug.utils import secure_filename
import os
import pandas as pd
from app.main.util.data_extractors import IMG_OCR, PDF_IMG_OCR, XURL


# Initialize boto3 client with DigitalOcean Spaces.
# """session = boto3.session.Session()
# client = session.client('assistantfilestorage',
#                         region_name='assistantfilestorage',  # For example, use your region.
#                         endpoint_url='https://assistantfilestorage.sfo3.digitaloceanspaces.com',  # Use your Spaces endpoint URL.
#                         aws_access_key_id='YOUR_DIGITALOCEAN_ACCESS_KEY',
#                         aws_secret_access_key='YOUR_DIGITALOCEAN_SECRET_KEY')

# bucket_name = 'YOUR_DIGITALOCEAN_SPACE_NAME'"""


# CHECK FOR DATA
def checkPDF(pdf_doc):
    """
    Check if the uploaded file is a PDF.

    Args:
        pdf_doc (bytes): The uploaded PDF file as a byte string.

    Returns:
        Union[List[str], bool]: A list of text lines from the PDF, or False if the file is not a PDF.
    """
    if pdf_doc.filename != None:
        #print(str(pdf_doc.filename)[-4:])
        if str(pdf_doc.filename)[-4:] == ".pdf":
            #pdf_txt_list = []
            #for pdf_doc  in pdf:
            pdf_doc.seek(0)
            
            pdf_filename = secure_filename(pdf_doc.filename)
            #key_name = os.path.join("uploaded_files/", pdf_filename)

            # Upload the file
            #client.upload_fileobj(pdf_doc, bucket_name, key_name)

            # Ensure the target directory exists
            target_directory = "uploaded_files"
            if not os.path.exists(target_directory):
                os.makedirs(target_directory)

            pdf_doc.save(os.path.join("uploaded_files/", pdf_filename))
            texts = PDF_IMG_OCR(pdf_filename)
            
            
            #pdf_txt_list.append(texts)

            return texts
        
        return False
    return False


def checkIMG(img):
    """
    Check if the uploaded file is an image.

    Args:
        img (flask.FileStorage): The uploaded image file.

    Returns:
        Union[List[str], bool]: A list of text lines from the image, or False if the file is not an image.
    """
    if img.filename != None:
        #print(img.filename)
        if img.filename[:4] == ".png" or img.filename[:4] == ".jpg" or img.filename[:5] == ".jpeg":
           
            img.seek(0)
            im_filename = secure_filename(img.filename)

            target_directory = "uploaded_images"
            if not os.path.exists(target_directory):
                os.makedirs(target_directory)

            img.save(os.path.join("uploaded_images/", im_filename))
            texts = IMG_OCR(im_filename)
         

            return texts
        else:
            return False
    else:
        return False        

def checkTXT(txt):
    if txt != None:          
        
        return txt

    return False

def checkURL(vid):
    """
    Check if the uploaded file is a URL.

    Args:
        vid (str): The uploaded URL.

    Returns:
        str: The text from the URL, or False if the file is not a URL.
    """
    if (vid) != None:
        
        text = XURL(vid)
        return text
       
    return False


def checkCSV(csv_file):
    """
    Check if the uploaded file is a CSV.

    Args:
        csv_file (flask.FileStorage): The uploaded CSV file.

    Returns:
        Union[pd.DataFrame, metadata]: A pandas DataFrame of the CSV data, or a JSON string of the CSV metadata.
    """
    if str(csv_file.filename)[-4:] == ".csv":
        csv_file.seek(0)
        csv_filename = secure_filename(csv_file.filename)
        # Ensure the target directory exists
        target_directory = "uploaded_files"
        if not os.path.exists(target_directory):
            os.makedirs(target_directory)

        csv_file.save(os.path.join("uploaded_files/", csv_filename))
        df = pd.read_csv("uploaded_files/" + csv_filename)
        metadata = df.iloc[0].to_json()
      
        return df, metadata