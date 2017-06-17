# Saltstack
The repo is a template for saltstack setup in production environment.
It includes:
- [x] directory layout
- [x] code linting using flake8 (pep8 + pylint + circular dependency)
- [x] enforce state file parsing and execution tests
- [x] create templates for new states -> create state, pillar, example for accessing modules, grains etc
- [x] build cli for templating
- [x] dev environment setup 
- [x] testing environment 
- [ ] add example for encrypted pillars
- [x] versioning of packages for state files
- [ ] prereq.sls if you allow version upgrade, cluster health check maybe ?
- [ ] check files changed by state files and ensure they are known
- [ ] add code for base image, base image and repo lockdown
- [ ] salt state for master or minion
- [ ] orch for sync_all on minion start
- [ ] add support for auto documentation
- [ ] ask if you want to overwrite template files
- [ ] ensure that all pillars and grains are used at top of file and set as variable
