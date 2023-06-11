# PostText

PostText is a QA system for querying your text data. When appropriate structured views are in place, PostText is good at answering queries that require computing aggregates over your data, such as "*How many times did I exercise last month?*". In this implementation, PostText will always generate two answers, one through a view-based QA engine and the other through a retrieval-based QA engine.

PostText Reference ---  [https://arxiv.org/abs/2306.01061](https://arxiv.org/abs/2306.01061):
```
@article{tan2023posttext,
      title={Reimagining Retrieval Augmented Language Models for Answering Queries},
      author={Wang-Chiew Tan and Yuliang Li and Pedro Rodriguez and Richard James and Xi Victoria Lin and Alon Halevy and Scott Yih},
      journal={arXiv preprint:2306.01061},
      year={2023},
}
```

To run posttext, first set up the environment and the relevant files. There are 3 datasets, sparse-100, medium-100, dense-100 already set up in this repo under the subdirectory data/TimelineQA. 

TimelineQA Reference --- [https://arxiv.org/abs/2306.01069](https://arxiv.org/abs/2306.01069):
```
@article{tan2023timelineqa,
      title={TimelineQA: A Benchmark for Question Answering over Timelines},
      author={Wang-Chiew Tan and Jane Dwivedi-Yu and Yuliang Li and Lambert Mathias and Marzieh Saeidi and Jing Nathan Yan and Alon Y. Halevy},
      journal={arXiv preprint:2306.01069},
      year={2023}
}
```


## Setting up your environment

Create and activate a new conda env:
```
conda create -n posttext python=3.10
conda activate posttext
```

Install python packages (for backend):
```
conda install --file requirements.txt
```

## Setting up your view-based QA engine

### Prepare your dataset for querying:

At present, PostText's view-based QA engine is implemented on top of SQLite. Hence, to prepare your dataset for querying by the view-based QA engine, you will need to first create views, as tables in csv format. For example, if you anticipate that there will be frequent queries about your cooking, you can create a view that keeps only information related to your cooking. Once you have created these views, you can continue with the following steps to prep your views for use by the view-based QA system. 


1. Create a config.ini file. An example can be found in the data/TimelineQA/sparse-100/config.ini. The best way is to get started is to copy this file to your data directory and modify it as appropriate. You can leave most of the specifications unchanged especially if you have access to OpenAI models. As you go through the remaining steps, make sure the paths to the files specified in the [input] section are correct.
Alternatively, if you wish to create config.ini file from scratch, you can make use of create_config_file.py as follows:

```
python util/create_config_file.py
```

2. Create a metadata file to describe your views. This information will be utilized by the LLM to understand which is the best view to use and how to query over it using SQLite. For example, the description of views for TimelineQA dataset is described in TimelineQA/sparse-100/views_metadata.txt

After you have completed the description, specify the path of your description file in config.ini under [input] --> "views_metadata.txt".

3. Create an index of your metadata file. To do this, execute the following command. The file create_metadata_idx.py is in the util subdirectory. Note that you will need your config.ini file for this step. 

```
python util/create_metadata_idx.py <views_description file from above> <your config.ini file> <output_file_name>
```

For example:

```
python util/create_metadata_idx.py views_metadata.txt config.ini views_idx.csv
```

This command will create the file views_idx.csv. Make sure the path under [input] in config.ini points the to right path of this file. 

3. Handling dates in SQLite.  Before you create the views db file in sqlite, ensure that your dates are in YYYY/MM/DD format for comparisons in SQLite to work correctly. You can make use of date_cleaner.py in util folder to format the dates correctly.
e.g., if your date format is in MM/DD/YYYY under a column called "date" in your <inputfile>, you can execute:

```
python date_cleaner.py <inputfile> date date <outputfile>
```

to convert the date column into YYYY/MM/DD and the new column will also be called "date". The file dd_cleaner.py in util also allows you to remove some columns or format dates with time concatenated in them.

4. Next, copy and modify the script "create_db.sql" (from TimelineQA/sparse-100/create_db.sql) to import the views in csv to SQLite.
You will need to specify the schema before you execute import statements in create_db.sql. Note that the attributes specified in create_db.sql must follow exactly those of the .csv view files. For SQLite, specify TEXT for date types. 

After this, execute:
```
 ```rm -f views_db.sqlite;sqlite3 views_db.sqlite ".read create_db.sql"```
```

This will create a views_db.sqlite file by importing data from your csv files. Once you have the file views_db.sqlite, you will not need to run this command again. PostText will read views_db.sqlite to access the views.

Specify the path of views_db.sqlite in config.ini under [input] --> "views_db".

5. Create a vectorstore of embeddings of the dataset for use by the retrieval-based QA engine. For example if your data file (not the views) is in one big csv file, you may execute the following command:

To do this execute:
```
python digital_data2vectorstore.py <your dataset csv filename>
```

This command will generate a file called output.pkl. You can move this file to a suitable directory and specify the path of this file in config.ini under [input] --> "source_idx". The example config.ini points to timeline.pkl and you should change the path to output.pkl. Once you have this file, you do not need to execute this command again.

6. Make sure your PYTHONPATH contains the root directory of posttext.
For example:

```
echo PYTHONPATH = "${PYTHONPATH}:<path to root of posttext dir where src and util are subdirectories>"
```

7. You can now run PostText. You can execute the following command from PostText's main directory. If you wish to execute with the frontend UI, please take a look at the next section.

```
python -m src.posttext data/TimelineQA/sparse-100
```

You should see the following in your terminal and you can start asking questions.

```
PostText v0.0 ====>
Enter your question:
```




## Setting up your UI

Install nodejs and yarn (for frontend):
```
conda install -c conda-forge nodejs==18.10.0 yarn
```

Install some react libraries:
```
npm install primereact primeicons
npm install react-syntax-highlighter
```

### To build and start the React frontend

```
cd frontend/
yarn
yarn build
yarn start
```

The homepage should be available at `http://localhost:3000/`. 

The frontend code is at `frontend/src/App.js`.

### To start the Flask backend

To run the backend, you will need to set up an OpenAI API [here](https://openai.com/api/).

After that, add the API key to your env variables:

```
export OPENAI_API_KEY=<api_key_goes_here>
```

```
python server.py
```

You can test the backend by curl
```
curl http://127.0.0.1:5000/test
```

You should get:
```
{
  "message": "okay"
}
```

## License

The codebase is licensed under the [Apache 2.0 license](LICENSE).

## Contributing

See [contributing](CONTRIBUTING.md) and the [code of conduct](CODE_OF_CONDUCT.md).
      
