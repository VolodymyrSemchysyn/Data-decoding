def encode_binary_file(parsed_data):
    binary_data = bytearray()

    binary_data.extend("MIR".encode("ascii"))
    binary_data.extend(struct.pack("f", parsed_data["temperature"]))
    operator_name = parsed_data.get("operator", "Unknown").ljust(20, "\x00")
    binary_data.extend(operator_name.encode("ascii"))

    for test in parsed_data["tests"]:
        if test["type"] == "PRR":
            binary_data.extend("PRR".encode("ascii"))
            binary_data.extend(struct.pack("I", test["part_number"]))
            binary_data.extend(struct.pack("B", test["pass_fail"]))

        elif test["type"] == "PTR":
            binary_data.extend("PTR".encode("ascii"))
            test_name = test["test_name"].ljust(20, "\x00")
            binary_data.extend(test_name.encode("ascii"))
            binary_data.extend(struct.pack("f", test["test_value"]))
            binary_data.extend(struct.pack("f", test["low"]))
            binary_data.extend(struct.pack("f", test["high"]))
            binary_data.extend(struct.pack("B", test["pass_fail"]))

    return binary_data
