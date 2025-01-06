# KotaemonRAG

A fork of the open source [Kotaemon](https://github.com/Cinnamon/kotaemon) project. This offers a high level interface to interact with local and cloud based RAG solutions.

![Preview](https://raw.githubusercontent.com/Cinnamon/kotaemon/main/docs/images/preview-graph.png)



## Installation

> If you are not a developer and just want to use the app, please check out our easy-to-follow [User Guide](https://cinnamon.github.io/kotaemon/). Download the `.zip` file from the [latest release](https://github.com/Cinnamon/kotaemon/releases/latest) to get all the newest features and bug fixes.

### System requirements

1. [Python](https://www.python.org/downloads/) >= 3.10
2. [Docker](https://www.docker.com/): optional, if you [install with Docker](#with-docker-recommended)
3. [Unstructured](https://docs.unstructured.io/open-source/installation/full-installation#full-installation) if you want to process files other than `.pdf`, `.html`, `.mhtml`, and `.xlsx` documents. Installation steps differ depending on your operating system. Please visit the link and follow the specific instructions provided there.

### With Docker

<details>

1. We support both `lite` & `full` version of Docker images. With `full`, the extra packages of `unstructured` will be installed as well, it can support additional file types (`.doc`, `.docx`, ...) but the cost is larger docker image size. For most users, the `lite` image should work well in most cases.

   - To use the `lite` version.

     ```bash
     docker run \
     -e GRADIO_SERVER_NAME=0.0.0.0 \
     -e GRADIO_SERVER_PORT=7860 \
     -p 7860:7860 -it --rm \
     ghcr.io/cinnamon/kotaemon:main-lite
     ```

   - To use the `full` version.

     ```bash
     docker run \
     -e GRADIO_SERVER_NAME=0.0.0.0 \
     -e GRADIO_SERVER_PORT=7860 \
     -p 7860:7860 -it --rm \
     ghcr.io/cinnamon/kotaemon:main-full
     ```

2. We currently support and test two platforms: `linux/amd64` and `linux/arm64` (for newer Mac). You can specify the platform by passing `--platform` in the `docker run` command. For example:

   ```bash
   # To run docker with platform linux/arm64
   docker run \
   -e GRADIO_SERVER_NAME=0.0.0.0 \
   -e GRADIO_SERVER_PORT=7860 \
   -p 7860:7860 -it --rm \
   --platform linux/arm64 \
   ghcr.io/cinnamon/kotaemon:main-lite
   ```

3. Once everything is set up correctly, you can go to `http://localhost:7860/` to access the WebUI.

4. We use [GHCR](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry) to store docker images, all images can be found [here.](https://github.com/Cinnamon/kotaemon/pkgs/container/kotaemon)


</details>

### Without Docker (recommended for dev)

<details>

1. Before begining, install [Microsoft C++ 14.0+](https://visualstudio.microsoft.com/fr/visual-cpp-build-tools/). Install the default recommended dependencies of the **Desktop C++ Development** package.

2. Clone and install required packages on a fresh python environment.

   ```shell
   # clone this repo
   git clone https://github.com/Cinnamon/kotaemon
   cd kotaemon

   # create a venv (this env is rather complex)
   python -m venv .venv
  
   # install the libraries dependencies (ignore python version for python>=3.12)
   pip install -e "libs/kotaemon[all]" --ignore-requires-python
   pip install -e "libs/ktem" --ignore-requires-python
   ```

2. Create a `.env` file in the root of this project. Use `.env.example` as a template

   The `.env` file is there to serve use cases where users want to pre-config the models before starting up the app (e.g. deploy the app on HF hub). The file will only be used to populate the db once upon the first run, it will no longer be used in consequent runs.

3. (Optional) To enable in-browser `PDF_JS` viewer, download [PDF_JS_DIST](https://github.com/mozilla/pdf.js/releases/download/v4.0.379/pdfjs-4.0.379-dist.zip) then extract it to `libs/ktem/ktem/assets/prebuilt`

<img src="https://raw.githubusercontent.com/Cinnamon/kotaemon/main/docs/images/pdf-viewer-setup.png" alt="pdf-setup" width="300">

4. Start the web server:

   ```shell
   python app.py
   ```

   - The app will be automatically launched in your browser.
   - Default username and password are both `admin`. You can set up additional users directly through the UI.

5. Check the `Resources` tab and `LLMs and Embeddings` and ensure that your `api_key` value is set correctly from your `.env` file. If it is not set, you can set it there.

</details>


## Further developments

### Setup Local Models (for local/private RAG)

See [Local model setup](docs/local_model.md).

### Setup multimodal document parsing (OCR, table parsing, figure extraction)

These options are available:

- [Azure Document Intelligence (API)](https://azure.microsoft.com/en-us/products/ai-services/ai-document-intelligence)
- [Adobe PDF Extract (API)](https://developer.adobe.com/document-services/docs/overview/pdf-extract-api/)
- [Docling (local, open-source)](https://github.com/DS4SD/docling)
  - To use Docling, first install required dependencies: `pip install docling`

Select corresponding loaders in `Settings -> Retrieval Settings -> File loader`

### Customize your application

- By default, all application data is stored in the `./ktem_app_data` folder. You can back up or copy this folder to transfer your installation to a new machine.

- For advanced users or specific use cases, you can customize these files:

  - `flowsettings.py`
  - `.env`

#### `flowsettings.py`

This file contains the configuration of your application. You can use the example
[here](flowsettings.py) as the starting point.

<details>

<summary>Notable settings</summary>

```python
# setup your preferred document store (with full-text search capabilities)
KH_DOCSTORE=(Elasticsearch | LanceDB | SimpleFileDocumentStore)

# setup your preferred vectorstore (for vector-based search)
KH_VECTORSTORE=(ChromaDB | LanceDB | InMemory | Qdrant)

# Enable / disable multimodal QA
KH_REASONINGS_USE_MULTIMODAL=True

# Setup your new reasoning pipeline or modify existing one.
KH_REASONINGS = [
    "ktem.reasoning.simple.FullQAPipeline",
    "ktem.reasoning.simple.FullDecomposeQAPipeline",
    "ktem.reasoning.react.ReactAgentPipeline",
    "ktem.reasoning.rewoo.RewooAgentPipeline",
]
```

</details>

#### `.env`

This file provides another way to configure your models and credentials.

<details>

<summary>Configure model via the .env file</summary>

- Alternatively, you can configure the models via the `.env` file with the information needed to connect to the LLMs. This file is located in the folder of the application. If you don't see it, you can create one.

- Currently, the following providers are supported:

  - **OpenAI**

    In the `.env` file, set the `OPENAI_API_KEY` variable with your OpenAI API key in order
    to enable access to OpenAI's models. There are other variables that can be modified,
    please feel free to edit them to fit your case. Otherwise, the default parameter should
    work for most people.

    ```shell
    OPENAI_API_BASE=https://api.openai.com/v1
    OPENAI_API_KEY=<your OpenAI API key here>
    OPENAI_CHAT_MODEL=gpt-3.5-turbo
    OPENAI_EMBEDDINGS_MODEL=text-embedding-ada-002
    ```

  - **Azure OpenAI**

    For OpenAI models via Azure platform, you need to provide your Azure endpoint and API
    key. Your might also need to provide your developments' name for the chat model and the
    embedding model depending on how you set up Azure development.

    ```shell
    AZURE_OPENAI_ENDPOINT=
    AZURE_OPENAI_API_KEY=
    OPENAI_API_VERSION=2024-02-15-preview
    AZURE_OPENAI_CHAT_DEPLOYMENT=gpt-35-turbo
    AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT=text-embedding-ada-002
    ```

  - **Local Models**

    - Using `ollama` OpenAI compatible server:

      - Install [ollama](https://github.com/ollama/ollama) and start the application.

      - Pull your model, for example:

        ```shell
        ollama pull llama3.1:8b
        ollama pull nomic-embed-text
        ```

      - Set the model names on web UI and make it as default:

        ![Models](https://raw.githubusercontent.com/Cinnamon/kotaemon/main/docs/images/models.png)

    - Using `GGUF` with `llama-cpp-python`

      You can search and download a LLM to be ran locally from the [Hugging Face Hub](https://huggingface.co/models). Currently, these model formats are supported:

      - GGUF

        You should choose a model whose size is less than your device's memory and should leave
        about 2 GB. For example, if you have 16 GB of RAM in total, of which 12 GB is available,
        then you should choose a model that takes up at most 10 GB of RAM. Bigger models tend to
        give better generation but also take more processing time.

        Here are some recommendations and their size in memory:

      - [Qwen1.5-1.8B-Chat-GGUF](https://huggingface.co/Qwen/Qwen1.5-1.8B-Chat-GGUF/resolve/main/qwen1_5-1_8b-chat-q8_0.gguf?download=true): around 2 GB

        Add a new LlamaCpp model with the provided model name on the web UI.

  </details>

### Adding your own RAG pipeline

#### Custom Reasoning Pipeline

1. Check the default pipeline implementation in [here](libs/ktem/ktem/reasoning/simple.py). You can make quick adjustment to how the default QA pipeline work.
2. Add new `.py` implementation in `libs/ktem/ktem/reasoning/` and later include it in `flowssettings` to enable it on the UI.

#### Custom Indexing Pipeline

- Check sample implementation in `libs/ktem/ktem/index/file/graph`

> (more instruction WIP).

<!-- end-intro -->
