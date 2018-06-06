# Search Engine using Python 


def get_page(url):  
    try:
        import urllib
        return urllib.urlopen(url).read()
    except:
        return ""
    

def get_next_target(page):
    start_link = page.find('<a href=')
    if start_link == -1:
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"',start_quote+1)
    url = page[start_quote+1:end_quote]
    return url, end_quote

def get_all_links(page):
    links = []
    while True:
        url, endpos = get_next_target(page)
        if url:
            links.append(url)
            page = page[endpos:]
        else:
            break
    return links

def union(p,q):
    for e in q:
        if e not in p:
            p.append(e)   
    
def crawl_web(seed): # returns index, graph of inlinks
    tocrawl = [seed]
    crawled = []
    graph = {}  # <url>, [list of pages it links to]
    index = {} 
    while tocrawl: 
        page = tocrawl.pop()
        if page not in crawled:
            content = get_page(page)
            add_page_to_index(index, page, content)
            outlinks = get_all_links(content)
            graph[page] = outlinks
            union(tocrawl, outlinks)
            crawled.append(page)
    return index, graph


def add_to_index(index,keyword,url):
    if keyword in index:
        index[keyword].append(url)
    else:
        index[keyword] = [url]
    
def add_page_to_index(index,url,content):
    words = content.split()
    for word in words:
        add_to_index(index,word,url)
        
    
    
def lookup(index,keyword):
    if keyword in index:
        return index[keyword]
    else:
        return None

def hash_string(keyword,buckets):
    h = 0
    for c in keyword:
        h = (h+ord(c))%buckets
    return h

def make_hashtables(nbuckets):
    table =[]
    for _ in range(0,nbuckets):
        table.append([])       
    return table

def hashtable_get_bucket(htable,key):
    return htable[hash_string(key,len(htable))]

def hashtable_add(htable,key,value):
    bucket = hashtable_get_bucket(htable,key)
    bucket.append([key,value])
    
    return htable  

def hashtable_lookup(htable,key):
    bucket = hashtable_get_bucket(htable,key)
    for v in bucket:     
        if v[0] == key:
            return v[1]
    return None

def hashtable_update(htable,key,value):
    bucket = hashtable_get_bucket(htable,key)
    for entry in bucket:
        if entry[0] == key:
            entry[1] = value
            return 
    bucket.append([key,value])


def compute_ranks(graph):
    d = 0.8 # damping factor
    numloops = 10
    
    ranks = {}
    npages = len(graph)
    for page in graph:
        ranks[page] = 1.0 / npages
    
    for i in range(0, numloops):
        newranks = {}
        for page in graph:
            newrank = (1 - d) / npages
            for node in graph:
                if page in graph[node]:
                    newrank = newrank + d * (ranks[node] / len(graph[node]))
            
            #Insert Code Here
            
            newranks[page] = newrank
        ranks = newranks
    return ranks

    


index, graph = crawl_web("http://shantagouda.me")
ranks = compute_ranks(graph)
