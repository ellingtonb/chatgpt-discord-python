# Discord Bot to ChatGPT with Python

A Discord bot integration to use with ChatGPT easily.

## Instructions

Create a new `.env` file and put all the environment variables with the corresponding values as the example below:

```dotenv
PYTHONUNBUFFERED=1
DISCORD_CLIENT_TOKEN="<Discord Client Token HERE>"
OPENAI_API_KEY="<OpenAI API Key HERE>"
```

Then execute the script with the command:

```bash
./start-docker
```

### Configure as SystemCTL Service

If you desire to enable this script as a `systemctl` service on your Linux operation system, keeping it in execution all the time and recovering itself automatically from failures, then copy the file `chatgpt-discord-python.service` of this repository into your systemctl services directory (ex.: `/etc/systemd/system`).

After that, enable it with the command `systemctl enable chatgpt-discord-python.service` and finally start it with the command `systemctl start chatgpt-discord-python.service`.

To check if the service is running correctly, use the command `systemctl status chatgpt-discord-python.service`.

And it is all you need!

## Contributors

* [Leonardo Lima](https://github.com/leop25): Thanks for the initiative in creating the script and influencing the use of ChatGPT.

### Contributing

All contributions are welcome, and if you want to contribute to this repository, create a new branch with a good name for your feature, make your implementation, and open a new pull request.

After that, I will review your PR and comment on or merge it in the main branch.
