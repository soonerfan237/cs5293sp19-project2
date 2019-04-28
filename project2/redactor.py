import argparse #for parsing command line arguments
import nltk #for text processing
from nltk.corpus import wordnet
import os #for checking if file or directory exists
import glob #for finding files in directory
import shutil #for copying files
import re #for regular expressions
import sys #used for stderr output

redacted_names = [] #list to store number of redacted names in each file
redacted_genders = [] #list to store number of redacted gender words in each file
redacted_dates = [] #list to store number of redacted dates in each file
redacted_addresses = [] #list to store number of redacted addresses in each file
redacted_phones = [] #list to store number of redacted phone numbers in each file
redacted_concepts = [] #list to store number of redacted concepts in each file
redacted_files = [] #array of all files processed
_args_concepts = [] #array to store the concepts passed through command line arguments

def main(args_input, args_output, args_names, args_genders, args_dates, args_addresses, args_phones, args_stats, args_concepts):
    #clearing initial arrays.  this is needed so that everything gets cleared between tests
    redacted_names.clear() #list to store number of redacted names in each file
    redacted_genders.clear() #list to store number of redacted gender words in each file
    redacted_dates.clear() #list to store number of redacted dates in each file
    redacted_addresses.clear() #list to store number of redacted addresses in each file
    redacted_phones.clear() #list to store number of redacted phone numbers in each file
    redacted_concepts.clear() #list to store number of redacted concepts in each file
    redacted_files.clear() #array of all files processed
    _args_concepts.clear() #array to store the concepts passed through command line arguments
 
    #for concept in args_concepts:
    #    _args_concepts.append(concept)
    input_files = inputfiles(args_input) #calling function to retrieve list of file paths at command line argument locations
    file_count = 0 #iterator for each file that is processed. used to store count at right part in lists
    for input_file in input_files: #for each file to process
        original_file_path = os.getcwd() + '/' + input_file #gets full path
        #print("FILE: " + original_file_path)
        with open(original_file_path, 'r') as originalfile: #reads from file
            originaltext = originalfile.read() #stores file text
            redactedtext = originaltext #variable to hold redacted text
            if len(redactedtext) > 1: #if document has contents
                #print(originaltext)
                redacted_files.append(original_file_path) #adding file to list of redacted files
                redacted_names.append(0) #initializing counts...
                redacted_genders.append(0)
                redacted_dates.append(0)
                redacted_addresses.append(0)
                redacted_phones.append(0)
                redacted_concepts.append(0)
                print("FILE: " + original_file_path)
                if (args_names): #if names in command line argument
                    redactedtext = redact_names(redactedtext,file_count) #redact names
                if(args_genders): #if genders in command line argument 
                    redactedtext = redact_genders(redactedtext,file_count) #redact genders
                if(args_dates): #if dates in command line argument
                    redactedtext = redact_dates(redactedtext,file_count) #redact dates
                if(args_addresses): #if addresses in command line argument
                    redactedtext = redact_addresses(redactedtext,file_count) #redact addresses
                if(args_phones): #if phones in command line arguments
                    redactedtext = redact_phones(redactedtext,file_count) #redact phones
                redact_concept_file_counts = []
                if (args_concepts is not None):
                    for concept in args_concepts:
                        redact_concept_result = redact_concept(redactedtext,file_count,concept)
                        redactedtext = redact_concept_result[0]
                        redact_concept_file_counts.append(redact_concept_result[1])
                    redacted_concepts[file_count] = redact_concept_file_counts
                file_count = file_count + 1 #increment count of processed files
        outputfile(input_file,args_output, redactedtext) #output redacted text to file
    #print("args_stats = " + args_stats)
    results = []
    if(args_stats == 'stdout'): #if stats to stdout
        results = outputstats_stdout() #print stats to stdout
    elif(args_stats == 'stderr'): #if stats to stderr
        results = outputstats_stderr() #print stats to stderr
    elif(args_stats is not None): #if stats to file
        results = outputstats_file(args_stats) #print stats to file
    return results #return redacted results

