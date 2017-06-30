{% set id = pillar.get('id') %}

boot.sync_all:
  salt.function:
    - name: saltutil.sync_all
    - tgt: '{{ id }}'

boot.state.run:
  salt.state:
    - tgt: '{{ id }}'
    - sls:
      - example.latest
    - require:
      - salt: boot.sync_all
