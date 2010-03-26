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
        print tag
        if tag == "li" and attrs[0][0] == "class" and attrs[0][1] == 'small-text': 
            self.in_small = True

        if self.in_small and tag == 'b':
            self.in_acro = True

        if self.in_small and tag == 'a':
            self.present_conference['link'] = 'http://portal.acm.org/' + attrs[0][1]
            self.in_a = True

    def handle_data(self, text):
        print text
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


class SingleConferenceParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.in_table = False
        self.in_row = False
        self.current_row = {}
        self.total = {}

    def handle_starttag(self, tag, attrs):
        if tag == "table" and attrs[0][0] == "align" and attrs[2][1] == '5':
            print "In table"
            self.in_table = True

        if self.in_table and tag == "td" and (attrs[0][1] == '#fff7e7' or attrs[0][1] == '#fff7e7'):
            print "In row"
            self.in_row = True


    def handle_data(self, text):
        if self.in_row:
            print text

    def handle_endtag(self, tag):
        if self.in_table and tag == "table":
            self.in_table = False
            self.in_row = False


###############################

def parse_conference_list():
    parser = ConferenceListParser()
    url_string = 'http://portal.acm.org/browse_dl.cfm?linked=1&part=series&coll=portal&dl=ACM&CFID=81659906&CFTOKEN=15682890'

    import urllib
    web_site = urllib.urlopen(url_string)
    parser.feed(web_site.read())

    return parser.conferentes

def parse_conference(conference_url):
    parser = ConferenceListParser()

    import urllib
    print conference_url
    web_site = urllib.urlopen(conference_url['link'])
    parser.feed(web_site.read())

conference_urls = parse_conference_list()

for url in conference_urls:
    parse_conference(url)

