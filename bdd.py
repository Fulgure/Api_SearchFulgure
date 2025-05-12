from pymongo import MongoClient
import re
from dotenv import load_dotenv
import os

class BDD:
    def __init__(self):
        load_dotenv()
        # Connexion à MongoDB
        self.client = MongoClient(os.getenv("DATABASE_URL"))
        # Création d'une nouvelle base de données
        self.db = self.client['fulgure']
        # Création de webpages
        self.webpages = self.db['webpages']
        self.mots_texte = self.db['mots_texte']
        self.mots_titres = self.db['mots_titres']

    def get_urls_with_word_and_their_number(self, word):
        mot = self.mots_texte.find_one({"mot": word})
        if not mot:
            return None, None
        return mot, len(mot.get("appear_in", []))
    
    def get_all_pages_word_counter(self):
        try:
            results = self.webpages.find({}, {"url": 1, "nb_mots": 1, "_id": 0})
            return {doc["url"]: doc.get("nb_mots") for doc in results}
        except Exception as e:
            print(f"An error occurred: {e}")
            return {}
    
    def get_info_for(self, url):
        website = self.webpages.find_one({"url": url})
        if not website:
            return website
        return website
    
    def get_count_of_webpages(self):
        return self.webpages.count_documents({})
    
    def how_many_words_in_url(self, url):
        doc = self.webpages.find_one({"url": url})
        if doc:
            return doc.get("nb_mots")
        else:
            return float('inf')
        
    def get_pagerank_for(self, url):
        website = self.webpages.find_one({"url": url})
        if not website:
            return 0
        return website.get("PageRank")
    
    def get_infos_for_urls(self, urls):
        infos = {}
        cursor = self.webpages.find({"url": {"$in": urls}})
        for doc in cursor:
            infos[doc["url"]] = {
                "PageRank": doc.get("PageRank", 0),
                "title": doc.get("title", ""),
                "description": doc.get("description", ""),
                "url": doc.get("url", "")
            }
        return infos
