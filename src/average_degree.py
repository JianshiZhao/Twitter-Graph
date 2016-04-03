# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 22:10:42 2016

@author: Jianshi
"""

import json
import os
import sys
from datetime import datetime


if len(sys.argv) > 1:
    tweet_input_file = sys.argv[1]
    tweet_output_file = sys.argv[2]


throwaway = datetime.strptime('20110101','%Y%m%d')  

class twitter_graph(object):
    '''
    Basic class to handle twitter updates. This class include methods to create
    hasgtags within designate time window, to create graph from hashtags, and
    to calculate the average degree of vertices.
    '''
    def __init__(self,timewindow = 60.0):
        '''        
        '''
        self.timewindow = timewindow # this defines the time window length
        self.hashtags = []  # initialize the hashtags with an empty list


    def create_hashtags(self, msg):
        '''
        Extract hashtags from a tweet message, and store it in a dictionary as
        {'created_at':time, 'hashtags':[nodes]}
        '''
        new_hashtag = {}  # used to store the extracted hashtags
        hashtag_len = len(msg['entities']['hashtags']) # check how many hashtags
        cre_time = msg['created_at']
        if hashtag_len > 0:
            tag = [msg['entities']['hashtags'][tagnum]['text'] for tagnum in range(hashtag_len)]
        else:
            tag = []

        new_hashtag['created_at'] = cre_time
        new_hashtag['hashtags'] = tag        
        return new_hashtag
                
    def is_twitter(self,msg):
        '''
        Check if the msg is twitter or other unrelated message. Return true or 
        false.
        '''
        return msg.has_key('created_at')

    def update_hashtags(self,new_hashtag):
        '''
        Gather hashtags that created in the last 60 s. Update the hashtags when 
        new one comes. Updated hashtags are stored in self.hashtags
        '''
        #check the current number of hashtags in the 60 s window
        hash_num = len(self.hashtags)
        tag_removel = [] # record the position of hashtags out of window
        UPDATE = True  # a flag used to show if the new hashtag is too old
        if hash_num == 0:
            self.hashtags.append(new_hashtag)
        else:
            msg_time = datetime.strptime(new_hashtag['created_at'],"%a %b %d %H:%M:%S +0000 %Y")
            
            for tagnum in range(hash_num):
                cre_time = datetime.strptime(self.hashtags[tagnum]['created_at'],"%a %b %d %H:%M:%S +0000 %Y")
                if (msg_time - cre_time).total_seconds() > self.timewindow:
                    tag_removel.append(tagnum)
                elif (msg_time - cre_time).total_seconds() < (-self.timewindow):
                    UPDATE = False
                    break

        if len(tag_removel)>0:
            newlist = [self.hashtags[n] for n in range(hash_num) if n not in tag_removel]            
            self.hashtags = newlist
            
        if UPDATE:
            self.hashtags.append(new_hashtag)

    def create_graph(self,hashtaglist):
        '''
        This methods is used to create a graph from the hashtags collected.
        This graph contains nodes and its neighbors in a dictionary
        graph = {node:[neighbors]}.
        '''
        graph = {}
        for tagnum in range(len(hashtaglist)):
            for vertex in hashtaglist[tagnum]['hashtags']:
                neighbors = [node for node in hashtaglist[tagnum]['hashtags'] if node!=vertex]
                if not graph.has_key(vertex):                    
                    graph[vertex] = neighbors
                else:
                    # combine neighbors for the same node, make the neighbors unique
                    graph[vertex] = list(set(graph[vertex]+neighbors))
        
        self.graph = graph


    def calculate_degree(self,graph):
        '''
        This method is to calculate the average degree of a vertex based on the
        graph we created from hashtags.
        '''
        node_count = 0 
        degree_count = 0
        for vertex in graph:
            degree_count += float(len(graph[vertex]))
            node_count += float(len(graph[vertex])>0) # only nodes with neighbors count
        if node_count!=0:
            avg_degree = degree_count/node_count
        else:
            avg_degree = 0
        return avg_degree



if __name__ == '__main__':
    with open(tweet_input_file,'r') as txt:
        tweet_input = txt.readlines()
    output = open(tweet_output_file,'w')       
    twitter = twitter_graph() # create a twitter_graph object 
    for twnum in range(len(tweet_input)): # read in each message one by one
        msg = json.loads(tweet_input[twnum])  # convert to python dictionary
        if twitter.is_twitter(msg): # check if the msg is twitter 
            # extract hashtag from the message
            new_hashtag = twitter.create_hashtags(msg) 
            # update the hashtags within the last 60s
            twitter.update_hashtags(new_hashtag)
            # create graph based on the hashtags
            twitter.create_graph(twitter.hashtags)
            #calculate the average degrees
            avg_degree = twitter.calculate_degree(twitter.graph)
            
            output.write(format(avg_degree,'.2f'))
            output.write("\n")
            
            
            print avg_degree
        else:
            pass
    output.close()
        
    
  