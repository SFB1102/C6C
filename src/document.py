'''
Created on 14.10.2019

@author: Katrin Ortmann
'''

############################

class Token:

    def __init__(self, **kwargs):
        for key in kwargs:
            self.add_value(key, kwargs.get(key, "_"))

    ####################

    def __str__(self):
        try:
            return self.FORM
        except:
            return ""

    ####################

    def add_value(self, key, val):
        self.__dict__[key] = val

############################

class Sentence:

    def __init__(self, tokens=[], **kwargs):
        self.n_toks = 0
        self.tokens = list()
        if tokens:
            for tok in tokens:
                self.add_token(tok)
        for key,val in kwargs.items():
            self.__dict__[key] = val

    #######################

    def add_token(self, token):
        self.n_toks += 1

        if token.__dict__.get("ID", None) in ("_", None):
            token.ID = str(self.n_toks)
        #TODO
        elif "-" in token.ID:
            pass
        #TODO
        elif "." in token.ID:
            pass

        self.tokens.append(token)

    #######################

    def __iter__(self):
        return iter(self.tokens)

    #######################

    def __str__(self):
        return " ".join(str(tok) for tok in self.tokens)

############################

class Doc(object):

    def __init__(self, filename, sentences = [], **kwargs):

        self.filename = filename

        for key,val in kwargs.items():
            self.__dict__[key] = val
        
        self.n_sents = 0
        
        self.sentences = []
        if sentences:
            for sent in sentences:
                self.add_sent(sent)
                
    ###################

    def __iter__(self):
        for sentence in self.sentences:
            yield sentence

    ####################

    def __str__(self):
        return "\n".join([str(sent) for sent in self.sentences])

    #######################

    def add_sent(self, sentence):
        self.n_sents += 1

        if sentence.__dict__.get("sent_id", None) in ("_", None):
            sentence.sent_id = str(self.n_sents)
        #TODO
        elif "-" in sentence.sent_id:
            pass
        #TODO
        elif "." in sentence.sent_id:
            pass

        self.sentences.append(sentence)

#################################

class Tree(object):

    def __init__(self, ID, cat, label, nodes = [], parent = None, **kwargs):

        self.ID = ID
        self.edge_label = label
        self.category = cat
        self.parent_node = parent
        self.children = []
        if nodes:
            for node in nodes:
                self.add_child(node)
        
        for key,val in kwargs.items():
            self.__dict__[key] = val

    #################

    def __iter__(self):
        for child in self.children:
            yield child

    #################

    def __len__(self):
        length = 0
        for child in self.children:
            if child.is_terminal:
                length += 1
            else:
                length += len(child)
        return length

    #################

    def __str__(self):
        if "token" in self.__dict__:
            return "(" + self.category + ":" + self.edge_label + " " + self.token.FORM + ")"
        else:
            return "(" + self.category + ":" + self.edge_label + "".join([str(child) for child in self.children]) + ")"
    
    #################

    def to_string(self):
        if self.is_terminal():
            #Map punctuation tags
            pos = self.token.XPOS
            if pos == "$(": pos = "$LBR"
            
            #Map bracket tokens
            tok = self.token.FORM
            tok = tok.replace("(", "LBR").replace(")", "RBR")
            #Return (POS:Label Token)
            return "(" + pos + ":" + self.label() + " " + tok + ")"
        else:
            #Return (Cat:Label(Children))
            tree_string = "(" + self.cat() + ":" + self.label() 
            children = "".join([c.to_string() for c in self.nodes()])
            tree_string += children + ")"
        return tree_string

    ##################

    def is_terminal(self):
        if not self.children:
            return True
        else:
            return False
    
    ################

    def terminals(self):
        if self.is_terminal():
            return [self]
        else:
            terminal_nodes = []
            for child in self.nodes():
                terminal_nodes.extend(child.terminals())
        return terminal_nodes
        
    ################

    def is_non_terminal(self):
        if self.is_terminal():
            return False
        else:
            return True

    ################

    def is_root(self):
        if not self.parent_node:
            return True
        else:
            return False

    ################

    def set_parent(self, node):
        self.parent_node = node

    ################

    def cat(self):
        return self.category

    ################

    def label(self):
        return self.edge_label

    ################

    def nodes(self):
        for child in self.children:
            yield child

    ################

    def terminals(self):
        terminal_nodes = []
        for c in self.children:
            if c.is_terminal():
                terminal_nodes.append(c)
            else:
                terminal_nodes.extend(c.terminals())
        return terminal_nodes
        
    ################

    def add_child(self, node):
        self.children.append(node)
        node.set_parent(self)
        
    ################

    @classmethod
    def from_PTB_string(cls, s):
        
        tree = None

        while s:
            char = s[0]

            #New subtree or token
            if char == "(":
                s = s[1:]
                cat = ""
                while s[0] != ":":
                    cat += s[0]
                    s = s[1:]
                s = s[1:]
                label = ""
                while s[0] not in ["(", " "]:
                    label += s[0]
                    s = s[1:]
                
                #Token
                if s[0] == " ":
                    s = s[1:]
                    form = ""
                    while s[0] != ")":
                        form += s[0]
                        s = s[1:]
                    #form = form.replace("LBR", "(").replace("RBR", ")")
                    #pos = cat.replace("LBR", "(").replace("RBR", ")")
                    token = Token(**{"FORM": form, "XPOS": cat, "PTBLabel": label})
                    child = Tree(None, cat=cat, label=label, **{"token" : token})
                    child.set_parent(tree)
                    tree.add_child(child)
                    s = s[1:]

                #Subtree
                else:
                    child = Tree(None, cat=cat, label=label)
                    if tree != None:
                        child.set_parent(tree)
                        tree.add_child(child)
                        tree = child
                    else:
                        tree = child                    
            
            elif char == ")":
                s = s[1:]
                if tree != None and tree.is_root():
                    return tree
                elif tree != None:
                    tree = tree.parent_node
                else:
                    return None

        return tree

###########################