def inputfiles(args_input):
    input_files = [] #array to store file paths
    for input in args_input: #for each input command line argument
        for file in glob.glob(input): #finds files in that location
            #print(file)
            input_files.append(file) #appending file path to a list
    return input_files #returning list of file paths

def replace(match): #function to replace contents with X's
    #print("match.group() = " + match.group())
    redacted_string = "" #intializing redacted string
    for i in range(0,len(match.group())): #for each character in the string
        if match.group()[i] == " ": #if a space
            redacted_string = redacted_string + " " #leave the space
        else: #if other character
            redacted_string = redacted_string + "X" #replace with X
    return redacted_string #return redacted string

def replace_string(match):
    redacted_string = ""
    for i in range(0,len(match)):
        if match[i] == " ":
            redacted_string = redacted_string + " " #leave the space
        else: #if other character
            redacted_string = redacted_string + "X" #replace with X
    return redacted_string #return redacted string


def redact_names(input_string,file_count): #function to redact names
    print("REDACTING NAMES...")
    #print("file_count = " + str(file_count))
    redacted_names[file_count] = 0 #intializing list to store number of redacted names
    output_string = input_string #initializing output string of redacted results
    #print(text)
    #get_entity(text)
    for sent in nltk.sent_tokenize(input_string):
        for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
            if hasattr(chunk, 'label') and chunk.label() == 'PERSON':
                #print(chunk.label(), ' '.join(c[0] for c in chunk.leaves()))
                name = ' '.join(c[0] for c in chunk.leaves())
                output_string = output_string.replace(name,replace_string(name))
                redacted_names[file_count] = redacted_names[file_count] + 1
                #print(name)
                #labels_text_name.append([text_path,name])
                #features = get_features(text_path,name)
                #print(features)

    
    
    #sentences = nltk.sent_tokenize(output_string) #tokenizing string into sentences
    #for sentence in sentences: #for each sentence
    #    #print("SENTENCE: " + sentence)
    #    redacted_sentence = sentence #initializing redacted sentence
    #    words = nltk.word_tokenize(sentence) #tokenizing each word in sentence
    #    tags = nltk.pos_tag(words) #tagging words
    #    chunks = nltk.ne_chunk(tags) #chunking word tags
    #    for chunk in chunks: #for each chunk
    #        if isinstance(chunk,nltk.tree.Tree): #if it finds a tree
    #            if chunk.label() == 'PERSON': #and the tree is a person
    #                #print(chunk)
    #                redacted_names[file_count] = redacted_names[file_count] + 1 #iterate count of redacted names
    #                for wordtag in chunk: #for each word in the chunk
    #                    #print(wordtag[0])
    #                    redacted_sentence = redacted_sentence.replace(wordtag[0],'X' * len(wordtag[0])) #replacing redacted words with X's
    #                    output_string = output_string.replace(sentence,redacted_sentence) #replacing redacted sentence into full text
        #print("REDACTED: " + redacted_sentence)
    return output_string #returning redacted text

def redact_genders(input_string,file_count): #function to redact gender words
    print("REDACTING GENDERS...")
    redacted_genders[file_count] = 0 #initializing count of redacted gender words
    output_string = input_string #initializing string for redacted text
    matches = re.findall(r'male|female|\bboy\b|\bgirl\b|\bman\b|woman|father|mother|\bson\b|daughter|niece|nephew|grandpa|grandma|uncle|aunt', output_string,flags=re.I) #counting number of words that are gender words
    redacted_genders[file_count] = redacted_genders[file_count] + len(matches) #storing count of gender words to redact
    output_string = re.sub(r'male|female|\bboy\b|\bgirl\b|\bman\b|woman|father|mother|\bson\b|daughter|niece|nephew|grandpa|grandma|uncle|aunt',replace,output_string,flags=re.I) #substituting gender word with X's
    matches = re.findall(r'\bhis\b|\bhim\b|\bher\b|\bhe\b|\bshe\b|\bmr.|\bmrs.|\bms.', output_string,flags=re.I) #finding more gender words
    redacted_genders[file_count] = redacted_genders[file_count] + len(matches) #adding to count
    output_string = re.sub(r'\bhis\b|\bhim\b|\bher\b|\bhe\b|\bshe\b|\bmr.|\bmrs.|\bms.',replace,output_string,flags=re.I) #replacing more gender words
    return output_string #returning redacted string

