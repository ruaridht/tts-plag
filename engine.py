#!/usr/bin/env python

"""
A simple plagiarism detector

Ruaridh Thomson
s0786036

Practical 2 for Text Technologies
"""

import re
import math
import md5
import os
import string

SPEECH_DIR = "0786036/"

class Preprocess(object):
  def __init__(self):
    amItrue = True
    
  def process():
    print ">>> Preprocessed (all files)"

class Documents(object):
  def __init__(self):
    self.docs     = []
    self.docNames = [] # Store the corresponding document name
    self.docWords = [] # Store each document as a list of words
    
  def _openDocuments(self):
    fileList = os.listdir(SPEECH_DIR)
    for fileName in fileList:
      self.docNames.append(fileName)
      f = open(SPEECH_DIR + fileName, 'r')
      fileContents = f.readlines()
      self.docs.append(fileContents)
      f.close()
  
  def _removeInitialSentence(self):
    d = []
    for doc in self.docs:
      stringValue = ''
      for sentence in doc[1:]:
        stringValue += sentence
      d.append(stringValue)
    self.docs = d
    
  def _buildDocWords(self):
    for doc in self.docs:
      self.docWords.append(string.split(doc))
    
  def retrieveDocs(self):
    self._openDocuments()
    self._removeInitialSentence() # Kind of preprocessing, but specific to the task.
    self._buildDocWords()
    
    print self.docWords[0]
    print len(self.docWords)
    print self.docNames[0]

def main():
  docs = Documents()
  docs.retrieveDocs()
  
  print ">>> Goodbye."

if __name__ == "__main__":
  main()
