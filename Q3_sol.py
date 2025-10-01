class _classtlv_verify_:
    def __init__(self, file):
        self.file = file

    def tlv_verify(self):
        with open(self.file, "rb") as f:                          # read file in bin mode
            data = f.read()                                       # read all bytes at once

        i = 0                                                     # indexing i to 0th byte - initializing
        data_len = len(data)                                      # total length of data
        data_chk = 0                                              # track parsed data - check

        # open file to save console output
        with open("result.txt", "w") as result:

            while i + 2 <= data_len:                              # at least type+length must remain
                start_offset = i                                  # offset of the Type byte
                typ_val = data[i]                                 # Type is 1 byte
                len_val = data[i + 1]                             # Length is 1 byte
                i += 2                                            # move pointer past type+length
                data_chk += 2

                if i + len_val > data_len:                        # check if enough bytes remain
                    line = f"Malformed TLV at offset 0x{start_offset:06x}: t={typ_val} l={len_val} -> not enough bytes (remaining {data_len - i})"
                    print(line)
                    result.write(line + "\n")
                    break

                byte_val = data[i:i + len_val]                    # slice out value part
                i += len_val                                      # move pointer past value
                data_chk += len_val

                # ascii - string decode and encode to num
                try:
                    ascii_val = byte_val.decode('ascii')         # decode as string
                except Exception:
                    ascii_val = None

                ascii_disp = f"{ascii_val}" if ascii_val is not None else byte_val.hex()

                # Determine PASS/FAIL
                if typ_val == 5:
                    try:
                        str_val = byte_val.decode('ascii')       #encode number
                        encoded_num = float(str_val)
                        status = "PASS" if encoded_num > 3.30 else "FAIL"
                        line = f"{status} [t={typ_val}, l={len_val}, v={ascii_val}]"
                    except Exception:
                        line = f"FAIL [t={typ_val}, l={len_val}, v={ascii_disp}]"
                else:
                    line = f"FAIL [t={typ_val}, l={len_val}, v={ascii_disp}]"     # other tlv fails

                # print to console
                print(line)

                # write to result.txt
                result.write(line + "\n")


# main fn
if __name__ == "__main__":
    filename = input("Enter the binary filename: ")
    print("_____________________________________\n")
    verifier = _classtlv_verify_(filename)
    verifier.tlv_verify()
    print("\nAll console output also saved in result.txt")
