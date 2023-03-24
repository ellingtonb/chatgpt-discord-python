import os
import time
import openai
import discord

if 'DISCORD_CLIENT_TOKEN' not in os.environ:
    raise ValueError('The environment variable \'DISCORD_CLIENT_TOKEN\' is required!')

if 'OPENAI_API_KEY' not in os.environ:
    raise ValueError('The environment variable \'OPENAI_API_KEY\' is required!')

MAX_ATTEMPTS = 5
DELAY_BETWEEN_ATTEMPTS_IN_SECONDS = 5

openai.api_key = os.getenv('OPENAI_API_KEY')

message_history = [
    {"role": "system", "content": "The chatGPT is amazing!"}
]

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.messages = True
intents.message_content = True

client = discord.Client(intents=intents)


async def generate_response(message_history):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=message_history
    )

    return response['choices'][0]['message']['content']


@client.event
async def on_ready():
    print(f"{client.user} has connected to Discord!")


@client.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content.startswith("!chat"):
        user_input = message.content[5:].strip()

        print('\nReceiving a new question:')
        print(user_input)

        print('\nProcessing the question in OpenAI...')

        message_history.append({"role": "user", "content": user_input})

        assistant_content = []
        attempt = 0
        while attempt < MAX_ATTEMPTS:
            try:
                assistant_response = await generate_response(message_history[-10:])
                assistant_content = assistant_response.split('\n')
                break
            except (openai.error.Timeout,
                    openai.error.APIConnectionError,
                    openai.error.ServiceUnavailableError,
                    openai.error.TryAgain) as e:
                print("Timeout requesting chatGPT on OpenAI with message: " + str(e))
                print("Retrying in [" + str(DELAY_BETWEEN_ATTEMPTS_IN_SECONDS) + "] seconds...")
                time.sleep(DELAY_BETWEEN_ATTEMPTS_IN_SECONDS)
                attempt += 1

        print('\nProcessing the question in OpenAI...')

        code_block = False
        code_content = list()
        new_content = ''
        try:
            for content in assistant_content:
                new_content = content

                if '```' in content and code_block is False:
                    code_block = True
                elif '```' in content and code_block is True:
                    code_content.append(str(content))
                    new_content = '\n'.join(code_content)
                    code_content = list()
                    code_block = False

                if code_block is True:
                    code_content.append(str(content))
                    continue

                if new_content.strip() != '':
                    message_history.append({"role": "assistant", "content": new_content})

                    attempt = 0
                    while attempt < MAX_ATTEMPTS:
                        try:
                            await message.channel.send(new_content)
                            break
                        except Exception as e:
                            print("Error sending message do Discord with message: " + str(e))
                            print("Retrying in [" + str(DELAY_BETWEEN_ATTEMPTS_IN_SECONDS) + "] seconds...")
                            time.sleep(DELAY_BETWEEN_ATTEMPTS_IN_SECONDS)
                            attempt += 1
        except Exception as error:
            print('\nFailed to send message do Discord:')
            print(new_content)
            print('\nDue to Error:')
            print(error)

        print('\nProcessed the question in OpenAI successfully!')


client.run(os.getenv('DISCORD_CLIENT_TOKEN'))
