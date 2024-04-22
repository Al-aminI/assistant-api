from flask_restx import Namespace, fields
from werkzeug.datastructures import FileStorage



class UploadContentDto:
    
    api = Namespace('uploadGenerate', description='content upload and chat related operations')
    
    combined_parser = api.parser()
    combined_parser.add_argument('files', location='files', type=FileStorage, required=False, action='append')
    combined_parser.add_argument('last_session_id', location='form', type=str, required=False)
    combined_parser.add_argument('chat_id', location='form', type=str, required=False)
    combined_parser.add_argument('text', location='form', type=str, required=False)
    # combined_parser.add_argument('vid_links', location='form', type=str, required=False)
    
 