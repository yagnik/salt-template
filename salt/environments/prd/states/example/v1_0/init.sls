{% from "example/v1_0/map.jinja" import example with context %}

example.pkg:
  test.succeed_without_changes:
    - name: {{ example.pkg }}
