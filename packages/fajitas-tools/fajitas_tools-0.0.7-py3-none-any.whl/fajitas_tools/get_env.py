import os

def find_code_in_env_file(code_to_find):    
    if os.path.exists(".env"):
        with open(".env", 'r') as file:
            for line in file:
                if code_to_find in line:
                    value = line.split("=")[1]
                    return value
    return None