from .utils.RestWrapper import APIWrapper
from .utils.AppletResponse import SyncResponse
import uuid


class Conversation:
    """
    Applet for interactive conversations. a question is provided as input to the applet
    and it allows user to continue the conversation using the applet
    and can asks multiple questions to the applet and the applet responds to the questions asked by the user ,
    user can also asks question through voice by providing the audio file path
    """

    def __init__(self, prompt: str = None, audio_file_path:str = None , conversation_id: str = None):
        self.prompt = prompt
        self.conversation_id = conversation_id
        self.audio_file_path = audio_file_path

    def run(self) -> SyncResponse:
        """
        Method to run the Conversation applet

        Parameters
        ----------
        prompt : str
            question to be asked to the AI agent
        audio_file_path : str
            path of the audio file of a voice to be used to ask the question
        conversation_id : str
            id of the conversation to continue the same conversation 
            
            
        Returns
        -------
        SyncResponse object
            An object with the **answer** and **conversation_id**
            
        """

        if not self.prompt and not self.audio_file_path:
            raise Exception("Prompt is required")
        
        if self.audio_file_path:
            prompt = APIWrapper().speech_to_text(audio_file_path=self.audio_file_path)
        else :
            prompt = self.prompt
            
        if not self.conversation_id:
            # Generate a new conversation ID if not provided
            self.conversation_id = str(uuid.uuid4())

        payload = {
            "applet_code": "conversation",
            "conversation_id": self.conversation_id,
            "user_params": {
                "prompt": prompt
            }
        }

        api_response = APIWrapper(payload).execute_sync()
        api_response_json = api_response.json()
        content = api_response_json['content']
        response = SyncResponse(
            answer=content, conversation_id=self.conversation_id)
        resp_obj = response.obj()

        return resp_obj
