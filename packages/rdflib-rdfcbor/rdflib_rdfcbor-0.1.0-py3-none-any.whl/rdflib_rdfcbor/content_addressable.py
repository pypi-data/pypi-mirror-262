# SPDX-FileCopyrightText: 2024 pukkamustard <pukkamustard@posteo.net>
# SPDX-FileCopyrightText: 2024 Moritz Feichtinger <moritz.feichtinger@unibas.ch>
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from rdflib import URIRef

import rdflib_rdfcbor.term as term
from rdflib_rdfcbor.term import FragmentReference
from rdflib_rdfcbor.dictionary import Dictionary
import rdflib_rdfcbor.molecule as molecule

import cbor2
from cbor2 import undefined, CBORTag
from io import BytesIO

from hashlib import blake2b
import base64

import graphlib

from operator import itemgetter
from itertools import groupby


def base32_encode(b):
    """Returns the unpadded Base32 encoding of [b]."""
    return base64.b32encode(b).decode().rstrip("=")


def blake2b_256_urn(b):
    h = blake2b(digest_size=32)
    h.update(b)
    d = h.digest()
    return URIRef("urn:blake2b:" + base32_encode(d))


class RDFCBORContentAddressableMolecule:
    def __init__(self, hash=blake2b_256_urn):
        self.hash = hash

        self.statements = set()

    def add(self, p, o):
        self.statements.add((undefined, p, o))

    def addf(self, f, p, o):
        if not isinstance(f, FragmentReference):
            f = FragmentReference(f)
        self.statements.add((f, p, o))

    def subjects(self):
        return set(map(itemgetter(0), self.statements))

    def predicates(self):
        return set(map(itemgetter(1), self.statements))

    def objects(self):
        return set(map(itemgetter(2), self.statements))

    def to_cbor(self):

        dictionary = Dictionary.from_graph(self)

        predicate_groups = []
        object_groups = []

        for s, predicate_objects in groupby(
            map(dictionary.locate_triple, term.sort_triples(self.statements)),
            key=lambda t: t[0],
        ):
            p_group = []

            for p, triples in groupby(predicate_objects, key=lambda t: t[1]):
                p_group.append(p)
                object_groups.append(list(map(lambda t: t[2], triples)))

            predicate_groups.append(p_group)

        p_bitmap, ps = molecule.bitmap(predicate_groups)
        o_bitmap, os = molecule.bitmap(object_groups)

        return CBORTag(302, [dictionary.to_cbor(), p_bitmap, ps, o_bitmap, os])

    def serialize(self, stream):
        cbor = self.to_cbor()
        cbor2.dump(cbor, stream)

    def base_subject(self):
        with BytesIO() as fp:
            self.serialize(fp)
            b = fp.getvalue()
            return self.hash(b)

    @staticmethod
    def __rdf_term_of_term(base_subject, term):
        if term == undefined:
            return base_subject
        elif isinstance(term, FragmentReference):
            return URIRef(base_subject + "#" + term.fragment)
        else:
            return term

    def triples(self, base_subject=None):
        """Yields a sequence of triples using the content-addressed base subject.

        Parameters
        ----------
        base_subject: rdflib.URIRef
            The base subject may be overriden. If not provided the
            `hash` function will be used to compute the base subject.

        Yields
        ------
        rdflib.triple
            Triples of the content-addressed molecule.
        """
        if not base_subject:
            base_subject = self.base_subject()

        for s in self.statements:
            yield (
                self.__rdf_term_of_term(base_subject, s[0]),
                self.__rdf_term_of_term(base_subject, s[1]),
                self.__rdf_term_of_term(base_subject, s[2]),
            )


def of_graph(graph, hash=blake2b_256_urn):
    """Content-address a RDF graph using RDF/CBOR.

    Yields a sequence of content-addressable RDF/CBOR
    molecules. Raises an error if graph contains a cycle or blank
    nodes.

    Parameters
    ----------
    graph: rdflib.Graph
        RDF graph to content-address

    hash:
        Hash function that takes a sequnce of bytes and returns an
        rdflib.URIRef.

    Yields
    ------
    RDFCBORContentAddressableMolecule
        Conent-addressed molecules. The union of the molecules is
        equivalent to the input graph (with different identifiers).

    """

    # Collect and group base subjects and fragment references
    # We need to do stupid stuff because python itertools doesn't
    # return persistent stuff...
    base_subjects = {}
    for base_subject, subjects in groupby(
        sorted(graph.subjects(), key=lambda s: s.defrag()), lambda s: s.defrag()
    ):
        base_subjects[base_subject] = set(subjects)

    # Find dependencies between fragment molecules
    #
    # In a first pass over the triples we need to find dependencies
    # between fragment molecules.

    # Create a graph with edges being dependencies between base subjects
    ts = graphlib.TopologicalSorter()
    for base_subject in base_subjects:
        ts.add(base_subject)

        # Iterate over all triples for the base_subject
        for s in base_subjects[base_subject]:
            for (_, p, o) in graph.triples((s, None, None)):

                # If predicate is a base_subject add dependency
                if isinstance(p, URIRef):
                    p_base = p.defrag()
                    if p_base != base_subject and p_base in base_subjects:
                        ts.add(base_subject, p_base)

                # If object is a base_subject add dependency
                if isinstance(o, URIRef):
                    o_base = o.defrag()
                    if o_base != base_subject and o_base in base_subjects:
                        ts.add(base_subject, o_base)

    # Content-address fragments
    #
    # Content-address the individual fragment molecules in an order
    # that allows replacing references.

    replacements = {}

    for base_subject in ts.static_order():
        m = RDFCBORContentAddressableMolecule()

        # Iterate over all triples for the base_subject
        for s in base_subjects[base_subject]:
            for (_, p, o) in graph.triples((s, None, None)):

                # Replace references to molecules that were previously
                # content-addressed
                if p.defrag() in replacements:
                    if p.fragment:
                        p = URIRef(replacements[p.defrag()] + "#" + p.fragment)
                    else:
                        p = replacements[p.defrag()]

                if isinstance(o, URIRef) and o.defrag() in replacements:
                    if o.fragment:
                        o = URIRef(replacements[o.defrag()] + "#" + o.fragment)
                    else:
                        o = replacements[o.defrag()]

                # Replace self-references
                if p.defrag() == base_subject:
                    if p.fragment:
                        p = FragmentReference(p.fragment)
                    else:
                        p = undefined

                if isinstance(o, URIRef) and o.defrag() == base_subject:
                    if o.fragment:
                        o = FragmentReference(o.fragment)
                    else:
                        o = undefined

                # Add statement to molecule
                if s.fragment:
                    m.addf(s.fragment, p, o)
                else:
                    m.add(p, o)

        replacements[base_subject] = m.base_subject()

        yield m