def redact_dates(input_string,file_count): #function to redact dates
    print("REDACTING DATES...")
    redacted_dates[file_count] = 0 #initializing count of redacted words to 0
    output_string = input_string #initializing string to redact
    matches = re.findall(r'\d\d?[/\-]\d\d?[/\-]\d\d\d?\d?',output_string) #finding matches for date formats
    redacted_dates[file_count] = redacted_dates[file_count] + len(matches) #adding count of redacted dates
    output_string = re.sub(r'\d\d?[/\-]\d\d?[/\-]\d\d\d?\d?',replace,output_string) #redacting dates

    matches = re.findall(r'monday|tuesday|wednesday|thursday|friday|saturday|sunday',output_string, flags=re.I) #matching days of week
    redacted_dates[file_count] = redacted_dates[file_count] + len(matches) #counting matches for days of week
    output_string = re.sub(r'monday|tuesday|wednesday|thursday|friday|saturday|sunday',replace,output_string, flags=re.I) #redacting days of week
    
    matches = re.findall(r'\d?\d? ?(january|february|march|april|may|june|july|august|september|october|november|december|\bjan\b|\bfeb\b|\bmar\b|\bapr\b|\bmay\b|\bjun\b|\bjul\b|\baug\b|\bsep\b|\boct\b|\bnov\b|\bdec\b) ?\d?\d?,? ?\d?\d?\d?\d?',output_string,flags=re.I) #counting months
    redacted_dates[file_count] = redacted_dates[file_count] + len(matches) #adding counts to stats
    output_string = re.sub(r'\d?\d? ?(january|february|march|april|may|june|july|august|september|october|november|december|\bjan\b|\bfeb\b|\bmar\b|\bapr\b|\bmay\b|\bjun\b|\bjul\b|\baug\b|\bsep\b|\boct\b|\bnov\b|\bdec\b) ?\d?\d?,? ?\d?\d?\d?\d?',replace,output_string,flags=re.I) #redacting months
    
    matches = re.findall(r'january|february|march|april|may|june|july|august|september|october|november|december',output_string, flags=re.I) #finding more month formats
    redacted_dates[file_count] = redacted_dates[file_count] + len(matches) #counting months
    output_string = re.sub(r'january|february|march|april|may|june|july|august|september|october|november|december',replace,output_string, flags=re.I) #redacting more month formats
    
    return output_string #returning redacted string

def redact_addresses(input_string,file_count): #function to redact addresses
    print("REDACTING ADDRESSES...")
    redacted_addresses[file_count] = 0 #initializing count of redacted addresses
    output_string = input_string #initializing output string for redacted text
    matches = re.findall(r'\b\d\d?\d?\d?\d? \w+ (street|st|hill|avenue|ave|way|boulevard|blvd|road|rd|drive|dr|lane|ln|grove|place|pl|square|sq)\b',output_string,flags=re.I) #finding matches to address formats
    #print(matches)
    redacted_addresses[file_count] = redacted_addresses[file_count] + len(matches) #counting redacted words
    output_string = re.sub(r'\b\d\d?\d?\d?\d? \w+ (street|st|hill|avenue|ave|way|boulevard|blvd|road|rd|drive|dr|lane|ln|grove|place|pl|square|sq)\b',replace,output_string,flags=re.I) #redacting words
    return output_string #returning redacted string

