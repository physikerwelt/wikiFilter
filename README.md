wikiFilter
==========

Simple script to filter wikidumps for wiki-tags

To filter all pages that contain math from enwiki you can do the following
```
git clone https://github.com/physikerwelt/wikiFilter
cd wikiFilter
mkdir wout
wget https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-pages-articles.xml.bz2
./wikiFilter.py
```
