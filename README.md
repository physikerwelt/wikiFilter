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
All options of wikiFilter can be seen via
```
./wikiFilter.py --help
usage: wikiFilter.py [-h] [-f FILE] [-s SIZE] [-d DIR] [-t TAG] [-v] [-T]

extract wikipages that contain the math tag

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --filename FILE
                        the bz2-file to be split and filtered (default:
                        enwiki-latest-pages-articles.xml.bz2)
  -s SIZE, --splitsize SIZE
                        the number of pages contained in each split (default:
                        1000000)
  -d DIR, --outputdir DIR
                        the directory name where the files go (default: wout)
  -t TAG, --tagname TAG
                        the tag to search for (default: math)
  -v, --verbosity
  -T, --template        include all templates (default: False)
```
