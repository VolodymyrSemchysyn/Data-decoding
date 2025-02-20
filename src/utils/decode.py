import struct

def decode_binary_file(filename: str):
    results = []
    temp = None
    operator_name = None

    with open(filename, "rb") as f:

        while True:
            header = f.read(4)
            if not header:
                break

            header = header.decode("latin-1").strip("\x00")
            print(header)
            if header == "MIR":
                temp = struct.unpack("f", f.read(4))[0]
                operator_name = f.read(20).decode("latin-1").strip("\x00")
            elif header == "PRR":
                part_number = struct.unpack("I", f.read(4))[0]
                pass_fail = struct.unpack("B", f.read(1))[0]
                results.append({"type": "PRR", "part_number": part_number, "pass_fail": pass_fail})
            elif header == "PTR":
                test_name = f.read(20).decode("latin-1").strip("\x00")
                test_value = struct.unpack("f", f.read(4))[0]
                low_limit = struct.unpack("f", f.read(4))[0]
                high_limit = struct.unpack("f", f.read(4))[0]
                pass_fail = struct.unpack("B", f.read(1))[0]
                results.append({
                    "type": "PTR",
                    "test_name": test_name,
                    "test_value": test_value,
                    "low": low_limit,
                    "high": high_limit,
                    "pass_fail": pass_fail,
                })

        return {"temperature": temp, "operator": operator_name, "tests": results}
