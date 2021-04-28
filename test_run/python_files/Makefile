ts := $(shell /bin/date "+%Y%m%d%H%M%S")

build:
	mvn clean install

merge:
	find ./prov/*.provn | sed "s/^/file, /; s/$$/, provn/" | provconvert -merge - -outfile mergey.provn

flatten:
	provconvert -infile mergey.provn -index -flatten -outfile flatten_file.provn

flattensvg:
	provconvert -infile mergey.provn -index -flatten -outfile flatten_file.svg

flattenpng:
	provconvert -infile mergey.provn -index -flatten -outfile flatten_file.png

flattenrdf:
	provconvert -infile mergey.provn -index -flatten -outfile flatten_file.rdf

flattenttl:
	provconvert -infile mergey.provn -index -flatten -outfile flatten_file.ttl


test:
	mkdir testaroni
