#!/usr/bin/python
import sys
import re
import urllib2


def get_html(url):
    response = urllib2.urlopen(url)
    raw_html = response.read()

    return raw_html

def clean_text(txt):
    
    # Create the expression to isolate the story
    source = re.compile('<div class="b-story-body-x x-r15"><div><p>([\w\s\W]*)</p></div></div><div class="b-story-stats-block">')
    
    # Isoate the story
    pulled_text = source.findall(txt)[0]
    
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

    return cleaned_text

def text_builder(url,output_text):
    txt = get_html(url)
    cleaned = clean_text(txt)
    output_text = output_text + '\n\n' + cleaned

    return output_text

def main():
    args = sys.argv
    rooturl = args[1]
    numpages = int(args[2])

    # Begin the output text
    output_text = "Text version of " + rooturl + "\n\n"

    # Build the text for the root page
    output_text = text_builder(rooturl, output_text)
    
    # Build the URL for each page after the first
    for i in range(2,numpages+1):
        url = rooturl + '?page=' + str(i)
        output_text = text_builder(url, output_text)
        


    # Eventually save to a file, for now print
    print output_text

if __name__ == "__main__":
    main()

