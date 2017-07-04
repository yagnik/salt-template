# Image creation using Packer

In order to build deterministic images across the platform we are leveraging packer by hashicorp. 

The centos directory hosts three files:
- pack.json: packer template which is the main file
- variables.json: all variables used in the packer build which can be changed
- salt.repo: centos 7 salt repo file 


## How to build docker image?
- [PREREQUISITE] install packer and put it on your path
- Execute the following command
```
packer build -var-file=packer/centos/variables.json packer/centos/pack.json
```
- The above command will finish and commit an image which can be seen with `docker images`


## Underneath ?

To build the images we execute salt 'base' state in order to bring it to the state where we expect it to be. Hence all the code and core packages move to base.
