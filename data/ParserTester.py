import io
import struct
import data.SubControllers as ctrl
import data.CompleteParserClasses as cpc

stream = io.BytesIO()

stream.write(struct.pack('>Q', 12))
stream.write(struct.pack('>B', 1))

stream.seek(0)
version = struct.unpack(">Q", stream.read(8))[0]
a = cpc.binaryFileMapForCompleteParser[version]()
a.generate(a, stream)
print(a)
a.update()