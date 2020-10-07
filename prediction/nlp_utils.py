import nltk
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer

nltk.download("stopwords")
nltk.download('words')
stop_english = set(stopwords.words('english'))
english_words = set(x.lower() for x in nltk.corpus.words.words())

def clean(df,field):
	df[field] = df[field].str.replace("[^a-zA-Z ]", "")
	df[field].str.lower()
	df = df.dropna(how="all")
	return df

def stem_sentences(sentence):
	tokens = sentence.split()
	stemmed_tokens = [stemmer.stem(token) for token in tokens]
	return " ".join(stemmed_tokens)

def stem_df(df,field,language): 	
	global stemmer
	stemmer = SnowballStemmer(language)
	df[field] = df[field].apply(stem_sentences)
	return df
    
def drop_stop_df(df,field):
	df[field] = df[field].apply(drop_stop_sentence)
	return df

def drop_stop_sentence(sentence):
	tokens = sentence.split()
	stopped_tokens = [x for x in tokens if x not in stop_english]
	return " ".join(stopped_tokens)

def remove_english(df,field):
	df[field] = df[field].apply(drop_eng_sentence)
	return df

def drop_eng_sentence(sentence):
	tokens = sentence.split()
	stopped_tokens = [x for x in tokens if x not in english_words]
	return " ".join(stopped_tokens)

def remove_non_english(df,field):
	df[field] = df[field].apply(drop_non_eng_sentence)
	return df

def drop_non_eng_sentence(sentence):
	tokens = sentence.split()
	stopped_tokens = [x for x in tokens if x in english_words]
	return " ".join(stopped_tokens)

def apply_tfidf(verbs):
    tfidf = TfidfVectorizer(sublinear_tf= True,
                            min_df= 3,
                            norm= "l2",
                            encoding= "latin-1",
                            ngram_range= (1,2),
                            stop_words= "english",
#                             max_features = 40000,
                           )
    features = tfidf.fit_transform(verbs)
    return features, tfidf