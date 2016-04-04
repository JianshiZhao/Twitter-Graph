# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 22:10:42 2016

@author: Jianshi
"""

import json
import sys
from datetime import datetime
throwaway = datetime.strptime('20110101','%Y%m%d')  

# Get the input and output file name 
try:
    tweet_input_file = sys.argv[1]
    tweet_output_file = sys.argv[2]
except:
    print "Filename Eorror! Please check the file path." 

class twitter_graph(object):
    '''
    Basic class to handle twitter updates. This class include methods to create
    a list of hasgtags within a time window, to create a graph from hashtags, and
    to calculate the average degree of a vertex.
    '''
    def __init__(self,timewindow = 60.0):
        '''
        Specify the timewindow and initialize the hashtags list.
        '''
        self.timewindow = timewindow # this specifies the time window
        self.hashtags = []  # initialize the hashtags list with an empty list


    def create_hashtags(self, msg):
        '''
        Extract hashtags from a tweet message, and store it in a dictionary as
        {'created_at':time, 'hashtags':[nodes]}
        '''
        new_hashtag = {}  # used to store the extracted hashtags
        hashtag_len = len(msg['entities']['hashtags']) # check how many nodes
        cre_time = msg['created_at']  # extract the time stamp
        if hashtag_len > 0:
            # extract all the 'text' contents under 'hashtags'
            tag = [msg['entities']['hashtags'][tagnum]['text'] for tagnum in range(hashtag_len)]
        else:
            tag = []
        
        new_hashtag['created_at'] = cre_time
        new_hashtag['hashtags'] = tag        
        return new_hashtag
                
    def is_twitter(self,msg):
        '''
        Check if the msg is a tweet or other unrelated message. Return true or 
        false.
        '''
        return msg.has_key('created_at')

    def update_hashtags(self,new_hashtag):
        '''
        Gather hashtags that created in the last 60 s. Update the hashtags list when 
        new one comes. 
        '''
        #check the current number of hashtags in the 60 s window
        hash_num = len(self.hashtags)
        tag_removel = []    # record the position of hashtags outside the window
        UPDATE = True       # a flag used to show if the new hashtag is too old
        if hash_num == 0:
            self.hashtags.append(new_hashtag) # if the list is empty, append the new one
        else:
            msg_time = datetime.strptime(new_hashtag['created_at'],"%a %b %d %H:%M:%S +0000 %Y")
            # compare the new message time with the ones in the list
            for tagnum in range(hash_num):
                cre_time = datetime.strptime(self.hashtags[tagnum]['created_at'],"%a %b %d %H:%M:%S +0000 %Y")
                if (msg_time - cre_time).total_seconds() > self.timewindow:
                    tag_removel.append(tagnum)  # record the hashtags more than 60 s older than the new one
                elif (msg_time - cre_time).total_seconds() < (-self.timewindow):
                    UPDATE = False  # don't update the list if the new message is 60s older than any one in the list
                    break
                
        if len(tag_removel)>0:
            # remove the ones falls outside the 60s window
            newlist = [self.hashtags[n] for n in range(hash_num) if n not in tag_removel]            
            self.hashtags = newlist
            
        if UPDATE:
            # add the new hashtags into the list if needed
            self.hashtags.append(new_hashtag)

    def create_graph(self,hashtaglist):
        '''
        This methods is used to create a graph from the hashtags list.
        This graph contains nodes and its neighbors in a dictionary
        graph = {node:[neighbors]}.
        '''
        graph = {}
        for tagnum in range(len(hashtaglist)):
            if len(hashtaglist[tagnum]['hashtags'])>0:
                # for each node in the hashtags, find its neighbors
                for vertex in hashtaglist[tagnum]['hashtags']:
                    neighbors = [node for node in hashtaglist[tagnum]['hashtags'] if node!=vertex]
                    if not graph.has_key(vertex):                    
                        graph[vertex] = neighbors
                    else:
                        # combine neighbors for the same node, and make the neighbors unique
                        graph[vertex] = list(set(graph[vertex]+neighbors))
            else: 
                pass
                        
        self.graph = graph


    def calculate_degree(self,graph):
        '''
        This method is to calculate the average degree of a vertex based on the
        graph we created from hashtags.
        '''
        node_count = 0 
        degree_count = 0
        if len(graph)==0:
            avg_degree = 0
        else:
            for vertex in graph:
                degree_count += float(len(graph[vertex])) # count the connections for a node
                node_count += float(len(graph[vertex])>0) # only nodes with neighbors count
            if node_count!=0:
                avg_degree = degree_count/node_count
            else:
                avg_degree = 0
        return avg_degree



if __name__ == '__main__':
    tweet_input = open(tweet_input_file,'r')
    tweet_output = open(tweet_output_file,'w')       
    twitter = twitter_graph() # create a twitter_graph object 
    for line in tweet_input: # read in each line one by one    
        msg = json.loads(line)  # convert to python dictionary
        try:
            if twitter.is_twitter(msg): # check if the msg is twitter 
                # extract hashtag from the message
                new_hashtag = twitter.create_hashtags(msg) 
                # update the hashtags list within the last 60s
                twitter.update_hashtags(new_hashtag)
                # create graph based on the hashtags
                twitter.create_graph(twitter.hashtags)
                #calculate the average degrees
                avg_degree = twitter.calculate_degree(twitter.graph)
                
                tweet_output.write(format(avg_degree,'.2f'))
                tweet_output.write("\n")
              
            else:
                pass
        except Exception as e:
            print e
            
    tweet_input.close()            
    tweet_output.close()
        
    
  