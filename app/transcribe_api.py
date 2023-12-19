from openai import OpenAI
import os
import sys

def whisper_transcribe(input_file):
    os.environ["OPENAI_API_KEY"] = os.getenv['OPENAI_KEY']
    client = OpenAI()

    txt_file = (input_file.split('.')[0] + '.txt')

    try:
        with open(input_file, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file, 
            response_format="text"
            )
    except Exception as e:
        print(f'Error generating transcript: {e}', file=sys.stderr)
    
    try:
        with open(txt_file, "w") as text_file:
            text_file.write(transcript)
    except Exception as e:
        print(f'Error saving txt file: {e}', file=sys.stderr)

# for local testing
if __name__ == "__main__":
    import json
    cur_path = os.getcwd()
    new_path = os.path.relpath('./credentials/openai_key.json', cur_path)

    with open(new_path) as f:
        credentials = json.load(f)
    file = input('Enter filename: ')
    whisper_transcribe(file)