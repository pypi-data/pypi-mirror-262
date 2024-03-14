#!/usr/bin/env python3
# test_helptext.py - helptext module test suite

import pytest
from helptext import parse


def test_no_inputs():
    args = []
    doc = ''
    opts, operands = parse(args, doc)
    assert opts == {}
    assert operands == []


def test_operands():
    args = ['lorem', 'ipsum']
    doc = ''
    opts, operands = parse(args, doc)
    assert opts == {}
    assert operands == ['lorem', 'ipsum']


def test_operands_dash():
    args = ['lorem', '-', 'ipsum']
    doc = ''
    opts, operands = parse(args, doc)
    assert opts == {}
    assert operands == ['lorem', '-', 'ipsum']


def test_operands_double_dash():
    args = ['lorem', '--', '-a', 'ipsum']
    doc = ''
    opts, operands = parse(args, doc)
    assert opts == {}
    assert operands == ['lorem', '-a', 'ipsum']


def test_invalid_option():
    args = ['-a']
    doc = ''
    with pytest.raises(ValueError):
        opts, operands = parse(args, doc)


def test_invalid_definition_dash():
    args = []
    doc = '-'
    opts, operands = parse(args, doc)
    assert opts == {}
    assert operands == []


def test_invalid_definition_double_dash():
    args = []
    doc = '--'
    opts, operands = parse(args, doc)
    assert opts == {}
    assert operands == []


def test_invalid_definition_triple_dash():
    args = []
    doc = '---'
    opts, operands = parse(args, doc)
    assert opts == {}
    assert operands == []


def test_invalid_definition_short_no_alnums():
    args = []
    doc = '-?'
    opts, operands = parse(args, doc)
    assert opts == {}
    assert operands == []


def test_invalid_definition_long_no_alnums():
    args = []
    doc = '--?'
    opts, operands = parse(args, doc)
    assert opts == {}
    assert operands == []


def test_invalid_definition_long_short():
    args = []
    doc = '-alpha'
    opts, operands = parse(args, doc)
    assert opts == {}
    assert operands == []


def test_shortopt_defaults():
    args = []
    doc = '-a'
    opts, operands = parse(args, doc)
    assert '-a' in opts
    assert opts['-a']['flags'] == ['-a']
    assert opts['-a']['argument'] is False
    assert opts['-a']['enabled'] == 0
    assert opts['-a']['value'] is None
    assert operands == []


def test_shortopt_enabled():
    args = ['-a']
    doc = '-a'
    opts, operands = parse(args, doc)
    assert '-a' in opts
    assert opts['-a']['flags'] == ['-a']
    assert opts['-a']['argument'] is False
    assert opts['-a']['enabled'] == 1
    assert opts['-a']['value'] is None
    assert operands == []


def test_shortopt_enabled_count():
    args = ['-a', '-a']
    doc = '-a'
    opts, operands = parse(args, doc)
    assert '-a' in opts
    assert opts['-a']['flags'] == ['-a']
    assert opts['-a']['argument'] is False
    assert opts['-a']['enabled'] == 2
    assert opts['-a']['value'] is None
    assert operands == []


def test_shortopt_enabled_combined():
    args = ['-ab']
    doc = '-a\n-b'
    opts, operands = parse(args, doc)
    assert '-a' in opts
    assert '-b' in opts
    assert opts['-a']['flags'] == ['-a']
    assert opts['-a']['argument'] is False
    assert opts['-a']['enabled'] == 1
    assert opts['-a']['value'] is None
    assert opts['-b']['flags'] == ['-b']
    assert opts['-b']['argument'] is False
    assert opts['-b']['enabled'] == 1
    assert opts['-b']['value'] is None
    assert operands == []


def test_shortopt_enabled_count_combined():
    args = ['-aaa']
    doc = '-a'
    opts, operands = parse(args, doc)
    assert '-a' in opts
    assert opts['-a']['flags'] == ['-a']
    assert opts['-a']['argument'] is False
    assert opts['-a']['enabled'] == 3
    assert opts['-a']['value'] is None
    assert operands == []


def test_operands_order():
    args = ['lorem', '-a', 'ipsum']
    doc = '-a arg'
    opts, operands = parse(args, doc)
    assert '-a' in opts
    assert opts['-a']['flags'] == ['-a']
    assert opts['-a']['argument'] is True
    assert opts['-a']['enabled'] == 1
    assert opts['-a']['value'] == 'ipsum'
    assert operands == ['lorem']


