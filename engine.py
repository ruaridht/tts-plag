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

class Adler32(object):
  def __init__(self):
    amItrue = True
  
  def checksum(self):
    print ">>> Calculated Alder32 checksum"

class Documents(object):
  def __init__(self):
    self.docs       = [] # Speeches with no punctuation or description at top
    self.docNames   = [] # Store the corresponding document name
    self.docsWords  = [] # Store each document as a list of words
    self.docsNoStop = [] # Speeches with stopwords removed
    
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
    regex = re.compile('[%s]' % re.escape(string.punctuation)) # Use this to strip punctuation2
    
    for doc in self.docs:
      speech = ''
      for sentence in doc[1:]:
        speech += regex.sub('',sentence) # Remove the punctuation
      d.append(speech)
    self.docs = d
    
  def _buildDocWords(self):
    stopwords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now']
    
    for doc in self.docs:
      words = string.split(doc)
      wordStopped = [w.lower() for w in words if w not in stopwords] # Remove the stopwords and convert to lowercase
      self.docsWords.append(words)
      self.docsNoStop.append(wordStopped)
    
  def processDocs(self):
    self._openDocuments()
    self._removeInitialSentence() # Removes the initial sentence and any punctuation
    self._buildDocWords() # Represents each speech as a list of words and removes stopwords

def main():
  docs = Documents()
  docs.processDocs()
  
  ad = Adler32()
  ad.checksum()
  
  print ">>> Goodbye."

if __name__ == "__main__":
  main()
