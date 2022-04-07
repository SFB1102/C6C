# -*- coding: utf-8 -*-
'''
Created on 14.10.2019

@author: Katrin Ortmann
'''

import os, re

############################

class Processor(object):

    def __init__(self):
        pass

############################


class DTAChopper(Processor):

    def __init__(self):
        pass

    #####################

    def chop(self, doc):

        s = 0
        while s < len(doc.sentences):
            if not any(tok.MovElemCat != "_" for tok in doc.sentences[s].tokens):
                del doc.sentences[s]
            else:
                s += 1

        pass

    #####################

    def reindex(self, doc):

        charoffset = 0

        for i, sent in enumerate(doc.sentences):
            for tok in sent.tokens:
                #Re-index sentences
                old_sentid = tok.TSVID.split("-")[0]
                new_sentid = str(i+1)
                tok.TSVID = new_sentid + "-" + tok.TSVID.split("-")[-1]

                #Re-index characters
                tokstart = charoffset
                tokend = charoffset + len(tok.FORM)
                tok.CHARS = str(tokstart) + "-" + str(tokend)
                charoffset += len(tok.FORM) + 1

                #Re-index annotations
                for annotation in tok.__dict__:
                    if annotation in ["TSVID", "CHARS", "FORM", "XPOS", "LEMMA", "OrthCorr",
                    "OrthCorrOp", "OrthCorrReason"]:
                        continue
                    tok.__dict__[annotation] = re.sub(old_sentid+r"(-\d+)", new_sentid + r"\1", tok.__dict__[annotation])

    #####################

    def process(self, doc):

        #Remove un-annotated sentences
        self.chop(doc)

        #Re-index sentences and chars
        self.reindex(doc)

        return doc

###########################

class TopFChopper(Processor):

    def __init__(self):
        pass

    #####################

    def chop(self, doc):

        s = 0
        while s < len(doc.sentences):
            if not any(not tok.TopF in ["_", "FRAG"] for tok in doc.sentences[s].tokens):
                del doc.sentences[s]
            else:
                s += 1
        pass

    #####################

    def process(self, doc):

        #Remove un-annotated sentences
        self.chop(doc)

        return doc

###########################

class DTASimplifier(Processor):

    #######################

    def __init__(self):
        self.mapping = {"ID" : "ID",
                        "FORM" : "FORM",
                        "XPOS" : "XPOS",
                        "LEMMA" : "LEMMA",
                        "OrthCorr" : "OrthCorr",
                        "Cite" : "Cite",
                        "AntecMovElem" : "Antec",
                        "AntecHead" : "AntecHead",
                        "SentBrcktType" : "SentBrckt",
                        "MovElemCat" : "MovElem",
                        "MovElemPos" : "MovElemPos",
                        "RelCType" : "RelCType",
                        "AdvCVPos" : "AdvCVPos",
                        "AdvCVHead" : "AdvCVHead"}

    #######################

    def process(self, doc):

        for sent in doc.sentences:
            for tok in sent.tokens:
                #print(tok.__dict__)
                #i = input()
                #Map annotation names and delete unneeded ones
                for annoname in list(tok.__dict__):

                    newname = self.mapping.get(annoname, None)
                    if newname:
                        tok.__dict__[newname] = tok.__dict__[annoname]
                    if newname != annoname:
                        del tok.__dict__[annoname]

                if tok.Antec != "_":
                    if not "|" in tok.Antec and "_" in tok.Antec:
                        tok.Antec = "_"
                    else:
                        tok.Antec = "|".join([re.sub(r"\[\d+\]", "", a).split("-")[-1] for a in tok.Antec.split("|")])

                if tok.AntecHead == "*":
                    tok.AntecHead = "_"
                elif tok.AntecHead != "_":
                    tok.AntecHead = "|".join([a.split("-")[-1] for a in tok.AntecHead.split("|") if not "*" in a])

                if tok.MovElemPos != "_":
                    tok.MovElemPos = "|".join([a for a in tok.MovElemPos.split("|") if not "*" in a])

                if tok.AdvCVPos == "*":
                    tok.AdvCVPos = "_"
                elif tok.AdvCVPos != "_":
                    if not "|" in tok.AdvCVPos and "_" in tok.AdvCVPos:
                        tok.AdvCVPos = "_"
                    else:
                        tok.AdvCVPos = "|".join([a for a in tok.AdvCVPos.split("|") if not "_" in a])
                if not tok.AdvCVPos:
                    tok.AdvCVPos = "_"

                if tok.AdvCVHead == "*":
                    tok.AdvCVHead = "_"
                elif tok.AdvCVHead != "_":
                    tok.AdvCVHead = "|".join([a.split("-")[-1] for a in tok.AdvCVHead.split("|") if not "*" in a])
                if not tok.AdvCVHead:
                    tok.AdvCVHead = "_"

                if "Cite" in tok.__dict__ and tok.Cite != "_":
                    tok.Cite = "|".join([a.replace("*", "cite") for a in tok.Cite.split("|")])
                #print(tok.__dict__)
                #i = input()
        return doc

############################

