# gaidme

> Yeah, need to check if port 3000 on firewall is open.
> 
> How did it go? utf ...???? fck i don't remember. will google/chatgpt that 🥲

Do you recognize that?? wait no more!
Introducing gaidme. gaidme is a cool command-line interface (CLI) tool designed to streamline and enhance your development workflow by leveraging AI to interpret and execute system commands. Whether you're automating tasks, querying information, or managing your development environment, gaidme provides an intuitive and efficient way to interact with your system.

## Getting Started

### Rules
- Do not use special characters like %#@| and other when creating the prompt

### Prerequisites

- Python 3.8 or higher
- Proper env variables setted. More in .env.example
#### OpenAI
```
export OPENAI_API_KEY=sk-...
```
#### AzureOpenAI
```
export AZURE_OPENAI_API_KEY=sk-...
export AZURE_OPENAI_ENDPOINT="https://docs-test-001.openai.azure.com/"
export AZURE_OPENAI_DEPLOYEMNT=gpt-4
```
#### Bash shell
```
export 'PROMPT_COMMAND=history -a';
```
### Installation

To install run:
```
pip install gaidme
``` 

## Usage
### ask

Type 'gaidme ask {your prompt}'
This will just send your prompt and as a answer you will get proper command
### reflect
***Still in development. High risk of damage to something*** 
Type instruction before. Like "docker image ls"
Type 'gaidme reflect {your prompt}'.
Then in the background gaidme will execute first command from the histroy. In this case "docker image ls", and based on this command and the result of this command gaidme will return proper command. 

Example:
```
$ docker image ls
$ gaidme reflect show id only
... some commands that is needed
$ TODO: result
``` 
### Video (demo)

## Features
- azure
- supported only zsh and bash
## Contributing

We welcome contributions to gaidme! If you have suggestions for improvements or bug fixes, please feel free to submit an issue or pull request.

## Support

If you need help or have questions, reach out to me via [GitHub Issues](https://github.com/mateusztylec/gaidme/issues).

## Buy Me A Coffee

If you find gaidme useful, consider buying me a coffee to show your support:
[![Buy Me A Coffee](https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png)](https://www.buymeacoffee.com/mateusztylec)

## License
MIT



I am currently working on my own API. It will have access to the current documentation of most popular tools. So it means more accurate responses. Do you want to get access to it? Sign up for the waiting list.
[waitlist](https://airtable.com/appsYU2AJudGb9B1V/pagVW8inby0MAnjP5/form)

<a href="https://www.buymeacoffee.com/mateusztylec" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" ></a>
