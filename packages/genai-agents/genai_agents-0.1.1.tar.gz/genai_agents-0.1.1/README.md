<div align="center">
<h1 align="center">GenAI Agents </h1>

<a href="https://img.shields.io/badge/Python-3.11+-3776AB.svg?style=flat&logo=python&logoColor=white"><img src="https://img.shields.io/badge/Python-3.11+-3776AB.svg?style=flat&logo=python&logoColor=white" alt="Python 3.11+"></a>

</div>

## Installation

1. Setup a virtual environment.

    #### Note: Use python3.11

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

2. Clone the repository

    ```bash
    git clone https://github.com/aiplanethub/agents.git
    ```

3. Go to the project directory

    ```bash
    cd agents
    ```

4. Install the package

    ```bash
    pip install .
    ```

    OR,


    ```bash
    pip install -e .
    ```

    When using the `-e` flag, the package is installed in editable mode. This means that if you make changes to the source code, you do not need to reinstall the package for the changes to take effect.

5. Run the application

    ```bash
    export AZURE_OPENAI_API_KEY="<your key>" # required AZURE OPENAI USAGE
    export SERPER_API_KEY="<your key>" # required for Google Serper API
    python usecases/ProfAgent.py
    ```


Note:
install "python -m spacy download en_core_web_sm" for executing "usecases/ProfAgentFeedback_Review.py"