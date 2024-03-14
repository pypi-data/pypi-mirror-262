from typing import Dict
from .utils.RestWrapper import APIWrapper
from .utils.AppletResponse import SyncResponse
import uuid


class DatasetAI:
    """
    Applet to ask a question on a dataset csv file, it takes dataset id and question as input.
    You can get dataset id by creating a dataset and uploading a csv file to it.
    """

    def __init__(self, dataset_id: str = None, prompt: str = None, conversation_id: str = None):
        self.dataset_id = dataset_id
        self.prompt = prompt
        self.conversation_id = conversation_id

    def run(self) -> SyncResponse:
        """
        Method to run the DatasetAI applet

        Parameters
        ----------
        dataset_id : str
            Dataset id where all the collections are stored
        prompt : str
            Question to be asked on the dataset

        Returns
        -------
        SyncResponse object
           An object with **answer** , **pipeline query** and **conversation_id** 

        """
        if not self.dataset_id:
            raise ValueError("dataset_id is required")

        if not self.prompt:
            raise ValueError("prompt is required")

        if not self.conversation_id:
            self.conversation_id = str(uuid.uuid4())

        payload = {
            "applet_code": "dataset-ai",
            "conversation_id": self.conversation_id,
            "user_params":{
                "dataset_id":self.dataset_id,
                "prompt":self.prompt
            }
        }


        api_response = APIWrapper(payload).execute_sync()
        api_response_json = api_response.json()
        content = api_response_json['content']
        sources= api_response_json.get('msg_info').get('sources')
        response = SyncResponse(
            answer=content, conversation_id=self.conversation_id, sources = sources)
        resp_obj = response.obj()

        return resp_obj

    def create_dataset(self, name: str, description: str = None) -> Dict:
        """
        Method to create a dataset

        Parameters
        ----------
        name : str
            Name of the dataset
        description : str
            Description of the dataset

        Returns
        -------
        dict
            A dict containing the **dataset_id** and **name** of the dataset

        """
        if not name:
            raise ValueError("name is required")
        payload = {
            "name": name,
            "description": description,
        }

        api_response = APIWrapper(payload).create_dataset()
        dataset_id = api_response.get('id')
        self.dataset_id = dataset_id
        name = api_response.get('name')
        return {"datset_id": dataset_id, "name": name}
    
    
    def upload_collection_csv(self, file_path: str, date_format:str ,collection_name: str = None, dataset_id: str = None) -> Dict:
        """
        Method to upload a collection csv to a dataset

        Parameters
        ----------
        collection_name : str
            Name of the collection
        file_path : str
            Path of the csv file to be uploaded
        date_format : str
            Date format of the date column in the csv file
            eg: "dd/mm/yyyy", "mm/dd/yyyy", "dd-mm-yyyy", "mm-dd-yyyy"

        Returns
        -------
        dict
            A dict containing the **dataset_id** and **collection_name** of the collection

        """
        if not self.dataset_id or not dataset_id:
            raise ValueError("dataset_id is required")
        if not file_path:
            raise ValueError("file_path is required")
        if not date_format:
            raise ValueError("date_format is required")
        dataset_id = self.dataset_id if self.dataset_id else dataset_id
        api_response = APIWrapper().upload_collection_csv(dataset_id, file_path, date_format, collection_name)
        
        return {"dataset_id": api_response.get('dataset_id'), "collection_name": api_response.get('name')}