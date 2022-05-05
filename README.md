This project is a small POC on the hooks feature of *runc*. It was created as a support for the Quarkslab blogpost article on the container runtime. 
The program builds a runtime bundle and customize the default config.json file. Then a runc container is launched with the initialized bundle. 


# Customization of config.json

To customize the fields which are different from the "hooks" json field, create a json file and indicate its position using the `ADDCNF` variable within the Dockerfile.

If you want to add - hooks add the directory path where the hooks will be placed to the SCRIPT_DIR variable in the Dockerfile. Please read the format of the hooks directory.

# Hooks directory
 The hooks directory has to follow the following format:
 - <type-of-hook>
    - path

The name of the directory (here <type-of-hook>) has to be one of the following:

- **createRuntime**;
- **createContainer**;
- **startContainer**;
- **poststart  hook**;
- **poststop hook**;


Each directory must contain a file named `path` which follows the format:
- <path-to-executable>;<arguments-;-separated>

Eg:
```text
/bin/bash;-c;/h00ks/scripts-hooks/poststart/postStart.sh
```
 
The default POC scripts do the following:
- createRuntime hook - inits a network stack in a new network namespace.
- createContainer hook - tests the connectivity between the two net namespaces.
- startContainer hook - gives information about the environment.
- poststart  hook - launches a http server in the root network namespace.
- poststop hook - cleans up the network namespace and other processes.


For more information about the contexts of execution of the above processes please refer to the blogpost article.

# Build and launch
The project can be build using the standard docker build way.

## Build
```bash
$> docker build -t hook
````
## Launch
Runc needs to be able to create cgroups hence to modify the cgroups vfs which are mounted inside. The default AppArmor policy of Docker doesn't allow that hence a container has to be launched using the `privileged` flag:

```bash
$> mkdir results-scripts;
$> docker run --privileged -it -v $(pwd)/results-scripts/:/h00ks/results-scripts hook
```
After this you can observe the results of the POC scripts in the `results-scripts` directory.



