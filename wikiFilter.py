#!/usr/bin/python
import os
import bz2
import argparse


def split_xml(filename, splitsize, dir, tags, template):
    ''' The function gets the filename of wiktionary.xml.bz2 file as  input and creates
    smallers chunks of it in a the diretory chunks
    '''
    # Check and create chunk diretory
    if not os.path.exists(dir):
        os.mkdir(dir)
    # Counters
    pagecount = 0
    filecount = 1
    ismath = 2
    header = ""
    footer = "</mediawiki>"
    tempstr = ""
    # open chunkfile in write mode
    chunkname = lambda filecount: os.path.join(dir, "chunk-" + str(filecount) + ".xml.bz2")
    chunkfile = bz2.BZ2File(chunkname(filecount), 'w')
    # Read line by line
    bzfile = bz2.BZ2File(filename)
    tags = tags.split(',')
    # the header
    for line in bzfile:
        header += line
        if '</siteinfo>' in line:
            break
    print header
    chunkfile.write(header)
    # and the rest
    for line in bzfile:
        # the </page> determines new wiki page
        if '<page' in line:
            if ismath == 2:  # start
                tempstr = header
            ismath = 0
            tempstr = ""
        tempstr = tempstr + line
        for tag in tags:
            if '&lt;' + tag in line:
                ismath = 1
                pagecount += 1
                print splitsize * filecount + pagecount
        if template and ('<ns>10</ns>' in line or '<ns>828</ns>' in line):
            ismath = 1
            pagecount += 1
            print 'template'
        if '</page>' in line:
            if ismath == 1:
                chunkfile.write(tempstr)
                tempstr = ""
        if pagecount > splitsize:
            # print chunkname() # For Debugging
            chunkfile.write(footer)
            chunkfile.close()
            pagecount = 0  # RESET pagecount
            filecount += 1  # increment filename
            chunkfile = bz2.BZ2File(chunkname(filecount), 'w')
            chunkfile.write(header)
    try:
        chunkfile.write(footer)
        chunkfile.close()
    except:
        print 'Files already close'


if __name__ == '__main__':  # When the script is self run
    parser = argparse.ArgumentParser(description='extract wikipages that contain the math tag',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-f', '--filename', help='the bz2-file to be split and filtered',
        default='enwiki-latest-pages-articles.xml.bz2', dest='file')
    parser.add_argument('-s', '--splitsize', help='the number of pages contained in each split',
        default=1000000, type=int, dest='size')
    parser.add_argument('-d', '--outputdir', help='the directory name where the files go',
        default='wout', type=str, dest='dir')
    parser.add_argument('-t', '--tagname', help='comma separated list of the tag names to search for',
        default='math,ce,chem', type=str, dest='tags')
    parser.add_argument("-v", "--verbosity", action="count", default=0)
    parser.add_argument('-T', '--template', help='include all templates',
        action="store_true", dest='template')
    args = parser.parse_args()
    split_xml(args.file, args.size, args.dir, args.tags, args.template)
