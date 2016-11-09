
from nltk.tokenize import TweetTokenizer
from nltk.stem.porter import PorterStemmer

import HTMLParser


def break_tag(tag):
    broken_tag = []
    word = ""
    for letter in tag:
        if letter.isupper():
            if word:
                broken_tag.append(word)
            word = letter[:]
        else:
            word = word + letter
    broken_tag.append(word)
    return broken_tag


# function to break up any tags or handles into words if in a normal format
# clean up hash tags which can contain useful information
def clean_tags(split_tweet):
    split_tweet_return = []
    for entry in split_tweet:
        if (entry[0] == "@" and len(entry) > 1):
            split_tweet_return.append("@")
            split_tweet_return.append(entry[1:])
        elif (entry[0] == "#" and len(entry) > 1):
            split_tweet_return.append("#")
            for tag_comp in break_tag(entry[1:]):
                split_tweet_return.append(tag_comp)
        else:
            split_tweet_return.append(entry)
    return split_tweet_return


# go through and label any numeric entries as a special numeric token
def num_token(split_tweet):
    num = "0 1 2 3 4 5 6 7 8 9 ,".split()
    split_tweet_return = []
    for entry in split_tweet:
        if entry == ",":
            split_tweet_return.append(entry)
        else:
            is_other = False
            for char in entry:
                if char not in num:
                    is_other = True
                    break
            if is_other:
                split_tweet_return.append(entry)
            else:
                split_tweet_return.append("|-num-|")
    return split_tweet_return


# go through and label any mixed number and letter entries as a special numalpha token
# make sure that this does not label anything as num_alpha that came from a handle (which is common)
def num_alpha_token(split_tweet):
    num = "0 1 2 3 4 5 6 7 8 9".split()
    alpha = "a b c d e f g h i j k l m n o p q r s t u v w x y z".split()
    split_tweet_return = []
    prior_entry = ""
    for entry in split_tweet:
        has_num = False
        has_alpha = False
        has_other = False
        for char in entry:
            if char in num:
                has_num = True
            elif char in alpha:
                has_alpha = True
            else:
                has_other = True
        if (has_num and has_alpha and not has_other and (prior_entry != "@")):
            split_tweet_return.append("|-num_alpha-|")
        else:
            split_tweet_return.append(entry)
        prior_entry = entry[:]
    return split_tweet_return


# go through and label any numeric words with special tokens
def word_num_token(split_tweet):
    units = [
        "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
        "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
        "sixteen", "seventeen", "eighteen", "nineteen"]
    tens = ["twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
    scales = ["hundred", "thousand", "million", "billion", "trillion"]
    split_tweet_return = []
    for entry in split_tweet:
        if entry in units:
            split_tweet_return.append("|-num_units-|")
        elif entry in tens:
            split_tweet_return.append("|-num_tens-|")
        elif entry in scales:
            split_tweet_return.append("|-num_scales-|")
        else:
            split_tweet_return.append(entry)
    return split_tweet_return


# tokenize a web address if present
def website_tokenize(split_tweet):
    split_tweet_return = []
    for entry in split_tweet:
        if entry[0:4] == "http":
            split_tweet_return.append("|-website-|")
        else:
            split_tweet_return.append(entry)
    return split_tweet_return


# determines if the token is likely an emoticon and if so returns a reduced representation
# the reduced representation is to aid in statistics since the eyes and mouth really convey
# emotions with minimal information included from a nose or something else
def is_emoji(token):
    # these features make up most smileys which is ~90% of all emojis
    # faces will be returned all facing the right ala eyes then mouth
    eyes = ": ; = 8"
    mouth = "( ) [ ] d p { } / @ |"
    found_eyes = False
    found_mouth = False
    emoji = ""
    for char in token:
        if (char in eyes and not found_eyes):
            emoji = emoji + char
            found_eyes = True
        if (char in mouth and not found_mouth):
            emoji = emoji + char
            found_mouth = True
    # flip all emojis to face normal direction if needed
    if (found_eyes and found_mouth):
        if emoji[0] in mouth:
            e_mouth = emoji[0]
            e_eyes = emoji[1]
            emoji = ""
            emoji = emoji + e_eyes
            if e_mouth == "(":
                emoji = emoji + ")"
            elif e_mouth == ")":
                emoji = emoji + "("
            elif e_mouth == "[":
                emoji = emoji + "]"
            elif e_mouth == "]":
                emoji = emoji + "["
            # this one is unique as it has a directionality so only need one check
            elif e_mouth == "d":
                emoji = emoji + "p"
            elif e_mouth == "{":
                emoji = emoji + "}"
            elif e_mouth == "}":
                emoji = emoji + "{"
            else:
                emoji = emoji + e_mouth
        return emoji
    else:
        return token

        # function to check common happy face tweets and reduce them down to only eyes and a mouth


# these are the dominant features that imply emotion
def downgrade_emoji(split_tweet):
    split_tweet_return = []
    for entry in split_tweet:
        split_tweet_return.append(is_emoji(entry))
    return split_tweet_return


def clean_and_tokenize(df):

    #clean up any html tags
    html_parser = HTMLParser.HTMLParser()
    #df["text"] = df["text"].apply(html_parser.unescape)
    #split text on hypenations
    #df["text"] = df["text"].apply(lambda(tweet): tweet.replace("-", " "))
    #start out tokenization using NLTK casual twitter token (store in text_tokenized)
    tknzr = TweetTokenizer(strip_handles=False, reduce_len=True)
    df["text_tokenized"] = df["text"].apply(tknzr.tokenize)
    #split up the tags

    df["text_tokenized"] = df["text_tokenized"].apply(clean_tags)
    #lowercase everything
    df["text_tokenized"] = df["text_tokenized"].apply(lambda(split_tweet): [entry.lower() for entry in split_tweet])
    #tokenize numbers
    df["text_tokenized"] = df["text_tokenized"].apply(num_token)
    #tokenize mixed alphabetical and numeric entries
    df["text_tokenized"] = df["text_tokenized"].apply(num_alpha_token)
    #tokenize any words that are numbers into base units, tens, and scales
    df["text_tokenized"] = df["text_tokenized"].apply(word_num_token)
    #tokenize website links
    df["text_tokenized"] = df["text_tokenized"].apply(website_tokenize)
    #actually modify the emojis
    df["text_tokenized"] = df["text_tokenized"].apply(downgrade_emoji)
    #go through and stem everything using the Porter Stemmer
    st = PorterStemmer()
    df["text_tokenized_stemmed"] = df["text_tokenized"].apply(lambda(split_tweet): [st.stem(entry) for entry in split_tweet])
    #send back the modified dataframe
    return df