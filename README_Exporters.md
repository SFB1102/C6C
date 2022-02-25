# C6C Exporters

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
