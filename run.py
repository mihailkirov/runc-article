#!/usr/bin/python3
"""Runs runc to generate default config.json.
    The contents of which is then updated with
    the contents of the configuration file passed as parameter.
    Python3 required
"""
import sys
import os
import json
import subprocess


def read_json(path:str) -> dict:
    """Read json file referenced by path"""

    with open(path, "r") as file:
        js_new = json.load(file)
        return js_new


def generate_config_return_json() -> dict:
    """The function generates a default config.json 
       using `runc spec` and then returns it as json (dict)
    """
    
    bundle_dir = os.environ["CDIR"] + "/bundle"
    with subprocess.Popen([
        "/bin/sh", 
        "-c", 
         "rm -f config.json; \
         runc spec;"],
         cwd=bundle_dir
         ) as proc: # async
        proc.wait()
        if proc.returncode != 0:
            return None  
        return read_json("{}/config.json".format(bundle_dir))


def customize(org_conf:dict) -> None: 
    """Add custom configuration to org_conf (config.json).
       ADDCNF - indicates configuration not related to hooks 
       SCRIPT_DIR - indicates configuration related to hooks. 
    """

    if "ADDCNF" in os.environ:
        additional_cnf = read_json(os.environ["ADDCNF"])
        for field in additional_cnf.keys():
            org_conf[field] = additional_cnf[field]

    if "SCRIPT_DIR" in os.environ:
        # add hooks
        org_conf["hooks"] = generate_hooks()

def generate_hooks() -> dict:
    """ Generates and returns dictionary object. 
        The object represents hooks in runc.
        Keys : types of hooks;
        Values: paths to executables;
        The generation is done by parsing the SCRIT_DIR directory
        composed by subdirectories holding hook scripts of each type.
        The names of the subdirectories must be the same as the hooks names 
        which scripts they hold. 
    """

    hooks_dict = {}
    for root, dirs, _ in os.walk(os.environ["SCRIPT_DIR"]):
        if not dirs:
            # type of hook in dict := name of the dir 
            hook_type = root.split("/")[-1]
            hooks_dict[hook_type] = []
            # parse the path file
            with open(root + "/" + "path") as file:
                for line in file:
                    # separate path and arguments
                    cmdl = line.strip().split(';')
                    obj = {
                        "path": cmdl[0],
                        "args": [str(cmdl[arg]) for arg in range(1, len(cmdl))]
                    }
                    obj["args"].insert(0, cmdl[0]) # POSIX classics    
                    hooks_dict[hook_type] += [obj]
    return hooks_dict


def run() -> None:
    """Runs runc with the created bundle.
       Program flow: create, start, delete.
       For the meaning of the env variables check 'runc --help'
    """

    print("Creating..")
    # create
    with subprocess.Popen([
        "/bin/bash", "-c", "runc {gopt} create -b {bundle} {cname} &"
        .format(bundle=os.environ["BUNDLEDIR"], gopt=os.environ["GOPT"], 
            cname=os.environ["CNAME"])], stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, stdin=subprocess.PIPE) as proc: # async
        proc.wait()
        if proc.returncode != 0:
            print(proc.stderr)
            sys.exit(proc.returncode)
     
    yield "Create phase completed"
    print("Starting..")
    # start
    with subprocess.Popen([
        "/bin/bash", "-c", "runc start c "
        ]) as proc: # async
        proc.wait()
        if proc.returncode != 0:
            print(proc.stderr)
            sys.exit(proc.returncode)
    
    yield "Start phase completed"
    print("Deleting...")
    # delete
    with subprocess.Popen([
        "/bin/sh", "-c", "runc delete c "
        ]) as proc: # async
        proc.wait()
        if proc.returncode != 0:
            print(proc.stderr)
            sys.exit(proc.returncode)
 
    print("Delete phase completed") 
    sys.exit(0)


def main():
    """Main function"""

    # call runc for config.json generation
    org_conf = generate_config_return_json()
    if not org_conf:
        sys.exit(-1)
    # customize the original configuration of runc
    customize(org_conf)
    # write down the configuration file
    with open("{}/config.json".format(os.environ["BUNDLEDIR"]), "w") as file1: # erases old content
        file1.write(json.dumps(org_conf))
    # launch
    for msg in run():
        print("{msg}\nContinue? [press enter]".format(msg=msg))
        input()

if __name__ == "__main__":

    main()
