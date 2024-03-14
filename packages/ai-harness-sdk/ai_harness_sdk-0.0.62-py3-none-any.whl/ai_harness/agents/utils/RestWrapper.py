"""REST API server for ai-harness-sdk."""
import requests
import os
import time


class APIWrapper:
    """
    to call the api's of the ai-harness server 

    Parameters
    ----------
    params: dict 
        payload: data to be sent to the server
    """

    def __init__(self, payload=None):
        self.payload = payload
        self.api_key, self.base_url = self.get_credentials()
        self.headers = {'API-Key': self.api_key}

    def get_credentials(self):
        api_key = os.environ.get("AI_HARNESS_API_KEY")
        base_url = os.environ.get('AI_HARNESS_BASE_URL')
        return api_key, base_url

    def execute_sync(self):
        """
        method for calling an api to complete the applet tasks synchronously

        Returns
        ----------
        response
            dict-like object containing content , msg_info and conversation_id as a id of the conversation

        """

        api_key, base_url = self.get_credentials()
        endpoint = '/api/conversations/complete'
        url = f"{base_url}{endpoint}"

        try:
            response = requests.post(
                url, headers=self.headers, json=self.payload, params=None)
            return response
        except Exception as e:
            raise Exception(f"An error occurred: {str(e)}")

    # it is method for calling an api to complete the applet tasks asynchronously
    def execute_async(self):
        """
        method for calling an api to submit the applet task to start running asynchronously

        Returns
        ----------
        data : dict-like object
            conversation_id : conversation_id of the async api call
        message : str
            message of the async api call whether the job is submitted or not

        """

        try:
            api_key, base_url = self.get_credentials()
            endpoint = '/api/conversations/execute/async'
            url = base_url + endpoint
            response = requests.post(
                url, headers=self.headers, json=self.payload, params=None)
            return response
        except Exception as e:
            raise Exception(f"An error occurred: {str(e)}")

    def getAsyncRunStatus(self, conversation_id: str, applet_code: str):
        """
        method for calling an api to get the status of the async api call

        Parameters
        ----------
        conversation_id: str
            id of the conversation for respective applet
        applet_code: str
            code of the applet for which the answer is to be fetched

        Returns
        ----------
            data : dict-like object
                processing_job_status : either completed or processing or failed or waiting
                conversation_id : id of the conversation for respective applet

        """

        try:
            api_key, base_url = self.get_credentials()
            url = f"{base_url}/api/conversations/{conversation_id}/state?applet_code={applet_code}"

            while True:
                response = requests.get(url, headers=self.headers)
                res = response.json()

                if res['data']['processing_job_status'] == 'completed':
                    async_api_answer = self.getConversationData(
                        conversation_id, applet_code)
                    return async_api_answer
                elif res['data']['processing_job_status'] == 'processing':
                    # Continue polling for status while processing
                    time.sleep(2)
                elif res['data']['processing_job_status'] == 'waiting':
                    # Continue polling for status while waiting
                    time.sleep(2)
                else:
                    raise Exception("Processing job failed")
        except Exception as e:
            raise Exception(f"An error occurred: {str(e)}")

    def getConversationData(self, conversation_id: str, applet_code: str):
        """
        method for calling an api to get the answer of the applet based on conversation id and applet code

        Parameters
        ----------
        conversation_id: str
            id of the conversation for respective applet
        applet_code: str
            code of the applet for which the answer is to be fetched

        Returns
        ----------
            data : dict-like object
                answer : answer of the applet
                conversation_id : id of the conversation for respective applet

        """
        try:
            api_key, base_url = self.get_credentials()
            url = f"{base_url}/api/conversations/{conversation_id}?applet_code={applet_code}"
            response = requests.get(url, headers=self.headers)
            res = response.json()
            return res['data']['answer']
        except Exception as e:
            raise Exception(f"An error occurred: {str(e)}")


    def speech_to_text(self, audio_file_path: str):
        """
        method for calling an api to convert audio to text

        Parameters
        ----------
        audio_file_path: str
            path of the audio file to be converted to text

        Returns
        ----------
            text : text converted from audio file
                

        """
        try:
            api_key, base_url = self.get_credentials()
            url = f"{base_url}/api/conversations/speech-to-text"
            with open(audio_file_path, 'rb') as file:
                files = {"files": file}
                response = requests.post(url, headers=self.headers, files=files)
            res = response.json()
            return res['data']
        except Exception as e:
            raise Exception(f"An error occurred: {str(e)}")
        
    def create_dataset(self):
        try:
            api_key, base_url = self.get_credentials()
            url = f"{base_url}/api/dataset"
        
            response = requests.post(url, json=self.payload, headers=self.headers)
            res = response.json()
            res= res.get('data')
            if not res:
                raise Exception(response.json())
            return res
        except Exception as e:
            raise Exception(f"An error occurred: {str(e)}")
        
    def upload_collection_csv(self, dataset_id:str, file_path: str, date_format:str ,collection_name: str = None):
        try:
            api_key, base_url = self.get_credentials()
            url = f"{base_url}/api/dataset/{dataset_id}/collection"
            files = {'files': open(file_path, 'rb')}
            data = {
                "name": collection_name,
                "date_format": date_format
            }
            response = requests.post(url, data=data, headers=self.headers, files=files)
            res = response.json()
            res= res.get('data')
            if not res:
                raise Exception(response.json())
            return res
        except Exception as e:
            raise Exception(f"An error occurred: {str(e)}")