from bs4 import BeautifulSoup
import numpy as np
import requests
from sentence_transformers import SentenceTransformer
from pypdf import PdfReader
from io import BytesIO
import requests
import json
import sys
from pathlib import Path


def menu():
	print(f"Enter 1 to make query.")
	print("Enter 2 to add new URL to database.")
	print("Enter 3 to add new PDF to database.")
	print("Enter q to quit.")

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def add_vectorized_website(url, vectors, dictionary):
	response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
	response.raise_for_status()

	soup = BeautifulSoup(response.text, "html.parser")

	paragarphs = soup.find_all("p")

	# for each paragraph on the page, turn the paragraph into a vector, then log it
	for p in paragarphs:
		text = p.get_text(strip=True)

		vector = model.encode(text, convert_to_numpy=True, normalize_embeddings=True)
		vectors.append(vector)

		dictionary[len(dictionary)] = { "url": url, "text": text}

def chunk_text(text, max_words=500):
	words = text.split()
	chunks = []

	for i in range(0, len(words), max_words):
		chunk = " ".join(words[i:i + max_words])
		chunks.append(chunk)

	return chunks

def add_vectorized_PDF(url, vectors, dictionary):
	response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
	response.raise_for_status()

	pdf = BytesIO(response.content)
	reader = PdfReader(pdf)

	for page_num, page in enumerate(reader.pages):
		text = page.extract_text()
		if not text:
			continue

		chunks = chunk_text(text)

		for chunk_num, chunk in enumerate(chunks):
			vector = model.encode(chunk, convert_to_numpy=True, normalize_embeddings=True)
			vectors.append(vector)
			dictionary[len(dictionary)] = {"url": url, "text": text}
	
def check_duplicate(url, dictionary):
	for index in range(len(dictionary)):
		if dictionary[index]["url"] == url:
			return True
		
	return False

def cosine_compare(query_vector, target_vector):
	similarity = (query_vector @ target_vector) / (np.linalg.norm(query_vector) * (np.linalg.norm(target_vector)))
	return similarity

def search_database(query_vector, vectors, dictionary, K):

	count = 0
	top_K_vectors = np.array()
	minimum = top_K_vectors.min()

	for vector in vectors:
		similarity_coefficient = cosine_compare(query_vector, vector)
		

def interface(embeddings, metadata, e_name, d_name):
	
	# give user options on terminal
	menu()
	selected_num = input()

	try:
		match str(selected_num):

			# Making A Query
			case "1":
				query = input("Enter query: ")
				query_vector = model.encode(query, convert_to_numpy=True, normalize_embeddings=True)

				# make query here

				return True
			
			case "2":
				should_continue = True
				while should_continue:
					mode = input("Enter 0 to log a Website or 1 to log a PDF.")

					# Website URL Entering
					if mode == 0:
						url = input("Enter new book URL: ")
						response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
						if response.raise_for_status == False:
							raise ValueError("Error: invalid website URL given.")
						
						is_duplicate = check_duplicate(url, metadata)
						if is_duplicate == True:
							raise ValueError("Error: URL already logged.")
						
						# log URL here
						return True
						
					# PDF URL Entering
					elif mode == 1:
						url = input("Enter new website URL: ")
						response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
						if response.raise_for_status == False:
							raise ValueError("Error: invalid pdf URL given.")
						
						is_duplicate = check_duplicate(url, metadata)
						if is_duplicate == True:
							raise ValueError("Error: URL already logged.")
						
						# log URL here
						return True

					# Invalid URL Type
					else:
						print("Error: Invalid URL type entered.")
						return True

			# Exit program
			case "q":
				print("Quitting Program.")
				return False

			# Invalid Option Entered
			case _:
				raise ValueError("Error: invalid command given.")
				return False

	except ValueError as e:
		print(e)
		return False