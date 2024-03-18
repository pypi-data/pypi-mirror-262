<p align="center">Gemini-cli</p>

<p align="center">
<img src="https://img.shields.io/badge/python-3.11+-blue.svg">
 </p>

<p align="center">This is a command line tool to use the Gemini API provided by Google cloud.</p>

## Usage

### Install dependencies

#### Clone the respository

```sh
git clone https://github.com/Yoru-cyber/Gemini-cli
```

#### Install dependencies

```sh
pip install -r requirements.txt
```

#### Setup your API key

First you need to have a [Google Cloud API key](https://ai.google.dev/tutorials/python_quickstart#setup_your_api_key) to use Gemini.
Once you have you API key, just create a .env file inside the Gemini-cli folder

#### Create .env
```sh
touch .env
```
#### Adding the key
Now you need to add your key as a variable

```sh
GOOGLE_API_KEY = YOUR KEY GOES HERE
```
You can rename it if you want but then you need to change where it says ***GOOGLE_API_KEY*** on **main.py**

#### Running
Now just execute on the terminal
```sh
python3 main.py
```
That's all 🤠

## Feedback

<p align="center">
<img src="https://media.tenor.com/PrNnVlIkeckAAAAM/chopper-crying.gif">
</p>

<p align="center">All types of positive feedback are welcomed.</p>
<p align="center">This is my first published project hoping that is useful to someone.</p>
<p align="center">Be free to improve or modify.</p>