import subprocess as sp
import requests

import re
import json

from tqdm import tqdm
import signal
import psutil


urlname = "http://sanskrit.inria.fr/cgi-bin/SKT/sktgraph2.cgi"
# if the Sanskrit Heritage Platform is installed in the machine,
# instead of fetching from the server like above, use the
# following and comment the previous line
# urlname = "http://localhost/cgi-bin/SKT/sktgraph2"


def get_env_variables(input_text, type_of_segmentation):
    """ Returns the parameters for the cgi call """
    
    env_vars = [
        "lex=SH", "cache=t", "us=f", "font=roma", "t=WX"
    ]
    
    if type_of_segmentation == "input_text":
        env_vars.append("st=t")
        env_vars.append("text=" + sentence.replace(" ", "+"))
        env_vars.append("mode=g")
    else:
        env_vars.append("st=f")
        env_vars.append("text=" + input_text)
        env_vars.append("mode=b")
        if type_of_segmentation == "stemmer":
            env_vars.append("stemmer=t")
        else:
            env_vars.append("pipeline=t")
    
    return env_vars
    

def run_sh(input_text, cgi_file, type_of_segmentation):
    """ Runs the cgi file with a given word/sentence.  
        
        Gets all the analyses in the form of a list of tuples 
        (called nodes).
        
        Returns the final nodes (list of tuples of SH analyses, where
        each tuple corresponds to an individual segment)
    """
    
    time_out = 30
    
    env_vars = get_env_variables(input_text, type_of_segmentation)
    
    query_string = "QUERY_STRING=\"" + "&".join(env_vars) + "\""
    command = query_string + " " + cgi_file
    
    p = sp.Popen(command, stdout=sp.PIPE, shell=True)
    try:
        outs, errs = p.communicate(timeout=time_out)
    except sp.TimeoutExpired:
        kill(p.pid)
        result = ""
    else:
        result = outs.decode('utf-8')
    
    if result == "":
        return ([], "", "Timeout")
    
    print(result)
    
    if ("error" in result) or ("head" in result):
        return ([], "", "Error")
    
    all_nodes_str = result.split("\n")
    
    all_nodes = [tuple(node_str.split("\t")) for node_str in all_nodes_str]
    
    return (all_nodes, result, "Success")
    

def call_sh(parameters):
    """ Calls the cgi of Sanskrit Heritage Segmenter with the 
        parameters
        
        Returns the response
    """
    
    try:
        response = requests.get(url = urlname, params = parameters)
        response_obj = json.loads(response.text)
        response_json = json.dumps(response_obj)
    except Exception as e:
        exception = {}
        exception["error"] = str(e)
        response_json = json.dumps(exception)
        
    return response_json
    


def request_word_analysis(input_text):
    """ Sets the parameters for word analysis
        Returns all possible morphological analyses for the input
    """
    
    env_vars = {
        "lex":"SH", "st":"f", "us":"f", "font":"roma", "t":"WX",
        "text": input_text.replace(" ", "+"), "mode":"b",
        "stemmer":"t"
    }
    
    return call_sh(env_vars)
    

def request_sentence_analysis_joint(input_text):
    """ Sets the parameters for joint sentence analysis
        Returns the analyses of a segmented sentence
    """
    
    env_vars = {
        "lex":"SH", "st":"t", "us":"t", "font":"roma", "t":"WX",
        "text": input_text.replace(" ", "+"), "mode":"b",
        "stemmer":"t"
    }
    
    return call_sh(env_vars)
    
    
def request_sentence_analysis_iterative(input_text):
    """ Returns all possible morphological analyses for the words in 
        the input sentence. Returns word-based analysis
    """
    
    words = input_text.split(" ")
    all_analyses = []
    for word in words:
        morph_analysis = {}
        morph_analysis[word] = request_word_analysis(word)
        all_analyses.append(morph_analysis)
    
    return all_analyses
    

def get_normalized_word(word):
    """ Returns the word in the normalized form.  Normalization
        takes place at the end of the words. If the word ends in
        anusvAra (M), then it is changed to (m)

        Sanskrit Heritage Segmenter presently does not accept 
        words ending in anusvAra (M)
    """

    word = word[:-1] + "m" if word[-1] == "M" else word

    return word


def get_stemmer_fn(stemmer_format):
    """ Returns the stemmer function according to the stemmer 
        format
    """
    
    if stemmer_format == "word":
        stemmer_fn = request_word_analysis
    elif stemmer_format == "sent-iter":
        stemmer_fn = request_sentence_analysis_iterative
    elif stemmer_format == "sent-joint":
        stemmer_fn = request_sentence_analysis_joint
    # The following two cases are under development and hence commented out
    #elif stemmer_format == "word-full":
    #    stemmer_fn = request_word_analysis
    #elif stemmer_format == "sent-full":
    #    stemmer_fn = request_word_analysis
    else:
        stemmer_fn = request_word_analysis

    return stemmer_fn


def run_stemmer_fn(input_text, stemmer_fn):
    """ Normalizes the input_text
        Calls the segmenter with appropriate modes
        Returns the results of the stemmer

        Avoids checking the stemmer function. One can either run the
        stemmer directly from here after getting the stemmer_fn or
        call the stemmer from "run_stemmer"
    """

    normalized_input = get_normalized_word(input_text)

    return stemmer_fn(normalized_input)


def run_stemmer(input_text, stemmer_format):
    """ Gets the stemmer function and redirects to "run_stemmer_fn" to
        normalize the input_text and run the stemmer.  If the
        stemmer_fn is already obtained, call "run_stemmer_fn"
    """

    stemmer_fn = get_stemmer_fn(stemmer_format)
    
    return run_stemmer_fn(input_text, stemmer_fn)

