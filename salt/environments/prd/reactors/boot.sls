minion_start.orchestration:
  runner.state.orchestrate:
    - mods: boot
    - pillar:
        id: {{ data['id'] }}
    - saltenv: prd
