from flask import jsonify
from app.main.model.models import (
    Chats,
)

from app.main.service.content_generators_helper_services import final_response_gen, reasoning_phase, title_gen
from app.main.service.content_upload_helper_services import (
    checkCSV,
    checkIMG,
    checkPDF,
    checkTXT,
    checkURL,
)

from app.main.util.data_extractors import whole_summary_generator
from app.main.util.hash_content_utility import hashblock
from app.main import db
import datetime
from app.main.util.interpreter import execute_step
import chromadb
import threading
import json
import uuid


chromadb_client = chromadb.PersistentClient(path="/chromaDB")


def content_generation(files, txt, chat_id, last_session_id):
    """
    This function is used to generate content based on the given input.

    Parameters:
    -----------
    files: List[FileStorage]
        A list of uploaded files
    txt: str
        The text input by the user
    chat_id: str
        The unique id of the chat session
    last_session_id: str
        The last session id

    Returns:
    --------
    Dict[str, str]
        A dictionary containing the generated content and the last session id
    """
    content = []
    # print(txt)

    if checkTXT(txt) != False:
        content.append(checkTXT(txt))
    else:
        pass
    columns_names = """no file uploaded by the user, if the user prompt requires uploading the data file, 
                        tell him to provide the csv file to retrieve the data for you to provide him with 
                        the appropriete assistant."""
    
    df = None
 
    if files != None:
        for file in files:
            img_check = checkIMG(file)
            if img_check == False:
                pass
            else:
                print("imC")

                content.append(img_check)

            pdf_check = checkPDF(file)
            if pdf_check == False:
                pass
            else:
                print("pdfC")
                content.extend(pdf_check)
            if str(file.filename)[-4:] == ".csv":
                df, columns_names = checkCSV(file)
            else:
                pass
    if last_session_id:
        pass
    else:
        last_session_id = ""
    current_session_id = hashblock(last_session_id + str(datetime.datetime.now()) + txt)
   
    if chat_id:
        pass
    
    else:
        try:
            
            collection = chromadb_client.get_collection(name="m_history_data") # in production we use chat_id
        except:
            
            whole_summary = whole_summary_generator(str(content))
            title = "generate title from the giving summary"
            content_title = title_gen(title + " " + whole_summary)
            # print("title: ", content_title)
            chat_id = hashblock(str(content) + str(datetime.datetime.now()))
            chat_session = Chats(
                # user_id=user_id,
                chat_id=chat_id,
                content="",
                prompt=txt,
                response="",
                title=content_title,
                session_id=current_session_id,
            )
            db.session.add(chat_session)
            db.session.commit()
            collection = chromadb_client.create_collection(name=chat_id) # we use chat_id here in production

    
    
    ids = [str(i) for i in range(1, len(content)+1)]
    collection.upsert(
        documents=content,
      
        ids=ids,
    )
    query_result = collection.query(query_texts=[txt], n_results=2)
    query_result = " ".join(query_result["documents"][0])
    
    # Generate summary
    summary = whole_summary_generator(str(query_result))
    # print("summary: ", summary)

    # Reasoning phase
    steps = reasoning_phase(summary, txt, columns_names)
    # print("steps: ", steps)

    # Generate response
    tasks_results = []
    for step in steps:
        if step.key() == "python_execution":
            response = execute_step(step.value(), df)
            tasks_results.append(response)
        else:
            tasks_results.append(step.value())

    final_response = final_response_gen(tasks_results, txt)
    # print("final response: ", final_response)
    
    collection.upsert(
        documents=[str(final_response)],
        metadatas=[{"source": "chat_session"}],
        ids=[hashblock(final_response)],
    )
    complete_chat_session = Chats(
            chat_id=chat_id,
            # user_id=user_id
            content=content,
            prompt=txt,
            response=final_response,
            title=chat_data.title,
            session_id=current_session_id,
        )
    db.session.add(complete_chat_session )
    db.session.commit()
    
    # return jsonify({"text": final_response, "last_session_id": current_session_id})
    return jsonify({"text": str(final_response), "last_session_id": "current_session_id"})