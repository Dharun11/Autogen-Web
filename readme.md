# Content Analysis and Classification

This project analyzes and classifies web content, determining whether it is spam or not. It uses a group of agents to extract, classify, summarize, and generate reports on the content.

## Prerequisites

- Python 3.8 or higher
- Virtual environment (recommended)

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/Dharun11/Autogen-Web.git
    cd AUTOGEN
    ```

2. Create and activate a virtual environment:
    ```sh
    python -m venv env
    env\Scripts\activate 
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

4. Set up environment variables:
    - Create a [.env](http://_vscodecontentref_/1) file in the root directory.
    - Add your `GROQ_API` key to the [.env](http://_vscodecontentref_/2) file:
        ```
        GROQ_API=your_api_key_here
        ```

## Running the Project

1. To run the Streamlit app, execute:
    ```sh
    streamlit run src/main.py
    ```

2. Open your web browser and navigate to the URL provided by Streamlit (usually `http://localhost:8501`).

3. Enter a URL to analyze in the input field and click "Analyze".

## Project Structure

- [logs](http://_vscodecontentref_/6): Contains log files generated during the execution.
- [src](http://_vscodecontentref_/7): Contains the main application and exception handling.
    - [main.py](http://_vscodecontentref_/8): Main script to run the Streamlit app.
    - [exception.py](http://_vscodecontentref_/9): Custom exception handling.
- [requirements.txt](http://_vscodecontentref_/10): Lists the dependencies required for the project.
- [sample.py](http://_vscodecontentref_/11): Sample script demonstrating the usage of agents for content analysis.

## License

This project is licensed under the MIT License.