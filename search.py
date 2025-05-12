from bdd import BDD
import threading
import time
import re
import math

class Search:
    PONDERATION_TF_IDF = 0.7
    PONDERATION_PAGERANK = 0.3

    def __init__(self):
        self.bdd = BDD()
        self.lock = threading.Lock()
        self.number_of_pages_indexed = self.bdd.get_count_of_webpages()
    
    def search_term(self, term):
        term = term.lower()
        urls_contenant_mot, nombre_urls_avec_mot = self.bdd.get_urls_with_word_and_their_number(term)
        tf_idf_scores = {}

        if not nombre_urls_avec_mot:
            return tf_idf_scores

        # Calculer IDF une seule fois pour le mot
        idf = math.log(self.number_of_pages_indexed / nombre_urls_avec_mot)
        
        all_webpages = self.bdd.get_all_pages_word_counter()

        # Calculer TF-IDF pour chaque document contenant le mot
        for occ in urls_contenant_mot.get('appear_in', []):
            url = occ['url']
            if url in all_webpages:
                count_words_in_url = all_webpages[url]
                tf = occ['occurrences'] / count_words_in_url
                tf_idf = tf * idf
                tf_idf_scores[url] = tf_idf
            else:
                print(f"URL '{url}' not found in all_webpages")

        return tf_idf_scores

    def combine_with_pagerank(self, website):
        combined_scores = {}
        urls = list(website.keys())
        infos = self.bdd.get_infos_for_urls(urls)  # une seule requête pour tous

        for url, score in website.items():
            website_infos = infos.get(url, {})
            combined_scores[url] = {
                "score": self.PONDERATION_TF_IDF * score + self.PONDERATION_PAGERANK * website_infos.get("PageRank", 0),
                "title": website_infos.get("title"),
                "description": website_infos.get("description"),
                "url": website_infos.get("url")
            }
            return combined_scores

    def process_term(self, term, all_tf_idf):
        tf_idf = self.search_term(term)
        with self.lock:
            all_tf_idf.append(tf_idf)
    
    def search_terms(self, query, limit):
        query = query.replace("œ", "oe")
        query = query.replace("æ", "ae")
        query = re.sub(r"[^a-zA-ZÀ-ÿ ']", " ", query)

        all_tf_idf = []
        threads = []
        for term in query.split():
            print(f"Processing term '{term}'")
            thread = threading.Thread(target=self.process_term, args=(term, all_tf_idf))
            thread.start()
            threads.append(thread)
        
        for thread in threads:
            thread.join()
        
        final_scores = {}
        print(all_tf_idf)
        for tf_idf in all_tf_idf:
            for url, score in tf_idf.items():
                if url not in final_scores:
                    final_scores[url] = score
                else:
                    final_scores[url] += score
        
        return dict(sorted(final_scores.items(), key=lambda x: x[1], reverse=True)[:limit])
    
    def search(self, query, limit=20):
        debut = time.time()
        if query.startswith("site:"):
            tf_idf = self.search_terms(query, limit)
        else:
            tf_idf = self.search_terms(query, limit)
        print(tf_idf)
        results = sorted(self.combine_with_pagerank(tf_idf).values(), key=lambda x: x[1], reverse=True)
        print(f"la recherche prend {time.time() - debut} secondes")
        return results
