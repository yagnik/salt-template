base:
  '*':
    - schedule
    - encrypted

dev:
  '*-dev-*':
    - example

stg:
  '*-stg-*':
    - example

prd:
  '*-prd-*':
    - example
