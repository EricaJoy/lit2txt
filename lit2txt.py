#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import re
import urllib2


def get_html(url):
    response = urllib2.urlopen(url)
    raw_html = response.read()

    return raw_html

def clean_text(txt, first_pass = False):
    
    # Create the expression to isolate the title, author, and story
    source = re.compile('<div class="b-story-header"><h1>([\w\s\W]*)</h1>'
                        '[\w\s\W]*<!-- ! --></span><a href=".*">([\w\s\W]*)'
                        '</a></span><span class="b-story-copy">©</span></div>'
                        '<div class="b-story-body-x x-r15"><div><p>([\w\s\W]*)'
                        '</p></div></div><div class="b-story-stats-block">')
    
    # Isolate the title, author, story
    matches = source.findall(txt)
    title = matches[0][0]
    author = matches[0][1]
    pulled_text = matches[0][2]
    
    # Create the expression to isolate remaning line breaks tags
    br = re.compile('<br  />')

    # Sub the remaining <br>'s with nothing, deleting them'
    cleaned_text = br.sub('', pulled_text)

    # Sub <i> tags with *'s
    ital = re.compile('<[iI/]*>')
    cleaned_text = ital.sub('*', cleaned_text)

    # Sub <b> tags with **'s
    bold = re.compile('<[bB/]*>')
    cleaned_text = bold.sub('**', cleaned_text)

    # If we are building page 1 of the story, return author, title, and text
    if first_pass:
        return title + '\n\n© ' + author + '\n\n' + cleaned_text

    # If we are not building page one, just return the text
    else:
        return cleaned_text

# Function to build the the text with URLs
def text_builder(url,output_text,first_pass = False):

    # Call the get_html function to return raw html
    txt = get_html(url)

    # Send the raw html to the clean_text function to make it pretty
    cleaned = clean_text(txt,first_pass)

    # Append the cleaned text to the output text
    output_text = output_text + '\n\n' + cleaned

    # Send back the cleaned and concatted output text
    return output_text

def main():

    # Take in the arguments from the command line and assign them to variables
    args = sys.argv
    rooturl = args[1]
    numpages = int(args[2])

    # Begin the output text
    output_text = "Text version of " + rooturl + "\n\n"

    # Build the text for the root page
    output_text = text_builder(rooturl, output_text, first_pass = True)
    
    # Build the URL for each page after the first
    for i in range(2,numpages+1):
        url = rooturl + '?page=' + str(i)
        output_text = text_builder(url, output_text)

    # Eventually save to a file, for now print


    print output_text

if __name__ == "__main__":
    main()

