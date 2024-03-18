# SPDX-FileCopyrightText: 2023 pukkamustard <pukkamustard@posteo.net>
# SPDX-FileCopyrightText: 2023 Moritz Feichtinger <moritz.feichtinger@unibas.ch>
#
# SPDX-License-Identifier: AGPL-3.0-or-later

"""RDF/CBOR Terms

Implements serialization and sorting of RDF/CBOR Terms.
"""

import cbor2
from cbor2 import CBORTag, undefined
from rdflib.term import URIRef, Literal, BNode
from rdflib.namespace import XSD

import dataclasses
from urllib.parse import urlparse
import base64
from uuid import UUID
from datetime import datetime


# Frament Reference


@dataclasses.dataclass(eq=True, frozen=True, order=True)
class FragmentReference:

    fragment: str

    def to_cbor(self):
        return CBORTag(305, self.fragment)


# It does not seem possible to use the documented extension points of
# the `cbor2` library to encode the types from rdflib.term (see
# https://cbor2.readthedocs.io/en/latest/customizing.html). The reason
# is that all `rdflib.term` types inherit from `str`, which `cbor2`
# can handle and then does not invoke the custom encoding handler.


# Encoding


def base32_decode(s):
    """Returns the bytes encoded as Base32 in [s]. Unlike
    `base64.b32decode` this can handle missing padding."""
    last_block_width = len(s) % 8
    if last_block_width != 0:
        s += (8 - last_block_width) * "="
    return base64.b32decode(s)


def add_fragment(url, cbor):
    if url.fragment:
        return CBORTag(305, [cbor, str(url.fragment)])
    else:
        return cbor


def eris_urn_to_cbor(url):
    binary_read_cap = base32_decode(url.path[5:])
    if len(binary_read_cap) == 66:
        return add_fragment(url, CBORTag(276, binary_read_cap))
    else:
        raise "Invalid ERIS read capability"


def uuid_urn_to_cbor(url):
    uuid = UUID(url.path[5:])
    return add_fragment(url, uuid)


def uri_to_cbor(uri):
    url = urlparse(uri)

    match url.scheme:
        case "urn":

            if url.path.startswith("eris:"):
                return eris_urn_to_cbor(url)
            elif url.path.startswith("uuid:"):
                return uuid_urn_to_cbor(url)
            else:
                return CBORTag(266, str(url))

        case _:
            return CBORTag(266, str(uri))


def literal_to_cbor(literal):
    match literal.datatype:

        case XSD.string:
            return str(literal.value)

        case XSD.boolean:
            return bool(literal.value)

        case XSD.integer:
            return int(literal.value)

        case XSD.float:
            return float(literal.value)

        case XSD.double:
            return float(literal.value)

        case XSD.dateTime:
            return literal.value

        case XSD.hexBinary:
            raise "TODO"
            # return CBORTag(32, literal)

        case XSD.base64Binary:
            return literal.value

        case _:

            if literal.language:
                return CBORTag(38, [literal.language, str(literal.value)])
            elif literal.datatype:
                return CBORTag(
                    303, [uri_to_cbor(literal.datatype), str(literal.normalize())]
                )
            else:
                return str(literal.value)


def bnode_to_cbor(bnode):
    return CBORTag(304, str(bnode))


def to_cbor(term):
    if isinstance(term, URIRef):
        return uri_to_cbor(term)
    elif isinstance(term, Literal):
        return literal_to_cbor(term)
    elif isinstance(term, BNode):
        return bnode_to_cbor(term)
    elif isinstance(term, FragmentReference):
        return term.to_cbor()
    elif term == undefined:
        return term
    else:
        raise TypeError(f"Can not encode {type(term)} as RDF/CBOR term.")


def dumps(term):
    """Encode an RDF term to a bytestring using RDF/CBOR.

    Parameters
    ----------
    term: rdflib.term
        RDF term to encode

    Returns
    -------
    bytes
        RDF/CBOR encoding of RDF term
    """
    return cbor2.dumps(to_cbor(term))


# Decoding


def base32_encode(b):
    """Returns the unpadded Base32 encoding of [b]."""
    return base64.b32encode(b).decode().rstrip("=")


