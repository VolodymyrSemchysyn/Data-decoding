def decode_binary_file(binary_data):
    offset = 0
    results = []
    temp = None

    while offset < len(binary_data):
        header = binary_data[offset:offset + 4].decode("ascii")
        offset += 4

        if header == "MIR":
            temp = struct.unpack("f", binary_data[offset:offset + 4])[0]
            offset += 4
            operator_name = binary_data[offset:offset + 20].decode("ascii").strip("\x00")
            offset += 20

        elif header == "PRR":
            part_number = struct.unpack("I", binary_data[offset:offset + 4])[0]
            offset += 4
            pass_fail = struct.unpack("B", binary_data[offset:offset + 1])[0]
            offset += 1
            results.append({"type": "PRR", "part_number": part_number, "pass_fail": pass_fail})

        elif header == "PTR":
            test_name = binary_data[offset:offset + 20].decode("ascii").strip("\x00")
            offset += 20
            test_value = struct.unpack("f", binary_data[offset:offset + 4])[0]
            offset += 4
            low_limit = struct.unpack("f", binary_data[offset:offset + 4])[0]
            offset += 4
            high_limit = struct.unpack("f", binary_data[offset:offset + 4])[0]
            offset += 4
            pass_fail = struct.unpack("B", binary_data[offset:offset + 1])[0]
            offset += 1
            results.append(
                {"type": "PTR", "test_name": test_name, "test_value": test_value, "low": low_limit, "high": high_limit,
                 "pass_fail": pass_fail})

    return {"temperature": temp, "tests": results}
