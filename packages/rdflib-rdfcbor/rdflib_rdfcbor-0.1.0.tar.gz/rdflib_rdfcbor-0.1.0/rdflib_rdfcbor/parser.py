# SPDX-FileCopyrightText: 2023 pukkamustard <pukkamustard@posteo.net>
# SPDX-FileCopyrightText: 2023 Moritz Feichtinger <moritz.feichtinger@unibas.ch>
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from rdflib.parser import Parser

import rdflib_rdfcbor.molecule as molecule

import cbor2
from cbor2 import CBORTag


class RDFCBORParser(Parser):
    def __init__(self):
        pass

    def parse(self, source, sink):

        match cbor2.load(source.getByteStream()):

            # RDF/CBOR Molecule
            case CBORTag(tag=301) as cbor:
                molecule.parse(cbor, sink)

            # TODO: handle streams and content-addressable molecule

            case _:
                raise ValueError("Could not find CBOR tag for RDF/CBOR")
