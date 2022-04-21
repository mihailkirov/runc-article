#!/usr/bin/python3
"""Runs runc to generate default config.json.
    The contents of which is then updated with
    the contents of the configuration file passed as parameter.
    Python3 required
"""

import sys
import os
import time
import json
import subprocess
import time


def read_json(path:str) -> dict:
    """Read a json config referenced by path.
        Could potentially raise exceptions (eg: if no valid json data).
    """

    with open(path, "r") as file:
        js_new = json.load(file)
        return js_new

def generate_config_return_json() -> dict:
    """Generates a config with runc and returns the result
        as a JSON object. Could potentially raise exceptions.
    """
    d = os.environ["CDIR"] + "/bundle"
    with subprocess.Popen([
        "/bin/sh", "-c", "cd {n1}; \
         rm {n2}/config.json 2>/dev/null; \
         runc spec;".format(n1=d, n2=d)
        ]) as proc: # async
        proc.wait()
        if proc.returncode != 0:
            return None  
        return read_json("{}/config.json".format(os.environ["CDIR"] + "/bundle"))



def generate_hooks_from_files() -> dict:
    """Generate hooks from directory scripthooks"""

    hooks_dict = {}
    for root, dirs, files in os.walk(os.environ["SCRIPT_DIR"]):

        if not dirs:
            # init the type of hook
            hook_type = root.split("/")[-1]
            hooks_dict[hook_type] = []

            with open(root + "/" + "path") as file:
                # read paths & shell info
                path_shells = file.readlines()
                # small sec checks
                if files.pop(files.index("path")) != "path":
                    return None

                length1, length2 = len(path_shells), len(files)
                if length1 % 2 != 0 or length2 != length1/2:
                    return None

                # parse the directory and construct JSON objects
                f_numb = 0
                for line in range(0, len(path_shells) - 1, 2):
                    # path to shell script
                    if path_shells[line+1] == '.':
                        path = "{}/{}".format(root, files[f_numb])
                    else:
                        path = path_shells[line+1]

                    # construct json object
                    obj = {
                     "path": path_shells[line].strip(),
                     "args": [path_shells[line].strip(), "-c", path.strip()]
                    }
                    # add it to the list of scripts of the given hook
                    hooks_dict[hook_type] += [obj]
                    # next file in the directory
                    f_numb += 1

    return hooks_dict


def run():
    """Runs runc.Program flow: create, start, delete"""

    print("Creating..")
    # create
    with subprocess.Popen([
        "/bin/sh", "-c", "runc create -b {} c".format(os.environ["CDIR"] + "/bundle")
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE) as proc: # async
        time.sleep(1)  
    
    print("Starting..")
    # start
    with subprocess.Popen([
        "/bin/sh", "-c", "runc start c "
        ]) as proc: # async
        proc.wait()
        if proc.returncode != 0:
            return None
        # check stdout too
    time.sleep(1)
    print("Deleting")
    # delete
    with subprocess.Popen([
        "/bin/sh", "-c", "runc delete c "
        ]) as proc: # async
        proc.wait()
        if proc.returncode != 0:
            return None

    sys.exit(0)

if __name__ == "__main__":

    # call runc for config.json generation
    org_conf = generate_config_return_json()
    if not org_conf:
        sys.exit(-1)
    org_conf["process"]["terminal"] = False # incompatible with the current prog
    org_conf["hooks"] = generate_hooks_from_files()
    if not org_conf["hooks"]:
        sys.exit(-1)
    # this is truly custom
    if "ADDCNF" in os.environ:
        additional_cnf = read_json(os.environ["ADDCNF"])
        for field in additional_cnf.keys():
            org_conf[field] = additional_cnf[field]

    # write down the modification
    with open("./bundle/config.json", "w") as file1: # erases old content
        file1.write(json.dumps(org_conf))
    # launch
    run()