class HIPKONtoSTTSMapper(Processor):

    def __init__(self):
        pass

    #####################

    def process(self, doc):

        filedir = "./../res"
        file = open(os.path.join(filedir, "HIPKON-STTS.txt"), mode="r", encoding="utf-8")

        #dictionary "HIPKON" : "STTS"
        tags = dict()
        for line in file:
            hipkon, stts = line.strip().split()
            tags[hipkon] = stts

        file.close()

        punct = [".", ":", "!", "?", ";"]
        comma = [",", "/"]
        other = ["(", ")", "[", "]", "-", '"', "'", "„"]
        #dictionary for used rules
        rules = dict()
        rules["$_"] = list()
        rules["ſ"] = list()

        for sent in doc.sentences:
            for tok in sent.tokens:

                if tok.POS != "_":
                    #punctuation
                    if tok.POS == "$_":
                        if tok.FORM in punct:
                            tok.__dict__["XPOS"] = "$."
                            if "$." not in rules["$_"]:
                                rules["$_"].append("$.")
                        elif tok.FORM in comma:
                            tok.__dict__["XPOS"] = "$,"
                            if "$," not in rules["$_"]:
                                rules["$_"].append("$,")
                        else:
                            tok.__dict__["XPOS"] = "$("
                            if "$(" not in rules["$_"]:
                                rules["$_"].append("$(")
                    #other
                    else:
                        try:
                            tok.__dict__["XPOS"] = tags[tok.POS]
                            rules[tok.POS] = tags[tok.POS]
                        except:
                            if tok.FORM in punct:
                                tok.__dict__["XPOS"] = "$."
                                if "$." not in rules["ſ"]:
                                    rules["ſ"].append("$.")
                            elif tok.FORM in comma:
                                tok.__dict__["XPOS"] = "$,"
                                if "$," not in rules["ſ"]:
                                    rules["ſ"].append("$,")
                            elif tok.FORM in other:
                                tok.__dict__["XPOS"] = "$("
                                if "$(" not in rules["ſ"]:
                                    rules["ſ"].append("$(")
                            else:
                                tok.__dict__["XPOS"] = "FEHLER"
                                print("FEHLER")
                else:
                    #punctuation?
                    if tok.FORM in punct:
                        tok.__dict__["XPOS"] = "$."
                    elif tok.FORM in comma:
                        tok.__dict__["XPOS"] = "$,"
                    elif tok.FORM in other:
                        tok.__dict__["XPOS"] = "$("

                    #missing tag
                    else:
                        info = dict()
                        info["Token"] = tok.FORM
                        info["Filename"] = doc.filename[:-4]
                        info["sent_id"] = sent.sent_id
                        info["tok_id"] = tok.ID

                        #output: list of token without tag
                        cats = ["Token", "Filename", "sent_id", "tok_id"]
                        missing_tags = open(os.path.join(filedir, "hipkon_missing_tags.csv"), mode="a", encoding="utf-8")
                        #Write header if
                        if missing_tags.tell() == 0:
                            print("\t".join(info), file=missing_tags)
                        print("\t".join([info[cat] for cat in cats]), file=missing_tags)
                        missing_tags.close()

        #output: list of rules which were used
        cats = ["POS", "STTS"]
        used_rules = open(os.path.join(filedir, "rules_" + doc.filename), mode="a", encoding="utf-8")
        #Write header if
        if used_rules.tell() == 0:
            print("\t".join(cats), file=used_rules)
        if rules["$_"]:
            print("$_" + "\t" + " ".join([rule for rule in rules["$_"]]), file=used_rules)
        if rules["ſ"]:
            print("ſ" + "\t" + " ".join([rule for rule in rules["ſ"]]), file=used_rules)
        for rule in tags:
            if rule in rules:
                print(rule + "\t" + rules[rule], file=used_rules)
        used_rules.close()

        return doc

############################

class addmissingSTTStoHIPKON(Processor):

    def __init__(self):
        pass

    #####################

    def process(self, doc):

        filedir = "./../res"
        missing_stts = open(os.path.join(filedir, "hipkon_missing_stts.csv"), mode="r", encoding="utf-8")

        for line in missing_stts:
            token, filename, sent_id, tok_id, stts = line.strip().split()
            if doc.filename[:-4] == filename:
                sent = doc.sentences[int(sent_id)-1]
                tok = sent.tokens[int(tok_id)-1]
                if tok.FORM == token:
                    tok.__dict__["XPOS"] = stts
                else:
                    print("FEHLER")

        missing_stts.close()

        return doc

###########################