def redact_phones(input_string,file_count): #function to redact phones
    print("REDACTING PHONES...")
    redacted_phones[file_count] = 0 #initializing count of redacted phones
    output_string = input_string #initializing output string of redacted text
    matches = re.findall(r'\b(\(?\d?\d?\d?\))? ?\d\d\d-\d\d\d\d\b',output_string) #matching phone number format
    #print(matches)
    redacted_phones[file_count] = redacted_phones[file_count] + len(matches) #counting redacted phone numbers
    output_string = re.sub(r'\b(\(?\d?\d?\d?\))? ?\d\d\d-\d\d\d\d\b',replace,output_string) #redacting phone numbers
    return output_string #returning redacted text

def redact_concept(input_string,file_count,concept): #function to redact concepts
    print("REDACTING CONCEPT (" + concept + ")...")
    redactedconcept = 0 #setting index of the concept to redact
    strings_to_redact = [] #initializing list of words related to concept
    output_string = input_string #initializing output string
    synonyms = wordnet.synsets(concept) #generating synset for concept
    for synonym in synonyms: #for each synonym
        strings_to_redact.append(synonym.name().split(".")[0]) #adding synonym to a list of words to redact
        similars = synonym.similar_tos() #finding words similar to each synonym
        for similar in similars: #for each similar word
            strings_to_redact.append(similar.name().split(".")[0]) #add it to the list of words to redact
    for string in strings_to_redact: #for each word to redact
        sentences = nltk.sent_tokenize(output_string) #tokenizing string into sentences
        for sentence in sentences: #for each sentence
            #print("SENTENCE: " + sentence)
            redacted_sentence = sentence #initializing redacted sentence
            redacted_string = ""
            if string in redacted_sentence: #if string to redact is in the sentence
                for i in range(0,len(redacted_sentence)): #for each character in the string
                    if redacted_sentence[i] == " ": #if a space
                        redacted_string = redacted_string + " " #leave the space
                    else: #if other character
                        redacted_string = redacted_string + "X" #replace with X
                redacted_sentence = redacted_string 
                redactedconcept = redactedconcept + 1 #iterate count of redacted concepts
                output_string = output_string.replace(sentence,redacted_sentence) #replacing redacted sentence into full text
    return [output_string, redactedconcept]

def outputfile(original_file, args_output, redactedtext): #function to output redacted text to file
    #print("REDACTED:")
    #print(redactedtext)
    cwd = os.getcwd() #getting current directory
    output_directory = cwd + '/' + args_output #generating output directory based on command line argument
    if not os.path.exists(output_directory): #if directory does not exist
        os.mkdir(output_directory) #create directory
    original_file_path = cwd + '/' + original_file #getting path of original file
    redacted_file_name = os.path.basename(original_file_path) + ".redacted" #generating path for redacted file
    redacted_file_path = output_directory + redacted_file_name #generating redacted file path
    print("REDACTED FILE: " + redacted_file_path)
    with open(redacted_file_path, 'w') as redacted_file: #open redacted file
        redacted_file.write(redactedtext) #write redacted contents to file

