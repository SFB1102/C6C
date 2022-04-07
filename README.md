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

> py C6C.py convert -i input_format -e export_format -p "['processor_name', 'processor_name']" input_dir_or_file output_dir_or_file

- `input_dir_or_file`: can be a single file or a folder
- `output_dir_or_file`: can be a single file or a folder
- `input_format`: the following input formats are currently supported ([documentation](#importers) see below): `text`, `tcfDTA`, `xmlDTA`, `tiger`, `tigerxml`, `mercuriustigerxml`, `conlluplus`, `conllu`, `conll2000`, `DTAtsv`, `tuebadz`, `annisgrid`, `webannotopf`, `webannotsv`, `coraxmlrem`, `coraxmlrefbo`, `coraxmlanselm`, `tuebadsconll`, `tuebatrees`, `ddbtigernegra`, `fuerstinnenexb`, `refup`, `germanc`, `sdewac`, `graphvar` 
- `export_format`: the following export formats are currently supported ([documentation](#exporters) see below): `conlluplus`, `conllu`, `DTAtsv`, `HIPKONtsv`, `text`, `pos`, `conll2000`, `ptb`
- `processor_name`: processors are called in the given order; the following processors are currently implemented ([documentation](#processors) see below): `dtachopper`, `dtasimplifier`, `hipkontostts`, `addmissingstts`, `topfsimplifier`, `satzklammertotopf`, `tsvindexer`, `hitstostts`,  `tuebadstopf`, `anselmtostts`, `topfchopper`, `conllindexer`, `refhitstostts`,  `depmanipulator`, `depprocessor`, `mercuriustostts`, `refuptostts`, `fuerstinnentostts`, `virgelmapper`, `pronominaladverb`, `refupcoding`, `bracketremover`, `treetobio`

## Documentation of pipeline components

1. [Importers](/README_Importers.md)
2. [Processors](/README_Processors.md)
3. [Exporters](/README_Exporters.md)
