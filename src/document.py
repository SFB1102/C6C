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
        """
        Initialize a tree object.

        A tree consists of non-terminal and terminal nodes,
        which are also tree objects. Terminal nodes have 
        a 'token' attribute, which is the token object.

        A tree can have:
        - an ID
        - a category (e.g. NP or MF)
        - a label (used for grammatical functions, e.g. SUBJ)
        - a list of child nodes
        - a parent node (or None)
        - additional attributes (as key-word arguments)
        """

        #Set attributes
        self.ID = ID
        self.edge_label = label
        self.category = cat
        self.parent_node = parent

        #Add child nodes
        self.children = []
        if nodes:
            for node in nodes:
                self.add_child(node)
        
        #Add additional attributes
        for key,val in kwargs.items():
            self.__dict__[key] = val

    #################

    def __iter__(self):
        """
        Yield child nodes
        """
        for child in self.children:
            yield child

    #################

    def __len__(self):
        """
        Return the number of dominated terminal nodes.
        """
        length = 0
        for child in self.children:
            if child.is_terminal:
                length += 1
            else:
                length += len(child)
        return length

    #################

    def __str__(self):
        """
        Return a bracketed string representation of the tree.
        
        Includes category, label and token form.
        """
        if "token" in self.__dict__:
            return "(" + self.category + ":" + self.edge_label + " " + self.token.FORM + ")"
        else:
            return "(" + self.category + ":" + self.edge_label + "".join([str(child) for child in self.children]) + ")"
    
    #################

    def to_string(self, include_gf=True):
        """
        Return a bracketed string representation of the tree.

        Includes category, label, POS and token form.
        If 'include_gf' is False, labels are excluded from the output.

        POS tags for punctuation are mapped to words:
        $( -> KLAMMER
        $. -> PUNKT
        $, -> KOMMA

        Bracket characters in word forms are mapped, too:
        ( -> LBR
        ) -> RBR
        """
        #Terminal node
        if self.is_terminal():

            #If there is nothing here,
            #return nothing
            if self.simple_cat == "":
                return ""

            #Map punctuation tags
            try:
                pos = self.token.XPOS
            except:
                breakpoint()
            if pos == "$(": pos = "KLAMMER"
            elif pos == "$.": pos = "PUNKT"
            elif pos == "$,": pos = "KOMMA"
            
            #Map brackets in tokens
            tok = self.token.FORM
            tok = tok.replace("(", "LBR").replace(")", "RBR")

            #Return (POS:Label Token)
            if include_gf:
                return "(" + pos + ":" + self.label() + " " + tok + ")"
            #Return (POS Token)
            else:
                return "(" + pos + " " + tok + ")"
        
        #Non-terminal node
        else:
            #Return (Cat:Label(Children))
            if include_gf:
                tree_string = "(" + self.cat() + ":" + self.label() 
            #Return (SimpleCat(Children))
            else:
                tree_string = "(" + self.simple_cat
            children = "".join([c.to_string(include_gf) for c in self.nodes()])
            tree_string += children + ")"
    
        return tree_string

    ##################

    def is_terminal(self):
        """
        Return if node is terminal.

        Terminal nodes are trees without child nodes.
        """
        if not self.children:
            return True
        else:
            return False
    
    ################

    def terminals(self):
        """
        Return list of dominated terminal nodes.

        If self is a terminal node, return list including self.
        """
        if self.is_terminal():
            return [self]
        else:
            terminal_nodes = []
            for child in self.nodes():
                terminal_nodes.extend(child.terminals())
        return terminal_nodes
    
    ################

    def is_non_terminal(self):
        """
        Return if node is non-terminal.
        """
        if self.is_terminal():
            return False
        else:
            return True

    ################

    def is_root(self):
        """
        Return if node is root.

        Root nodes are trees without parent node.
        """
        if not self.parent_node:
            return True
        else:
            return False

    ################

    def get_start_index(self, ignore_punct=False):
        """
        Return zero-based index of the first dominated token.

        If punctuation should be ignored, returns index of the
        first token that is not tagged as punctuation.
        If there are only punctuation tokens, returns index of the first one.

        Otherwise returns None.
        """
        #Get terminals
        terminals = self.terminals()
        if terminals:

            #If punctuation should be ignored
            if ignore_punct:
                #Strip off punctuation
                no_punct_terminals = [t for t in self.terminals() 
                                      if "token" in t.__dict__ 
                                         and not t.token.XPOS.startswith("$")]
                #Return index of first non-punct terminal
                if no_punct_terminals:
                    try:
                        return int(no_punct_terminals[0].__dict__["token"].__dict__.get("ID", None))-1
                    except ValueError:
                        return None
                else: 
                    pass
            
            #If punctuation should be included
            #or there is only punctuation
            if "token" in terminals[0].__dict__:
                try:
                    #Return index of first token
                    return int(terminals[0].__dict__["token"].__dict__.get("ID", None))-1
                except ValueError:
                    return None
            else:
                return None
        else:
            return None

    ########################

    def get_end_index(self, ignore_punct=False):
        """
        Return zero-based index of the last dominated token.

        If punctuation should be ignored, returns index of the
        last token that is not tagged as punctuation.
        If there are only punctuation tokens, returns index of the last one.

        Otherwise returns None.
        """
        #Get terminals
        terminals = self.terminals()
        if terminals:

            #If punctuation should be ignored
            if ignore_punct:
                #Strip off punctuation
                no_punct_terminals = [t for t in self.terminals() 
                                      if "token" in t.__dict__ 
                                         and not t.token.XPOS.startswith("$")]
                #Return index of last non-punct terminal
                if no_punct_terminals:
                    try:
                        return int(no_punct_terminals[-1].__dict__["token"].__dict__.get("ID", None))-1
                    except ValueError:
                        return None
                else: 
                    pass
            
            #If punctuation should be included
            #or there is only punctuation
            if "token" in terminals[-1].__dict__:
                try:
                    #Return index of last token
                    return int(terminals[-1].__dict__["token"].__dict__.get("ID", None))-1
                except ValueError:
                    return None
            else:
                return None
        else:
            return None

    ################

    def set_parent(self, node):
        """
        Set parent node
        """
        self.parent_node = node

    ################

    def get_parent(self):
        """
        Return parent node (or None)
        """
        return self.parent_node

    ################

    def cat(self):
        """
        Return category
        """
        return self.category

    ################

    def label(self):
        """
        Return label
        """
        return self.edge_label

    ################

    def nodes(self):
        """
        Yield child nodes
        """
        for child in self.children:
            yield child
        
    ################

    def add_child(self, node):
        """
        Append child node to the tree.
        Self is new parent of the child node.
        """
        self.children.append(node)
        node.set_parent(self)
        
    ################

    def remove_child(self, node):
        """
        Delete node from the list of child nodes.
        Return True, if node was included in the list. False, otherwise.
        """
        if node in self.children:
            del self.children[self.children.index(node)]
            return True
        else:
            return False

    ################

    def insert_child(self, index, node):
        """
        Insert node in the list of child nodes a the given index.
        Self is new parent of the child node.

        Return True, if insertion was succesful. False, otherwise.
        """
        try:
            self.children.insert(index, node)
            node.set_parent(self)
            return True
        except IndexError:
            return False
        
    ################

    @classmethod
    def from_PTB_string(cls, s):
        """
        Read a tree object from a string in Penn-Treebank style.

        Accepts trees with labels:
        (Cat:Label(Subtree))
        (POS:Label TokenForm)

        and without labels:
        (Cat(Subtree))
        (POS TokenForm)

        Missing labels are set to '--'.

        In case of an empty string or '(VROOT)', returns None.
        """
        tree = None

        #Empty tree, return None
        if s == "(VROOT)":
            return tree
        
        #Go through tree string
        while s:
            char = s[0]

            #New subtree or token
            if char == "(":
                s = s[1:]

                #Read cat (or POS in case of token)
                cat = ""
                while s[0] not in ["(", " ", ":", ")"]:
                    cat += s[0]
                    s = s[1:]
                
                #Read label
                if s[0] == ":":
                    s = s[1:]
                    label = ""
                    while s[0] not in ["(", " "]:
                        label += s[0]
                        s = s[1:]
                    simple_cat = cat + ":" + label
                #No label? Set default
                else:
                    label = "--"
                    simple_cat = cat

                #If token: read token form
                if s[0] == " ":
                    s = s[1:]
                    form = ""
                    while s[0] != ")":
                        form += s[0]
                        s = s[1:]

                    #Create token object
                    #Map POS
                    token = Token(**{"FORM": form, 
                                     "XPOS": cat.replace("KLAMMER", "$(").replace("PUNKT", "$.").replace("KOMMA", "$,").replace("LBR", "(").replace("RBR", ")"), 
                                     "PTBLabel": label})
                    
                    #Create terminal node with token attribute
                    child = Tree(str(len(tree.terminals())+1), cat=cat, label=label, 
                                 **{"token" : token, "simple_cat" : simple_cat})
                    
                    #Set parent of terminal node and add to tree
                    child.set_parent(tree)
                    tree.add_child(child)
                    s = s[1:]

                #If subtree: read subtree
                else:
                    #Create non-terminal
                    child = Tree(None, cat=cat, label=label, 
                                 **{"simple_cat" : simple_cat})
                    #Set parent and add to tree
                    if tree != None:
                        child.set_parent(tree)
                        tree.add_child(child)
                        tree = child
                    #Or set root node
                    else:
                        tree = child                    

            #End of node
            elif char == ")":
                s = s[1:]
                #Set terminal IDs
                if tree != None and tree.is_root():
                    for i, t in enumerate(tree.terminals()):
                        t.ID = str(i+1)
                    return tree
                #Move up in tree and continue
                elif tree != None:
                    tree = tree.parent_node
                else:
                    return None

            #Neither start nor end
            else:
                input("Error: Unexpected char '{0}'. Press any key to continue.".format(char))
                s = s[1:]

        #Set terminal IDs
        for i, t in enumerate(tree.terminals()):
            t.ID = str(i+1)

        return tree

###########################