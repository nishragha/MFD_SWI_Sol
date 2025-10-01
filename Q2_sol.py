import json
import re

class _Response_Verifier:                                          #class to verify response from .json file
    def __init__(self, filepath):
        with open(filepath) as f:                                   # Load JSON data from file
            self.data = json.load(f)
        self.hex_verify = re.compile(r"^[0-9A-Fa-f]{6}$")           # Regex pattern to verify Result4 has valid 6 HEX char

    #check Results for each Response
    def _resp_check_(self, vals):
        verify = {}
        
        verify["Result1"] = "PASS" if vals["Result1"] == "PASSED" else f"FAIL ({vals['Result1']})"          # Verify Result1: must be 'PASSED'
        
        verify["Result2"] = "PASS" if vals["Result2"] >= 3.30 else f"FAIL ({vals['Result2']} < 3.30V)"      # Verify Result2: voltage >= 3.30V
        
        r3_val = int(vals["Result3"].rstrip('%'))                                                           # Verify Result3: percentage >= 80%
        verify["Result3"] = "PASS" if r3_val >= 80 else f"FAIL ({vals['Result3']} < 80%)"
        
        verify["Result4"] = "PASS" if self.hex_verify.fullmatch(vals["Result4"]) else f"FAIL ({vals['Result4']} invalid HEX)"         # Verify Result4: exactly 6 HEX characters
        
        Final_Response = all(v.startswith("PASS") for v in verify.values())                               # Final Result: PASS only if all Result pass
        verify["Total"] = "PASS" if Final_Response else "FAIL"
        return verify

    # Output Result on console
    def _write_output_(self):
        for i, resp in enumerate(self.data, 1):                                                           #Iterate through all Responses
            name = f"RESPONSE{i}"  
            vals = resp[f"Response{i}"]
            verify = self._resp_check_(vals)                                                              # Verify this response

            print(f"\n{name}: {verify['Total']}\n")                                                       # console print Response Result
            for k in ["Result1", "Result2", "Result3", "Result4"]:
                print(f"  {k}: {verify[k]}")
            print("_______________________________")

        print("\n VERIFICATION COMPLETE!")     
        


if __name__ == "__main__":
    filepath = input("Enter JSON file: ").strip()
    print("_______________________________")                                                # user input .json file
    try:
        verifier = _Response_Verifier(filepath)
        verifier._write_output_()
    except FileNotFoundError:
        print(f"Error: File '{filepath}' Missing.")
    except json.JSONDecodeError:
        print("Error: Invalid JSON format.")