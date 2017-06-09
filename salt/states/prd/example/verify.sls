{% from "example/map.jinja" import example with context %}

example.verify.pkg.installed:
  test.succeed_without_changes:
    - name: {{ example.pkg }}