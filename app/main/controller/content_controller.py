
from flask_restx import Resource
from typing import Dict, Tuple
from app.main.service.content_generation_service import content_generation

from flask_cors import CORS, cross_origin

from app.main.util.dto import UploadContentDto



api = UploadContentDto.api
_contentFields = UploadContentDto.combined_parser


@api.produces('multipart/form-data')
@api.route('/uploadAndChat')

class UploadContents(Resource):
    @api.doc('upload content and chat')
   
    @api.expect(_contentFields, validate=True)
    @api.response(201, 'prompt processed successifully.')
    @api.doc('upload files(PDF/CSV), youtube tutorials and podcasts links and prompt it to get a seamless assistant ')
    def post(self):
        """
        This function takes in a list of files, a prompt text, a chat id, and the last session id.
        It then sends the files and prompt to the content generation service, which returns a response.
        If the response is empty, it returns a 404 Not Found error.
        Otherwise, it returns the response.
        """
        
        # Access other fields from the 'contents' model using request.json
        args = UploadContentDto.combined_parser.parse_args()
        files = args['files']
        print(files)
        text = args['text']
        # vid_links = args['vid_links']
        chat_id = args['chat_id']
        last_session_id = args['last_session_id']
        response = content_generation(files, text, chat_id, last_session_id)
        if not response:
            api.abort(404)
        else:
            return response
        
@api.route('/check-status')
class CheckServiceStatus(Resource):
    """
    Health check
    """
    
    @api.doc('Check service status')
    def post(self) -> Tuple[Dict[str, str], int]:
        """
        Check the status of the service.

        Returns:
            A JSON object containing a status field with the value "success".
        """
        response_object = {'status': 'success'}
        return response_object, 200
        
 
    
   