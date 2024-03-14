def parse(args, doc, version=None, posixly_correct=False):
    opts, operands = {}, []
    for line in [i for i in doc.split('\n') if i.lstrip().startswith('-')]:
        flags, optarg = [], False
        for arg in line.lstrip().split('  ', 1)[0].replace(',', ' ').split():
            if not arg.startswith('-') or arg == '-':
                optarg = True
            elif len(arg) == 2 or arg.startswith('--') and not posixly_correct:
                if arg.startswith('--') and '=' in arg:
                    arg, optarg = arg.split('=', 1)[0], True
                if arg.isascii() and arg.replace('-', '').isalnum():
                    flags = list(dict.fromkeys(flags + [arg]))
        opts.update({i: {'flags': flags, 'argument': optarg,
                         'enabled': 0, 'value': None} for i in flags})
    while args:
        flag, args, optarg, combined = args[0], args[1:], None, []
        if not flag.startswith('-') or flag in ('-', '--'):
            operands += [] if flag == '--' else [flag]
            if flag == '--' or posixly_correct:
                break
            continue
        if flag.startswith('--') and not posixly_correct:
            flag, optarg = (flag.split('=', 1) + [None])[:2]
            if flag not in opts:
                matches = [f for f in opts if f.startswith(flag)]
                if 1 < len(matches):
                    raise ValueError(f"ambiguous abbreviated option: {flag}")
                flag = matches[0] if matches else flag
            if optarg and flag in opts and not opts[flag]['argument']:
                raise ValueError(f"option takes no argument: {flag}")
        while 2 < len(flag) and flag[:2] in opts:
            if opts[flag[:2]]['argument']:
                flag, optarg = flag[:2], flag[2:]
                break
            flag, combined = '-' + flag[2:], combined + [flag[:2]]
        if flag not in opts:
            raise ValueError(f"invalid option: {flag}")
        while opts[flag]['argument'] and optarg is None:
            if args:
                optarg, args = args[0], args[1:]
                break
            raise ValueError(f"option requires argument: {flag}")
        for f in [j for i in combined + [flag] for j in opts[i]['flags']]:
            opts[f]['enabled'] += 1
            opts[f]['value'] = optarg if opts[f]['argument'] else None
    for flag, msg in ('--help', doc), ('--version', version):
        if version is not None and flag in opts and opts[flag]['enabled']:
            print(str(msg).strip())
            raise SystemExit(0)
    return opts, operands + args
