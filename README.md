<a id="readme-top"></a>

<br />
<div align="center">
<h1 align="center">Rag-Speech-2-Text</h1>
</div>

<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
  </ol>
</details>

## About The Project

This project is a Speech-to-Text API implementation using Python. It leverages the Deepgram API for real-time speech recognition, allowing users to interact with a system via voice commands. The project includes functionality for detecting specific wake words and stopping the process based on specific voice commands. 

This project is only one part of the bigger Home-Assitant-Project, which consists of the two other repositories [Rag-Assistant-API](https://github.com/HerbiHerb/rag_assistant_api) and [RAG-Chat-UI](https://github.com/HerbiHerb/rag_chat_ui). 

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

* [![Python](https://img.shields.io/badge/Python-3.9-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Getting Started

To get a local copy up and running, follow these simple steps.

### Prerequisites

- Python 3.9 or later
- Virtual environment (optional, but recommended)

### Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/your_username/speech-to-text-api.git
   cd speech-to-text-api
   ```

2. Install dependencies:

    With pip:
    ```sh
    pip install -r requirements.txt

    ```
3. Ensure Redis is running on your machine or update the redis.StrictRedis configuration in main.py as needed.
4. Set up your environment variables in a .env file:
    ```sh
    DEEPGRAM_API_KEY=your_deepgram_api_key
    LISTENING_SOUND_PATH=path_to_listening_sound.wav
    ```
5. Configure the application:
    Edit the config/config.yaml file according to your requirements. Add appropriate values for the host_url and chat_ui_url variables.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Usage

* Run the main script:
    ```sh
    python main.py
    ```
* The application will start listening for voice input via the microphone. It uses a wake word "hey jarvis" to activate and "jarvis stop" to deactivate.
* The detected voice commands will be processed and sent to a backend service via HTTP requests.
    Once installed and configured, the application can be accessed via your browser at http://localhost:5001. Users can log in, upload documents, and interact with the language model.
    Features

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Roadmap

- [ ]  Add support for multiple languages
- [ ] Improve wake word detection accuracy
- [ ] Integrate with additional speech-to-text services for better accuracy
<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Contributing

Contributions are welcome! If you have suggestions for improving this project, please fork the repo and create a pull request. Alternatively, you can open an issue with the "enhancement" tag.

1. Fork the Project
2. Create a new Branch (git checkout -b feature/AmazingFeature)
3. Commit your Changes (git commit -m 'Add some AmazingFeature')
4. Push to the Branch (git push origin feature/AmazingFeature)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### License

Distributed under the MIT License. See `LICENSE` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>
