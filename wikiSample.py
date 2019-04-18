#!/usr/bin/python
import os
import bz2
import argparse
import random


def split_xml(filename, splitsize, dir, total, size):
    ''' The function gets the filename of wiktionary.xml.bz2 file as  input and creates
    smallers chunks of it in a the diretory chunks
    '''
    # Check and create chunk diretory
    if not os.path.exists(dir):
        os.mkdir(dir)
    # Counters
    pagecount = 0
    filecount = 1
    ismatch = 2
    header = b''
    footer = b'</mediawiki>'
    tempstr = b''
    # open chunkfile in write mode
    chunkname = lambda filecount: os.path.join(dir, "chunk-" + str(filecount) + ".xml.bz2")
    chunkfile = bz2.BZ2File(chunkname(filecount), 'w')
    # Read line by line
    bzfile = bz2.BZ2File(filename)
    # the header
    selected = random.sample(range(0, total - 1), size)
    for line in bzfile:
        header += line
        if b'</siteinfo>' in line:
            break
    chunkfile.write(header)
    i = 0
    # and the rest
    for line in bzfile:
        # the </page> determines new wiki page
        if b'<page' in line:
            tempstr = b''
            ismatch = 0
            i += 1
            if i in selected:
                ismatch = 1
                pagecount += 1
                print(splitsize * filecount + pagecount, i)
        tempstr = tempstr + line
        if b'</page>' in line:
            if ismatch == 1:
                chunkfile.write(tempstr)
                tempstr = b''
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
        print('Filtered',pagecount,'files in',i,'processed pages')
    except:
        print('Files already close')


if __name__ == '__main__':  # When the script is self run
    parser = argparse.ArgumentParser(description='draws a random sample from a wikidump',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-f', '--filename', help='the bz2-file to be split and filtered',
                        default='enwiki-latest-pages-articles.xml.bz2', dest='file')
    parser.add_argument('-s', '--splitsize', help='the number of pages contained in each split',
                        default=1000000, type=int, dest='splitsize')
    parser.add_argument('-d', '--outputdir', help='the directory name where the files go',
                        default='wout', type=str, dest='dir')
    parser.add_argument('-t', '--total', help='total size of the dataset', type=int, dest='total', required=True)
    parser.add_argument('-c', '--size', help='size of the sample', type=int, dest='size', required=True)
    parser.add_argument("-v", "--verbosity", action="count", default=0)
    args = parser.parse_args()
    split_xml(args.file, args.splitsize, args.dir, args.total, args.size)
