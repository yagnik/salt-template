minion_start.orchestration:
  runner.state.orchestrate:
    - mods: orch.boot
    - pillar:
        id: {{ data['id'] }}
    - saltenv: dev
