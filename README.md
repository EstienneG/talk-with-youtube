# YouTube Video Interaction Tool

This Python tool allows you to interact with YouTube videos by simulating a conversation. Your inputs and the generated responses are logged to `discussion.txt` when you type 'exit'.

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt

2. **Configure your .env file:**
API_KEY=your_openai_api_key
MODEL_NAME=your_model_name ('gpt-3.5-turbo')

## Usage

1. **Run the tool:**
   ```bash
   python youtubeToSummary.py --video_id 'video_id'

Id of the youtube video can be found after the v= in the url

example for https://www.youtube.com/watch?v=XGQlo18w00Q :
   ```bash
   python youtubeToSummary.py --video_id 'XGQlo18w00Q'

2. **Interact with the video:**

- Input a YouTube video Id.
- Type your questions or comments.
- Type **exit** to end the session and save the conversation to discussion.txt.