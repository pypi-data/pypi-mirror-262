# SPDX-FileCopyrightText: 2023 pukkamustard <pukkamustard@posteo.net>
# SPDX-FileCopyrightText: 2023 Moritz Feichtinger <moritz.feichtinger@unibas.ch>
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from rdflib.serializer import Serializer

import rdflib_rdfcbor.molecule as molecule

import cbor2


class RDFCBORSerializer(Serializer):
    def __init__(self, store):
        super(RDFCBORSerializer, self).__init__(store)

    def to_cbor(self):
        """Serialize to a CBOR item.

        Returns
        -------
        cbor2.item: CBOR encoding of the store.
        """
        molecule.to_cbor(self.store)

    def serialize(self, stream, base=None, encoding=None, **args):
        cbor = molecule.to_cbor(self.store)
        cbor2.dump(cbor, stream)