class TopFSimplifier(Processor):

    def __init__(self):
        self.mapping = {"ID" : "ID",
                        "FORM" : "FORM",
                        "XPOS" : "XPOS",
                        "LEMMA" : "LEMMA",
                        "FEATS" : "FEATS",
                        "DEPREL" : "DEPREL",
                        "HEAD" : "HEAD",
                        "CHUNK" : "CHUNK",
                        "TopF" : "TopF"}

    #####################

    def process(self, doc):

        for sent in doc.sentences:
            for tok in sent.tokens:

                #Map annotation names and delete unneeded ones
                for annoname in list(tok.__dict__):

                    newname = self.mapping.get(annoname, None)
                    if newname:
                        tok.__dict__[newname] = tok.__dict__[annoname]
                    if newname != annoname:
                        del tok.__dict__[annoname]

                #Remove backslash escapes from FEAT
                if tok.__dict__.get("FEATS", None):
                    tok.FEATS = re.sub(r"\\", "", tok.FEATS)

                #Simplify TopF column
                TopF = ""
                annotations = tok.TopF.split("|")
                if len(annotations) == 1:
                    if annotations[0] == "_" or not "[" in annotations[0]:
                        pass
                    else:
                        tok.TopF = re.sub(r"\[\d+\]", "", annotations[0])
                else:
                    sorted_annotations = []
                    for a in annotations:
                        field = a.split("[")[0]
                        number = a.split("[")[-1].rstrip("]")
                        try:
                            number = int(number)
                        except:
                            number = 99999
                        sorted_annotations.append((field, number))
                    sorted_annotations.sort(key=lambda l: int(l[1]))
                    tok.TopF = "-".join([a for a,i in sorted_annotations])

                #Create Sentence Bracket Column
                tok.__dict__["SentBrckt"] = ""
                for anno in tok.TopF.split("-"):
                    if anno in ["LK", "RK"]:
                        if tok.SentBrckt:
                            tok.__dict__["SentBrckt"] += "-" + anno
                        else:
                            tok.__dict__["SentBrckt"] += anno
                if not tok.SentBrckt:
                    tok.__dict__["SentBrckt"] = "_"

                #Strip sentID from depHead
                if tok.__dict__.get("HEAD", None) and tok.HEAD != "_":
                    tok.HEAD = tok.HEAD.split("-")[-1]

        return doc

################################

class SATZKLAMMERtoTopF(Processor):

    ######################

    def __init__(self):
        self.mapping = {"LI" : "LK", "RE" : "RK", "_" : "_"}

    ######################

    def process(self, doc):

        topfID = 1
        for sent in doc.sentences:
            openbracket = ""

            for i,tok in enumerate(sent.tokens):
                if tok.SATZKLAMMER != "_":
                    if openbracket:
                        #Bracket continues
                        if openbracket.startswith(self.mapping.get(tok.SATZKLAMMER, "_")):
                            if not "[" in openbracket:
                                openbracket = openbracket + "[" + str(topfID) + "]"
                                sent.tokens[i-1].TopF = openbracket
                            tok.TopF = openbracket
                        #New bracket
                        else:
                            if "[" in openbracket: topfID += 1
                            openbracket = ""
                            openbracket = self.mapping.get(tok.SATZKLAMMER, "_")
                            tok.TopF = self.mapping.get(tok.SATZKLAMMER, "_")
                    #New bracket
                    else:
                        openbracket = self.mapping.get(tok.SATZKLAMMER, "_")
                        tok.TopF = self.mapping.get(tok.SATZKLAMMER, "_")
                #No bracket
                else:
                    #End previous bracket
                    if openbracket:
                        if "[" in openbracket: topfID += 1
                        openbracket = ""
                    tok.TopF = "_"
        return doc

###############################

class TSVIndexer(Processor):

    def __init__(self):
        pass

    def process(self, doc):

        charoffset = 0

        for i, sent in enumerate(doc.sentences):
            for j, tok in enumerate(sent.tokens):
                #Re-index sentences
                new_sentid = str(i+1)
                new_tokid = str(j+1)
                tok.TSVID = new_sentid + "-" + new_tokid

                #Re-index characters
                tokstart = charoffset
                tokend = charoffset + len(tok.FORM)
                tok.CHARS = str(tokstart) + "-" + str(tokend)
                charoffset += len(tok.FORM) + 1

            charoffset += 1

            #Add spaces to text, so WebAnno finds the tokens
            sent.text = " ".join([tok.FORM for tok in sent.tokens])

        return doc

#######################

class CoNLLUPLUSIndexer(Processor):

    def __init__(self):
        pass

    def process(self, doc):

        for i, sent in enumerate(doc.sentences):
            for j, tok in enumerate(sent.tokens):
                tok.ID = j + 1
            sent.sent_id = i + 1

        return doc

############################

class HiTStoSTTSMapper(Processor):

    def __init__(self):
        pass

    #####################

    def process(self, doc):

        file = open("./../res/HiTS_STTS_mapping.csv", mode="r", encoding="utf-8")

        #dictionary {"pos" : {"posLemma" : "STTS"}}
        tags = dict()
        for line in file:
            line = line.strip().split("\t")
            if line[0] in tags:
                tags[line[0]][line[1]] = line[4]
            else:
                tags[line[0]] = {line[1] : line[4]}

        file.close()

        punct = [":", "!", "?", ";"]
        comma = [",", "/", "//"]
        other = ["(", ")", "[", "]", "-", '"', "'", "„"]

        for sent in doc.sentences:
            for tok in sent.tokens:

                if "-" not in tok.ID:

                    #punctuation
                    if tok.POS == "$_":
                        #look up tok.FORM and punc-annotation
                        if tok.FORM in [".", "·"]:
                            if tok.PUNC == "$E":
                                tok.__dict__["XPOS"] = "$."
                            else:
                                tok.__dict__["XPOS"] = "$,"
                        elif tok.FORM in punct:
                            tok.__dict__["XPOS"] = "$."
                        elif tok.FORM in comma:
                            tok.__dict__["XPOS"] = "$,"
                        elif tok.FORM in other:
                            tok.__dict__["XPOS"] = "$("

                    #other
                    elif tok.POS == "_":
                        if tok.POS_GEN == "_":
                            tok.__dict__["XPOS"] = tags["--"]["--"]
                        else:
                            tok.__dict__["XPOS"] = tags["--"][tok.POS_GEN]

                    else:
                        tok.__dict__["XPOS"] = tags[tok.POS][tok.POS_GEN]

        return doc

