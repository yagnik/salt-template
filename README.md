# Saltstack
The repo is a template for saltstack setup in production environment.
It includes:
- [x] directory layout
- [x] code linting using flake8 (pep8 + pylint + circular dependency)
- [x] enforce state file parsing and execution tests
- [x] create templates for new states -> create state, pillar, example for accessing modules, grains etc
- [x] build cli for templating
- [x] dev environment setup 
- [ ] testing environment 
- [ ] add support for encrypted pillars
- [ ] add support for auto documentation
- [ ] versioning of packages for state files
- [ ] check files changed by state files and ensure they are known
- [ ] add coed for base image
- [ ] make sure base image and repo are synced and tested
- [ ] change docker images to use to base image
- [ ] add support for ssh roster for verification
