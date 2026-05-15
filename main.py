from bs4 import BeautifulSoup
import numpy as np
from sentence_transformers import SentenceTransformer
from vector_db_package import utils
import requests
import json
import sys

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

if __name__ == "__main__":
    print("Load in embeddings matrix and metadata")
    e_name = input("Enter embeddings file name: ")
    try:
        embeddings_matrix = np.load(e_name)
    except Exception as e:
        print("Error: Failed to read embeddings file.")
        sys.exit(1)

    d_name = input("Enter metadata file name: ")
    try:
        with open(d_name) as meta_fp:
            metadata = json.load(meta_fp)
            metadata = {int(k): v for k, v in metadata.items()}

    except Exception as e:
            print("Error: Failed to read metadata file")
            sys.exit(1)

    utils.menu()
    selected_num = input()

    try:
        match selected_num:

            # Making A Query
            case 1:
                query = input("Enter query: ")
                query_vector = model.encode(query, convert_to_numpy=True, normalize_embeddings=True)

            case 2:
                should_continue = True
                while should_continue:
                    mode = input("Enter 0 to log a Website or 1 to log a PDF.")

                    # Website URL Entering
                    if mode == 0:
                        url = input("Enter new book URL: ")
                        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
                        if response.raise_for_status == False:
                            raise ValueError("Error: invalid website URL given.")
                        
                        is_duplicate = utils.check_duplicate(url, metadata)
                        if is_duplicate == True:
                            raise ValueError("Error: URL already logged.")
                        
                    # PDF URL Entering
                    elif mode == 1:
                        url = input("Enter new website URL: ")
                        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
                        if response.raise_for_status == False:
                            raise ValueError("Error: invalid pdf URL given.")
                        
                        is_duplicate = utils.check_duplicate(url, metadata)
                        if is_duplicate == True:
                            raise ValueError("Error: URL already logged.")

                    # Invalid URL Type
                    else:
                        raise ValueError("Error: Invalid URL type entered.")
                    
                    entered_message = input("Enter DONE if done entering in data.")
                    if entered_message == "DONE":
                        should_continue = False
                    else:
                        should_continue = True

            # Invalid Option Entered
            case _:
                raise ValueError("Error: invalid command given.") 
            
    except ValueError as e:
        print(e)
            
    