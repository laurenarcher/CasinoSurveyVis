import csv
import re
import itertools

import webbrowser

from collections import Counter

import numpy as np

from pytagcloud import create_tag_image, make_tags
from pytagcloud.lang.counter import get_tag_counts
from pytagcloud.lang.stopwords import StopWords

import colorbrewer


SentiList = ["Opposed", "Neutral", "All", "Favour"]
AgeList = [ "15-24", "25-34", "35-44", "45-54", "55-64", "65 or older"]
GenderList = ["Male", "Female"]
AllList = [ "Opposed", "Neutral", "Favour", "Male", "Female", "15-24", "25-34", "35-44", "45-54", "55-64", "65 or older"]

#Make output CSV Files

def MakeFiles():
    input_file = open('casinosurvey.csv', 'r')
    data = csv.reader(input_file)
    for line in data:
        [Q1,Q1_B1,Q1_B2,Q1_B3,Q9,Age,Gender,PostalCode] = line

        for entry in SentiList:
            sentiment = "Sentiment"
            strength = "Strength"
            conditions = "Conditions"
            comment = "Comment"
            Age = "Age"
            Gender = "Gender"
            PostalCode = "Postal Code"
            new_line = sentiment,strength,conditions,comment,Age,Gender,PostalCode
            csv.writer(open((entry +'.csv'), 'w')).writerow(new_line)

#Write cleaned survey data to .csv
            
def WriteCSV():
    input_file = open('casinosurvey.csv', 'r') 
    data = csv.reader(input_file)
    for line in data:
        [Q1,Q1_B1,Q1_B2,Q1_B3,Q9,Age,Gender,PostalCode] = line
        
        if Q1 == "Q1":
            data.next()
        else:
            if Q1 == "Strongly in Favour" or Q1 == "Somewhat in Favour":
                sentiment = "Favour"
                strength = Q1
                conditions = Q9
                comment = Q1_B1 +" " + Q1_B2 + " " + Q1_B3
                new_line = sentiment,strength,conditions,comment,Age,Gender,PostalCode
                csv.writer(open((sentiment +'.csv'), 'a')).writerow(new_line)
                csv.writer(open(('All.csv'), 'a')).writerow(new_line)
            elif Q1 == "Strongly Opposed" or Q1 == "Somewhat Opposed":
                sentiment = "Opposed"
                strength = Q1
                conditions = Q9
                comment = Q1_B1 +" " + Q1_B2 + " " + Q1_B3
                new_line = sentiment,strength,conditions,comment,Age,Gender,PostalCode
                csv.writer(open((sentiment +'.csv'), 'a')).writerow(new_line)
                csv.writer(open(('All.csv'), 'a')).writerow(new_line)
            elif Q1 == "Neutral or Mixed Feelings":
                sentiment = "Neutral"
                strength = Q1
                conditions = Q9
                comment = Q1_B1 +" " + Q1_B2 + " " + Q1_B3
                new_line = sentiment,strength,conditions,comment,Age,Gender,PostalCode
                csv.writer(open((sentiment +'.csv'), 'a')).writerow(new_line)
                csv.writer(open(('All.csv'), 'a')).writerow(new_line)
            elif Q1 == "Null":
                data.next()

                


HEADER = [ "Sentiment","Strength","Conditions","Comment","Age","Gender","Postal Code"]
HEADER_DICT = dict( (name,i) for i, name in enumerate(HEADER) )

#Get words from comments

def get_words(comment_text):
    return [word.lower() for word in re.findall('\w+', comment_text) if len(word) > 3]

#Get word frequencies and visualize in word clouds.

def word_frequency():
    for entry in SentiList:
        sentiment = "Sentiment"
        word = "Word"
        count = "Count"
        new_line = word, count, sentiment
        csv.writer(open(('words' + entry + '.csv'), 'w')).writerow(new_line)
        comments = []
        file_path = entry + ".csv"
        with open(file_path,'r') as csvfile:
            csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
            csvreader.next() # Skip header
            for row in csvreader:
                comments.append(row)

       # print comments[:10]

        c = Counter()
        s = StopWords()     
        s.load_language("english")
        
        for comment in comments:
            for word in get_words( comment[ HEADER_DICT['Comment'] ] ):
                if not s.is_stop_word(word):
                    if c.has_key(word):
                        c[ word ] += 1
                    else:
                        c[ word ] = 1
                        
        for word in c.most_common(100):
            new_line = entry, word[0], word[1]
            csv.writer(open(('words' + entry + '.csv'), 'a')).writerow(new_line)

        #Making word clouds for your most common words

        colours = {"Favour": (colorbrewer.BrBG[5]) , "Opposed":(colorbrewer.PiYG[5]), "Neutral" : (colorbrewer.PuOr[5]), "All":(colorbrewer.RdPu[5])}

        ctags = make_tags(c.most_common(75), minsize=8, maxsize=65, 
                             colors = colours[entry])
        create_tag_image(ctags, 'c_' + entry +'_most_common.png', size=(400, 440), fontname='Lobster', layout=2, rectangular=True)
        webbrowser.open('c_' + entry +'_most_common.png')

