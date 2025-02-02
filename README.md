A short function to copy my files to a remote host without having me type the command over and over again. Here is how I fit this into my workflow: 

### Create a new config
./c2r -n {local_path} {username} {hostname} {key_filename}
--> key_filename is optional 
--> if hostname is going to be changing a lot, give dummy hostname and specify when running the config

 ### Show all configs
 ./c2r -ls (-v for verbose)
 --> prints all configs (and information if -v)

### Execute a certain config 
./c2r -r {config number} (--host a.b.c) 
--> executes the scp command on a specified config 
--> contains optional parameter to specify a custom host (i.e. you launch/connect to a new instance each time)

Here is how I use this. I will launch a new instance/cluster and get the IP. I have created a config with necessary information, and then run ```./c2r -r 1 --host {ip addr}```. 
