#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import xml.dom.minidom as minidom
import xml.etree.ElementTree as ET
import sys

def BadHandler():
    pass

def main(wiki_xml_file):
    data = ""
    if not wiki_xml_file:
        return False
    # with open(wiki_xml_file, 'r') as fp:
    # #     try:
    # #         wiki_xml = BeautifulSoup(fp, features="xml") 
    # #     except:
    # #         print("Unexpected error:", sys.exc_info()[0])
    # #         raise
    #     for line in fp:
    #         data += line

    # wiki_xml = BeautifulSoup(data, "xml")
    # print(wiki_xml.prettify())
    tree = ET.parse(wiki_xml_file)
    root = tree.getroot()
    print(root)

if __name__ == "__main__":
    wiki_xml_file = '/home/yammsm/code/wikisimple/simplewiki-20210820-pages-articles-multistream.xml'
    main(wiki_xml_file)
