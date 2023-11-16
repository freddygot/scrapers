import json
import os

def create_assistant(client):
  assistant_file_path = 'assistant.json'

  if os.path.exists(assistant_file_path):
    with open(assistant_file_path, 'r') as file:
      assistant_data = json.load(file)
      assistant_id = assistant_data['assistant_id']
      print("Loaded existing assistant ID.")
  else:
    file = client.files.create(file=open("knowledge.docx", "rb"),
                               purpose='assistants')

    assistant = client.beta.assistants.create(instructions="""
          Assistenten skal å hjelpe folk med å finne den rette psykologen for dem i Oslo.
          Den vil gi informasjon og veiledning om å velge psykologer basert på ulike faktorer som spesialisering, beliggenhet, 
          tilgjengelighet og tilnærming. GPT vil ikke gi psykologisk rådgivning eller diagnoser, men heller bistå i det praktiske aspektet ved å 
          finne en passende fagperson. Den vil også veilede brukere om generelle spørsmål om
           psykisk helse-tjenester og hvordan man får tilgang til dem i Oslo.
          """,
                                              model="gpt-4-1106-preview",
                                              tools=[{
                                                  "type": "retrieval"
                                              }],
                                              file_ids=[file.id])

    with open(assistant_file_path, 'w') as file:
      json.dump({'assistant_id': assistant.id}, file)
      print("Created a new assistant and saved the ID.")

    assistant_id = assistant.id

  return assistant_id
