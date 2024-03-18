# SPDX-FileCopyrightText: 2023 pukkamustard <pukkamustard@posteo.net>
# SPDX-FileCopyrightText: 2023 Moritz Feichtinger <moritz.feichtinger@unibas.ch>
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from rdflib_rdfcbor.serializer import RDFCBORSerializer
from rdflib_rdfcbor.parser import RDFCBORParser

from rdflib_rdfcbor.term import FragmentReference
from rdflib_rdfcbor.content_addressable import RDFCBORContentAddressableMolecule


# Register Serializer/Parser as RDFLib plugins

import rdflib

rdflib.plugin.register(
    "rdf-cbor", rdflib.parser.Parser, "rdflib_rdfcbor.parser", "RDFCBORParser"
)

rdflib.plugin.register(
    "rdf-cbor",
    rdflib.serializer.Serializer,
    "rdflib_rdfcbor.serializer",
    "RDFCBORSerializer",
)
