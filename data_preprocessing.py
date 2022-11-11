import string
import re
from nltk.corpus import stopwords
import nltk
import yaml


nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

nltk.download('stopwords')
ar_stopwords = set(stopwords.words('arabic'))
ar_stopwords.update(["مع","من","إلى","في","فى","كان","على","علي", "يا"])

with open(r'keywords.yml', encoding='utf-8-sig') as file:
    # The FullLoader parameter handles the conversion from YAML
    # scalar values to Python the dictionary format
    config = yaml.load(file, Loader=yaml.FullLoader)


def remove_special(text):
    for letter in '#.][!XR':
        text = text.replace(letter, '')
    return text


def remove_punctuations(text):
    arabic_punctuations = '''`÷×؛<>_()*&^%][ـ،/:"؟.,'{}~¦+|!”…“–ـ'''
    english_punctuations = string.punctuation
    punctuations_list = arabic_punctuations + english_punctuations
    translator = str.maketrans('', '', punctuations_list)
    return text.translate(translator)


def normalize_arabic(text):
    text = re.sub("[إأآا]", "ا", text)
    text = re.sub("ى", "ي", text)
    text = re.sub("ة", "ه", text)
    text = re.sub("گ", "ك", text)
    return text


def remove_repeating_char(text):
    return re.sub(r'(.)\1+', r'\1', text)


def clean_str(text):
    search = ["أ", "إ", "آ", "ة", "_", "-", "/", ".", "،", " و ", " يا ", '"', "ـ", "'", "ى", "\\", '\n', '\t',
              '&quot;', '?', '؟', '!']
    replace = ["ا", "ا", "ا", "ه", " ", " ", "", "", "", " و", " يا", "", "", "", "ي", "", ' ', ' ', ' ', ' ? ', ' ؟ ',
               ' ! ']

    # remove tashkeel
    p_tashkeel = re.compile(r'[\u0617-\u061A\u064B-\u0652]')
    text = re.sub(p_tashkeel, "", text)
    # #remove longation
    # p_longation = re.compile(r'(.)\1+')
    # subst = r"\1\1"
    # text = re.sub(p_longation, subst, text)

    text = text.replace('وو', 'و')
    text = text.replace('يي', 'ي')
    text = text.replace('اا', 'ا')

    for i in range(0, len(search)):
        text = text.replace(search[i], replace[i])

    # trim
    text = text.strip()

    return text


def keep_only_arabic(text):
    return re.sub(r'[a-zA-Z?]', '', text).strip()


def split_hashtag_to_words(tag):
    tag = tag.replace('#', '')
    tags = tag.split('_')
    if len(tags) > 1:
        return tags
    pattern = re.compile(r"[A-Z][a-z]+|\d+|[A-Z]+(?![a-z])")
    return pattern.findall(tag)


def clean_hashtag(text):
    words = text.split()
    text = list()
    for word in words:
        if is_hashtag(word):
            text.extend(extract_hashtag(word))
        else:
            text.append(word)
    return " ".join(text)


def is_hashtag(word):
    if word.startswith("#"):
        return True
    else:
        return False


def extract_hashtag(text):
    hash_list = ([re.sub(r"(\W+)$", "", i) for i in text.split() if i.startswith("#")])
    word_list = []
    for word in hash_list:
        word_list.extend(split_hashtag_to_words(word))
    return word_list


def remove_mentions(text):
    words = text.split()
    words = [w for w in words if not w.startswith("@")]
    return " ".join(words)


def replace_words(text):
    splitted_text = text.split()
    for i in range(len(splitted_text)):
        if splitted_text[i] in config['convert']:
            splitted_text[i] = config['convert'][splitted_text[i]]

        if splitted_text[i] in ar_stopwords:
            splitted_text[i] = ''

    return " ".join(splitted_text)


def preprocess_text(text):
    text = text[:250]
    text = remove_mentions(text)
    # Replace @username with empty string
    text = re.sub('@[^\s]+', ' ', text)
    text = replace_words(text)

    # Convert www.* or https?://* to " "
    text = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', ' ', text)

    # Replace #word with word
    text = re.sub(r'#([^\s]+)', r'\1', text)
    # remove punctuations
    text = remove_punctuations(text)

    # normalize the text
    text = normalize_arabic(text)

    # remove repeated letters
    text = remove_repeating_char(text)

    # remove special letters
    text = remove_special(text)

    # Clean/Normalize Arabic Text
    text = clean_str(text)

    # remove english words
    text = keep_only_arabic(text)
    # stemming
    # text= stemmer.stem(text)
    if not text:
        text = ' '
    return text.strip()


