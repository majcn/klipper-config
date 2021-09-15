CONFIG_LEFT = ('.', 'printer.cfg')
CONFIG_RIGHT = ('.', 'printer.cfg.old')

import os
import webbrowser
import difflib as dl

def get_config_raw(path, filename):
    f = open(os.path.join(path, filename)).readlines()
    f = [x.rstrip() for x in f]
    f = [x for x in f if not x.startswith('#')]
    f = [x.rstrip() for x in f]
    f = [x for x in f if x]
    return f

def get_config(path, filename, included_from='', result=None):
    if result is None:
        result = {}

    f = get_config_raw(path, filename)

    key = None
    for x in f:
        if x.startswith('[include '):
            result = get_config(path, x[9:-1], x[9:-1], result)
        elif x.startswith('['):
            key = x
            if included_from:
                key = f'{key} -> {included_from}'
            while key in result:
                key += '_'
            result[key] = []
        else:
            result[key].append(x)

    return result

def config_as_str(config):
    result = ""
    for k in sorted(config):
        result += k + '\n'
        result += '\n'.join(config[k]) + '\n'
        result += '\n'
    return result

def open_in_browser(diff):
    html_file = '/tmp/klipper_config_diff.html'
    f = open(html_file,'w')
    f.write(diff)
    f.close()

    webbrowser.open(f'file://{html_file}')

c1 = config_as_str(get_config(*CONFIG_LEFT))
c2 = config_as_str(get_config(*CONFIG_RIGHT))
diff = dl.HtmlDiff().make_file(c1.split('\n'), c2.split('\n'))
open_in_browser(diff)