def outputstats_file(file_name): #function to output stats to file
    print("SAVING STATS TO FILE: " + file_name)
    cwd = os.getcwd() #getting current directory
    outputstats_directory = cwd + '/' + file_name #getting directory name to output file
    #if not os.path.isfile(outputstats_directory):
        #print("directory NOT exist")
        #os.mkdir(outputstats_directory)
    with open(outputstats_directory, 'w') as outputstats_file:
        outputstats_file.write("") #clearing file contents
    with open(outputstats_directory, 'a+') as outputstats_file: #appending redacted stats to file
        outputstats_file.write("==============REDACTION STATISTICS================\n")
        total_redacted_names = 0
        total_redacted_genders = 0
        total_redacted_dates = 0
        total_redacted_addresses = 0
        total_redacted_phones = 0
        total_redacted_concepts = []
        for j in range(0,len(_args_concepts)):
            total_redacted_concepts.append(0)
        for i in range(0,len(redacted_files)):
            total_redacted_names = total_redacted_names + redacted_names[i]
            total_redacted_genders = total_redacted_genders + redacted_genders[i]
            total_redacted_dates = total_redacted_dates + redacted_dates[i]
            total_redacted_addresses = total_redacted_addresses + redacted_addresses[i]
            total_redacted_phones = total_redacted_phones + redacted_phones[i]
            for j in range(0,len(_args_concepts)):
                total_redacted_concepts[j] = total_redacted_concepts[j] + redacted_concepts[i][j]
            outputstats_file.write("FILE: " + redacted_files[i] + "\n")#output results
            outputstats_file.write(str(redacted_names[i]) + " names redacted.\n")
            outputstats_file.write(str(redacted_genders[i]) + " gender words redacted.\n")
            outputstats_file.write(str(redacted_dates[i]) + " dates redacted.\n")
            outputstats_file.write(str(redacted_addresses[i]) + " addresses redacted.\n")
            outputstats_file.write(str(redacted_phones[i]) + " phone numbers redacted.\n")
            for j in range(0,len(_args_concepts)):
                outputstats_file.write(str(redacted_concepts[i][j]) + " " + _args_concepts[j] + " concepts redacted.\n")
            outputstats_file.write("==============================================\n")
        outputstats_file.write("TOTALS:\n") #printing total stats to file
        outputstats_file.write(str(total_redacted_names) + " names redacted.\n")
        outputstats_file.write(str(total_redacted_genders) + " gender words redacted.\n")
        outputstats_file.write(str(total_redacted_dates) + " dates redacted.\n")
        outputstats_file.write(str(total_redacted_addresses) + " addresses redacted.\n")
        outputstats_file.write(str(total_redacted_phones) + " phone numbers redacted.\n")
        for j in range(0,len(_args_concepts)):
            outputstats_file.write(str(total_redacted_concepts[j]) + " " + _args_concepts[j] + " concepts redacted.\n")
    return [total_redacted_names, total_redacted_genders, total_redacted_dates, total_redacted_addresses, total_redacted_phones, total_redacted_concepts] #returning total stats - this is needed for test functions

def outputstats_stderr(): #function to print redacted stats to stderr.  see function above for explanation of each line. the only difference is the locatin of output
    print(" ",file=sys.stderr)
    print(" ",file=sys.stderr)
    print("==============REDACTION STATISTICS================",file=sys.stderr)
    total_redacted_names = 0
    total_redacted_genders = 0
    total_redacted_dates = 0
    total_redacted_addresses = 0
    total_redacted_phones = 0
    total_redacted_concepts = []
    for j in range(0,len(_args_concepts)):
        total_redacted_concepts.append(0)
    for i in range(0,len(redacted_files)):
        total_redacted_names = total_redacted_names + redacted_names[i]
        total_redacted_genders = total_redacted_genders + redacted_genders[i]
        total_redacted_dates = total_redacted_dates + redacted_dates[i]
        total_redacted_addresses = total_redacted_addresses + redacted_addresses[i]
        total_redacted_phones = total_redacted_phones + redacted_phones[i]
        for j in range(0,len(_args_concepts)):
            total_redacted_concepts[j] = total_redacted_concepts[j] + redacted_concepts[i][j]
        print("FILE: " + redacted_files[i],file=sys.stderr)
        print (str(redacted_names[i]) + " names redacted.",file=sys.stderr)
        print (str(redacted_genders[i]) + " gender words redacted.",file=sys.stderr)
        print (str(redacted_dates[i]) + " dates redacted.",file=sys.stderr)
        print (str(redacted_addresses[i]) + " addresses redacted.",file=sys.stderr)
        print (str(redacted_phones[i]) + " phone numbers redacted.",file=sys.stderr)
        for j in range(0,len(_args_concepts)):
            print(str(redacted_concepts[i][j]) + " " + _args_concepts[j] + " concepts redacted.",file=sys.stderr)
        print("==============================================",file=sys.stderr)
    print("TOTALS:",file=sys.stderr)
    print (str(total_redacted_names) + " names redacted.",file=sys.stderr)
    print (str(total_redacted_genders) + " gender words redacted.",file=sys.stderr)
    print (str(total_redacted_dates) + " dates redacted.",file=sys.stderr)
    print (str(total_redacted_addresses) + " addresses redacted.",file=sys.stderr)
    print (str(total_redacted_phones) + " phone numbers redacted.",file=sys.stderr)
    for j in range(0,len(_args_concepts)):
            print(str(total_redacted_concepts[j]) + " " + _args_concepts[j] + " concepts redacted.",file=sys.stderr)
    return [total_redacted_names, total_redacted_genders, total_redacted_dates, total_redacted_addresses, total_redacted_phones, total_redacted_concepts]

