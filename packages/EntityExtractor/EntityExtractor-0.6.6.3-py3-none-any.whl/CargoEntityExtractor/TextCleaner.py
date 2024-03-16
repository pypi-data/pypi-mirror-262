import re
from bs4 import BeautifulSoup
import spacy
from .WordReplacements import word_replacements
import logging
import base64

logging.basicConfig(level=logging.INFO) 


class NLPOBJ:
    _instance = None
    
    def __new__(cls,*args,**kwargs):
        if NLPOBJ._instance is None:
            spacy.cli.download("en_core_web_lg")
            
            NLPOBJ._instance = spacy.load("en_core_web_lg")
        return NLPOBJ._instance




class TextCleaner:

    irr_words = ["//n", "//r", "/n", "/r", "\n",'\r','\\r','\\n','\xa0',"\u200b","\ufeff","\\u200b"]
    punct = list('!"#$\'*+:;<=>?@[\\]^_`{|}~')
    stop_words = ['dear' , 'mr' , 'telix' , 'msg' , 'ref','fm','good','day' , 'woorim']
            
    @classmethod
    def clean_text(self, text):
        try:
            soup = BeautifulSoup(text, "html.parser")
            text = soup.get_text(separator=' ')
            text = text.lower()
            pattern = '|'.join(map(re.escape, self.irr_words))
            text = re.sub(pattern, ' -- ', text)
            content_before_disclaimer = re.search(r'(.+?)\bdisclaimer\b', text, re.DOTALL)
            if content_before_disclaimer:
                text = content_before_disclaimer.group(1).strip()
            # Replace 'm[./]v' with 'mv'
            text = re.sub(r'm[./]v', 'mv', text)
            return text.strip()
        except Exception as e:
            logging.error("Cleaning text failed %s",e)
            return None
        
    @classmethod
    def clean(self , text):
        try:
            nlp = NLPOBJ()
            text = TextCleaner.clean_text(text)
            words_list = []
            doc = nlp(text)
            for token in doc:
                if not token.like_email and not token.like_url and token.text not in self.punct and not token.is_space:
                    word_to_append = token.text
                    if word_to_append in word_replacements:
                        word_to_append = word_replacements[word_to_append]
                    if word_to_append not in self.stop_words :
                        words_list.append(word_to_append)
                    
            replaced_text = ' '.join(words_list)
            return replaced_text
        except Exception as e:
            logging.error("Cleaning Failed %s",e)
            return None
        

    def decode_into_text(self, text):
        try:
            decoded_bytes = base64.b64decode(text)
            decoded_text = decoded_bytes.decode('utf-8')
            return decoded_text
        except Exception as e:
            logging.error("Given input is not in base64 form")
                