import argparse
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain.schema import SystemMessage
from langchain_openai.chat_models import ChatOpenAI


from youtube_transcript_api import YouTubeTranscriptApi
from dotenv import load_dotenv

import os

system_prompt = """
                You are a chatbot making summaries from input text. Here is the response template you use :
                Title :
                Two sentences describing what the content is about.
                Conclusion :
                A detailed, six-sentence spoiler with the final results.

                Key Points :
                A list of the most important 10 key points with details in the format:
                Emoji concept: takeaway

                Summary :
                A numbered list of the 10 most relevant things in the content, each with two sentences.

                Enter a number to expand.

                Shortcuts
                [A]: Transform into article
                [E]: Expand summary
                [Q]: Extract quotes
                [Z]: Create Quiz
                [F]: Write FAQs

                Translate
                Enter any language to translate (e.g., Spanish, French, Chinese).
                """

parser = argparse.ArgumentParser(description='YouTube Video Interaction Tool')
parser.add_argument('--video_id', type=str, help='Id of the youtube video, can be found after the v= in the url')
args = parser.parse_args()

def chatWithYoutubeVideo(video_id=args.video_id):

    load_dotenv()
    api_key = os.getenv("API_KEY")
    model = os.getenv("MODEL")

    """# Extract the transcript"""

    transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en','fr'])

    formatted_transcript = ''
    for i in range(len(transcript)):
        formatted_transcript += transcript[i]['text'] + ' '

    """# Prepare the agent"""

    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage(
                content=system_prompt,
            ),
            MessagesPlaceholder(variable_name="chat_history"),
            HumanMessagePromptTemplate.from_template("{human_input}"),
        ]
    )

    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    llm = ChatOpenAI(model_name=model, openai_api_key=api_key)

    chat_llm_chain = LLMChain(
        llm=llm,
        prompt=prompt,
        memory=memory,
        verbose=True,
    )

    """# Talk with the agent"""

    discussion = []

    answer = chat_llm_chain.predict(human_input = formatted_transcript)

    print(answer)

    discussion.append(answer)

    while True:
        user_input = input("Enter your message (or 'exit' to close the application): ")
        if user_input == "exit":
            with open('discussion.txt', 'w') as file:
                file.write('\n'.join(discussion))
            break
        answer = chat_llm_chain.predict(human_input=user_input)

        print(answer)

        discussion.append(user_input)
        discussion.append(answer)

chatWithYoutubeVideo()