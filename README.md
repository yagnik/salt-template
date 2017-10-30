# Salt Template [![Build Status](https://travis-ci.org/yagnik/salt-template.svg?branch=master)](https://travis-ci.org/yagnik/salt-template)

## Introduction
Setting up salt in production can require knowing a lot of details of every piece of salt and how they work. The repository provides opinioinated barebone salt setup with dev and test environment based on docker containers.

The setup was used to manage ~ 5k nodes with a team of ~ 30 core devops and ~100 developers contributing to it. 

The structure is made to balance between technical and people efficiency while ensuring stability of infrastructure. More details in the opinionated section.

## Setup
- (PREREQUISITE) Please have docker and docker-compose installed to run dev and tests environment
- Clone this repo:
```
git clone git@github.com:yagnik/saltstack-template.git
```
- Inside the directory where you cloned the repo
```
make test
```
The above will bring up docker containers using docker-compose and run tests to ensure everything is setup properly.

## Image Building
Look under [packer readme](https://github.com/yagnik/salt-template/blob/master/packer/README.md)

## Layouts and opinions
The directory structure of the repo is as follows:
- salt -> this directory houses all salt code including states and modules
- scripts -> scripts that makes it easier to work with this repo such as generating templates for custom modules and states
- templates -> templates for configs and modules
- tests -> tests that ensure validity of modules, states and team specific requirements

### Salt
The salt directory houses the extension module present in `ext` directory and the four environments most salt deployments have `base`, `dev`, `stg`, `prd`.

`ext` : The ext folder is meant to house all custom extension modules with examples of each and how to write them. Their corresponding unit tests go into `tests/unit` directory.

`base` : All salt deployments need a `base` environment to pick the pillar base from. This environment is where we put common pillars. One thing to note here is we don't put state files here. More details in `prd` section.

`dev`, `stg`, `prd` : The other three environments each houses orchestrators, pillars, reactors and states. The pillars here are merged with base environment and overwritten. Orchestrators, reactors and states on the other hand can look ahead. For example: if you have a state `foo` in prd environment, it is available in dev environment. This is possible due to our `file_roots` setting in config. This allows us to have a sane production environment while also support testing new states without the overhead of maintaining two copies of the same state.

### Tests
`integration` : Integration tests are used to test master <-> minion interaction which include state runs, orchestrations etc.

`unit` : These are unit tests for all custom modules.

`validation` : These are best practices that we enforced to ensure unwanted bugs. More details in the best practices section.


### Best Practices
- The environment should be top level concern so that code from one environment doesn't impact the other until explicitly asked.
- All python code needs to be linted by flake8
- Ensure that all state files have sane defaults and can be parsed and executed without any custom cli options
- All state files need to have core files to make it easier for future maintenance:
    + state name
        * v(major)_(minor): version folder, ensure it matches the version of the recipe you are installing
            - defaults.yaml: list of all defaults that this recipe needs, also source for all options that can be overwritten
            - init.sls:  base state where things get done by default
            - map.jinja: merge default, pillars and any logic based on os etc
            - metadata.yml: tells us which file, service, package this file edits
            - readme.me: tells what the state does and how to execute for new devs
            - requisite.sls: a state to check whether the state can be run, this was added to support the use case wherein you are upgrading a cluster and need ot ensure that no one else is doing anything
            - verify.sls: state to ensure that everything is setup correctly, cannot modify the system and is only allowed to use modules.
        * latest.sls: this points to latest stable we support
- All execution modules and state should follow same template for anyone to diggin. Convention over configuration supported through templates.
- All pillars need to have their top level key same as file name to ensure no collision. 
- All states need to have their id start from state name.
- All files are snake case.

### Gotachas
-  Add boot orchestrate to sync_all on minion start to allow custom module at boot time. https://docs.saltstack.com/en/latest/topics/reactor/#syncing-custom-types-on-minion-start
-  Unlike all other external modules, pillars are not loaded from their pluralized name. They are loaded from "_pillar" directory.


### TO-DO
- [ ] check files changed by state files and ensure they are known
- [ ] add example of encrypted pillars [nacl encryption](https://github.com/saltstack/salt/pull/41868) and [encrypted tags](https://github.com/saltstack/salt/pull/41956)
- [ ] ensure all tests are present and running
- [ ] ensure all templates are present
- [ ] ability for docker to setup container without salt-minion, salt-ssh maybe or docker salt module ?
- [ ] ability for packer to use salt rpm instead of github for salt minion setup



- [ ] test for pillars
- [ ] ensure that pillars name starts from file name
- [ ] ensure that top file has all pillars
- [ ] test for orchestration
- [ ] ensure orchestrators start with filename
- [ ] test for reactors
- [ ] ensure reactors start with filename
- [ ] test for state files
- [ ] ensure states start with filename


ext:
- [ ] test for beacons # u + i
- [ ] test for engines # u + i
- [ ] test for returners
- [ ] test fot runners # u + i
- [ ] test for state modules
- [ ] fix reactor setup
- [ ] use salt rpm instead of packer installer