def test_operands_order_posix():
    args = ['lorem', '-a', 'ipsum']
    doc = '-a arg'
    opts, operands = parse(args, doc, posixly_correct=True)
    assert '-a' in opts
    assert opts['-a']['flags'] == ['-a']
    assert opts['-a']['argument'] is True
    assert opts['-a']['enabled'] == 0
    assert opts['-a']['value'] is None
    assert operands == ['lorem', '-a', 'ipsum']


def test_shortopt_argument():
    args = ['-a', 'lorem', 'ipsum']
    doc = '-a arg'
    opts, operands = parse(args, doc)
    assert '-a' in opts
    assert opts['-a']['flags'] == ['-a']
    assert opts['-a']['argument'] is True
    assert opts['-a']['enabled'] == 1
    assert opts['-a']['value'] == 'lorem'
    assert operands == ['ipsum']


def test_shortopt_argument_missing():
    args = ['-a']
    doc = '-a arg'
    with pytest.raises(ValueError):
        opts, operands = parse(args, doc)


def test_shortopt_argument_unexpected():
    args = ['-alorem']
    doc = '-a'
    with pytest.raises(ValueError):
        opts, operands = parse(args, doc)


def test_shortopt_argument_empty():
    args = ['-a', '', 'ipsum']
    doc = '-a arg'
    opts, operands = parse(args, doc)
    assert '-a' in opts
    assert opts['-a']['flags'] == ['-a']
    assert opts['-a']['argument'] is True
    assert opts['-a']['enabled'] == 1
    assert opts['-a']['value'] == ''
    assert operands == ['ipsum']


def test_shortopt_argument_prefixed():
    args = ['-a', '-b', 'ipsum']
    doc = '-a arg'
    opts, operands = parse(args, doc)
    assert '-a' in opts
    assert opts['-a']['flags'] == ['-a']
    assert opts['-a']['argument'] is True
    assert opts['-a']['enabled'] == 1
    assert opts['-a']['value'] == '-b'
    assert operands == ['ipsum']


def test_shortopt_argument_attached():
    args = ['-alorem', 'ipsum']
    doc = '-a arg'
    opts, operands = parse(args, doc)
    assert '-a' in opts
    assert opts['-a']['flags'] == ['-a']
    assert opts['-a']['argument'] is True
    assert opts['-a']['enabled'] == 1
    assert opts['-a']['value'] == 'lorem'
    assert operands == ['ipsum']


def test_shortopt_argument_combined():
    args = ['-abc', 'lorem', 'ipsum']
    doc = '-a\n-b\n-c arg'
    opts, operands = parse(args, doc)
    assert '-a' in opts
    assert '-b' in opts
    assert '-c' in opts
    assert opts['-a']['flags'] == ['-a']
    assert opts['-a']['argument'] is False
    assert opts['-a']['enabled'] == 1
    assert opts['-a']['value'] is None
    assert opts['-b']['flags'] == ['-b']
    assert opts['-b']['argument'] is False
    assert opts['-b']['enabled'] == 1
    assert opts['-b']['value'] is None
    assert opts['-c']['flags'] == ['-c']
    assert opts['-c']['argument'] is True
    assert opts['-c']['enabled'] == 1
    assert opts['-c']['value'] == 'lorem'
    assert operands == ['ipsum']


def test_shortopt_argument_combined_attached():
    args = ['-abclorem', 'ipsum']
    doc = '-a\n-b\n-c arg'
    opts, operands = parse(args, doc)
    assert '-a' in opts
    assert '-b' in opts
    assert '-c' in opts
    assert opts['-a']['flags'] == ['-a']
    assert opts['-a']['argument'] is False
    assert opts['-a']['enabled'] == 1
    assert opts['-a']['value'] is None
    assert opts['-b']['flags'] == ['-b']
    assert opts['-b']['argument'] is False
    assert opts['-b']['enabled'] == 1
    assert opts['-b']['value'] is None
    assert opts['-c']['flags'] == ['-c']
    assert opts['-c']['argument'] is True
    assert opts['-c']['enabled'] == 1
    assert opts['-c']['value'] == 'lorem'
    assert operands == ['ipsum']


def test_longopt_defaults():
    args = []
    doc = '--alpha'
    opts, operands = parse(args, doc)
    assert '--alpha' in opts
    assert opts['--alpha']['flags'] == ['--alpha']
    assert opts['--alpha']['argument'] is False
    assert opts['--alpha']['enabled'] == 0
    assert opts['--alpha']['value'] is None
    assert operands == []


def test_longopt_posix():
    args = []
    doc = '--alpha'
    opts, operands = parse(args, doc, posixly_correct=True)
    assert opts == {}
    assert operands == []


