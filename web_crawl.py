# Search Engine using Python 


def get_page(url):
    print 'Inside Get_Page'
    try:
        import urllib
        return urllib.urlopen(open).read()
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
    print 'Getting all links '
    links = []
    while True:
        url, endpos = get_next_target(page)
        if url:
            links.append(url)
            page = page[endpos:]
        else:
            break

def union(p,q):
    print 'Union in Action '
    print 'P and Q are:', p,q
    for e in q:
        if e not in p:
            p.append(e)   
    
def crawl_web(seed):
    print "Crwaling"
    tocrawl = [seed]
    crawled = []
    index = []
    while tocrawl:
        page = tocrawl.pop()
        if page not in crawled:
            content = get_page(page)
            add_page_to_index(index,page,content)
            crawled.append(page)
            union(tocrawl,get_all_links(content))   
    return index


def add_to_index(index,keyword,url):
    for entry in index:
        if entry[0] == keyword:
            entry[1].append(url)
            return
    index.append([keyword,[url]])
    
def add_page_to_index(index,url,content):
    words = content.split()
    for word in words:
        add_to_index(index,word,url)
        
    
    
def lookup(index,keyword):
    print 'Looking up for keyword:',keyword
    for entry in index:
        if entry[0] == keyword:
            print 'Url:',entry[1]
            return entry[1]
        
    return []


crawl_web("http://shantagouda.me")
