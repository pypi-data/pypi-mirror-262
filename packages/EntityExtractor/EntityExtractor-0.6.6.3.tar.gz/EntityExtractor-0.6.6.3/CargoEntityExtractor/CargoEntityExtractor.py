import threading
import re
import nltk 
from bs4 import BeautifulSoup 
from nltk.corpus import stopwords
import spacy
from collections import defaultdict
import base64
import os
from spacy.tokens import DocBin
import requests
import zipfile
import logging
from concurrent.futures import ThreadPoolExecutor
from .Load_Cargo_Model import LoadCargoModel
from .TextCleaner import TextCleaner



logging.basicConfig(level=logging.INFO) 



class GetArguments:
    def __init__(self,res:dict) -> None:
        self.res = res

    def get_cargo(self):
        if len(self.res.get('CARGO',[])) != 0:
            output_list = []
            seen = set()  
            for string in self.res['CARGO']:
                if string not in seen:
                    output_list.append(string)
                    seen.add(string) 
            return output_list
        else:
            return None
    
    def get_cargo_size(self):
        if len(self.res.get('CARGO_SIZE',[])) != 0:
            words_to_remove = ['deadweight', 'dwt', 'dwat', 'sdwat', 's.dwat', 'sdwt', 's.dwt', 'dead', 'weight','abt' , 'abt.','k']
            output_list = []
            seen_set = set()  # To keep track of seen items for efficient duplicate checking
            for string in self.res['CARGO_SIZE']:
                cleaned_string = ' '.join(word for word in string.split() if word.lower() not in words_to_remove)
                if cleaned_string not in seen_set:  # Check if the cleaned string is not seen before
                    output_list.append(cleaned_string)
                    seen_set.add(cleaned_string)  # Add the cleaned string to seen set
            return output_list
        else:
            return None
    
    def get_laycan(self):
        output_list = []
        seen = set()
        if len(self.res.get('LAYCAN',[])) != 0:
            for cleaned_string in self.res.get('LAYCAN',[]):
                if cleaned_string not in seen:            
                    output_list.append(cleaned_string)
                    seen.add(cleaned_string)
            return self.res['LAYCAN']
        else:
            return None
        
    def get_load_port(self):
        if len(self.res.get('LOAD_PORT',[])) != 0:
            words_to_remove = ['load','port','l/d','l']
            output_list = []
            seen = set()
            for string in self.res['LOAD_PORT']:
                cleaned_string = ' '.join(word for word in string.split() if word not in words_to_remove)
                if cleaned_string not in seen:
                    output_list.append(cleaned_string)
                    seen.add(cleaned_string)
            return output_list
        else:
            return None
        
    def get_discharge_port(self):
        if len(self.res.get('DISCHARGE_PORT',[])) != 0:
            words_to_remove = ['discharge','l/d']
            output_list = []
            for string in self.res['DISCHARGE_PORT']:
                cleaned_string = ' '.join(word for word in string.split() if word not in words_to_remove)
                output_list.append(cleaned_string)
            return output_list
        else:
            return None
    
        
    def get_discahrge_term(self):
        if len(self.res.get('DISCHARGE_TERM',[])) != 0:
            words_to_remove = ['load','port','/','l/d','load/discharge']
            output_list = []
            seen = set()
            for string in self.res['DISCHARGE_TERM']:
                cleaned_string = ' '.join(word for word in string.split() if word not in words_to_remove)
                if cleaned_string not in seen:
                    output_list.append(cleaned_string)
                    seen.add(cleaned_string)
            return output_list
        else:
            return None

        
        
    def get_load_term(self):
        if len(self.res.get('LOAD_TERM',[])) != 0:
            words_to_remove = ['load','port','/','l/d','load/discharge']
            output_list = []
            seen = set()
            for string in self.res['LOAD_TERM']:
                cleaned_string = ' '.join(word for word in string.split() if word not in words_to_remove)
                if cleaned_string not in seen:
                    output_list.append(cleaned_string)
                    seen.add(cleaned_string)
            return output_list
        else:
            return None

        
    def get_broker_com(self):
        if len(self.res.get('BROKER_COMM',[])) != 0:
            words_to_remove = ['addcomm', '%', 'adcom']
            output_list = []
            for string in self.res['BROKER_COMM']:
                cleaned_string = ' '.join(word for word in string.split() if word not in words_to_remove)
                output_list.append(cleaned_string)
            return output_list
        else:
            return None

    def get_address_com(self):
        if len(self.res.get('ADD_COMM',[])) != 0:
            words_to_remove = ['addcomm', '%', 'adcom']
            output_list = []
            for string in self.res['ADD_COMM']:
                cleaned_string = ' '.join(word for word in string.split() if word not in words_to_remove)
                output_list.append(cleaned_string)
            return output_list
        else:
            return None

  




from functools import partial

class ThreadPoolManager:
    _instance = None

    def __new__(cls, max_workers=3):
        if cls._instance is None:
            cls._instance = super(ThreadPoolManager, cls).__new__(cls)
            cls._instance.executor = ThreadPoolExecutor(max_workers=max_workers)
        return cls._instance

class CargoEntityExtractor(LoadCargoModel):

    def __init__(self):
        super().__init__()
        self.__nlp_cargo = self._LoadCargoModel__get_modal_instance()
        self.text_cleaner = TextCleaner()
        self.__executor = ThreadPoolExecutor()

    def process_nlp(self, nlp, entities_dict, text):
        doc = nlp(text)
        for ent in doc.ents:
            entities_dict[ent.label_].append(ent.text)

    

    def extract_entities(self, text):

        text = self.text_cleaner.decode_into_text(text) 
        cleaned_text_parts = self.text_cleaner.clean(text)
        entities_dict = defaultdict(list)
        futures = []
        if cleaned_text_parts is None:
            return GetArguments(entities_dict)
        else:

            future = self.__executor.submit(self.process_nlp, self.__nlp_cargo, entities_dict, cleaned_text_parts)
            futures.append(future)

            for future in futures:
                future.result()
            
            return GetArguments(entities_dict)