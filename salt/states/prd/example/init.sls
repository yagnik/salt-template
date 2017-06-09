{% from "example/map.jinja" import example with context %}

example.pkg:
  test.succeed_without_changes:
    - name: {{ example.pkg }}
