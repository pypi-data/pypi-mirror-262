# RDFLib plugin providing RDF/CBOR serialization

This is an implementation of the [RDF/CBOR](https://openengiadina.codeberg.page/rdf-cbor/) serialization for the Python [RDFlib](https://rdflib.dev/) library.

RDF/CBOR is a binary serialization of RDF based on the [Concise Binary Object Representation (CBOR) as defined by RFC 8949](https://www.rfc-editor.org/rfc/rfc8949.html). Like CBOR the serialization is optimized for small code size and fairly small message size. The serialization is suitable for systems and devices that are possibly constrained in terms of network or computation.

RDF/CBOR can also be used to make RDF content-addressable - an identifier for a group of statements can be deterministically derived from the statements themselves.

## Installation

```
pip install rdflib-rdfcbor
```

## Usage

```
from rdflib import Graph
import rdflib_rdfcbor

# Create a Graph and load some triples from a Turtle file
g1 = Graph()
g1.parse("./test/example.ttl")

# Serialize to RDF/CBOR
cbor_bytes = g1.serialize(format="rdf-cbor", encoding="ascii")

print("RDF/CBOR bytes (in hex): ", cbor_bytes.hex())

# Parse triples from encoded bytes
g2 = Graph()
g2.parse(data=cbor_bytes, format="rdf-cbor")
```
### Content-addressable RDF

RDF/CBOR allows content-addressed RDF by defining a grouping of statements as well as a canonical serialization (see [Content-addressable Molecule in the RDF/CBOR specification](https://openengiadina.codeberg.page/rdf-cbor/#name-content-addressable-molecul)). This allows distributed systems to compute the same identifier for the same RDF satements independently.

RDF can be content-addressed by either creating a content-addressable graph from scratch or by content-addressing a graph that is not content-addressed.

#### From scratch

```
from rdflib import RDF, Literal
from rdflib.namespace import FOAF
import rdflib_rdfcbor.content_addressable

m = RDFCBORContentAddressableMolecule()

m.add(RDF.type, FOAF.Person)
m.add(FOAF.nick, Literal("pukkamustard"))

print(m.base_subject())
# urn:blake2b:QG75V2OGPFMURZTI5U6DJIWGP6JISNGVAYL5C2KDHULVBZXXZUUQ
```

#### Content-addressing an existing graph

```
import rdflib_rdfcbor.content_addressable

for m in rdflib_rdfcbor.content_addressable.of_graph(graph):
    g = Graph()
    for t in m.triples():
        g.add(t)
    print(g.serialize())
```

This works by first splitting the graph into [fragment-molecules](https://openengiadina.codeberg.page/rdf-cbor/#name-fragment-molecule) and then content-addressing them sequentially. As references between fragments are replaced with the new computed identifiers this only works if there are no cycles between fragment-molecules.

## Publishing to PyPi

```
pip install build twine

# Build the package
python -m build

# Upload using twine
twine upload dist/*
```

## Acknowledgements

This software was initially developed as part of the SNSF-Ambizione funded research project ["Computing the Social. Psychographics and Social Physics in the Digital Age"](https://data.snf.ch/grants/grant/201912).

## License

[AGPL-3.0-or-later](./LICENSES/AGPL-3.0-or-later.txt)
