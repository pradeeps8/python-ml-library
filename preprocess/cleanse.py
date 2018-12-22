from nltk.stem.snowball import SnowballStemmer
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import WhitespaceTokenizer
from nltk.corpus import stopwords
import nltk
nltk.download('stopwords')
nltk.download('wordnet')

def clean_text(df, cols):
    for col in cols:
        df[col]=df[col].str.replace('<.*?>', ' ', regex=True) #HTML
        df[col]=df[col].str.replace('\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{7}', ' ', regex=True) #TimeStamp 
        df[col]=df[col].str.replace('[A-Za-x0-9]{8}-[A-Za-x0-9]{4}-[A-Za-x0-9]{4}-[A-Za-x0-9]{4}-[A-Za-x0-9]{12}', ' ', regex=True)#ID
        df[col]=df[col].str.replace(r'\n', ' ', regex=False) #Newline
        df[col]=df[col].str.replace(r'\r', ' ', regex=False) #Newline
        df[col]=df[col].str.replace('&nbsp', ' ', regex=False) #&
        df[col]=df[col].str.replace('[^A-Za-z]+', ' ', regex=True) #remove all characters other than alphabets
        df[col]=df[col].str.replace('\s\s+', ' ', regex=True) #remove extra space
    return df

def generate_tokens(df, cols, language, merged_col_name):
    tokenizer = WhitespaceTokenizer()
    lemmatizer = WordNetLemmatizer()
    snowball_stemmer = SnowballStemmer(language)
    stop_words = set(stopwords.words(language))
    
    def lemmatize(text):
        if type(text)!=None:
            txt= [lemmatizer.lemmatize(w) for w in tokenizer.tokenize(text.lower())]
            li_txt=[snowball_stemmer.stem(w) for w in txt if w not in stop_words]
        else:
            li_txt=[]
        return li_txt
    
    df[merged_col_name] = df[cols[0]].apply(lemmatize)
    for i in range(1, len(cols)):
        df[merged_col_name] += df[cols[i]].apply(lemmatize)
    
    return df

