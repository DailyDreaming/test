WDL Support in Toil
********

How to Run toilwdl.py
-----------
WDL files all require json files to accompany them.  To run a workflow, simply run:

python toilwdl.py wdlfile.wdl jsonfile.json

This will create a folder, toil_outputs, with all of the outputs of the current workflow.

WDL Specifications
----------
WDL Language specifications can be found here: https://github.com/broadinstitute/wdl/blob/develop/SPEC.md
Implementing support for all features is currently very basic, but a basic roadmap so far is:

CURRENTLY IMPLEMENTED:
 * scatter over tsv
 * handles calls, priority, and output file wrangling
 * handles single commands on the commandline
 * currently handles: $primitive_type & $array_type

TO BE IMPLEMENTED:
 * handle yml/ymal
 * handle inserting memory requirements
 * handle docker usage
 * handle multiple commands in commandline(?... test this)
 * implement type: $type_postfix_quantifier
 * "default" values inside variables
 * Alternative heredoc syntax ('>>>' & '<<<')
 * read_csv()
 * read_json()

MAYBE IMPLEMENT LATER ON
 * validate wdl file & json prior?  the Broad has this written in java
 * these types: $map_type & $object_type
 * wdl files that "import" other wdl files (including URI handling for 'http://' and 'https://')
