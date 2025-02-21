import struct

from fastapi import HTTPException

from src.schemas.data import EditFileRequest


def encode_binary_file(data: EditFileRequest):
    binary_data = bytearray()

    try:
        binary_data.extend("MIR".encode("latin-1").ljust(4, b"\x00"))
        binary_data.extend(struct.pack("f", data.temperature))
        operator_name = data.operator.ljust(20, "\x00")
        binary_data.extend(operator_name.encode("latin-1"))

        for test in data.tests:
            if test.type == "PRR":
                binary_data.extend("PRR".encode("latin-1").ljust(4, b"\x00"))
                binary_data.extend(struct.pack("I", test.part_number))
                binary_data.extend(struct.pack("B", test.pass_fail))

            elif test.type == "PTR":
                binary_data.extend("PTR".encode("latin-1").ljust(4, b"\x00"))
                test_name = test.test_name.ljust(20, "\x00")
                binary_data.extend(test_name.encode("latin-1"))
                binary_data.extend(struct.pack("f", test.test_value))
                binary_data.extend(struct.pack("f", test.low))
                binary_data.extend(struct.pack("f", test.high))
                binary_data.extend(struct.pack("B", test.pass_fail))

        return binary_data

    except KeyError as e:
        print(f"Error: Missing key in parsed data - {e}")
        return HTTPException(status_code=400, detail="Missing key in parsed data")
    except struct.error as e:
        print(f"Error packing binary data: {e}")
        raise HTTPException(status_code=400, detail="Error packing binary data")

