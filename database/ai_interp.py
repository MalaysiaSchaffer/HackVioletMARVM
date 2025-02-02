from openai import OpenAI
import os


API_KEY = os.getenv("API_KEY")
#def generate_label(image_path):
def generate_label():
   '''
   with open(image_file, "rb") as image_file:
       image = base64.b64encode(image_file.read()).decode("utf-8")
   '''
   client = OpenAI(
       api_key=API_KEY
   )


   response = client.chat.completions.create(
       model="gpt-4o-mini",
       messages=[
           {
               "role": "user",
               "content": [
                   {
                       "type": "text",
                       "text": "Describe the object in this image in one word.",
                   },
                   {
                       "type": "image_url",
                       "image_url": {"url": "https://images.pexels.com/photos/20787/pexels-photo.jpg?cs=srgb&dl=pexels-kmerriman-20787.jpg&fm=jpg"}, 
                   },
               ],
           }
       ],
       max_completion_tokens=10
   )


   return response.choices[0].message.content






generate_label()