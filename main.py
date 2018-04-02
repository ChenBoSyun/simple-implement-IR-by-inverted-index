
# coding: utf-8

# In[1]:


import re
import csv


# In[28]:


class Search_engine:
    def __init__(self):
        self.__word_index = {} #
    def build_index(self , article):
        regex = r'([a-zA-Z]+)'
        x = 0
        with open(article, encoding="utf-8-sig") as csvfile:
            spamreader = csv.reader(csvfile)
            for line in spamreader:

                string = re.sub(r'[^\w]','',line[1])
                
                en_list = re.findall(regex,line[1])
                for word in en_list:
                    if word not in self.__word_index:
                        self.__word_index[word] = []
                    if line[0] not in self.__word_index[word]:
                        self.__word_index[word].append(line[0])

                for n in range(2,4):
                    for i in range(len(string)-n+1):
                        if string[i:i+n] not in self.__word_index:
                            self.__word_index[string[i:i+n]] = []
                        if line[0] not in self.__word_index[string[i:i+n]]:
                            self.__word_index[string[i:i+n]].append(line[0])

                            
    def search(self , s_type , query_l):
        query_l = [set(self.__word_index[x]) for x in query_l]
        if s_type == "and":
            s = query_l[0]
            for i in query_l[1:]:
                s = set.intersection(s,i)
        elif s_type == "or":
            s = query_l[0]
            for i in query_l[1:]:
                s = set.union(s,i)
        elif s_type == "not":
            s = query_l[0]
            for i in query_l[1:]:
                s = set.difference(s,i)
        return s


# In[6]:


if __name__ == '__main__':
    # You should not modify this part.
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--source',
                        default='source.csv',
                        help='input source data file name')
    parser.add_argument('--query',
                        default='query.txt',
                        help='query file name')
    parser.add_argument('--output',
                            default='output.txt',
                            help='output file name')
    args = parser.parse_args() 
    
    article = args.source
    query = args.query
    output = args.output
    
    search_engine = Search_engine()
    search_engine.build_index(article)
    
    with open(output, 'w') as out_file, open(query, 'r', encoding='utf-8') as query_file:
        lines = query_file.readlines()
        last = lines[-1].strip()
        for line in lines:
            line = line.strip()
            query = re.sub(r"\s+", "", line, flags=re.UNICODE)
            
            if query.find("and") != -1:
                s_type = "and"
                query_l = query.split("and")
            elif query.find("or") != -1:
                s_type = "or"
                query_l = query.split("or")
            elif query.find("not") != -1:
                s_type = "not"
                query_l = query.split("not")
            
            result = list(search_engine.search(s_type, query_l))
            if result:
                for i in range(len(result)):
                    out_file.write("%s" % result[i])
                    if i != len(result)-1:
                        out_file.write(",")
            else:
                out_file.write("0")
                
            if line != last:
                out_file.write("\n")
        
    

