import pdb
import sys


import pdb
from HTMLParser import HTMLParser

###############################
class ConferenceListParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.in_small = False
        self.in_acro = False
        self.conferentes = []
        self.present_conference ={} 
        self.in_a = False

    def handle_starttag(self, tag, attrs):
        if tag == "li" and attrs[0][0] == "class" and attrs[0][1] == 'small-text': 
            self.in_small = True

        if self.in_small and tag == 'b':
            self.in_acro = True

        if self.in_small and tag == 'a':
            self.present_conference['link'] = attrs[0][1]
            self.in_a = True

    def handle_data(self, text):
        if self.in_acro:
            self.present_conference['acro'] = text[:-1]
        if self.in_a:
            self.present_conference['description'] = text[1:]


    def handle_endtag(self, tag):
        if self.in_acro and tag == "b":
            self.in_acro = False

        if self.in_small and tag == "li":
            self.in_small = False
            self.conferentes.append(self.present_conference)
            self.present_conference = {}

        if self.in_a == True and tag == 'a':
            self.in_a = False

###############################

def parse_conference_list():
    parser = ConferenceListParser()
    url_string = 'http://portal.acm.org/browse_dl.cfm?linked=1&part=series&coll=portal&dl=ACM&CFID=81659906&CFTOKEN=15682890'

    import urllib
    web_site = urllib.urlopen(url_string)
    print web_site
    parser.feed(web_site.read())
    print parser.conferentes

def parse_conference_page():
    pass

parse_conference_list()
