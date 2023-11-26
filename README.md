
# LLM Query Engine

A query engine in the form of a Flask API which implements an LLM on the queries of a Qdrant vector database sourced from the BigBasketProducts dataset.

The architecture of this query engine can be seen in the below representation:
![App Screenshot](https://via.placeholder.com/468x300?text=App+Screenshot+Here)
## Table of Contents

- [Tech Stack](#tech-stack)

- [Run Locally](#run-locally)

- [Development Operations](#development-options)

- [Examples](#examples)

- [Roadmap](#roadmap)

- [Environment Variables](#environment-variables)

- [Author](#author)

- [Acknowledgements](#acknowledgements)
## Tech Stack

To implement the query engine, the following tech was used:

**Embedding:** BERT

**DB:** Qdrant

**LLM:** T5

**API Server:** Flask

The preprocessing was done with pandas, followed by a bert embedding to convert it to vectors. These vectors were then stored in the Qdrant database. An instance is hosted on Qdrant cloud. A Flask app API is created to handle get_answer POST requests as sent by a test python script to use the flan-t5-small LLM on the closest vector determined by the DB and the query. 


## Run Locally

#### Clone the project:

Create a local copy of this repository on your machine. You can use github cli/ssh keys as some other options!

```bash
  git clone https://github.com/rashmigr01/llm-query-engine.git
```

#### Go to the project directory:

Switch to the installed directory with a simple cd command.

```bash
  cd llm-query-engine
```

#### Create a virtual environment:

This step is recommended when you plan to run multiple projects on a system to organize package versions and requirements. However, you can choose to skip it if you are confident otherwise. Read more [here](https://docs.python.org/3/library/venv.html).

```bash
  python -m venv venv
  source venv/bin/activate
```

#### Install dependencies:

The requirements.txt file contains the necessary dependencies. Install the packages to your system with the following command.

```bash
  pip install -r requirements.txt
```

#### Start the API:

To host the API on a local server, first navigate to the API folder with this command.

```bash
  cd API
```

Begin the local Flask API with this command:

```bash
  python3 api.py
```

You can now interact with the API by running the following program:

```bash
  python3 test_api.py "Your query goes here!"
```

If you choose to not enter a question, a default question is chosen. To query the API, make sure to pass a string question in the above command. The JSON answer is printed in the terminal!


## Development Operations

After the above local installation, you can perform development operations to generate intermediate files of this application.

To preprocess the [BigBasketProducts.csv](https://www.kaggle.com/datasets/surajjha101/bigbasket-entire-product-list-28k-datapoints) dataset, navigate to the Preprocess directory. Run the preprocess script to generate a CSV file and a pickled version in the embeddings directory.

```bash
  cd ../Preprocess
  python3 preprocess.py
```

To generate vector embeddings, navigate to the Embeddings directory. Run the embeddings script, follwed by the modify_csv script to get the embeddings and their ids. Run the embeddings_json script to generate the main JSON embeddings file in the qdrant directory.

```bash
  cd ../Embeddings
  python3 generate_embeddings.py
  python3 modify_csv.py
  python3 embeddings_json.py
```

To generate the required metadata which will serve as the payload, navigate to the Metadata directory. Run the script to get the JSON file in the qdrant directory.

```bash
  cd ../Metadata
  python3 generate_metadata.py
```

To operate on the Qdrant database, navigate to the Qdrant directory. Run the qdrant_interaction script to create an index and upsert vectors in batches.

```bash
  cd ../Qdrant
  python3 qdrant_interaction.py
```

The changes made to the cloud hosted Qdrant DB will reflect in the Flask API calls to generate different query answers.
    
## Examples

Here are some query examples as output by the Flask API:

#### Test 1

```bash
python3 test_api.py "What is the cost of orange juice?"
```

```
{'answer': '306.0'}
```

#### Test 2

```bash
python3 test_api.py "Category of coconut oil"
```

```
{'answer': '"sub_category": "Edible Oils & Ghee"'}
```

#### Test 3

```bash
python3 test_api.py "What is the rating of Rich Creme Hair Colour"
```

```
{'answer': '4.3'}
```

#### Test 4

```bash
python3 test_api.py "What is the market price of Mountain Dew?"
```

```
{'answer': '105.84'}
```

#### Query 5

```bash
python3 test_api.py "Brand of Jeera Powder?"
```

```
{'answer': '"brand": "Dabur"'}
```



## Roadmap

The following steps were taken to complete this project:

- Preprocess the CSV dataset to remove spaces, convert to lower case string and handle numeric data.

- Generate vector embeddings using the BERT model to convert these strings to float vectors.

- Add indices to get unique ids for each of the embeddings.

- Generate a metadata JSON file and an embeddings JSON file.

- Create Qdrant DB and upsert vectors to the cloud cluster.

- Create a Flask API mask and a test script to interact with the API.

- Implement a T5 LLM on the search query to the Qdrant DB with the question and the question to generate the API response.

- Refactor codebase, add env variables, add readme.


## Environment Variables

The following environment variables are used and stored in the *.env* file. It is currently included in the repository for submission purposes but would otherwise be added to gitignore.

`QDRANT_URL` - The URL to the cloud hosted vector DB.

`QDRANT_API_KEY` - The API access key to the Qdrant DB.


## Author

This query engine was built by me, [@rashmigr01](https://www.github.com/rashmigr01), a senior undergraduate pursuing a B. Tech in CSE at IIT Kanpur. Please feel free to reach out to me with any queries at [rashmigr20@iitk.ac.in](mailto:rashmigr20@iitk.ac.in).


## Acknowledgements

This project wouldn't be possible without the wonderful opportunity by [Chaabi](https://www.chaabi.ai/). Through brainstorming and exploration, I learnt more than I ever expected all while having lots of fun!
