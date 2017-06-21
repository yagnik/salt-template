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
- [x] versioning of packages for state files
- [x] prereq.sls if you allow version upgrade, cluster health check maybe ?
- [x] metadata.yaml for state files to list versions, files and packages managed by state
- [x] add test to run prereq.sls
- [x] add test to check metadata schema
- [ ] check files changed by state files and ensure they are known
- [ ] add code for base image, base image and repo lockdown
- [x] orch for sync_all on minion start
- [ ] add support for auto documentation
- [ ] add support for beacons and setup for logical event processing
- [ ] add example for encrypted pillars
