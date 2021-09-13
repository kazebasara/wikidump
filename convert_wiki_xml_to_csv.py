# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
# -*- coding: utf-8 -*-
import lxml 
from lxml import etree
from io import BytesIO
import re, sys
import csv


# %%
infile = 'simplewiki-latest-pages-articles-multistream.xml'
import codecs

# enc_file = codecs.EncodedFile(open(infile,'r'), "ASCII", "ASCII", "xmlcharrefreplace")
context = etree.iterparse(infile, tag='{http://www.mediawiki.org/xml/export-0.10/}page',
                            recover=True,
                            encoding='UTF-8')


# %%
results = []
f = open('result.csv','w+' )
writer = csv.writer(f)
writer.writerow(["page_id", "revision_id", "link"])
for event, page in context:
    page_id_list = page.xpath('./i:id', namespaces={'i':'http://www.mediawiki.org/xml/export-0.10/'})
    revision_id_list = page.xpath('./i:revision/i:id', namespaces={'i':'http://www.mediawiki.org/xml/export-0.10/'})
    revision_text_list = page.xpath('./i:revision/i:text', namespaces={'i':'http://www.mediawiki.org/xml/export-0.10/'})
    for page_id_elem, revision_id_elem, revision_text_elem in zip(page_id_list,revision_id_list, revision_text_list):
        page_id = page_id_elem.text
        revision_id = revision_id_elem.text
        revision_text = revision_text_elem.text if revision_text_elem.text else ""
        # print(page_id, revision_id)
        categories = []
        categories_match = re.findall('\[\[Category:(.*?)\]\]', revision_text)
        if categories_match:
            for i in categories_match:
                if isinstance(i, list):
                    categories.extend(i)
                else:
                    categories.append(i)
        # print(categories)
        links = re.findall('\[\[([^:]*?)\]\]', revision_text)
        # links = links if links else "[]"
        # result = [page_id,revision_id,categories,links]
        if links:
            for link in links:
                link = link.capitalize().replace(" ", "_").split('|')[0]
                result = [page_id, revision_id, link]
                writer.writerow(result)

f.close()
# with open('result.csv','w' )as f:
#     writer = csv.writer(f)
#     writer.writerow(results)
# print(results)


# %%
# # context = etree.iterparse(infile, tag='{http://www.mediawiki.org/xml/export-0.10/}page')
# # context = etree.iterparse(infile)
 
# #data = []

# def printText(element, page_info):
#     tag_full = element.tag
#     namespace , tag = tag_full.split('}')
#     namespace = namespace[1:]
#     s = element.text
    
            
#     # if tag == '{http://www.mediawiki.org/xml/export-0.10/}text':
#     if tag == 'text':
#         if s:
#             m = re.findall('\[\[Category:(.*?)\]\]', s)
#             text = m if m else "null"
#             text = ','.join(text) if isinstance(text, list)  else text
#         else:
#             text = "null"
#         output = 'pageno=%s, tag=%s, category=%s\n'
#     else:
#         text = s
#         output = 'pageno=%s, tag=%s, {0}=%s\n'.format(tag)
        
#     # print( output % (num, str(tag), text ))
#     page_info[tag]=text
#     return page_info

# num = 0
# all_page_dict = {}
# for event, elem in context:
#     num +=1
#     if num > 2:
#         break
#         # sys.exit(1)
#     # print(type(elem))
#     ns = "http://www.mediawiki.org/xml/export-0.10/"
#     # print(elem.xpath('*[local-name()="title" and namespace-uri()="http://www.mediawiki.org/xml/export-0.10/"]'))

#     results = elem.xpath('./i:title|./i:id|./i:revision/i:text|./i:revision/i:id', namespaces={'i':ns})

#     page_info = {}
    
#     for i in results:
#         #print(i.)
#         page_info = printText(i,page_info)
    
#     all_page_dict[page_info['id']] = page_info
    
#     # print(page_info)
#  print(all_page_dict)
# #     [ WORKED ] 
# #     page_content = etree.iterparse(BytesIO(etree.tostring(elem, encoding='UTF-8')), 
# #                                     tag=['{http://www.mediawiki.org/xml/export-0.10/}title', 
# #                                          '{http://www.mediawiki.org/xml/export-0.10/}timestamp',
# #                                          '{http://www.mediawiki.org/xml/export-0.10/}text'],
# #                                     recover=True,
# #                                     encoding='UTF-8')
# #     for e , page_elem in page_content:
# #         if num > 2:
# #             sys.exit(1)
# #         try:
# #             printText(page_elem)
            
# #         except:
# #             print("How come " + sys.exc_info)
# #             break


# # print("Hello")
# # print(data)


