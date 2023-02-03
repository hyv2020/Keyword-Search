# Imports Here
import os
import csv
import re

from os import walk
from os.path import join

def load_rules(path: str) -> list:
    input_file = open(path, "r")
    text = input_file.read()
    input_file.close()
    keywords_file = text.strip().split() #Split the text into a list for later use
    return keywords_file # Output the list   


def get_hits(path: str, keywords: str)-> list: 
# Creates a function with an input for file path and an input for keywords search
    search_file = open(path, "r") # Open a file from this path in read mode
    text = search_file.read() # Read the file
    search_file.close() # Close the file
    hits = [] # Array to store many results
    for keyword in keywords: # For each of x in y
        re.IGNORECASE # Ignore casing when counting
        text_count = len(re.findall(keyword,text)) # Count the number regex 
        hits.append(text_count) # Add the result to array
    return hits # Outputs the array of search results    


def scan(path: str, keywords:list)-> dict:
# Creates a function to scan the folder with an input for file path and keywords
    walker = walk(path) # Use the walk function to use the path directory
    results = {} # dictionary for storing output.
    for given in walker: # Loop to look at every file
        for file in given[2]: # Second loop because there are more folders
            full_path = join(given[0], file) # Join the path to get full path
            list_of_words = get_hits(full_path, keywords) # Use the get_hits function to count keywords in each file
            if sum(list_of_words) > 0:
                # This gives the sum of add the values of the keywords found. if no matches found, don't add to dictionary.               
                results[full_path] = list_of_words # Add to dictionary
    return results # Output the dictionary


def sort_2d_list(data: list, index: int, reverse=False):
# Sort the formatted list.
    sorted_data = sorted(data, 
        key = lambda x: (x[index], -x[index+2]), 
        reverse=reverse)
    # Sort first index then reverse sort the third index
    return sorted_data


def format_results(results: dict, keywords: list) -> list:
# This function use both keywords list and dictionary from scan to create a formatted list.
    data = [] # Array for the formated list
    for key, value in results.items():# For the key and value in dictionary
        for x in range (0,len(keywords)): # for each index in value
            insert_keywords = results[key] # Set variable for value in key
            if insert_keywords[x] > 0: # Don't add to array if its 0
                data.append([key, keywords[x], insert_keywords[x]]) # Add path, keyword, hits to array
    return data    


def save_results(output_path: str, results: list):
# Export the sorted results and saves to a csv file.
    with open(output_path, 'w', newline='') as file: # Write to output_path
        writer = csv.writer(file) # Write on this file
        writer.writerows([['File Path','Keyword','Hits']]) # Write these in first row
        writer = csv.writer(file, quoting = csv.QUOTE_NONNUMERIC)
        writer.writerows(results) # Write results while only quoting the words.
    file.close()

        #There is probably a smarter way to only quote first two rows


def main (input_path: str, load_dir: str, output_path: str):
#This program's run sequence    
    keywords_array = load_rules(input_path) # Use the keyword list created from load_rules
    results = scan(load_dir, keywords_array) # Use the dictionary of hits results from scan
    data = format_results(results,keywords_array) # Use this array of formated dictionary
    index = 0
    reverse = False
    new_results = sort_2d_list(data, index, reverse) # Sorted and formatted results
    save_results(output_path, new_results)   
    input("Scan complete! Press <ENTER> to close...")


# Main statement
if __name__ == '__main__':
    # Your testing here.
    this_path = os.path.realpath(__file__)
    this_path = os.path.dirname(this_path) 
    file_dir = this_path + "//test_data"
    file_path = this_path + "//test_config3.txt"   
    output_path = this_path + "//output.csv"
    main(file_path, file_dir, output_path)
    