def of_cbor(cbor):
    match cbor:

        # URI
        case CBORTag(tag=266, value=uri):
            return URIRef(uri)

        case CBORTag(tag=305, value=[uri_cbor, fragment]):
            uri = of_cbor(uri_cbor)
            return URIRef(uri + "#" + fragment)

        case CBORTag(tag=276, value=binary_read_cap):
            return URIRef("urn:eris:" + base32_encode(binary_read_cap))

        case UUID() as uuid:
            return URIRef(uuid.urn)

        case CBORTag(tag=37, value=binary_uuid):
            uuid = UUID(binary_uuid)
            return URIRef(uuid.urn)

        # Literals

        case str() as value:
            return Literal(value)

        case bool() as value:
            return Literal(value)

        case int() as value:
            return Literal(value)

        case float() as value:
            return Literal(value)

        case datetime() as value:
            return Literal(value)

        case bytes() as value:
            return Literal(base64.b64encode(value), datatype=XSD.base64Binary)

        case CBORTag(tag=38, value=[lang, value]):
            return Literal(value, lang=lang)

        case CBORTag(tag=303, value=[datatype, value]):
            return Literal(value, datatype=of_cbor(datatype))

        # BNode

        case CBORTag(tag=304, value=identifier):
            return BNode(identifier)

        # Fragment Reference

        case CBORTag(tag=305, value=[fragment]):
            return FragmentReference(fragment)

        case _:
            # Handle the Base Subject for content-addressable molecules
            if cbor == undefined:
                return undefined
            else:
                # Raise error on unparseable CBOR
                raise ValueError(f"Can not decode RDF/CBOR Term from CBOR ({cbor})")


def loads(bytes):
    """Decode an RDF/CBOR encoded term from a bytestring.

    Parameters
    ----------
    bytes: bytes
        RDF/CBOR encoded term

    Returns
    -------
    rdflib.term
        Decoded RDF term
    """
    cbor = cbor2.loads(bytes)
    return of_cbor(cbor)


# Sorting of Terms


class Sortable:
    """A class that allows Terms to be sorted as required by the
    RDF/CBOR specification.

    This is an example of the Decorate-Sort-Undecorate pattern
    (https://docs.python.org/3/howto/sorting.html#decorate-sort-undecorate)."""

    def __init__(self, term):
        self.term = term

    def __lt__(self, other):

        if (self.term == undefined) and (other.term == undefined):
            return False

        elif self.term == undefined:
            return True

        elif other.term == undefined:
            return False

        elif isinstance(self.term, FragmentReference) and isinstance(
            other.term, FragmentReference
        ):
            return self.term < other.term

        elif isinstance(self.term, FragmentReference):
            return True

        elif isinstance(other.term, FragmentReference):
            return False

        elif isinstance(self.term, URIRef) and isinstance(other.term, URIRef):
            return str(self.term) < str(other.term)

        elif isinstance(self.term, URIRef):
            return True

        elif isinstance(other.term, URIRef):
            return False

        elif isinstance(self.term, Literal) and isinstance(other.term, Literal):
            return dumps(self.term) < dumps(other.term)

        elif isinstance(self.term, Literal):
            return True

        elif isinstance(other.term, Literal):
            return False

        elif isinstance(self.term, BNode) and isinstance(other.term, BNode):
            return str(self.term) < str(self.term)

        else:
            return self.term < other.term


def sort_terms(terms):
    return [sortable.term for sortable in sorted(map(Sortable, terms))]


# Sorting of Triples


class SortableTriple:
    def __init__(self, triple):
        self.triple = triple

    def __lt__(self, other):

        if Sortable(self.triple[0]) < Sortable(other.triple[0]):
            return True

        elif Sortable(other.triple[0]) < Sortable(self.triple[0]):
            return False

        elif Sortable(self.triple[1]) < Sortable(other.triple[1]):
            return True
        elif Sortable(other.triple[1]) < Sortable(self.triple[1]):
            return False
        elif Sortable(self.triple[2]) < Sortable(other.triple[2]):
            return True
        elif Sortable(other.triple[2]) < Sortable(self.triple[2]):
            return False
        else:
            return False


def sort_triples(triples):
    return map(lambda s: s.triple, sorted(map(SortableTriple, triples)))
