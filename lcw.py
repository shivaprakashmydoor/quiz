import sys

class node:
    def __init__(self, char = False, end = False):
        self.children = {}
        self.char = char
        self.end = end

    def get_node(self, char):
        if char in self.children:
            return self.children[char]
        else:
            return None

    def add_node(self, char):
        tnode = node(char)
        self.children[char] = tnode
        return tnode

class trie_tree:
    def __init__(self):
        self.root = node()

    def __contains__(self, token):
        tnode = self.root
        for char in token:
            if char not in tnode.children:
                return False
            tnode = tnode.children[char]
        return tnode.end
        
    def generate_prefixes(self, token):
        prefix = ''
        prefix_list = []
        tnode = self.root
        for char in token:
            tnode = tnode.get_node(char)
            if not tnode:
                return prefix_list
         
            prefix += char
            if tnode.end:
                prefix_list.append(prefix)
        return prefix_list

    def insert_token(self, token):
        tnode = self.root
        for char in token:
            child = tnode.get_node(char)
            if not child:
                child = tnode.add_node(char)
            tnode = child
        tnode.end = True

def get_lcw(trie, prefix_db):
    lcw = ''
    lcw_len = 0

    #prefix_db.sort(key = len, reverse=True)
    while prefix_db:
        token, suffix = prefix_db.pop()
        if suffix in trie:
            if len(token) > lcw_len:
                lcw = token
                lcw_len = len(token)
        else:
            prefix_list = trie.generate_prefixes(suffix)
            for prefix in prefix_list:
                prefix_db.add((token,suffix[len(prefix):]))
                
    return lcw

def lcw_ops(argv):
    trie = trie_tree()
    prefix_db = set()

    fp = open(sys.argv[1], 'r')
    for token in fp:
        token = token.rstrip()
        prefix_list = trie.generate_prefixes(token)
        for prefix in prefix_list:
            prefix_db.add((token, token[len(prefix):]))
        trie.insert_token(token)

    lcw = get_lcw(trie, prefix_db)

    print 'Longest compound word: %s' %(lcw)

    fp.close()

    
if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise Exception('Usage: Enter the input file')

    lcw_ops(sys.argv[0:])