#Make word tables organized by variables like sentiment, age and gender, to use to build a heat map
        #This section is super repetitive, and I will make it better later!

def word_tables():
    output_file = open(('wordcounts.csv'), 'a')
    variable = "Variable"
    word = "Word"
    count = "Count"
    new_line = variable, word, count
    csv.writer(open(('wordcounts.csv'), 'w')).writerow(new_line)

    for entry in SentiList:

        print entry

        c = Counter()
        s = StopWords()     
        s.load_language("english")
        
        input_file = open('All.csv', 'r')
        data = csv.reader(input_file)

        for line in data:
            [Sentiment,Strength,Conditions,Comment,Age,Gender,PostalCode] = line
            if entry == Sentiment:
                for word in get_words(Comment):
                    if not s.is_stop_word(word):
                        if c.has_key(word):
                            c[ word ] += 1
                        else:
                            c[ word ] = 1
                
        for word in c.most_common(4000):
            new_line = entry, word[0], word[1]
            csv.writer(output_file).writerow(new_line)

    for entry in AgeList:

        print entry

        c = Counter()
        s = StopWords()     
        s.load_language("english")
        
        input_file = open('All.csv', 'r')
        data = csv.reader(input_file)

        for line in data:
            [Sentiment,Strength,Conditions,Comment,Age,Gender,PostalCode] = line
            if entry == Age:
                for word in get_words(Comment):
                    if not s.is_stop_word(word):
                        if c.has_key(word):
                            c[ word ] += 1
                        else:
                            c[ word ] = 1
                
        for word in c.most_common(4000):
            new_line = entry, word[0], word[1]
            csv.writer(output_file).writerow(new_line)

    for entry in GenderList:

        print entry

        c = Counter()
        s = StopWords()     
        s.load_language("english")
        
        input_file = open('All.csv', 'r')
        data = csv.reader(input_file)

        for line in data:
            [Sentiment,Strength,Conditions,Comment,Age,Gender,PostalCode] = line
            if entry == Gender:
                for word in get_words(Comment):
                    if not s.is_stop_word(word):
                        if c.has_key(word):
                            c[ word ] += 1
                        else:
                            c[ word ] = 1
                
        for word in c.most_common(4000):
            new_line = entry, word[0], word[1]
            csv.writer(output_file).writerow(new_line)
            
#Make your word count heat map .csv to import into tableau
            
def word_heat_map():
    var = "Variable"
    ent = "Entertainment/Tourism"
    fam = "Family/ies"
    gam = "Gambling"
    rev = "Revenue/s"
    poor = "Poor/Bankruptcy"
    add = "Addiction/ing/ive"
    bis = "Businesses/Economic"
    crime = "Crime"
    cong = "Congestion/Parking/Infrastructure"
    com = "Community/Neigbourhood/Residents"
    new_line = var, gam, ent, rev, poor, add, bis, fam, cong, com
    csv.writer(open("wordheatmap.csv", 'w')).writerow(new_line)
    for entry in AllList:
        input_file = open("wordcounts.csv", 'r')
        output_file = open("wordheatmap.csv", 'a')
        data = csv.reader(input_file)
        wlist = ["gambling", "tourism", "entertainment", "revenue", "revenues", "poor", "bankruptcy", "addiction", "addicting", "additctions", "addicted", "buisnesses", "economic", "crime", "congestion", "parking", "infrastructure", "family", "families","community", "neigbourhood", "residents"]
        wdict = {}
        for word in wlist:
            wdict.setdefault(word, 0)
        for line in data:
            [variable, word, count] = line
            if variable == entry:
                wdict[word] = int(count)
        ent = wdict["entertainment"] + wdict["tourism"]
        fam = wdict["family"] + wdict["families"]
        gam = wdict["gambling"]
        rev = wdict["revenue"] + wdict["revenues"]
        poor = wdict["poor"] + wdict["bankruptcy"]
        add = wdict["addiction"] + wdict["addicting"] + wdict["additctions"] + wdict["addicted"]
        bis = wdict["buisnesses"] + wdict["economic"]
        crime = wdict["crime"]
        cong = wdict["congestion"] + wdict["parking"] + wdict["infrastructure"]
        com = wdict["community"] + wdict["neigbourhood"] + wdict["residents"]
    
        new_line = entry, gam, ent, rev, poor, add, bis, fam, cong, com
        csv.writer(output_file).writerow(new_line)
            
        
                
            
MakeFiles()
WriteCSV()
word_frequency()
word_tables()
word_heat_map()

