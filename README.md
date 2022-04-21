A small POC on the hooks feature of *runc*. The program builds a bundle with a custom config.json file. The hooks section of this file is filled with the contents of the scripts-hooks directory. Each represents a type of hook and contains files to be executed by the hook process. Each directory contains a file named `path` which contains the following data **for each file in the directory** :
- <path-to-executable>
- <arguments>
 
 If you have 3 scripts in this directory you'll have 6 lines in this file. Each line corresponds to a uniaque file in an alphabetic order. 

The default POC h00ks do the following:

- createRuntime hook - inits a network stack in a new network namespace.
- createContainer hook - tests the connectivity between the two net namespaces.
- startContainer hook - gives information about the environment.
- poststart  hook - launches a http server in the root network namespace.
- poststop hook - cleans up the network namespace and other processes.

For more information about the contexts of execution of the above processes please refer to the article.

Build and Launch with 
```
$> docker build -t hook . < Dockerfile
$> docker run --privileged -it -v $(pwd)/results-scripts/:/h00ks/results-scripts hook

```

Privileged flag is needed for write access to the cgroups vfs. 