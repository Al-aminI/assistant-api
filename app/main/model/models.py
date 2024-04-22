
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import Column, DateTime 
from .. import db, flask_bcrypt
import datetime

from ..config import key

from typing import Union
from sqlalchemy.dialects.postgresql import ARRAY
import logging
import os






class Chats(db.Model):
    """ Model for storing all of the extracted content from the documents uploaded by the user and the chat sessions"""
    #__tablename__ = "contents_uploaded"
    id = db.Column("id",db.Integer, primary_key=True)
    title = db.Column("title", db.String(500))
    # user_id = db.Column("user_id", db.String(500))
    chat_id = db.Column("content_id", db.String(500))
    content = db.Column("content", db.String(500000))
    prompt = db.Column("prompt", db.String(5000))
    response = db.Column("response", db.String(500))
    time = Column(DateTime(timezone=True), server_default = func.now()) 

    def __init__(self, chat_id, content, prompt, title, response, session_id):
        self.chat_id = chat_id
        # self.user_id = user_id
        self.content = content
        self.prompt = prompt
        self.title = title
        self.response = response
        self.session_id = session_id