def test_longopt_words():
    args = []
    doc = '--alpha-beta-gamma'
    opts, operands = parse(args, doc)
    assert '--alpha-beta-gamma' in opts
    assert opts['--alpha-beta-gamma']['flags'] == ['--alpha-beta-gamma']
    assert opts['--alpha-beta-gamma']['argument'] is False
    assert opts['--alpha-beta-gamma']['enabled'] == 0
    assert opts['--alpha-beta-gamma']['value'] is None
    assert operands == []


def test_longopt_enabled():
    args = ['--alpha']
    doc = '--alpha'
    opts, operands = parse(args, doc)
    assert '--alpha' in opts
    assert opts['--alpha']['flags'] == ['--alpha']
    assert opts['--alpha']['argument'] is False
    assert opts['--alpha']['enabled'] == 1
    assert opts['--alpha']['value'] is None
    assert operands == []


def test_longopt_enabled_words():
    args = ['--alpha-beta-gamma']
    doc = '--alpha-beta-gamma'
    opts, operands = parse(args, doc)
    assert '--alpha-beta-gamma' in opts
    assert opts['--alpha-beta-gamma']['flags'] == ['--alpha-beta-gamma']
    assert opts['--alpha-beta-gamma']['argument'] is False
    assert opts['--alpha-beta-gamma']['enabled'] == 1
    assert opts['--alpha-beta-gamma']['value'] is None
    assert operands == []


def test_longopt_enabled_count():
    args = ['--alpha', '--alpha']
    doc = '--alpha'
    opts, operands = parse(args, doc)
    assert '--alpha' in opts
    assert opts['--alpha']['flags'] == ['--alpha']
    assert opts['--alpha']['argument'] is False
    assert opts['--alpha']['enabled'] == 2
    assert opts['--alpha']['value'] is None
    assert operands == []


def test_longopt_shortened():
    args = ['--a', '--al', '--alp', '--alph']
    doc = '--alpha'
    opts, operands = parse(args, doc)
    assert '--alpha' in opts
    assert opts['--alpha']['flags'] == ['--alpha']
    assert opts['--alpha']['argument'] is False
    assert opts['--alpha']['enabled'] == 4
    assert opts['--alpha']['value'] is None
    assert operands == []


def test_longopt_shortened_overlap():
    args = ['--alpha']
    doc = '--alpha\n--alphabet'
    opts, operands = parse(args, doc)
    assert '--alpha' in opts
    assert '--alphabet' in opts
    assert opts['--alpha']['flags'] == ['--alpha']
    assert opts['--alpha']['argument'] is False
    assert opts['--alpha']['enabled'] == 1
    assert opts['--alpha']['value'] is None
    assert opts['--alphabet']['flags'] == ['--alphabet']
    assert opts['--alphabet']['argument'] is False
    assert opts['--alphabet']['enabled'] == 0
    assert opts['--alphabet']['value'] is None
    assert operands == []


def test_longopt_shortened_ambiguous():
    args = ['--al']
    doc = '--alpha\n--alternate'
    with pytest.raises(ValueError):
        opts, operands = parse(args, doc)


def test_longopt_argument():
    args = ['--alpha', 'lorem', 'ipsum']
    doc = '--alpha arg'
    opts, operands = parse(args, doc)
    assert '--alpha' in opts
    assert opts['--alpha']['flags'] == ['--alpha']
    assert opts['--alpha']['argument'] is True
    assert opts['--alpha']['enabled'] == 1
    assert opts['--alpha']['value'] == 'lorem'
    assert operands == ['ipsum']


def test_longopt_argument_missing():
    args = ['--alpha']
    doc = '--alpha arg'
    with pytest.raises(ValueError):
        opts, operands = parse(args, doc)


def test_longopt_argument_unexpected():
    args = ['--alpha=lorem']
    doc = '--alpha'
    with pytest.raises(ValueError):
        opts, operands = parse(args, doc)


def test_longopt_argument_prefixed():
    args = ['--alpha', '--beta', 'ipsum']
    doc = '--alpha arg'
    opts, operands = parse(args, doc)
    assert '--alpha' in opts
    assert opts['--alpha']['flags'] == ['--alpha']
    assert opts['--alpha']['argument'] is True
    assert opts['--alpha']['enabled'] == 1
    assert opts['--alpha']['value'] == '--beta'
    assert operands == ['ipsum']


def test_longopt_argument_attached():
    args = ['--alpha=lorem', 'ipsum']
    doc = '--alpha=arg'
    opts, operands = parse(args, doc)
    assert '--alpha' in opts
    assert opts['--alpha']['flags'] == ['--alpha']
    assert opts['--alpha']['argument'] is True
    assert opts['--alpha']['enabled'] == 1
    assert opts['--alpha']['value'] == 'lorem'
    assert operands == ['ipsum']


