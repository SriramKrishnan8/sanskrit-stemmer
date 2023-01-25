import subprocess as sp
import requests

import re
import json

from tqdm import tqdm
import signal
import psutil


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
    
    #urlname = "http://sanskrit.inria.fr/cgi-bin/SKT/sktgraph2.cgi"
    urlname = "http://localhost/cgi-bin/SKT_experimental/sktgraph2"
    
    response = requests.get(url = urlname, params = parameters)
    
    return response
    


def request_word_analysis(input_text):
    """ Returns all possible morphological analyses for the input """
    
    env_vars = {
        "lex":"SH", "st":"f", "us":"f", "font":"roma", "t":"WX",
        "text": input_text.replace(" ", "+"), "mode":"b",
        "stemmer":"t"
    }
    
    response = call_sh(env_vars)
    r_json = json.loads(response.text)
    
    return r_json
    

def request_sentence_analysis_joint(input_text):
    """ Returns the analyses of a segmented sentence """
    
    env_vars = {
        "lex":"SH", "st":"t", "us":"t", "font":"roma", "t":"WX",
        "text": input_text.replace(" ", "+"), "mode":"b",
        "stemmer":"t"
    }
    
    response = call_sh(env_vars)
    r_json = json.loads(response.text)
    
    return r_json
    
    
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


#print("Segmenter Word -> " + str(run_sh("xaSaraWaH", "https://sanskrit.inria.fr/cgi-bin/SKT/sktgraph.cgi", "sentence")[0]) + "\n")
#print("Segmenter Word -> " + str(run_sh("xaSaraWaH", "/usr/lib/cgi-bin/SKT/sktgraph", "sentence")[0]) + "\n")
#print("Segmenter Sentence -> " + str(run_sh("AxISvarAya praNamAmi wasmE yena upaxiRtA haTayogavixyA", "/usr/lib/cgi-bin/SKT/sktgraph", "sentence")[0]) + "\n")
#print("Stemmer Word -> " + str(request_word_analysis("xaSaraWaH")) + "\n")
#print("Stemmer Sentence (Iterative) -> " + str(request_sentence_analysis_iterative("AxISvarAya praNamAmi wasmE yena upaxiRtA haTayogavixyA")) + "\n")
#print("Stemmer Sentence (Joint) -> " + str(request_sentence_analysis_joint("AxISvarAya praNamAmi wasmE yena upaxiRtA haTayogavixyA")) + "\n")

