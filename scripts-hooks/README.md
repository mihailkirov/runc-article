Build and Launch with 

```
$> docker build -t hook . <Dockerfile
$> docker run/create --privileged -it -v $(pwd)/results-scripts/:/h00ks/results-scripts --rm hook

```

Privileged flag is needed for write access to the cgroups vfs. Circumvent with custom AppArmor profile + cgroup namespace allowing write access to runc for process isolation. 