# SPDX-FileCopyrightText: 2023 pukkamustard <pukkamustard@posteo.net>
# SPDX-FileCopyrightText: 2023 Moritz Feichtinger <moritz.feichtinger@unibas.ch>
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from rdflib import Graph, URIRef

import cbor2
import rdflib_rdfcbor.term as term

from itertools import takewhile


def lcp_l(a, b):
    """Returns the length of the longest common prefix between string
    a and b"""
    return len(list(takewhile(lambda cs: cs[0] == cs[1], zip(a, b))))


class Dictionary:

    """RDF/CBOR Dictionary

    Implements the RDF/CBOR Dictionary. Terms in the dictionary can be
    extracted with an integer identifier (dictionary reference). Given
    a term it can be located in the dictionary to find the integer
    identifier.

    Attributes:
      terms: Sorted list of terms in the dictionary.

    """

    def __init__(self, terms):
        self.terms = terms

    @classmethod
    def from_graph(cls, store):
        """Create a Dictionary from terms appearing in an RDF Graph.

        Parameters
        ----------
        store : rdflib.Graph

        Returns
        -------
        Dictionary : Dictionary of terms appearing in the provided graph.
        """
        subjects = set(store.subjects())

        predicate_objects = (set(store.predicates()) | set(store.objects())) - subjects

        terms = list(term.sort_terms(subjects) + term.sort_terms(predicate_objects))

        return cls(terms)

    @classmethod
    def from_cbor(cls, items):
        """Decodes the dictionary from a CBOR serialization.

        Parameters
        ----------
        items : list(cbor2.item)

        Returns
        -------
        Dictionary : Decoded dictionary
        """
        cur = items[0]
        cur_term = term.of_cbor(cur)

        terms = [cur_term]
        prev = cur_term

        for cur in items[1:]:

            match cur:
                case [prefix_length, suffix]:
                    prefix = prev[:prefix_length]
                    cur_term = URIRef(prefix + suffix)

                case _:
                    cur_term = term.of_cbor(cur)

            terms.append(cur_term)
            prev = cur_term

        return cls(terms)

    def extract(self, ref):
        """Extract term from dictionary.

        Parameters
        ----------
        ref : int
            Dictionary reference.

        Returns
        -------
        term : RDF/CBOR term
        """
        return self.terms[ref]

    def extract_triple(self, t):
        """Extract triple from dictionary

        Extracts subject, predicate and object term from triple
        returning an RDF/CBOR triple.

        Parameters
        ----------
        t : Tuple[int, int, int]

        Returns
        -------
        Tuple[term, term, term]: RDF/CBOR Triple
        """
        s, p, o = t
        return (self.extract(s), self.extract(p), self.extract(o))

    def locate(self, term):
        """Locate term in dictionary.

        Parameters
        ----------
        term : term
            Term to lookup in directory.

        Returns
        -------
        int : Dictionary reference
        """
        return self.terms.index(term)

    def locate_triple(self, triple):
        """Locate triple in dictionary.

        Parameters
        ----------
        triple: Tuple[term, term, term]
            Triple to lookup in directory.

        Returns
        -------
        Tuple[int, int, int] : Dictionary reference
        """
        s, p, o = triple
        return (self.locate(s), self.locate(p), self.locate(o))

    def to_cbor(self):
        """Encode dictionary to CBOR.

        Returns an encoded and compressed list of CBOR items
        representing the terms in the dictionary.

        Returns
        -------
        list(cbor2.item) : Dictionary encoded as CBOR items
        """

        prev = self.terms[0]
        cbor = [term.to_cbor(prev)]

        for cur in self.terms[1:]:
            if isinstance(prev, URIRef) and isinstance(cur, URIRef):
                n = lcp_l(prev, cur)
                if n > 9:
                    cbor.append([n, cur[n:]])
                else:
                    cbor.append(term.to_cbor(cur))
            else:
                cbor.append(term.to_cbor(cur))

            prev = cur

        return cbor

    def encode(self):
        """Encode dictionary to bytes using CBOR.

        Returns
        -------
        bytes: Binary encoding of dictionary.
        """
        return cbor2.dumps(self.to_cbor())
