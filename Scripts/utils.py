from os.path import dirname
import inspect


title_case_exceptions = [
    "and", "as", "but", "for", "if", "nor", "or", "so", "yet", "a", "an", "the",
    "as", "at", "by", "for", "in", "of", "off", "on", "per", "to", "up", "via"]

# https://stackoverflow.com/questions/3728655/titlecasing-a-string-with-exceptions?rq=3
def get_capitalised(string):
    word_list = string.lower().split(' ')
    capitalised = [word_list[0].capitalize()]
    for word in word_list[1:]:
        capitalised.append(word if word in title_case_exceptions else word.capitalize())
    capitalised = " ".join(capitalised)
    return capitalised

def add_line_breaks(string, length=25):
    if len(string) > length:
        splits = get_splits(string)
        differences = {abs(len(split[0]) - len(split[1])): split for split in splits}
        minimum_difference = min(list(differences.keys()))
        string = "\n".join(differences[minimum_difference])
    return string

def get_splits(string):
    words = string.split(" ")
    splits = [[" ".join(word for word in words[:word_limit]),
               " ".join(word for word in words[word_limit:])]
              for word_limit in range(len(words))]
    return splits

def get_time_columns(dataframe):
    columns = set(dataframe.columns.values)
    non_time_columns = set([
        "LSOA", "Borough", "Minor Category", "Major Category", "Population"])
    time_columns = sorted(list(columns - non_time_columns))
    return time_columns

def get_base_path(source):
    if hasattr(source, "__module__"):
        source = inspect.getfile(source.__class__)
    path = dirname(dirname(dirname(source)))
    return path


purple = "#6c17b9"
blue   = "#1db8f7"
grey   = "#6d6d6d"
