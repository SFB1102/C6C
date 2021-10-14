# C6C

C6C is built to convert different historical Corpora from various input formats to common, standardized output format(s). It also allows for custom processing of the input data, e.g., to map historical POS tagsets to the modern standard tagset.

## General Structure

The pipeline takes one or more files in a given input format and imports them into document objects. These document can then be modified by one or more processors, before exporting them into the same or another export format.

![Pipeline structure](/doc/pipeline.svg)
## Usage

### Requirements

- Python 3
- [click package](https://pypi.org/project/click/)([Documentation](https://click.palletsprojects.com/))

### Command line usage

The pipeline is called via the command line:

> py C6C.py convert -i input_format -o output_format -p "['processor_name', 'processor_name']" input_dir_or_file output_dir_or_file

- `input_dir_or_file`: can be a single file or a folder
- `output_dir_or_file`: can be a single file or a folder
- `input_format`: the following input formats are currently supported ([documentation](#importers) see below): `text`, `tcfDTA`, `xmlDTA`, `tiger`, `tigerxml`, `mercuriustigerxml`, `conlluplus`, `conllu`, `conll2000`, `DTAtsv`, `tuebadz`, `annisgrid`, `webannotopf`, `webannotsv`, `coraxmlrem`, `coraxmlrefbo`, `coraxmlanselm`, `tuebadsconll`, `tuebatrees`, `ddbtigernegra`, `fuerstinnenexb`, `refup`, `germanc`, `sdewac` 
- `output_format`: the following output formats are currently supported ([documentation](#exporters) see below): `conlluplus`, `conllu`, `DTAtsv`, `HIPKONtsv`, `text`, `pos`, `conll2000`, `ptb`
- `processor_name`: processors are called in the given order; the following processors are currently implemented ([documentation](#processors) see below): `dtachopper`, `dtasimplifier`, `hipkontostts`, `addmissingstts`, `topfsimplifier`, `satzklammertotopf`, `tsvindexer`, `hitstostts`,  `tuebadstopf`, `anselmtostts`, `topfchopper`, `conllindexer`, `refhitstostts`,  `depmanipulator`, `depprocessor`, `mercuriustostts`, `refuptostts`, `fuerstinnentostts`, `virgelmapper`, `pronominaladverb`, `refupcoding`, `bracketremover`

## Importers

1. [CoNLLUPlusImporter](#conlluplusimporter)
2. [CoNLLUImporter](#conlluimporter)
3. [CoNLL2000Importer](#conll2000importer)
4. [TigerImporter](#tigerimporter)
5. [TigerXMLImporter](#tigerxmlimporter)
6. [TuebaDzImporter](#tuebadzimporter)
7. [TUEBADSConllImporter](#tuebadsconllimporter)
8. [TuebaDZPTBImporter](#tuebadzptbimporter)
9. [ANNISGridSentenceImporter](#annisgridsentenceimporter)
10. [WebAnnoTopFImporter](#webannotopfimporter)
11. [WebAnnoTSVImporter](#webannotsvimporter)
12. [CoraXMLReMImporter](#coraxmlremimporter)
13. [CoraXMLAnselmImporter](#coraxmlanselmimporter)
14. [CoraXMLReFBoImporter](#coraxmlrefboimporter)
15. [TextImporter](#textimporter)
16. [XMLKaJuKImporter](#xmlkajukimporter)
17. [MercuriusTigerXMLImporter](#mercuriustigerxmlimporter)
18. [ReFUPImporter](#refupimporter)
19. [XMLFnhdCImporter](#xmlfnhdcimporter)
20. [GerManCCoNLLImporter](#germancconllimporter)
21. [DDBTigerNegraImporter](#ddbtigernegraimporter)
22. [FuerstinnenEXBImporter](#fuerstinnenexbimporter)
23. [SDeWaCIteratorImporter](#sdewaciteratorimporter)

### CoNLLUPlusImporter

- Name for usage in command line: `conlluplus`

#### Input Format

- [CoNLL-U Plus Format](https://universaldependencies.org/ext-format.html)
- Lines containing the annotations of a word (seperated by tabs), blank lines marking sentence boundaries.
- Comment lines starting with hash (#).
- First line is a comment line listing the column names.
- Field contains an underscore if info is not available for the current word.

#### Meta-Info

- No meta-info available in this format.

#### Annotations

- Can contain any subset of the following annotations plus additional annotations.

column name | annotation
------ | ------
ID | word index
FORM | word form
LEMMA | Lemma
UPOS | Universal POS-Tag
XPOS | STTS-Tag
FEATS | morphological features
HEAD | head
DEPREL | dependency relation to the head
DEPS | dependency graph
MISC | other annotation  

### CoNLLUImporter

- Name for usage in command line: `conllu`

#### Input Format

- [CoNLL-U Format](https://universaldependencies.org/format.html)
- Lines containing the annotations of a word (seperated by tabs), blank lines marking sentence boundaries
- 10 columns containing the following annotations for each word:  
	ID (word index), FORM (word form), LEMMA (Lemma), UPOS (universal POS-tag), XPOS (language specific POS-tag),
	FEATS (Morphological features), HEAD (head), DEPREL (dependency relation to the head), DEPS (dependency graph),
	MISC (other annotation)
- Field contains an underscore if info is not available for the current word

#### Input Data

- e.g. RIDGES Corpus ([RIDGES Herbology Version 8.0](https://www.laudatio-repository.org/browse/corpus/EyR8CnMB7CArCQ9CsY6Y/corpora))

#### Meta-Info

- No meta-info available in this format.

#### Annotations

column name | annotation
------ | ------
ID | word index
FORM | word form
LEMMA | Lemma
UPOS | Universal POS-Tag
XPOS | STTS-Tag
FEATS | morphological features
HEAD | head
DEPREL | dependency relation to the head
DEPS | dependency graph
MISC | other annotation  

#### Additional Info

- Only for RIDGES Corpus: annotations in three columns of the CoNLL-U format (normally corresponding to UPOS, DEPS, MISC) weren't extracted because they contained the same information as the columns XPOS, HEAD, DEPREL

### CoNLL2000Importer

- Name for usage in command line: `conll2000`

#### Input Format

- [CoNLL-2000](https://www.clips.uantwerpen.be/conll2000/chunking/)
- Lines containing the annotations of a word (seperated by whitespaces), blank lines marking sentence boundaries.
- 3 columns containing the following annotations for each word:  
	FORM (word form), XPOS (language specific POS-tag), CHUNK (syntactically correlated parts of words)
- Field contains an underscore if info is not available for the current word.

#### Input Data

- e.g. Data for the [CoNLL-2000 shared task](https://www.clips.uantwerpen.be/conll2000/chunking/)

#### Meta-Info

- No meta-info available in this format.

#### Annotations

column name | annotation
------ | ------
FORM | word form
XPOS | language specific POS-tag
CHUNK | syntactically correlated parts of words  

### TigerImporter

- Name for usage in command line: `tiger`

#### Input Format

- [CoNLL-2009](https://ufal.mff.cuni.cz/conll2009-st/task-description.html)
- Lines containing the annotations of a word (seperated by tabs), blank lines marking sentence boundaries
- 15 columns containing the following annotations for each word:  
	ID (word index), FORM (word form), LEMMA (Lemma), PLEMMA (automatically predicted Lemma), POS (language specific POS-tag),
	PPOS (automatically predicted POS-tag), FEAT (Morphological features), PFEAT (automatically predicted features), HEAD (head),
	PHEAD (automatically predicted head), DEPREL (dependency relation to the head), PDEPREL (automatically predicted dependency relation),
	FILLPRED (contains `Y` if PRED should be filled), PRED (predicate), APREDs (additional predicates)
- Field contains an underscore if info is not available for the current word

#### Input Data

- [Tiger Corpus Release 2.2](https://www.ims.uni-stuttgart.de/forschung/ressourcen/korpora/tiger/)
- All Documents are stored in the file `tiger_release_aug07.corrected.16012013.conll09`

#### Meta-Info

- TSV-Files containing the meta-info for all documents are stored in the directory `TIGER2.2.doc.zip\TIGER2.2.doc`
- Following meta-infos are extracted into a seperate file:  
  filename, author, gender (of the author), folder (train/dev/test), category of note (collection/other), note (type/heading of collection doc/description)
- Following meta-infos are extracted into the output file:  
  sentence ID in Tiger, sentence type

#### Annotations

column name | annotation
------ | ------
ID | word index
FORM | word form
LEMMA | Lemma
UPOS | Universal POS-Tag
XPOS | STTS-Tag
FEATS | morphological features
HEAD | head
DEPREL | dependency relation to the head
DEPS | dependency graph
MISC | other annotation  

### TigerXMLImporter

- Name for usage in command line: `tigerxml`

#### Input Format

- [TIGER-XML Format](https://www.ims.uni-stuttgart.de/documents/ressourcen/werkzeuge/tigersearch/doc/html/TigerXML.html)
- The `<head>` node contains meta-information and information about the annotations.
- The `<body>` node contains the individual sentences with their syntax-graphs.
- Each graph consists of `<terminals>`, which contain the words and the corresponding annotations, and `<nonterminals>`,
	which contain the structure of the syntax-tree including the corresponding edge and node labels.

#### Input Data

- [TIGER Corpus](https://www.ims.uni-stuttgart.de/forschung/ressourcen/korpora/tiger/)

#### Meta-Info

- Not available in this format.

#### Annotations

column name | annotation
------ | ------
ID | word index
FORM | word form
LEMMA | Lemma
XPOS | STTS-Tag
FEATS | morphological features
TigerID | word index in the Tiger-files  

### TuebaDzImporter

- Name for usage in command line: `tuebadz`

#### Input Format

- [CoNLL-U Format](https://universaldependencies.org/format.html)
- Lines containing the annotations of a word (seperated by tabs), blank lines marking sentence boundaries
- 10 columns containing the following annotations for each word:  
	ID (word index), FORM (word form), LEMMA (Lemma), UPOS (universal POS-tag), XPOS (language specific POS-tag),
	FEATS (Morphological features), HEAD (head), DEPREL (dependency relation to the head), DEPS (dependency graph),
	MISC (other annotation)
- Field contains an underscore if info is not available for the current word

#### Input Data

- [TüBa-D/Z Release 11.0](https://uni-tuebingen.de/fakultaeten/philosophische-fakultaet/fachbereiche/neuphilologie/seminar-fuer-sprachwissenschaft/arbeitsbereiche/allg-sprachwissenschaft-computerlinguistik/ressourcen/corpora/tueba-dz/)
- All Documents are stored in the file `tuebadz-11.0-conll-u-v2.txt`

#### Meta-Info

- Following meta-infos are extracted into the output file:  
  document ID in TüBa, sentence ID in TüBa
  
#### Annotations

column name | annotation
------ | ------
ID | word index
FORM | word form
LEMMA | Lemma
UPOS | Universal POS-Tag
XPOS | STTS-Tag
FEATS | morphological features from the universal feature inventory
HEAD | head
DEPREL | dependency relation to the head
DEPS | dependency graph
MISC | SpaceAfter
Morph | morphological features from the source TüBa-D/Z data
NE | named entity type
TopoField | topological field
Typo | typo correction
WSD | GermaNet ID of the word sense  

#### Additional Info

- We divided the documents up into a training, development and test set (80-10-10) via random choice.

### TUEBADSConllImporter

- Name for usage in command line: `tuebadsconll`

#### Input Format

- CoNLL Format
- Lines containing the annotations of a word (seperated by tabs), blank lines marking sentence boundaries
- 5 columns containing the following annotations for each word:  
	ID (word index), FORM (word form), XPOS (language specific POS-tag), POS:HD (head), SYNTAX (syntactical information)
- Field contains an underscore if info is not available for the current word

#### Input Data

- Tübingen Treebank of Spoken German (TüBa-D/S)

#### Meta-Info

- Not available in this format.
  
#### Annotations

column name | annotation
------ | ------
ID | word index
FORM | word form
XPOS | STTS-Tag
POS:HD | head
SYNTAX | syntactical information  

#### Additional Info

- The Processor `TUEBADSTopFExtractor` can be used to extract the topological field information out of the SYNTAX column.

### TuebaDZPTBImporter

- Name for usage in command line: `tuebatrees`

#### Input Format

- Penn Treebank Format
- Each line contains one sentence in a syntactic bracketing style

#### Input Data

- [TüBa-D/Z Release 11.0](https://uni-tuebingen.de/fakultaeten/philosophische-fakultaet/fachbereiche/neuphilologie/seminar-fuer-sprachwissenschaft/arbeitsbereiche/allg-sprachwissenschaft-computerlinguistik/ressourcen/corpora/tueba-dz/)

#### Meta-Info

- Following meta-info is extracted into the output file:
	syntax-tree string
  
#### Annotations

column name | annotation
------ | ------
ID | word index
FORM | word form
XPOS | STTS-Tag
PTBLabel | Penn Treebank Label  

### ANNISGridSentenceImporter

- Name for usage in command line: `annisgrid`

#### Input Format

- Grid-Format from the [GridExporter](http://korpling.github.io/ANNIS/3.6/user-guide/aql-export.html) of ANNIS
- Each entry contains one sentence, blank lines mark sentence boundaries
- Each line consists of an annotation layer and the corresponding annotations, in which
	the span of tokens covered by each annotation is given in square brackets
- Lines containing metadata are marked with `meta::`

#### Input Data

- e.g. HIPKON ([Historisches Predigtenkorpus zum Nachfeld, Version 1.0](https://www.laudatio-repository.org/browse/corpus/yiTKCnMB7CArCQ9CxLhJ/corpora))

#### Meta-Info

- Following meta-infos are extracted into a seperate file:  
  filename, selection, edition, Überlieferungsträger (transmitter of the tradition), language stage, corpus part
- Following meta-infos are extracted into the output file:  
  sentence ID in Grid
  
#### Annotations

column name | annotation
------ | ------
ID | word index
FORM | word form
XPOS | STTS-Tag
CAT | category of a phrase (nominal, verbal etc.)
CLEAN | normalized word form
EDITION | page and line number of the corresponding edition
FOKUS | focus type
GF | grammatical function
IS | information status
Kommentar | remark
POS | POS-Tag
Rekonstruktion | reconstructed word
SATZKLAMMER | left or right sentence bracket
SATZSTATUS | sentence status
Sprache | remark about the language
UEBERLIEFERUNGSTRAEGER | information about the transmission
VERLINKUNG | linking
WIEDERAUFNAHME | coreference   

#### Additional Info

- The Processors `HIPKONtoSTTSMapper` and `addmissingSTTStoHIPKON` can be used to match the POS-tags of HIPKON to the corresponding STTS-tags.

### WebAnnoTopFImporter

- Name for usage in command line: `webannotopf`

#### Input Format

- [WebAnno TSV 3.2](https://webanno.github.io/webanno/releases/3.4.5/docs/user-guide.html#sect_webannotsv)
- Lines containing the annotations of a word (seperated by tabs), blank lines marking sentence boundaries.
- Comment lines starting with hash (#).
- Field contains an underscore if info is not available for the current word.

#### Input Data



#### Meta-Info

- Following meta-info is extracted into the output file:
	sent_id(TSV)
  
#### Annotations

- Can contain a subset of the following annotations:

column name | annotation
------ | ------
TSVID | sentence and word index
CharOffset | character offset
FORM | word form
LEMMA | Lemma
POS | POS-tag
XPOS | STTS-Tag
CHUNK | syntactically correlated parts of words
TopF | Topological Field
HEAD | head
DEPREL | dependency relation to the head
DepFlavor | dependency annotation
animacy | morphological feature
aspect | morphological feature
case | morphological feature
definiteness | morphological feature
degree | morphological feature
gender | morphological feature
mood | morphological feature
negative | morphological feature
numType | morphological feature
number | morphological feature
person | morphological feature
possessive | morphological feature
pronType | morphological feature
reflex | morphological feature
tense | morphological feature
transitivity | morphological feature
FEATS | morphological features
verbForm | morphological feature
voice | morphological feature  

### WebAnnoTSVImporter

- Name for usage in command line: `webannotsv`

#### Input Format

- [WebAnno TSV 3.2](https://webanno.github.io/webanno/releases/3.4.5/docs/user-guide.html#sect_webannotsv)
- Lines containing the annotations of a word (seperated by tabs), blank lines marking sentence boundaries.
- Comment lines starting with hash (#).
- Field contains an underscore if info is not available for the current word.

#### Input Data



#### Meta-Info

- Following meta-info is extracted into the output file:
	sent_id(TSV)
  
#### Annotations

- Can contain the following annotations plus additional ones.

column name | annotation
------ | ------
TSVID | sentence and word index
CharOffset | character offset
FORM | word form
LEMMA | Lemma
XPOS | STTS-Tag  

### CoraXMLReMImporter

- Name for usage in command line: `coraxmlrem`

#### Input Format

- [CorA-XML Format](https://cora.readthedocs.io/en/latest/coraxml/)
- Each document may contain the following elements:  
	`<cora-header>`, `<header>`, `<layoutinfo>`, `<shifttags>` and an ordered list of `<token>` and `<comment>` elements
- Each `<token>` element may contain diplomatic (`<tok_dipl>`) and modernized (`<tok_anno>`) tokens which could contain further annotations
- Sentence boundaries are realized different: In this corpus there is a sentence bound if the punc-annotation is one of "DE", "IE", "EE", "QE" and
	if the punc-annotation is "$E", the current token also belongs to the sentence before

#### Input Data

- [Referenzkorpus Mittelhochdeutsch](https://www.linguistics.rub.de/rem/access/index.html#)

#### Meta-Info

- Meta Information is included in the `<header>` element of each XML-file.
- Following of these meta-infos are extracted into a seperate file:  
	filename, text, abbr_ddd (abbreviation of the text in ReM), abbr_mwb (abbreviation of the text in the dictionary of Middle High German),
	topic, text-type, genre (P = Prose, U = Urkunde (certificate), V = Verse), reference, reference-secondary, library, library-shelfmark,
	online (link to online database), medium, extent, extract, language, language-type, language-region, language-area, place, time, notes-manuscript,
	date, text-place, text-author, text-language (language of the author), text-source, edition, notes-transcription, notes-annotation

#### Annotations

column name | annotation
------ | ------
ID | word index
FORM | word form (utf-form of tok_anno)
LEMMA | Lemma
XPOS | STTS-Tag
ANNO_ASCII | ascii-form of tok_anno
ANNO_ID | word index of tok_anno
ANNO_TRANS | trans-form of tok_anno
DIPL | utf-form of tok_dipl
DIPL_ID | word index of tok_dipl
DIPL_TRANS | trans-form of tok_dipl
INFL | morphological information
INFLCLASS | specific inflection class
INFLCLASS_GEN | general inflection class
LEMMA_GEN | general Lemma
LEMMA_IDMWB | Lemma index in the dictionary of Middle High German
LOC | location
NORM | normalized word form
POS | word-specific HiTS-Tag
POS_GEN | lemma-specific HiTS-Tag
PUNC | Tag marking a sentence or segment boundary
SHIFTTAG | Tag marking that a range of token has certain attributes (e.g. "quote")
TOKEN | trans-form of token-element
TOKEN_TYPE | Tag marking the type of difference (if there is one) between the diplomatic and modern token
TOK_ID | word index of token-element  

#### Additional Info

- The Processor `HiTStoSTTSMapper` can be used to match the HiTS-tags of ReM to the corresponding STTS-tags.


### CoraXMLAnselmImporter

- Name for usage in command line: `coraxmlanselm`

#### Input Format

- [CorA-XML Format](https://cora.readthedocs.io/en/latest/coraxml/)
- Each document may contain the following elements:  
	`<cora-header>`, `<header>`, `<layoutinfo>`, `<shifttags>` and an ordered list of `<token>` and `<comment>` elements
- Each `<token>` element may contain diplomatic (`<tok_dipl>`) and modernized (`<tok_anno>`) tokens which could contain further annotations
- Sentence boundaries are realized different: In this corpus there is always a sentence bound if the pos-annotation is "$."

#### Input Data

- [Anselm-Korpus](https://www.linguistics.rub.de/anselm/access/index.html)

#### Meta-Info

- Meta Information is included in the `<header>` element of each XML-file.
- Following of these meta-infos are extracted into a seperate file:  
	filename, Sigle (abbreviation), Aufbewahrungsort (place to keep), shelf mark, printed work, handwritten or printed, prose or verse,
	date, language, language type, language area, number of token, label, URL-facsimile

#### Annotations

column name | annotation
------ | ------
ID | word index
FORM | word form (utf-form of tok_anno)
LEMMA | Lemma
XPOS | STTS-Tag
ANNO_ASCII | ascii-form of tok_anno
ANNO_ID | word index of tok_anno
ANNO_TRANS | trans-form of tok_anno
DIPL | utf-form of tok_dipl
DIPL_ID | word index of tok_dipl
DIPL_TRANS | trans-form of tok_dipl
MORPH | morphological information
NORM | normalized word form
NORM_BROAD | modern equivalent of the word form
NORM_TYPE | type of adjustment between normalized and modern word form
POS | POS-Tag (slightly modified version of the STTS)
SHIFTTAG | Tag marking that a range of token has certain attributes (e.g. "quote")
TOKEN | trans-form of token-element
TOKEN_TYPE | Tag marking the type of difference (if there is one) between the diplomatic and modern token
TOK_ID | word index of token-element  

#### Additional Info

- The Processor `ANSELMtoSTTSMapper` can be used to match the POS-tags of Anselm to the corresponding STTS-tags.

### CoraXMLReFBoImporter

- Name for usage in command line: `coraxmlrefbo`

#### Input Format

- [CorA-XML Format](https://cora.readthedocs.io/en/latest/coraxml/)
- Each document may contain the following elements:  
	`<cora-header>`, `<header>`, `<layoutinfo>`, `<shifttags>` and an ordered list of `<token>` and `<comment>` elements
- Each `<token>` element may contain diplomatic (`<tok_dipl>`) and modernized (`<tok_anno>`) tokens which could contain further annotations
- Sentence boundaries are realized different: In this corpus there is always a sentence bound if there is a boundary- or a punc-annotation which contains "(.)"

#### Input Data

- [Referenzkorpus Frühneuhochdeutsch](https://www.ruhr-uni-bochum.de/wegera/ref/index.htm)

#### Meta-Info

- Meta Information is included in the `<header>` element of each XML-file.
- Following of these meta-infos are extracted into a seperate file:  
	filename, language area, language region, language type, genre, medium, time, reference, corpus-sigle, text, author, text type, assignment quality, hoffmann_wetter_nr,
	library, library-shelfmark, date, place, printer, edition, literature, size, language, notes-transcription, abbr_ddd (text abbreviation), extent, extent-size


#### Annotations

column name | annotation
------ | ------
ID | word index
FORM | word form (utf-form of tok_anno)
LEMMA | Lemma
XPOS | STTS-Tag
ANNO_ASCII | ascii-form of tok_anno
ANNO_ID | word index of tok_anno
ANNO_TRANS | trans-form of tok_anno
ANNO_TYPE | type of annotation (manually or automatically)
BOUNDARY | type of punctuation
DIPL | utf-form of tok_dipl
DIPL_ID | word index of tok_dipl
DIPL_TRANS | trans-form of tok_dipl
LEMMA_ID | Lemma index in the dictionary of Middle High German
LEMMA_URL | Link to the entry in the dictionary of Middle High German
LEMMA_VERIFIED | annotation is y (yes) or n (no)
MORPH | morphological information
POS | word-specific HiTS-Tag
POS_LEMMA | lemma-specific HiTS-Tag
PUNC | type of punctuation (if not in BOUNDARY-column)
SHIFTTAG | Tag marking that a range of token has certain attributes (e.g. "quote")
TOKEN | trans-form of token-element
TOKEN_TYPE | Tag marking the type of difference (if there is one) between the diplomatic and modern token
TOK_ID | word index of token-element  

#### Additional Info

- The Processor `ReFHiTStoSTTSMapper` can be used to match the POS-tags of ReF.BO to the corresponding STTS-tags.


### TextImporter

- Name for usage in command line: `text`

#### Input Format

- One word per line, blank lines marking sentence boundaries.

#### Meta-Info

- No meta-info available in this format.

#### Annotations

- Except of the word form there are no annotations available in this format.


### XMLKaJuKImporter

- Name for usage in command line: `xmlkajuk`

#### Input Format

- XML-Format
- Sentences consist of one or more `<lb>` nodes which contain annotated parts of the sentence
- One of these parts can have up to three annotation levels which possibly have further attributes
- Second annotations are put into square brackets (for example used at clitics)
- For further information refer to [KaJuK Documentation](https://www.uni-giessen.de/fbz/fb05/germanistik/absprache/sprachtheorie/kajuk)

#### Input Data

- [Kasseler Junktionskorpus, Version 1.1](https://www.laudatio-repository.org/browse/corpus/nCQsCnMB7CArCQ9CDmun/corpora)
- XML-Files are stored in the directory `KaJuK.zip/kasseler-junktionskorpus/XML`

#### Meta-Info

- XML-Files containing the meta-info for each document are stored in `KaJuK.zip/kasseler-junktionskorpus/TEI-HEADERS/document`
- Following of these meta-infos are extracted into a seperate file:  
	filename, file_id, style, author, editor, title, number of tokens, publisher, place, year, series, language code, language

#### Annotations

column name | annotation
------ | ------
ID | word index
FORM | word form
ADDIR | additional content relation
ADDtype | additional type
Ebene1 | tag at hierarchical level 1 (if there is another `<lb>` node under the current `lb` node the tag here is `lb_1` or `lb_2`, according to the current `lb` level)
Ebene2 | tag at hierarchical level 2
Ebene3 | tag at hierarchical level 3
Ebene4 | tag at hierarchical level 4 (can only exist if the first level has tag `lb`)
IR | content relation (causal, temporal etc.)
Ident | identity of a verb (finite, infinite etc.)
change | change of an ellipsis
dir | direction of an ellipsis
lb_ADDIR | additional content relation of the current `<lb>` node
lb_EB | level of the current `<lb>` node
lb_IR | content relation of the current `<lb>` node
lb_n | number of the current `<lb>` node (for expressing the relations between different `<lb>` nodes)
lb_type | type of the current `<lb>` node
line | line number
norm | normalised spelling
page | page number
real | realisation of a word/phrase
type | type of a word/phrase

#### Additional Info

- Manual changes of the input files (because of mistakes in the xml-format) are documented in the file `Korrektur.txt`
- In the text of the output file, parts of the sentence that are annotated as ellipsis are put into square brackets

### MercuriusTigerXMLImporter

- Name for usage in command line: `mercuriustigerxml`

#### Input Format

- XML-Tiger/Negra-Format
	  - The `<head>` node contains meta-information and information about the annotations.
	  - The `<body>` node contains the individual sentences with their syntax-graphs.
	  - Each graph consists of `<terminals>`, which contain the words and the corresponding annotations, and `<nonterminals>`,
		which contain the structure of the syntax-tree including the corresponding edge and node labels.

#### Input Data

- [Mercurius-Baumbank, Version 1.1](https://www.laudatio-repository.org/browse/corpus/VyQiCnMB7CArCQ9CjF3O/corpora)

#### Meta-Info

- Not available.

#### Annotations

column name | annotation
------ | ------
ID | word index
FORM | word form
XPOS | STTS-Tag
FEATS | morphological features
POS | POS-Tag from Mercurius
TigerID | word index in the Tiger/Negra-files  

#### Additional Info

- The Processor `MercuriusToSTTSMapper` can be used to match the POS-tags of Mercurius to the corresponding STTS-tags.

### ReFUPImporter

- Name for usage in command line: `refup`

#### Input Format

- XML-Tiger/Negra-Format
	  - The `<head>` node contains meta-information and information about the annotations.
	  - The `<body>` node contains the individual sentences with their syntax-graphs.
	  - Each graph consists of `<terminals>`, which contain the words and the corresponding annotations, and `<nonterminals>`,
		which contain the structure of the syntax-tree including the corresponding edge and node labels.

#### Input Data

- [Referenzkorpus Frühneuhochdeutsch](https://www.ruhr-uni-bochum.de/wegera/ref/index.htm)

#### Meta-Info

- Not available.

#### Annotations

column name | annotation
------ | ------
ID | word index
FORM | word form
XPOS | STTS-Tag
FEATS | morphological features
POS | POS-Tag from ReFUP
TigerID | word index in the Tiger/Negra-files  

#### Additional Info

- The Processor `ReFUPToSTTSMapper` can be used to match the POS-tags of ReFUP to the corresponding STTS-tags.
- The Processor `ReFUPCoding` can be used to have the correct coding of 'ß' in the output file.

### XMLFnhdCImporter

- Name for usage in command line: `xmlfnhdc`

#### Input Format

- XML-Format
- The `<bibliographie>` node contains meta-information
- The nodes `<seite>` and `<zeile>` contain the wordforms and their annotations
- For further information refer to the XML-schemata files (e.g. `Fnhd.rnc`) or the [Online-Documentation](https://korpora.zim.uni-duisburg-essen.de/FnhdC/Dokumentation.html)

#### Input Data

- [Bonner Frühneuhochdeutschkorpus](https://korpora.zim.uni-duisburg-essen.de/FnhdC/Download) (XML-Version 2017)

#### Meta-Info

- Following meta-infos are extracted into a seperate file:  
  filename, textname, textnumber, specification number, author, text, title, editor, place of publication,
  year of publication, number of pages, included pages, language area, place, year, text type, URL
  
#### Annotations

column name | annotation
------ | ------
ID | word index
FORM | word form given under the annotation `gelesen` (if not available, word form under the annotation `gefunden` is taken)
lemma | Lemma
Anmerkungen | annotation is `Name` if the word belongs to a name
Layout | layout information (title, quotation etc.)
Seite_col | page column
Seite_lage | page location
Seite_lf_nr | page number 
Seite_nr | original page number
Seite_position | page position (recto/verso)
Seite_teil | text part on this page
Seite_typ | page type (sheet/chapter/page)
Zeile_lf_nr | continuous line number
Zeile_nr | original line number
adj_links | word form on the left side of an adjective
adj_rechts | word form on the right side of an adjective
adj_rolle | adjective role
adverbial | marking if an adjective is used adverbial
anno_nr | annotation number
fern_teile | number of seperated parts
flexiv | flexes of an adjective
fremdwort | marking if the word form is a foreign word
gefunden | word form where the morphemes are connected via `#`
genus | gender
kasus | case of a noun or adjective
klasse | inflection class of a verb
komparation | comparison morpheme
komparationsstufe | degree of comparison (superlative etc.)
leer | marking if a word form has no morphological annotations
lemma | Lemma
link_lemma | Lemma for searching in the "Wörterbuchnetz" (a digital dictionary network)
modus | mood of a verb
morph | single morphemes of a word form, seperated by whitspaces (only if the morphemes in the original text are not written in one word)
numerus | number (singular/plural)
person | person
praefixe | prefix blocks (`![a,b]` means that there is an isolated prefix block that contains the prefixes a and b; `~[c,d]` means there is an non-isolated prefix block that contains the prefixes c and d)
suffix | suffix of the word form
tempus | tense
typ | word form type (noun, verb etc.)
verb_form | form of a verb (infinitive, participle etc.)
vokal | stresed vowel
wf_nr | word form number  

### GerManCCoNLLImporter

- Name for usage in command line: `germanc`

#### Input Format

- [CoNLL-U Format](https://universaldependencies.org/format.html)
- Lines containing the annotations of a word (seperated by tabs), blank lines marking sentence boundaries
- 10 columns containing the following annotations for each word (the columns here differ slightly from the original CoNLL-U format):  
	ID (word index), FORM (word form), NORM (normalized word form), POS (POS-tag), LEMMA (Lemma), FEATS (Morphological features),
	HEAD (head), DEPREL (dependency relation to the head), DEPS (dependency graph), MISC (other annotation)
- Field contains an underscore if info is not available for the current word
- For further information refer to the [GerManC documentation](https://www1.ids-mannheim.de/fileadmin/lexik/uwv/dateien/GerManC_Documentation.pdf)

#### Input Data

- [GerManC, Version 1.0](https://www.laudatio-repository.org/browse/corpus/9SX7DnMB7CArCQ9CBB_J/corpora)

#### Meta-Info

- XML-Files containing the meta-info for each document are stored in `germanc.zip/germanc-v1.0TEI-HEADERS/document`
- Following of these meta-infos are extracted into a seperate file:  
	filename, style, author, title, number of words, place and year of publication, scope of bibliographic reference,
	source, reference, language, language code, language type

#### Annotations

column name | annotation
------ | ------
ID | word index
FORM | word form
LEMMA | Lemma
UPOS | Universal POS-Tag
XPOS | STTS-Tag
FEATS | morphological features
HEAD | head
DEPREL | dependency relation to the head
DEPS | dependency graph
MISC | other annotation
NORM | normalized word form
POS | POS-Tag from GerManC  

#### Additional Info

- Several documents contain only 8 columns (ID, FORM, NORM, POS, LEMMA, FEATS, DEPREL, HEAD) instead of 10.
- In some documents the columns HEAD/DEPREL/FORM or NORM/LEMMA are swapped.
- Sometimes there is a single line containing a bracket `)` as word form, without any other annotations.
	In this cases the bracket will be attached to the preceding sentence.

### DDBTigerNegraImporter

- Name for usage in command line: `ddbtigernegra`

#### Input Format

Two different formats:

- XML-Tiger/Negra-Format
	  - The `<head>` node contains meta-information and information about the annotations.
	  - The `<body>` node contains the individual sentences with their syntax-graphs.
	  - Each graph consists of `<terminals>`, which contain the words and the corresponding annotations, and `<nonterminals>`,
		which contain the structure of the syntax-tree including the corresponding edge and node labels.

- EXMARaLDA-Format
	  - The `<head>` node contains meta-information about the file.
	  - The `<basic-body>` consists of a `<common-timeline>` and the `<tier>` nodes, where each node contains the words or one annotation category.
	  - Each word and each annotation belong to one or more timeline-IDs, so one can match the words to their corresponding annotations with this IDs. 

#### Input Data

- [Deutsche Diachrone Baumbank, Version 1.0](https://www.laudatio-repository.org/browse/corpus/bSQeC3MB7CArCQ9Cw8yZ/corpora)

#### Meta-Info

- XML-Files containing the meta-info for each document are stored in `deutsche-diachrone-baumbank.zip/deutsche-diachrone-baumbank-v1.0TEI-HEADERS/document`
- Following of these meta-infos are extracted into a seperate file:  
	filename, style, title, author, number of tokens, publisher, place and year of publication, scope of bibliographic reference,
	original year/place/title, source, reference, language, language code, language type, language area
- Following meta-infos are extracted into the output file (only for files in Tiger/Negra-Format):  
  sentence ID in the Tiger/Negra-files, syntax-tree string

#### Annotations

Annotations of files in XML-Tiger/Negra-Format:

column name | annotation
------ | ------
ID | word index
FORM | word form
XPOS | STTS-Tag
FEATS | morphological features
POS | POS-Tag from DDB
TigerID | word index in the Tiger/Negra-files  

Annotations of files in the other XML-Format:

column name | annotation
------ | ------
ID | word index
FORM | word form
XPOS | STTS-Tag
FEATS | morphological features
ASPECT | aspect
CAT | corresponding syntactical sentence part
CONTEXT | context
POS | POS-Tag from DDB
TENSE | tense
TimelineID | corresponding index in the timeline
VOICE | voice  

#### Additional Info

- Not all files of the corpus are avilable in the XML-Tiger/Negra-Format; only the files in the folder with Old High German texts have this format,
	while the other texts (Middle High German and Early New High German) have a different format (as discribed under "Input Format").
- Since the POS-tags from DDB partly are uncomplete or do not contain the right STTS-tag (especially for punctuation marks),
	the tags are corrected in the Importer and the right STTS-tags are saved in the XPOS-column.

### FuerstinnenEXBImporter

- Name for usage in command line: `fuerstinnenexb`

#### Input Format

- EXMARaLDA-Format
- The `<head>` node contains meta-information about the file.
- The `<basic-body>` consists of a `<common-timeline>` and the `<tier>` nodes, where each node contains the words or one annotation category.
- Each word and each annotation belong to one or more timeline-IDs, so one can match the words to their corresponding annotations with this IDs. 

#### Input Data

- [Fuerstinnenkorrespondenz, Version 1.1](https://www.laudatio-repository.org/browse/corpus/ZCSVC3MB7CArCQ9CVedt/corpora)
- For further information refer to the [Documentation](http://dwee.eu/Rosemarie_Luehr/?Projekte___DFG-Projekte___Fruehneuzeitliche_Fuerstinnenkorrespondenz_im_mitteldeutschen_Raum)

#### Meta-Info

- XML-Files containing the meta-info for each document are stored in `fuerstinnenkorrespondenz.zip/fuerstinnenkorrespondenz-v1.1TEI-HEADERS/document`
- Following of these meta-infos are extracted into a seperate file:  
	filename, style, title, author, addressee, number of tokens, place, date, scope of bibliographic reference,
	manuscript name, language, language code, language type, language area, comment

#### Annotations

column name | annotation
------ | ------
ID | word index
FORM | word form
LEMMA | Lemma
XPOS | STTS-Tag
FEATS | morphological features
CLAUSE-ST | clause-status
COMMENT | explanation of the features that are tagged under LEX_GR
COMPLEX | sentence complexity
FORMAL | formal features
GRAPH | graphematic features
GRFUNCT | grammatical function
LEX_GR | lexical or grammatical features
MANU | marking if text is from foreign hand
MEAN | meaning of certain lemmata
MOD_POLITE | tagging signals of modesty and politeness
NORM | normalized word form
ORIG | original writing
PHON | phonological features
PHRAS | phrasing categories of the letter
POS | POS-tags from the Fuerstinnnen-Corpus
QUOT | biblical quotations or proverbial expressions
S_GRFUNCT | grammatical function of subclauses
TimelineID | corresponding index in the timeline  

#### Additional Info

- The Processor `FuerstinnentoSTTSMapper` can be used to match the POS-tags of the 'Fuerstinnenkorrespondez' to the corresponding STTS-tags.

### SDeWaCIteratorImporter

- Name for usage in command line: `sdewac`

#### Input Format

- Lines containing the annotations of a word (seperated by tabs), blank lines marking sentence boundaries
- Field contains an underscore if info is not available for the current word

#### Input Data

- [SdeWaC](ims.uni-stuttgart.de/forschung/ressourcen/korpora/sdewac/)

#### Meta-Info

- Following meta-info is extracted into the output file:  
  sentence ID in SDeWaC

#### Annotations

column name | annotation
------ | ------
ID | word index
Joined_ID | sentence and word index
FORM | word form
LEMMA | Lemma
UPOS | Universal POS-Tag
XPOS | STTS-Tag
FEATS | morphological features
HEAD | head
DEPREL | dependency relation to the head
UNK1 | unknown
UNK2 | unknown
UNK3 | unknown
UNK4 | unknown
UNK5 | unknown
UNK6 | unknown  

## Processors

1. [DTASimplifier](#dtasimplifier)
2. [TopFSimplifier](#topfsimplifier)
3. [DTAChopper](#dtachopper)
4. [TopFChopper](#topfchopper)
5. [SATZKLAMMERtoTopF](#satzklammertotopf)
6. [TSVIndexer](#tsvindexer)
7. [CoNLLUPLUSIndexer](#conlluplusindexer)
8. [TUEBADSTopFExtractor](#tuebadstopfextractor)
9. [HIPKONtoSTTSMapper](#hipkontosttsmapper)
10. [addmissingSTTStoHIPKON](#addmissingsttstohipkon)
11. [HiTStoSTTSMapper](#hitstosttsmapper)
12. [ANSELMtoSTTSMapper](#anselmtosttsmapper)
13. [ReFHiTStoSTTSMapper](#refhitstosttsmapper)
14. [MercuriusToSTTSMapper](#mercuriustosttsmapper)
15. [ReFUPToSTTSMapper](#refuptosttsmapper)
16. [FuerstinnentoSTTSMapper](#fuerstinnentosttsmapper)
17. [VirgelMapper](#virgelmapper)
18. [PronominalAdverbMapper](#pronominaladverbmapper)
19. [ReFUPCoding](#refupcoding)
20. [BracketRemover](#bracketremover)

### DTASimplifier

- Removes unneeded annotation columns and simplifies some annotations from the DTA corpus.

#### Required Input

- Doc-Object that contains tokens with annotations from the DTA Corpus.

#### Output

- Doc-Object that contains tokens with simplified columns.
- The remaining columns are:  
	ID, FORM, XPOS, LEMMA, OrthCorr, Cite, Antec, AntecHead, SentBrckt,
	MovElem, MovElemPos, RelCType, AdvCVPos, AdvCVHead
	

### TopFSimplifier

- Removes unneeded annotation columns, simplifies the topological field annotation and creates a sentence bracket column.

#### Required Input

- Doc-Object that contains tokens with TopF annotation.

#### Output

- Doc-Object that contains tokens with simplified columns.
- The remaining columns are:  
	ID, FORM, XPOS, LEMMA, FEATS, DEPREL, HEAD, CHUNK, TopF, SentBrckt
	

### DTAChopper

- Removes unannotated sentences and reindexes the sentences and character offsets.

#### Required Input

- Doc-Object that contains tokens that have at least a MovElemCat, TSVID, CHARS and FORM attribute.

#### Output

- Doc-Object that contains only sentences with relevant MovElemCat annotation.


### TopFChopper

- Removes unannotated sentences.

#### Required Input

- Doc-Object that contains tokens that have at least a TopF attribute.

#### Output

- Doc-Object that contains only sentences with relevant TopF annotation.


### SATZKLAMMERtoTopF

- Maps the attribute 'SATZKLAMMER' from HIPKON to the corresponding topological field.

#### Required Input

- Doc-Object that contains tokens that have at least a SATZKLAMMER attribute.

#### Output

- Doc-Object that contains tokens with added TopF attribute.


### TSVIndexer

- Adds the sentence and word index and the character offsets for the WebAnno TSV Format.

#### Required Input

- Doc-Object that contains tokens that have at least a FORM attribute.

#### Output

- Doc-Object that contains tokens with added TSVID and CHARS attribute.


### CoNLLUPLUSIndexer

- Adds the sentence and word index for the CoNLL-U Plus Format.

#### Required Input

- Doc-Object that contains sentences with tokens.

#### Output

- Doc-Object that contains sentences with added sent_id attribute and tokens with added ID attribute.


### TUEBADSTopFExtractor

- Extracts the topological field information from TueBa-D/S.

#### Required Input

- Doc-Object that contains tokens with at least a POS:HD and SYNTAX attribute.

#### Output

- Doc-Object that contains tokens with added PHRASE:HEAD and TopoField attribute.


### HIPKONtoSTTSMapper

- Maps the POS-Tags from HIPKON to their corresdponding STTS-Tags.

#### Required Input

- Text-file of the form `POS-Tag\tSTTS-Tag` that contains the rules for the mapping.
- Doc-Object that contains tokens that have at least a FORM and POS attribute.

#### Output

- Doc-Object that contains tokens with added XPOS attribute for the STTS-Tags.
- CSV-File with tokens that still don't have an STTS-Tag and their exact location.
- List of rules which effectively were used during the mapping.


### addmissingSTTStoHIPKON

- Maps the POS-Tags of the remaining tokens after processing with the HIPKONtoSTTSMapper to their corresponding STTS-Tags.

#### Required Input

- CSV-File of the form `Token\tFilename\tSent_id\tTok_id\tSTTS-Tag` that contains the STTS-Tags of the remaining tokens.
- Doc-object that contains the tokens.

#### Output

- Doc-Object where all tokens have an XPOS attribute with their STTS-Tag.


### HiTStoSTTSMapper

- Maps the HiTS-Tags from ReM to their corresponding STTS-Tags.

#### Required Input

- CSV-File of the form `POS-Tag\tPOSLEMMA-Tag\tCount\tCandidates\tSTTS-Tag\tRemarks` that contains the rules for the mapping.
- Doc-Object that contains tokens that have at least ID, FORM, POS, POS_GEN and PUNC attributes.

#### Output

- Doc-Object that contains tokens with added XPOS attribute for the STTS-Tags.


### ANSELMtoSTTSMapper

- Maps the POS-Tags from Anselm to their corresponding STTS-Tags.

#### Required Input

- CSV-File of the form `POS-Tag\tSTTS-Tag` that contains the rules for the mapping.
- Doc-Object that contains tokens that have at least a POS attribute.

#### Output

- Doc-Object that contains tokens with added XPOS attribute for the STTS-Tags.


### ReFHiTStoSTTSMapper

- Maps the HiTS-Tags from ReF.BO to their corresponding STTS-Tags.

#### Required Input

- CSV-File of the form `POS-Tag\tPOSLEMMA-Tag\tSTTS-Tag` that contains the rules for the mapping.
- Doc-Object that contains tokens that have at least ID, FORM, POS and POS_LEMMA attributes.

#### Output

- Doc-Object that contains tokens with added XPOS attribute for the STTS-Tags.


### MercuriusToSTTSMapper

- Maps the POS-Tags from Mercurius to their corresponding STTS-Tags.

#### Required Input

- CSV-file of the form `POS-Tag\tSTTS-Tag\tComments` that contains the rules for the mapping.
- Doc-Object that contains tokens that have at least ID, FORM and POS attributes.

#### Output

- Doc-Object that contains tokens with added XPOS attribute for the STTS-Tags.


### ReFUPToSTTSMapper

- Maps the POS-Tags from ReF.UP to their corresponding STTS-Tags.

#### Required Input

- CSV-file of the form `POS-Tag\tSTTS-Tag` that contains the rules for the mapping.
- Doc-Object that contains tokens that have at least ID, FORM and POS attributes.

#### Output

- Doc-Object that contains tokens with added XPOS attribute for the STTS-Tags.


### FuerstinnentoSTTSMapper

- Maps the POS-Tags from Fuerstinnenkorrespondenz to their corresponding STTS-Tags.

#### Required Input

- CSV-file of the form `POS-Tag\tSTTS-Tag` that contains the rules for the mapping.
- Doc-Object that contains tokens that have at least a POS and LEMMA attribute.

#### Output

- Doc-Object that contains tokens with added XPOS attribute for the STTS-Tags.


### VirgelMapper

- Maps all Virgel (token of the form "/") in a document to the XPOS-Tag "$(".

#### Required Input

- Doc-Object that contains tokens that have at least a FORM attribute.

#### Output

- Doc-Object that contains tokens with updated XPOS-Tag for Virgel.


### PronominalAdverbMapper

- Maps all Pronominal Adverbs with XPOS-tag "PROAV" to the XPOS-Tag "PAV".

#### Required Input

- Doc-Object that contains tokens that have at least an XPOS attribute.

#### Output

- Doc-Object that contains tokens with updated XPOS-Tag for Pronominal adverbs.


### ReFUPCoding

- Corrects the coding of "ß" in ReF.UP.

#### Required Input

- Doc-Object that contains tokens that have at least a FORM attribute.

#### Output

- Doc-Object that contains tokens with updatet coding.


### BracketRemover

- Removes all forms of brackets from the tokens (except of punctuation-token).

#### Required Input

- Doc-Object that contains tokens that have at least a FORM attribute.

#### Output

- Doc-Object that contains tokens without brackets in their word form.

## Exporters

1. [CoNLLUPlusExporter](#conlluplusexporter)
2. [CoNLLUExporter](#conlluexporter)
3. [CoNLL2000Exporter](#conll2000exporter)
4. [TextExporter](#textexporter)
5. [POSExporter](#posexporter)
6. [PTBExporter](#ptbexporter)
7. [HIPKONTSVExporter](#hipkontsvexporter)
8. [DTATSVExporter](#dtatsvexporter)

### CoNLLUPlusExporter

- Name for usage in command line: `conlluplus`

#### Output Format

- [CoNLL-U Plus Format](https://universaldependencies.org/ext-format.html)
- Lines containing the annotations of a word (seperated by tabs), blank lines marking sentence boundaries.
- Comment lines starting with hash (#).
- First line is a comment line listing the column names.
- Field contains an underscore if info is not available for the current word.

#### Example

>\# global.columns = ID FORM LEMMA UPOS XPOS FEATS HEAD DEPREL DEPS MISC  
\# sent_id = 1  
\# sent_id(Tiger) = 50  
\# sent_type = Header  
\# text = IBM und Siemens gelten nicht mehr als Schimpfworte  
1	IBM	IBM	_	NE	case=nom|number=sg|gender=*	4	SB	_	_  
2	und	und	_	KON	_	1	CD	_	_  
3	Siemens	Siemens	_	NE	case=nom|number=sg|gender=*	2	CJ	_	_  
4	gelten	gelten	_	VVFIN	number=pl|person=3|tense=pres|mood=ind	0	--	_	_  
...

### CoNLLUExporter

- Name for usage in command line: `conllu`

#### Output Format

- [CoNLL-U Format](https://universaldependencies.org/format.html)
- Lines containing the annotations of a word (seperated by tabs), blank lines marking sentence boundaries.
- 10 columns containing the following annotations for each word:  
	ID (word index), FORM (word form), LEMMA (Lemma), UPOS (universal POS-tag), XPOS (language specific POS-tag),
	FEATS (Morphological features), HEAD (head), DEPREL (dependency relation to the head), DEPS (dependency graph),
	MISC (other annotation)
- Field contains an underscore if info is not available for the current word.

#### Example

>1	IBM	IBM	_	NE	case=nom|number=sg|gender=*	4	SB	_	_  
2	und	und	_	KON	_	1	CD	_	_  
3	Siemens	Siemens	_	NE	case=nom|number=sg|gender=*	2	CJ	_	_  
4	gelten	gelten	_	VVFIN	number=pl|person=3|tense=pres|mood=ind	0	--	_	_  
...

### CoNLL2000Exporter

- Name for usage in command line: `conll2000`

#### Output Format

- Lines containing the annotations of a word (seperated by whitespaces), blank lines marking sentence boundaries.
- 3 columns containing the following annotations for each word:  
	FORM (word form), XPOS (language specific POS-tag), CHUNK (syntactically correlated parts of words)
- Field contains an underscore if info is not available for the current word.

#### Example

>Confidence NN B-NP  
in IN B-PP  
the DT B-NP  
pound NN I-NP  
...


### TextExporter

- Name for usage in command line: `text`

#### Output Format

- Text-file containing one word per line, blank lines marking sentence boundaries.

#### Example

>Von  
Wermut  
.  
>
>Das  
erste  
Kapitel  
.  
>  
>...

### POSExporter

- Name for usage in command line: `pos`

#### Output Format

- Text-file containing in each line the XPOS- or POS-tags of one sentence (seperated by whitespaces).

#### Example

>APPR NE $.  
ART ADJA NN $.  
NN $.  
...

### PTBExporter

- Name for usage in command line: `ptb`

#### Output Format

- Text-file containing the PTB-String of a sentence per line.

#### Example

>(NP:--(PDAT:NK dheso)(NN:NK burgi)(NN:AG israhelo))  
(S:--(ADV:MO aer)(ADV:MO dhanne)(VVFIN:HD quuimit))  
(CS:--(KON:CD ni)(KON:CD noh)(S:CJ(NN:SB scalk))(S:CJ(VAFIN:HD ist)(NN:SB iungiro)(PP:MO(APPR:AC ubar)(NN:NK meistar))))  
...

### HIPKONTSVExporter

- Name for usage in command line: `HIPKONtsv`

#### Output Format

- [WebAnno TSV 3.2](https://webanno.github.io/webanno/releases/3.4.5/docs/user-guide.html#sect_webannotsv)
- Lines containing the annotations of a word (seperated by tabs), blank lines marking sentence boundaries.
- Comment lines starting with hash (#).
- 6 columns containing the following annotations for each word:  
	TSVID (sentence and word index), CHARS (character offsets), FORM (word form), XPOS (language specific POS-tag), LEMMA (Lemma), TopF (Topological Field)
- Field contains an underscore if info is not available for the current word.

#### Example

>\#FORMAT=WebAnno TSV 3.2  
\#T_SP=de.tudarmstadt.ukp.dkpro.core.api.lexmorph.type.pos.POS|PosValue  
\#T_SP=de.tudarmstadt.ukp.dkpro.core.api.segmentation.type.Lemma|value  
\#T_SP=webanno.custom.TopF|TopologicalField  
>
>
>\#Text=*{N*}v ſchvlt ir hivte lazzin gniezzin die heiligin chriſtenheit .  
1-1	0-6	*{N*}v	ADV	_	_  
1-2	7-13	ſchvlt	VMFIN	_	LK  
1-3	14-16	ir	PPER	_	_  
...

### DTATSVExporter

- Name for usage in command line: `DTAtsv`

#### Output Format

- [WebAnno TSV 3.2](https://webanno.github.io/webanno/releases/3.4.5/docs/user-guide.html#sect_webannotsv)
- Lines containing the annotations of a word (seperated by tabs), blank lines marking sentence boundaries.
- Comment lines starting with hash (#).
- 28 columns containing the following annotations for each word:  
	TSVID (sentence and word index), CHARS (character offsets), FORM (word form), XPOS (language specific POS-tag), POS (POS-tag), LEMMA (Lemma),
	OrthCorr, OrthCorrOp, OrthCorrReason, Cite, AntecDepLink, AntecMovElem, AntecHeadLink, AntecHead, AntecHeadLemLink, AntecHeadLem,
	SentBrcktLink, SentBrckt, SentBrcktType, MovElemAntecLink, MovElemAntec, MovElemCat, MovElemPos, RelCType, MovElemRole, MovElemTyp, AdvCVPos, AdvCVHead
- Field contains an underscore if info is not available for the current word.