def test_longopt_argument_attached_empty():
    args = ['--alpha=', 'lorem', 'ipsum']
    doc = '--alpha=arg'
    opts, operands = parse(args, doc)
    assert '--alpha' in opts
    assert opts['--alpha']['flags'] == ['--alpha']
    assert opts['--alpha']['argument'] is True
    assert opts['--alpha']['enabled'] == 1
    assert opts['--alpha']['value'] == ''
    assert operands == ['lorem', 'ipsum']


def test_aliases_shortopts():
    args = ['-a']
    doc = '-a, -b'
    opts, operands = parse(args, doc)
    assert '-a' in opts
    assert '-b' in opts
    assert opts['-a']['flags'] == ['-a', '-b']
    assert opts['-a']['argument'] is False
    assert opts['-a']['enabled'] == 1
    assert opts['-a']['value'] is None
    assert opts['-b']['flags'] == ['-a', '-b']
    assert opts['-b']['argument'] is False
    assert opts['-b']['enabled'] == 1
    assert opts['-b']['value'] is None
    assert operands == []


def test_aliases_longopts():
    args = ['--alpha']
    doc = '--alpha, --beta'
    opts, operands = parse(args, doc)
    assert '--alpha' in opts
    assert '--beta' in opts
    assert opts['--alpha']['flags'] == ['--alpha', '--beta']
    assert opts['--alpha']['argument'] is False
    assert opts['--alpha']['enabled'] == 1
    assert opts['--alpha']['value'] is None
    assert opts['--beta']['flags'] == ['--alpha', '--beta']
    assert opts['--beta']['argument'] is False
    assert opts['--beta']['enabled'] == 1
    assert opts['--beta']['value'] is None
    assert operands == []


def test_aliases_mixed():
    args = ['--alpha']
    doc = '-a, --alpha'
    opts, operands = parse(args, doc)
    assert '-a' in opts
    assert '--alpha' in opts
    assert opts['-a']['flags'] == ['-a', '--alpha']
    assert opts['-a']['argument'] is False
    assert opts['-a']['enabled'] == 1
    assert opts['-a']['value'] is None
    assert opts['--alpha']['flags'] == ['-a', '--alpha']
    assert opts['--alpha']['argument'] is False
    assert opts['--alpha']['enabled'] == 1
    assert opts['--alpha']['value'] is None
    assert operands == []


def test_aliases_mixed_arg_separate():
    args = ['--alpha', 'lorem', 'ipsum']
    doc = '-a arg, --alpha'
    opts, operands = parse(args, doc)
    assert '-a' in opts
    assert '--alpha' in opts
    assert opts['-a']['flags'] == ['-a', '--alpha']
    assert opts['-a']['argument'] is True
    assert opts['-a']['enabled'] == 1
    assert opts['-a']['value'] == 'lorem'
    assert opts['--alpha']['flags'] == ['-a', '--alpha']
    assert opts['--alpha']['argument'] is True
    assert opts['--alpha']['enabled'] == 1
    assert opts['--alpha']['value'] == 'lorem'
    assert operands == ['ipsum']


def test_aliases_mixed_arg_attached():
    args = ['--alpha', 'lorem', 'ipsum']
    doc = '-a, --alpha=arg'
    opts, operands = parse(args, doc)
    assert '-a' in opts
    assert '--alpha' in opts
    assert opts['-a']['flags'] == ['-a', '--alpha']
    assert opts['-a']['argument'] is True
    assert opts['-a']['enabled'] == 1
    assert opts['-a']['value'] == 'lorem'
    assert opts['--alpha']['flags'] == ['-a', '--alpha']
    assert opts['--alpha']['argument'] is True
    assert opts['--alpha']['enabled'] == 1
    assert opts['--alpha']['value'] == 'lorem'
    assert operands == ['ipsum']


def test_helpers_help(capsys):
    args = ['-h']
    doc = '-h, --help  lorem ipsum'
    with pytest.raises(SystemExit):
        opts, operands = parse(args, doc, version='1.2.3')
    captured = capsys.readouterr()
    assert captured.out == '-h, --help  lorem ipsum\n'


def test_helpers_version(capsys):
    args = ['--version']
    doc = '--version'
    with pytest.raises(SystemExit):
        opts, operands = parse(args, doc, version='1.2.3')
    captured = capsys.readouterr()
    assert captured.out == '1.2.3\n'


def test_helpers_skip():
    args = []
    doc = '--help'
    opts, operands = parse(args, doc, version='1.2.3')
    assert '--help' in opts
    assert opts['--help']['flags'] == ['--help']
    assert opts['--help']['argument'] is False
    assert opts['--help']['enabled'] == 0
    assert opts['--help']['value'] is None
    assert operands == []
