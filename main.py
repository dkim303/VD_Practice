from bs4 import BeautifulSoup
import numpy as np
from sentence_transformers import SentenceTransformer
from vector_db_package import utils
import requests
import json
import sys
from pathlib import Path

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

if __name__ == "__main__":
    print("Load in embeddings matrix and metadata")
    e_name = input("Enter embeddings file name: ")
    d_name = input("Enter metadata file name: ")

    try:
        embeddings_path = Path(e_name)
        data_path = Path(d_name)

        # check for mismatch in file existance
        if (embeddings_path.exists() == False and data_path.exists() == True):
            raise Exception("Error: Embeddings file does not exist but Data file exists.")
        elif (embeddings_path.exists() == True and data_path.exists() == False):
            raise Exception("Error: Data file does not exist but Embeddings file exists.")   
        
        # later on add function to check if all items in the 2 files match correctly

        if embeddings_path.exists():
            embeddings_matrix = np.load(e_name)
        # case of creating empty matrix, dim-384, num vectors is 0
        else:
            embeddings_matrix = np.empty((0,384), dtype=np.float32)

        if data_path.exists():
            with open(d_name) as data_fp:
                data = json.load(data_fp)
                data = {int(k): v for k, v in data.items()}
        else:
        # case of creating empty data list, no data recorded yet in JSON format
            data = {}

    except Exception as e:
        print(e)
        sys.exit(1)

    should_continue = True
    while should_continue:
        # handles all user inputs for command sequences and program quitting
        should_continue = utils.interface(embeddings_matrix, data, e_name, d_name)
            
    