###################################

class TUEBADSTopFExtractor(Processor):

    def __init__(self):
        self.tuebatagset = ["LV", "VF", "LK", "C", "MF", "MFE",
                            "VC", "VCE", "NF", "KOORD", "PARORD", "FKOORD"]

    def process(self, doc):
        for sent in doc.sentences:

            open_fields = []

            #Move HD info from POS column to new col
            for tok in sent.tokens:
                head = tok.__dict__.get("POS:HD", "_")
                if head != "_" and not ":HD" in head:
                    head = "_"
                elif head != "_":
                    head = "HD"
                tok.__dict__["PHRASE:HEAD"] = head
                tok.__dict__["POS:HD"] = "_"

                #Read topological fields from syntax col
                syntax = tok.__dict__.get("SYNTAX", "_")

                #Add open fields to token annotation
                tok.__dict__["TopoField"] = ""
                for field in open_fields:
                    if field in self.tuebatagset:
                        if tok.TopoField: tok.TopoField += "-" + field
                        else: tok.TopoField = field

                #Analyze token's own syntax annotation
                if syntax:
                    syntax = syntax.replace("(", " (").replace(")", " )")#re.sub(r"\(", r" \(", syntax)
                    #syntax = re.sub(r"\)", r" \)", syntax)
                    syntax = syntax.split()
                    for node in syntax:
                        if node.strip() in ["*", "_"]:
                            continue
                        #End of node
                        elif node.strip() == ")":
                            open_fields = open_fields[:-1]
                        #New node
                        else:
                            node = node.strip().replace("(", "").replace("*", "")
                            if ":" in node:
                                node = node.split(":")[0]
                            open_fields.append(node)
                            if node in self.tuebatagset:
                                if tok.TopoField:
                                    tok.TopoField += "-" + node
                                else:
                                    tok.TopoField = node

                if not tok.TopoField: tok.TopoField = "_"

        return doc

#############################

def map_tueba_tagset(orig_folder, target_folder):
    from importer import CoNLLUPlusImporter
    from exporter import CoNLLUPlusExporter

    for of in [os.path.join(orig_folder, f) for f in os.listdir(orig_folder)]:
        doc = CoNLLUPlusImporter().import_file(of)
        doc = TUEBATopFSimplifier().process(doc)
        CoNLLUPlusExporter().export(doc, target_folder)

############################

def convert_tuebads(indir, outdir):
    from importer import TUEBADSConllImporter
    from exporter import CoNLLUPlusExporter

    for conllfile in [os.path.join(indir, f) for f in os.listdir(indir)]:
        doc = TUEBADSConllImporter().import_file(conllfile)
        doc = TUEBADSTopFExtractor().process(doc)
        CoNLLUPlusExporter().export(doc, outdir)

############################

