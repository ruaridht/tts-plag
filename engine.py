#!/usr/bin/env python

"""
A simple plagiarism detector

Ruaridh Thomson
s0786036

Practical 3 for Text Technologies
"""

import re
import math
import os
import string

#import md5
import hashlib
#from zlib import adler32
#from zlib import crc32

SPEECH_DIR     = "0786036/" #"train/"
HASH_BITS      = 64
DUPE_THRESHOLD = 0.90

class Documents(object):
  def __init__(self):
    self.docs       = [] # Speeches with no punctuation or description at top
    self.docNames   = [] # Store the corresponding document name
    self.docsWords  = [] # Store each document as a list of words (lowercase)
    self.docsNoStop = [] # Speeches with stopwords removed
    self.directCopy = [] # list of speeches that are exact duplicates
    self.checksums  = [] # list of corresponding checksums
    self.checkCopy  = [] # list of speeches with the same md5
    self.simhashes  = [] # list of simhashes for each speech
    self.nearDupes  = [] # list of near-duplicates found through simhash
    
  def _openDocuments(self):
    fileList = os.listdir(SPEECH_DIR)
    for fileName in fileList:
      self.docNames.append(fileName.replace('.txt',''))
      
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
    print ">>> Documents processed"
  
  def directCheck(self):
    firstIndex = 0
    for doc in self.docs:
      secondIndex = 0
      for doc2 in self.docs:
        if (doc == doc2):
          # check that we're not adding itself as a duplicate
          if (self.docNames[firstIndex] != self.docNames[secondIndex]):
            # check if we've already identified this duplicate
            dupesReverse = self.docNames[secondIndex] + '-' + self.docNames[firstIndex]
            if (dupesReverse not in self.directCopy):
              self.directCopy.append(self.docNames[firstIndex] + '-' + self.docNames[secondIndex])
        secondIndex += 1
      firstIndex += 1
    print self.directCopy
    print ">>> Exact duplicates found: ", len(self.directCopy)
    print ">>> Done direct check"
    
  def checksum(self):
    for doc in self.docs:
      m = hashlib.md5()
      m.update(doc)
      #print m.hexdigest()
      self.checksums.append(m.hexdigest())
    return
    firstIndex = 0
    for check in self.checksums:
      secondIndex = 0
      for check2 in self.checksums:
        if (check == check2):
          # check that we're not adding itself as a duplicate
          if (self.docNames[firstIndex] != self.docNames[secondIndex]):
            # check if we've already identified this duplicate
            dupesReverse = self.docNames[secondIndex] + '-' + self.docNames[firstIndex]
            if (dupesReverse not in self.checkCopy):
              self.checkCopy.append(self.docNames[firstIndex] + '-' + self.docNames[secondIndex])
        secondIndex += 1
      firstIndex += 1
    print ">>> Exact duplicates found via MD5: ", len(self.checkCopy)
    print ">>> Done checksum"
    
  def simhash(self, tokens):
    v = [0]*HASH_BITS
  
    for t in [x.__hash__() for x in tokens]:
      bitmask = 0
      for i in range(HASH_BITS):
        bitmask = 1 << i
        if t & bitmask:
          v[i] += 1
        else:
          v[i] -= 1
    
    fingerprint = 0
    for i in range(HASH_BITS):
      if v[i] >= 0:
        fingerprint += 1 << i
    return fingerprint
  
  def similarity(self, a, b):
    x = (a ^ b) & ((1 << HASH_BITS) - 1)
    tot = 0
    while x:
      tot += 1
      x &= x-1
    return float(HASH_BITS-tot)/HASH_BITS
  
  def sim(self):
    simDupes = []
    for doc in self.docsNoStop:
      h = self.simhash(doc)
      self.simhashes.append(h)
    
    f = 0
    for h1 in self.simhashes:
      s = 0
      for h2 in self.simhashes:
        a = self.similarity(h1,h2)
        if a>DUPE_THRESHOLD:
          if (self.docNames[f] != self.docNames[s]):
            dupesReverse = self.docNames[s] + '-' + self.docNames[f]
            if (dupesReverse not in simDupes):
              simDupes.append(self.docNames[f] + '-' + self.docNames[s])
        s += 1
      f += 1
      
    self.nearDupes = simDupes
    print ">>> Near-duplicates found: ", len(simDupes)
    print ">>> Done simhash"
    
  def writeOut(self):
    f = open('duplicates.txt','w')
    for dupe in self.nearDupes:
      f.write(dupe + "\n")
    f.close()
    print ">>> Duplicates written to: duplicates.txt"
    

def main():
  print ">>> Begin plagiarism detection."
  docs = Documents()
  docs.processDocs()
  docs.directCheck() # We can either directly check
  #docs.checksum()
  docs.sim()
  docs.writeOut()
  
  print ">>> Goodbye."

if __name__ == "__main__":
  main()
