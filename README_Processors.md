# C6C Processors

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
21. [DependencyProcessor](#dependencyprocessor)
22. [DependencyManipulator](#dependencymanipulator)
23. [TreeToBIOProcessor](#treetobioprocessor)

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

### DependencyProcessor

- Extracts the dependency relations of all tokens.

#### Required Input

- Doc-Object that contains tokens with dependency annotations (at least ID and HEAD attributes).

#### Output

- Doc-Object with added head_tok attribute (for the parent) and dep_toks attribute (for the children) for each token
and added roots attribute (list of all root tokens) for each sentence.

### DependencyManipulator

- Maps dependency annotations to a different dependency annotation scheme.

#### Required Input

- Doc-Object that contains tokens with dependency annotations (at least ID, HEAD and DEPREL attributes).

#### Output

- Doc-Object with changed dependency annotations of the tokens.

### TreeToBIOProcessor

- Converts a tree object to stacked BIO annotations.

#### Required Input

- Doc-Object that contains sentences with a tree object as attribute `tree`.

#### Output

- Doc-Object with BIO annotations as `TREE` attribute of the tokens.