def find_ANNIS_matches(grid_file, conll_folder, outdir):

    from importer import CoNLLUPlusImporter
    from exporter import DTATSVExporter, CoNLLUPlusExporter
    from document import Doc

    #Import grid file
    grid = open(grid_file, mode="r", encoding="utf-8").readlines()

    matches = dict()
    n = 0
    for line in grid:
        if not line.strip() or line.strip() == "finished":
            if not n+1 in matches:
                n += 1
        else:
            line = line.split("\t")
            if not n in matches:
                matches[n] = {line[1] : line[2].strip()}
            else:
                matches[n][line[1]] = line[2].strip()

    #For each annis match import coresponding conll file
    conll = None
    doc = None
    for _, match in sorted(matches.items()):
        filename = match["meta::annis:doc"]
        #If match is from same file as previous one
        if conll and conll.filename.startswith(filename):
            #Continue with same conll and output doc
            pass
        #Match from a new file
        else:
            #Export previous doc
            if doc:
                TSVIndexer().process(doc)
                if not os.path.isdir(os.path.join(outdir, "tsv")):
                    os.makedirs(os.path.join(outdir, "tsv"))
                if not os.path.isdir(os.path.join(outdir, "conllup")):
                    os.makedirs(os.path.join(outdir, "conllup"))
                DTATSVExporter().export(doc, os.path.join(outdir, "tsv"))
                CoNLLUPlusExporter().export(doc, os.path.join(outdir, "conllup"))
            #Import conll
            conll = CoNLLUPlusImporter().import_file(os.path.join(conll_folder, filename+".conllup"))
            #Create output doc
            doc = Doc(filename)

        #Get matched token sequence
        tok_annos = [re.sub(r"\[\d+-\d+\]$", "", t) for t in match["tok_anno"].split()]
        middle_tok = tok_annos[(len(tok_annos)-1)//2]
        if (len(tok_annos)-1)//2-5 >= 0:
            prev_5_toks = tok_annos[(len(tok_annos)-1)//2-5:(len(tok_annos)-1)//2]
        else:
            prev_5_toks = tok_annos[:(len(tok_annos)-1)//2]
        prev_5_toks.reverse()
        try:
            next_5_toks = tok_annos[(len(tok_annos)-1)//2+1:(len(tok_annos)-1)//2+6]
        except IndexError:
            try:
                next_5_toks = tok_annos[(len(tok_annos)-1)//2+1:]
            except IndexError:
                next_5_toks = []


        #Search for token sequence in conll
        for sent in conll.sentences:
            hits = [t for t in sent.tokens if t.ANNO_ASCII == middle_tok]

            #Every time the search word appears in a sentence
            for hit in hits:

                contains_previous_toks = True
                contains_following_toks = True

                #Check previous tokens
                prev_forms = [t.ANNO_ASCII for t in sent.tokens[:sent.tokens.index(hit)]]
                prev_forms.reverse()

                if not prev_forms or not prev_5_toks:
                    contains_previous_toks = False
                else:
                    for prev_tok,prev_form in zip(prev_5_toks, prev_forms):
                        if prev_tok != prev_form:
                            contains_previous_toks = False
                            break

                #Check following tokens
                if len(sent.tokens) > sent.tokens.index(hit)+1:
                    next_forms = [t.ANNO_ASCII for t in sent.tokens[sent.tokens.index(hit)+1:]]
                else:
                    next_forms = []

                if not next_forms or not next_5_toks:
                    contains_following_toks = False
                else:
                    for next_tok,next_form in zip(next_5_toks, next_forms):
                        if next_tok != next_form:
                            contains_following_toks = False
                            break

                #Add sentence(s) to doc
                if contains_previous_toks or contains_following_toks:
                    if not sent in doc.sentences:
                        doc.sentences.append(sent)
                        for tok in doc.sentences[-1].tokens:
                            tok.XPOS = tok.POS
                    break

    if doc:
        TSVIndexer().process(doc)
        if not os.path.isdir(os.path.join(outdir, "tsv")):
            os.makedirs(os.path.join(outdir, "tsv"))
        if not os.path.isdir(os.path.join(outdir, "conllup")):
            os.makedirs(os.path.join(outdir, "conllup"))
        DTATSVExporter().export(doc, os.path.join(outdir, "tsv"))
        CoNLLUPlusExporter().export(doc, os.path.join(outdir, "conllup"))

############################

class ANSELMtoSTTSMapper(Processor):

    def __init__(self):
        pass

    #####################

    def process(self, doc):

        file = open("./../res/Anselm_pos_tags.csv", mode="r", encoding="utf-8")

        #dictionary {"Anselm" : "STTS"}
        tags = dict()
        for line in file:
            anselm, stts = line.strip().split("\t")
            tags[anselm] = stts
        tags["_"] = "_"
        file.close()

        for sent in doc.sentences:
            for tok in sent.tokens:
                tok.__dict__["XPOS"] = tags[tok.POS]

        return doc

############################

class ReFHiTStoSTTSMapper(Processor):

    def __init__(self):
        pass

    #####################

    def process(self, doc):

        file = open("./../res/ReF_HiTS-STTS_mapping.csv", mode="r", encoding="utf-8")

        #dictionary {"pos" : {"posLemma" : "STTS"}}
        tags = dict()
        for line in file:
            line = line.strip().split("\t")
            if line[0] in tags:
                tags[line[0]][line[1]] = line[2]
            else:
                tags[line[0]] = {line[1] : line[2]}
        tags["_"] = {"_" : "_"}
        file.close()

        punct = [":", "!", "?", ";"]
        comma = [","]

        for sent in doc.sentences:
            for i, tok in enumerate(sent.tokens):

                if "-" not in tok.ID:

                    del tok.__dict__["XPOS"]

                    #punctuation
                    if tok.POS == "$_":
                        #look up tok.FORM and boundary-tag
                        if tok.FORM in [".", "·", "/"]:
                            if "." in tok.__dict__.get("BOUNDARY", ""):
                                tok.__dict__["XPOS"] = "$."
                            elif "," in tok.__dict__.get("BOUNDARY", ""):
                                tok.__dict__["XPOS"] = "$,"
                            else:
                                for punc in punct:
                                    if punc in tok.__dict__.get("BOUNDARY", ""):
                                        tok.__dict__["XPOS"] = "$."
                        elif tok.FORM in punct:
                            tok.__dict__["XPOS"] = "$."
                        elif tok.FORM in comma:
                            tok.__dict__["XPOS"] = "$,"

                        if "XPOS" not in tok.__dict__:
                            if i == len(sent.tokens)-1:
                                tok.__dict__["XPOS"] = "$."
                            else:
                                tok.__dict__["XPOS"] = "$,"

                    #other
                    elif tok.POS == "DRELS":
                        tok_id = int(tok.ID)
                        for token in sent.tokens:
                            if token.ID == str(tok_id + 1):
                                if tags[token.POS][token.POS_LEMMA] in ["ADJA", "NN"]:
                                    tok.__dict__["XPOS"] = "PRELAT"
                                else:
                                    tok.__dict__["XPOS"] = "PRELS"

                    elif tok.POS == "PW":
                        tok_id = int(tok.ID)
                        for token in sent.tokens:
                            if token.ID == str(tok_id + 1):
                                if tags[token.POS][token.POS_LEMMA] in ["ADJA", "NN"]:
                                    tok.__dict__["XPOS"] = "PWAT"
                                else:
                                    tok.__dict__["XPOS"] = "PWS"

                    else:
                        tok.__dict__["XPOS"] = tags[tok.POS][tok.POS_LEMMA]

        return doc

############################

class MercuriusToSTTSMapper(Processor):

    def __init__(self):
        pass

    #####################

    def process(self, doc):

        filedir = "./../res"
        file = open(os.path.join(filedir, "mercurius_STTS.csv"), mode="r", encoding="utf-8")

        #dictionary "Mercurius" : "STTS"
        tags = dict()
        for line in file:
            mercurius, stts, comments = line.strip().split("\t")
            tags[mercurius] = stts

        file.close()

        for sent in doc.sentences:
            for i, tok in enumerate(sent.tokens):

                if tok.POS != "_":
                    stts = tags.get(tok.POS, None)

                    if stts:

                        #Virgel
                        if stts == "$(" and tok.FORM == "/":
                            tok.XPOS = "$,"

                        #For compounds
                        elif stts == "#" and tok.POS == "KOMPE":

                            #Get STTS of next token
                            if i < len(sent.tokens)-1:
                                j = i
                                nextstts = None
                                while j < len(sent.tokens)-1 and (nextstts is None or nextstts == "#"):
                                    nexttok = sent.tokens[j+1]
                                    nextstts = tags.get(nexttok.POS, None)
                                    j += 1

                                if not nextstts or nextstts == "#":
                                    print("POS", nextstts, "of token", tok.ID, "in sentence", sent.sent_id, "after KOMPE is not in mapping.")
                                    tok.XPOS = "NN"

                                #And assign it to all compound parts
                                else:
                                    tok.XPOS = nextstts

                            else:
                                print("KOMPE is last token in sentence.")
                                tok.XPOS = "NN"
                        else:
                            tok.XPOS = stts

                    else:
                        print("Not in mapping:", tok.POS)

                else:
                    print("Token", tok.ID, tok.FORM, "in sentence", sent.sent_id, "in doc", doc.filename, "not annotated")
                    tok.XPOS = "XY"

        return doc

############################

class ReFUPToSTTSMapper(Processor):

    def __init__(self):
        pass

    #####################

    def process(self, doc):

        filedir = "./../res"
        file = open(os.path.join(filedir, "ReF-UP-STTS.csv"), mode="r", encoding="utf-8")

        #dictionary "ReF.UP" : "STTS"
        tags = dict()
        for line in file:
            if "POS" in line and "STTS" in line:
                continue
            refup = line.strip().split("\t")[0]
            stts = line.strip().split("\t")[1]
            tags[refup] = stts

        file.close()

        for sent in doc.sentences:
            for t, tok in enumerate(sent.tokens):

                if tok.POS != "_":
                    stts = tags.get(tok.POS, None)

                    if stts:
                        if stts.startswith("$") and tok.POS in ["$MK", "$MSBI", "$QL", "$QR"] \
                           and t > 0 and sent.tokens[t-1].XPOS.startswith("$"):
                            sent.tokens[t-1].XPOS = stts

                        tok.XPOS = stts

                    else:
                        print("Not in mapping:", tok.POS)

                else:
                    print("Token", tok.ID, tok.FORM, "in sentence", sent.sent_id, "in doc", doc.filename, "not annotated")
                    tok.XPOS = "XY"

        return doc

############################

class FuerstinnentoSTTSMapper(Processor):

    def __init__(self):
        pass

    #####################

    def process(self, doc):

        file = open("./../res/Fuerstinnen_STTS.csv", mode="r", encoding="utf-8")

        #dictionary {"POS" : "STTS"}
        tags = dict()
        for line in file:
            pos, stts = line.strip().split("\t")
            tags[pos] = stts
        file.close()

        for sent in doc.sentences:
            for tok in sent.tokens:

                if tok.__dict__["POS"] == "_":
                    if tok.__dict__["LEMMA"] == "_":
                        tok.__dict__["XPOS"] = "XY"
                        tok.__dict__["LEMMA"] = "#"
                    else:
                        tok.__dict__["XPOS"] = "XY"

                else:
                    tok.__dict__["XPOS"] = tags[tok.POS]

        return doc

############################

class VirgelMapper(Processor):

    def __init__(self):
        pass

    #####################

    def process(self, doc):

        for sent in doc.sentences:
            for tok in sent.tokens:

                if tok.__dict__["FORM"] == "/":
                    tok.__dict__["XPOS"] = "$("

        return doc

############################

class PronominalAdverbMapper(Processor):

    def __init__(self):
        pass

    #####################

    def process(self, doc):

        for sent in doc.sentences:
            for tok in sent.tokens:

                if tok.__dict__["XPOS"] == "PROAV":
                    tok.__dict__["XPOS"] = "PAV"

        return doc

############################

class ReFUPCoding(Processor):

    def __init__(self):
        pass

    #####################

    def process(self, doc):

        for sent in doc.sentences:
            for tok in sent.tokens:

                if "Ã" in tok.__dict__["FORM"]:
                    #print(tok.__dict__["FORM"])
                    tok.__dict__["FORM"] = tok.__dict__["FORM"].replace("Ã", "ß")

            sent.text = " ".join([tok.FORM for tok in sent.tokens])

        return doc

############################

class BracketRemover(Processor):

    def __init__(self):
        pass

    #####################

    def process(self, doc):

        brackets = ["(", ")", "{", "}", "[", "]", "<", ">"]

        for sent in doc.sentences:
            for tok in sent.tokens:

                if any(c.isalnum() for c in tok.FORM) and any(b in tok.FORM for b in brackets):
                    for b in brackets:
                        if b in tok.FORM: tok.FORM = tok.FORM.replace(b, "")

        return doc

#########################

class DependencyProcessor(Processor):

    def __init__(self):
        pass

    #####################

    def process_sentence(self, sent):

        #Add root(s) to sentence
        #And inform every tok about its head-token
        sent.roots = []
        for tok in sent.tokens:
            if tok.HEAD == "0":
                sent.roots.append(tok)
                tok.head_tok = "ROOT"
            elif tok.HEAD != "_":
                try:
                    tok.head_tok = [t for t in sent.tokens if t.ID == tok.HEAD][0]
                except:
                    tok.head_tok = None
            else:
                tok.head_tok = None

        #Then inform every tok about its children
        for tok in sent.tokens:
            tok.dep_toks = [t for t in sent.tokens if t.head_tok == tok]          

        return sent

    #####################

    def process(self, doc):

        for sent in doc.sentences:
            sent = self.process_sentence(sent)
        
        return doc

############################

class DependencyManipulator(Processor):

    def __init__(self):
        pass

    #####################

    def process_sentence(self, sent):

        if not "roots" in sent.__dict__:
            sent = DependencyProcessor().process_sentence(sent)

        #for tok in sent.tokens:
        #    print(tok.ID, tok.FORM, tok.DEPREL, tok.HEAD)

        #Switch copula relation
        copulas = [tok for tok in sent.tokens if tok.DEPREL == "cop"]
        for copula in copulas:
            new_pred = copula.head_tok
            if new_pred == "ROOT" or new_pred == None:
                continue
            #Dependents of former head become dependents of former copula
            deps = [tok for tok in sent.tokens 
                    if tok.head_tok == new_pred and tok != copula
                    and not tok.DEPREL in ["amod", "case", 'det', 'det:neg', "nmod:poss", "nmod", "fixed", 
                                           "appos", 'flat', 'flat:foreign', "nummod"]]
            for dep in deps:
                dep.head_tok = copula
                dep.HEAD = copula.ID
            #Former copula becomes head
            copula.head_tok = new_pred.head_tok
            copula.HEAD = new_pred.HEAD
            copula.DEPREL = new_pred.DEPREL
            #Former head becomes pred dependent
            new_pred.head_tok = copula
            new_pred.HEAD = copula.ID
            new_pred.DEPREL = "pred"

        #Switch aux relation
        #auxiliaries = [tok for tok in sent.tokens if tok.DEPREL.startswith("aux")]
        verbs = [tok for tok in sent.tokens 
                 if any(t.DEPREL.startswith("aux") and t.head_tok == tok for t in sent.tokens)]
        for verb in verbs:
            auxiliaries = [tok for tok in sent.tokens 
                           if tok.DEPREL.startswith("aux") and tok.head_tok == verb]
            finite_aux = [tok for tok in auxiliaries if tok.XPOS.endswith("FIN")]
            if finite_aux:
                head_aux = finite_aux[0]
                auxiliaries.remove(head_aux)
            else:
                head_aux = auxiliaries.pop(0)
            #nsubj/nsubj:pass, advmod:neg -> dep of aux
            deps = [tok for tok in sent.tokens 
                    if tok.head_tok == verb 
                       and tok.DEPREL in ["nsubj", "nsubj:pass", "advmod:neg", "conj", "cc", "mark", "case"]]
            for dep in deps:
                dep.head_tok = head_aux
                dep.HEAD = head_aux.ID
            #aux head is head of verb
            head_aux.head_tok = verb.head_tok
            head_aux.HEAD = verb.HEAD
            head_aux.DEPREL = verb.DEPREL
            #Other auxiliaries deps of one another
            for aux in reversed(auxiliaries):
                aux.head_tok = head_aux
                aux.HEAD = head_aux.ID
                aux.DEPREL = "oc"
                head_aux = aux
            #verb dep of aux
            verb.head_tok = head_aux
            verb.HEAD = head_aux.ID
            verb.DEPREL = "oc"
            
        #Switch case relation for preposition  
        prep_heads = [tok for tok in sent.tokens 
                      if any(t.head_tok == tok and t.DEPREL == "case" 
                             and t.XPOS.startswith("AP") for t in sent.tokens)]
        for prep_head in prep_heads:
            preps = [tok for tok in sent.tokens 
                     if tok.head_tok == prep_head and tok.DEPREL == "case" 
                     and tok.XPOS.startswith("AP")]
            circumpreps = [tok for tok in sent.tokens
                           if tok.head_tok == prep_head and tok.DEPREL == "fixed"
                           and tok.XPOS == "APZR"]
            #Define prep_head
            new_head = preps[-1]

            #Make prep head of zircumpreps
            for cp in circumpreps:
                cp.head_tok = new_head
                cp.HEAD = new_head.ID
                cp.DEPREL = "ac"
            #Make prep head of other preps
            for p in preps[:-1]:
                p.head_tok = new_head
                p.HEAD = new_head.ID
                p.DEPREL = "ac"
            #Make prep head of its prior head
            new_head.head_tok = prep_head.head_tok
            new_head.HEAD = prep_head.HEAD
            new_head.DEPREL = prep_head.DEPREL
            prep_head.head_tok = new_head
            prep_head.HEAD = new_head.ID
            prep_head.DEPREL = "nk" 

        #Switch coordination
        conjuncts = [tok for tok in sent.tokens if tok.DEPREL == "conj"]
        for conj in conjuncts:
            conjunctions = [tok for tok in sent.tokens if tok.head_tok == conj and tok.DEPREL == "cc"]
            if not conjunctions:
                continue
            new_head = conjunctions.pop(0)
            for cc in conjunctions:
                cc.head_tok = new_head
                cc.HEAD = new_head.ID
            new_head.head_tok = conj.head_tok
            new_head.HEAD = conj.HEAD
            conj.head_tok = new_head
            conj.HEAD = new_head.ID

        #Switch flat relation
        flat_heads = [tok for tok in sent.tokens 
                      if any(t.head_tok == tok and t.DEPREL == "flat" for t in sent.tokens)]
        for flat_head in flat_heads:
            #Identify new head
            flat_deps = [tok for tok in sent.tokens 
                         if tok.head_tok == flat_head and tok.DEPREL == "flat"]
            new_head = flat_deps[-1]
            #Change head of all deps of previous head
            all_deps = [tok for tok in sent.tokens if tok.head_tok == flat_head and not tok == new_head]
            for dep in all_deps:
                dep.head_tok = new_head
                dep.HEAD = new_head.ID
            #Make last flat dep the new head
            new_head.head_tok = flat_head.head_tok
            new_head.HEAD = flat_head.HEAD
            new_head.DEPREL  = flat_head.DEPREL
            #Make previous head a dep of new head
            flat_head.head_tok = new_head
            flat_head.HEAD = new_head.ID
            flat_head.DEPREL = "flat"

        #for tok in sent.tokens:
        #    print(tok.ID, tok.FORM, tok.DEPREL, tok.HEAD)
        #input()

        return sent

    #####################

    def process(self, doc):

        for sent in doc.sentences:
            sent = self.process_sentence(sent)
        
        return doc

############################

class TreeToBIOProcessor(Processor):
    
    def __init__(self):
        pass

    #########################

    def tree_to_BIO_annotation(self, sentence, treename="tree", annoname="TREE"):
        """
        Turn a tree object into BIO annotations.

        BIO annotations are stored as attribute of the tokens.
        Hierarchical annotations are stacked with pipes.

        Example annotations:
        I-S|I-NF|I-MF|B-LK

        Tokens outside of the tree are annotated with 'O'.

        Input: Sentence object, name of the tree attribute, attribute name of annotations.
        Output: Modified sentence object.
        """

        ##########################

        def get_bio_spans(node):
            """
            Recursively get node tuples.

            Input: Tree object
            Output: List of node tuples (cat, startIndex, endIndex)
            """
            if node.is_terminal():
                return []

            spans = []

            #If node does not contain any token
            #and (therefore) has no start or end, skip it
            if node.get_start_index() == None or node.get_end_index() == None:
                pass
            #Add tuple of this node
            else:
                spans.append((node.cat(), node.get_start_index(), node.get_end_index()))

            #Recursively repeat
            for child in node:
                if not child.is_terminal():
                    spans.extend(get_bio_spans(child))

            return spans

        ##########################
        
        #Create list with empty annotation for all tokens
        bio_annotations = ["" for _ in sentence.tokens]

        bio_spans = []
        
        #Recursively get tuples of cat, start and end
        for node in sentence.__dict__.get(treename, []):
            bio_spans.extend(get_bio_spans(node))
            
        #Add spans to annotation of the respective tokens
        for span in sorted(bio_spans, key=lambda l: (l[1], 0-l[2])):
            
            if bio_annotations[span[1]]:
                bio_annotations[span[1]] += "|" + "B-"+span[0]
            else:
                bio_annotations[span[1]] += "B-"+span[0]
            for i in range(span[1]+1, span[2]+1):
                if bio_annotations[i]:
                    bio_annotations[i] += "|" + "I-"+span[0]
                else:
                    bio_annotations[i] += "I-"+span[0]
        
        #Add O for tokens outside spans
        for t in range(len(bio_annotations)):
            if not bio_annotations[t]:
                bio_annotations[t] = "O"
        
        #Move annotations from list to token attributes
        for tok, bio in zip(sentence.tokens, bio_annotations):
            tok.__dict__[annoname] = bio
        
        return sentence

    #########################

    def process_sentence(self, sent):

        sent = self.tree_to_BIO_annotation(sent)

        return sent

    #########################

    def process(self, doc):
        
        for sent in doc.sentences:
            sent = self.process_sentence(sent)

        return doc