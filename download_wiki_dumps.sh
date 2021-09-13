#! /bin/bash

curl -fsSL -O "https://dumps.wikimedia.org/simplewiki/latest/simplewiki-latest-category.sql.gz" 
curl -fsSL -O "https://dumps.wikimedia.org/simplewiki/latest/simplewiki-latest-categorylinks.sql.gz"
curl -fsSL -O "https://dumps.wikimedia.org/simplewiki/latest/simplewiki-latest-page.sql.gz"
curl -fsSL -O "https://dumps.wikimedia.org/simplewiki/latest/simplewiki-latest-pagelinks.sql.gz"
curl -fsSL -O "https://dumps.wikimedia.org/simplewiki/latest/simplewiki-latest-pages-articles-multistream.xml.bz2"

gunzip -f *.sql.gz
bunzip2 -f *.xml.bz2

curl -fsSL -O 'https://raw.githubusercontent.com/dumblob/mysql2sqlite/master/mysql2sqlite' 
chmod +x mysql2sqlite

for i in $(ls -1 simplewiki-latest-*.sql); do
	cat $i | ./mysql2sqlite simplewiki.db
done

rm result.csv 
python3 convert_wiki_xml_to_csv.py
sqlite3 simplewiki.db '.mode csv' '.import result.csv pagel'
