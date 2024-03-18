# SPDX-FileCopyrightText: 2023 pukkamustard <pukkamustard@posteo.net>
# SPDX-FileCopyrightText: 2023 Moritz Feichtinger <moritz.feichtinger@unibas.ch>
#
# SPDX-License-Identifier: AGPL-3.0-or-later


"""RDF/CBOR Molecule

This module implements the serializer and parser for RDF/CBOR
Molecules.

In most cases functions provided by this module should not be used
directly. Instead use the RDFCBORSerializer and RDFCBORParser classes
in the `rdflib_rdfcbor` module.
"""

import rdflib_rdfcbor.term as term
from rdflib_rdfcbor.dictionary import Dictionary

import cbor2
from cbor2 import CBORTag

from operator import itemgetter
from itertools import accumulate, chain, count, groupby, product

# Serializer


def bitmap(groups):
    elements = []
    bits = 0

    group_end = 0
    for group in groups:
        group_end = group_end + len(group)
        # mark the ith position
        bits = bits | (1 << group_end)
        elements = elements + group

    return bits, elements


def to_cbor(store):

    dictionary = Dictionary.from_graph(store)

    predicate_groups = []
    object_groups = []

    for s, predicate_objects in groupby(
        map(dictionary.locate_triple, term.sort_triples(store)),
        key=lambda t: t[0],
    ):
        p_group = []

        for p, triples in groupby(predicate_objects, key=lambda t: t[1]):
            p_group.append(p)
            object_groups.append(list(map(lambda t: t[2], triples)))

        predicate_groups.append(p_group)

    # print(f'predicate_groups {predicate_groups}')
    # print(f'object_group: {object_groups}')

    p_bitmap, ps = bitmap(predicate_groups)
    o_bitmap, os = bitmap(object_groups)

    return CBORTag(301, [dictionary.to_cbor(), p_bitmap, ps, o_bitmap, os])


# Parser


def groups_of_bitmap(bitmap, elements):

    element_count = len(elements)

    # A list that maps every element to a group
    groups = list(
        accumulate(
            map(
                lambda i: 1 if bitmap & (1 << i) else 0,
                range(element_count + 1),
            )
        )
    )

    return map(
        lambda t: list(map(itemgetter(1), t[1])),
        groupby(zip(groups, elements), key=itemgetter(0)),
    )


def parse(cbor, sink):
    match cbor:
        case CBORTag(tag=301, value=[cbor_dictionary, p_bitmap, ps, o_bitmap, os]):

            dictionary = Dictionary.from_cbor(cbor_dictionary)

            # Decode the bitmaps to groups
            predicate_groups = groups_of_bitmap(p_bitmap, ps)
            object_groups = groups_of_bitmap(o_bitmap, os)

            # match subjects with the predicate groups
            subject_predicate_groups = zip(count(), predicate_groups)

            # unwind predicate_groups for every subect to a iterable of subject-predicates
            subject_predicates = chain.from_iterable(
                map(
                    lambda sps: product([sps[0]], sps[1]),
                    subject_predicate_groups,
                )
            )

            # match subject_predicates with object groups
            subject_predicate_object_groups = zip(subject_predicates, object_groups)

            # and unwind the object_groups to individual tripls
            triple_ids = map(
                # unpack the tuple of tuples to a triple
                lambda spos: (spos[0][0], spos[0][1], spos[1]),
                chain.from_iterable(
                    map(
                        lambda spos: product([spos[0]], spos[1]),
                        subject_predicate_object_groups,
                    )
                ),
            )

            # get triples with dictionary and add to sink
            for triple in map(dictionary.extract_triple, triple_ids):
                sink.add(triple)
