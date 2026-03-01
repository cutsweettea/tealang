class ByteReprable():
    @staticmethod
    def bimport():
        raise NotImplementedError('bimport not implemented')

    def bexport(self) -> bytes:
        raise NotImplementedError('bexport not implemented')

    def _repr_vals(self, vals: list) -> bytes:
        bts = []
        for i in range(len(vals)):
            val = vals[i]
            bts.extend([i+1, *[ord(x) for x in str(val)]])

        return bytes(bts)