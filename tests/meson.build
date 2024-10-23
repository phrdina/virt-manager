pylint_prog = find_program(['pylint', 'pylint-3'])
# meson sets this MALLOC_PERTURB_ to random value by default but it
# doesn't work correctly with pylint so we need to override it
nomalloc = environment({'MALLOC_PERTURB_': '0'})
test(
  'pylint',
  pylint_prog,
  args: [
    'virtManager/virtmanager.py',
    'tests', 'virtinst', 'virtManager',
    '--rcfile', '.pylintrc',
  ],
  env: nomalloc,
  workdir: meson.project_source_root(),
  timeout: 300,
)

pytest_prog = find_program(['pytest', 'pytest-3'])
test(
  'pytest',
  pytest_prog,
  workdir: meson.project_source_root(),
  timeout: 300,
)

pycodestyle_prog = find_program(['pycodestyle', 'pycodestyle-3'])
test(
  'pycodestyle',
  pycodestyle_prog,
  args: [
    '--config', 'setup.cfg',
    '--format', 'pylint',
    'tests', 'virtinst', 'virtManager'
  ],
  workdir: meson.project_source_root(),
)

codespell_prog = find_program('codespell', required:false)
if codespell_prog.found()
  test(
    'codespell',
    codespell_prog,
    args: [
      '--ignore-words', 'tests/data/codespell_dict.txt',
      '--skip', '*.pyc,*.iso,*.xml,NEWS.md',
      'tests', 'virtinst', 'virtManager',
      '*.md', 'man/*.rst',
      'data/virt-manager.appdata.xml.in',
      'data/virt-manager.desktop.in',
      'data/org.virt-manager.virt-manager.gschema.xml',
      'virt-manager.spec',
    ],
    workdir: meson.project_source_root(),
  )
endif
