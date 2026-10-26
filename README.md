# Local LLM Inference using Ollama

## Objective
To run an open-source Large Language Model locally using Ollama,
generate responses to different prompts, and compare the outputs.

## Tools Used
- Python
- Ollama
- Llama 3.2
- Pandas
- Jupyter Notebook
- Visual Studio Code

## Project Structure
- dataset/prompts.csv: Contains 10 prompts from different domains.
- dataset/llm_responses.csv: Stores prompts and generated responses.
- dataset/response_comparison.csv: Compares simple and detailed prompts.
- dataset/conversation_history.txt: Stores the conversation history.
- notebook/Week8_Local_LLM_Inference.ipynb: Displays the project analysis.
- local_llm.py: Generates and saves model responses.
- requirements.txt: Lists the required Python libraries.

## Execution
1. Install Ollama.
2. Download the model using `ollama pull llama3.2`.
3. Install dependencies using `python -m pip install -r requirements.txt`.
4. Run `python local_llm.py`.
5. Open and execute the Jupyter Notebook in VS Code.

## Observations
The model generated responses for prompts from education,
healthcare, coding, travel, and business.

Simple prompts produced direct answers, while detailed prompts
often encouraged more structured explanations.

Response length alone does not guarantee accuracy. Generated
answers should be reviewed for factual correctness.

## Conclusion
Running an LLM locally allows users to generate responses on
their own computer without sending each prompt to a cloud LLM API.
Ollama provides a convenient way to experiment with local models.