def outputstats_stdout(): #function to print results to stdout.  see function above for full explanation of each line.
    print(" ")
    print(" ")
    print("==============REDACTION STATISTICS================")
    total_redacted_names = 0
    total_redacted_genders = 0
    total_redacted_dates = 0
    total_redacted_addresses = 0
    total_redacted_phones = 0
    total_redacted_concepts = []
    for j in range(0,len(_args_concepts)):
        total_redacted_concepts.append(0)
    for i in range(0,len(redacted_files)):
        total_redacted_names = total_redacted_names + redacted_names[i]
        total_redacted_genders = total_redacted_genders + redacted_genders[i]
        total_redacted_dates = total_redacted_dates + redacted_dates[i]
        total_redacted_addresses = total_redacted_addresses + redacted_addresses[i]
        total_redacted_phones = total_redacted_phones + redacted_phones[i]
        for j in range(0,len(_args_concepts)):
            total_redacted_concepts[j] = total_redacted_concepts[j] + redacted_concepts[i][j]
        print("FILE: " + redacted_files[i])
        print (str(redacted_names[i]) + " names redacted.")
        print (str(redacted_genders[i]) + " gender words redacted.")
        print (str(redacted_dates[i]) + " dates redacted.")
        print (str(redacted_addresses[i]) + " addresses redacted.")
        print (str(redacted_phones[i]) + " phone numbers redacted.")
        for j in range(0,len(_args_concepts)):
            print(str(redacted_concepts[i][j]) + " " + _args_concepts[j] + " concepts redacted.")
        print("==============================================")
    print("TOTALS:")
    print (str(total_redacted_names) + " names redacted.")
    print (str(total_redacted_genders) + " gender words redacted.")
    print (str(total_redacted_dates) + " dates redacted.")
    print (str(total_redacted_addresses) + " addresses redacted.")
    print (str(total_redacted_phones) + " phone numbers redacted.")
    for j in range(0,len(_args_concepts)):
            print(str(total_redacted_concepts[j]) + " " + _args_concepts[j] + " concepts redacted.")
    return [total_redacted_names, total_redacted_genders, total_redacted_dates, total_redacted_addresses, total_redacted_phones, total_redacted_concepts]

if __name__ == '__main__': #parsing command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, action="append",required=True,help="File extension to be read.")
    parser.add_argument("--names", action='store_true',help="Redact names.")
    parser.add_argument("--genders", action='store_true',help="Redact genders.")
    parser.add_argument("--dates", action='store_true',help="Redact dates.")
    parser.add_argument("--addresses", action='store_true',help="Redact addresses.")
    parser.add_argument("--phones", action='store_true',help="Redact phone numbers.")
    parser.add_argument("--concept", type=str, action="append",help="Redact concept.")
    parser.add_argument("--output", type=str,required=True,help="Output location.")
    parser.add_argument("--stats", type=str,help="Redaction stats.")    
    args = parser.parse_args()
    if args.input:
        main(args.input, args.output, args.names, args.genders, args.dates, args.addresses, args.phones, args.stats, args.concept)
