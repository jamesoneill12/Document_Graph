# Linking Legal Entities between Documents

## Description
The purpose of linking entities between documents is to allow law practitioners to find specific information across many documents.
This is essential for Regulatory Compliance (RC) and also Regulatory Change Management (RCM) to keep track of regulations concerning specific entities.
Another concern is to link ammendements or references in the text e.g Article (49)2 refers to this subject ..

# Steps

* Preprocessing - Standard string cleaning using regex and tokenization
* Named Entity Recognition and Coreference Resolution - NER is performed to extract the legal entities that are in the graph, Co-reference resolution is then performed to group entities that refer to the same singular entity.
* N-gram graph - Convert each document in the collection to a graph and convert it to json for linking and visualization
* Entity Linking - Documents are connected by entities, keyphrases and possibly other relatedness techniques
* Open Relation Extraction - When entities are linked across documents the subject and object of these entities (i.e using Open Relation Extraction techniques) are also linked, or given some similarity score
* Entity Information Retrieval - Entities can be queried upon over the whole supergraph


# Evaluation

The core mode of evaluation is feedback from SMEs in the area over a period of time working with the tool.
A subset of entities can be tested.
