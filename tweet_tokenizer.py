"""
This tokenize method is based on Christopher Potts's.

http://sentiment.christopherpotts.net/code-data/happyfuntokenizing.py

1. The tuple regex_str defines a list of regular expression
   strings.

2. The regex_str strings are put, in order, into a compiled
   regular expression object called tokens_re.

3. The tokenization is done by tokens_re.findall(s), where s is the
   user-supplied string, inside the tokenize() method of the class
   Tokenizer.

4. When instantiating Tokenizer objects, there is a single option:
   preserve_case.  By default, it is set to True. If it is set to
   False, then the tokenizer will downcase everything except for
   emoticons.

5. Stop words and punctuations are then removed
"""
import string
import re
import htmlentitydefs
import nltk.data
tokenizer = nltk.data.load('nltk:tokenizers/punkt/english.pickle')
from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer

SlangLookupTable = "./data/SentStrength_Data/SlangLookupTable.txt"
EmoticonLookupTable = "./data/SentStrength_Data/EmoticonLookupTable.txt"

informal_words = []
emoticons = []

with open(SlangLookupTable) as f:
    for line in f.readlines():
        word = line.split()[0]
        informal_words.append(word)

with open(EmoticonLookupTable) as f:
    for line in f.readlines():
        emoticon = line.split()[0]
        emoticons.append(emoticon)

stop_words = set(stopwords.words("english"))
# stop_words_tweets = set(stopwords.words('english_tweet'))

# print informal_words

# emoticons_str = ' '.join(informal_words)

emoticon_str = r"""
    (?:
      [<>]?
      [:;=8]                     # eyes
      [\-o\*\']?                 # optional nose
      [\)\]\(\[dDpP/\:\}\{@\|\\] # mouth
      |
      [\)\]\(\[dDpP/\:\}\{@\|\\] # mouth
      [\-o\*\']?                 # optional nose
      [:;=8]                     # eyes
      [<>]?
    )"""

# print emoticon_str
emoticon_str = r"""(%s)""" % "|".join(map(re.escape, emoticons + emoticon_str.split()))

# exit()

# The components of the tokenizer:
regex_str = (
    # Phone numbers:
    r"""
    (?:
      (?:            # (international)
        \+?[01]
        [\-\s.]*
      )?
      (?:            # (area code)
        [\(]?
        \d{3}
        [\-\s.\)]*
      )?
      \d{3}          # exchange
      [\-\s.]*
      \d{4}          # base
    )"""
    ,
    # Emoticons:
    emoticon_str
    ,
    r"""
     (<[^>]+>)        # HTML tags:
    """
    ,
    r"""
    (?:@[\w_]+)     # Twitter username
    """
    ,
    r"""
    (?:\#+[\w_]+[\w\'_\-]*[\w_]+)   # Twitter hashtags
    """
    # Remaining word types:
    ,
    r"""
    (?:[a-z][a-z'\-_]+[a-z])        # Words with apostrophes or dashes.
    # |
    # (?:[+\-]?\d+[,/.:-]\d+[+\-]?)   # Numbers, including fractions, decimals.
    |
    (?:[\w_]+)                      # Words without apostrophes or dashes.
    # |
    # (?:\.(?:\s*\.){1,})             # Ellipsis dots.
    |
    (?:\S)                          # Everything else that isn't whitespace.
    """
    )

# print emoticon_str

# exit()

# The emoticon string gets its own regex so that we can preserve case for them as needed:
emoticon_re = re.compile(emoticon_str, re.VERBOSE | re.IGNORECASE| re.UNICODE)

# This is the core tokenizing regex:
tokens_re = re.compile(r"""(%s)""" % "|".join(regex_str), re.VERBOSE | re.IGNORECASE | re.UNICODE)
# tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE | re.UNICODE)

# These are for regularizing HTML entities to Unicode:
html_entity_digit_re = re.compile(r"&#\d+;")
html_entity_alpha_re = re.compile(r"&\w+;")
amp = "&amp;"


def html2unicode(s):
    """
    Internal method that seeks to replace all the HTML entities in
    s with their corresponding unicode characters.
    """
    # First the digits:
    ents = set(html_entity_digit_re.findall(s))
    if len(ents) > 0:
        for ent in ents:
            entnum = ent[2:-1]
            try:
                entnum = int(entnum)
                s = s.replace(ent, unichr(entnum))
            except:
                pass
    # Now the alpha versions:
    ents = set(html_entity_alpha_re.findall(s))
    ents = filter((lambda x: x != amp), ents)
    for ent in ents:
        entname = ent[1:-1]
        try:
            s = s.replace(ent, unichr(htmlentitydefs.name2codepoint[entname]))
        except:
            pass
        s = s.replace(amp, " and ")
    return s

PUNCTS = set(string.punctuation)
NUMBERS = set('0123456789')


def nltk_tokenize(s):
    # Try to ensure unicode:
    try:
        s = unicode(s)
    except UnicodeDecodeError:
        s = str(s).encode('string_escape')
        s = unicode(s)
    # Fix HTML character entitites:
    s = html2unicode(s)

    tknzr = TweetTokenizer(strip_handles=False, reduce_len=True)
    words = tknzr.tokenize(s)
    return words

tokenizer = "NLTK"

def tokenize(s, preserve_case=False):
    # Try to ensure unicode:
    try:
        s = unicode(s)
    except UnicodeDecodeError:
        s = str(s).encode('string_escape')
        s = unicode(s)

    # Fix HTML character entitites:
    s = html2unicode(s)


    if tokenizer == "NLTK":
        """
        NLTK tokenizer
        """
        tknzr = TweetTokenizer(strip_handles=False, reduce_len=True)
        words = tknzr.tokenize(s)
    elif tokenizer == "Custom":
        s.replace("\n", " ")  # merge multiple lines of tweets if any
        s = re.sub('[\s]+|&amp;', ' ', s)  # Remove additional white spaces
        s = re.sub(r'https?:\/\/.*\/[a-zA-Z0-9]*', '', s)  # Remove hyperlinks

        """
        custom tokenizer
        """
        s = nltk.tokenize.casual.remove_handles(s)          # remove twitter username handles from text
        # Tokenize:
        words = tokens_re.findall(s)
        # print s
        # print words
        # Possible alter the case, but avoid changing emoticons like :D into :d:
        if not preserve_case:
            words = map((lambda x: x[0] if emoticon_re.search(x[0]) else x[0].lower()), words)

        words = [w for w in words if not (w.strip() in stop_words or w.strip() in PUNCTS) and not w.strip().isnumeric()] # remove stop words AND punctuations

    return words