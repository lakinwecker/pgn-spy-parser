#!/usr/bin/env python3
import os
import sys

position_types = ['undecided', 'losing']
t_metrics = ['t1', 't2', 't3']
cp_metrics = [
    '>0cp_loss',
    '>10cp_loss',
    '>25cp_loss',
    '>50cp_loss',
    '>100cp_loss',
    '>200cp_loss',
    '>500cp_loss',
]
metrics = t_metrics + cp_metrics
sub_metrics = ['activated', 'positions', 'percentage', 'std_error']
global_metrics = ['positions', 'cp_loss_mean', 'cp_loss_std_dev']

metric_base = {sm: 0 for sm in sub_metrics}
position_type_base = {gm: 0 for gm in global_metrics}
for m in metrics:
    position_type_base[m] = metric_base.copy()

def parse_pgn_spy_file(file):
    results = {
        'games': 0,
    }
    for pt in position_types:
        results[pt] = position_type_base.copy()
    with open(file, 'r') as fd:
        lines = fd.read().replace("\r", "").split('\n')
        line = lines.pop(0)
        assert 'games' in line
        results['games'] = int(line.strip().replace(' games', ''))
        def parse_line(line):
            t, rest = line.split(': ')
            if not rest.startswith("0/0"):
                positions, rest = rest.split('; ')
                activated, positions = positions.split('/')
                percent, rest = rest.split('% ')
                _, std_error = rest.split('(std error ')
            else:
                activated = positions = percent = std_error = "0"
            return {
                'positions': int(positions),
                'activated': int(activated),
                'percentage': float(percent),
                'std_error': float(std_error.replace(')', '')),
            }


        def positions_parse(lines, d):
            d['positions'] = int(lines.pop(0).replace('Positions: ', ''))
            if d['positions'] == 0:
                return
            for m in metrics:
                d[m] = parse_line(lines.pop(0))
            _, rest = lines.pop(0).split('CP loss mean ')
            cp_loss_mean, std_dev = rest.split(', std deviation ')
            d['cp_loss_mean'] = float(cp_loss_mean)
            d['cp_loss_std_dev'] = float(std_dev)

        line = lines.pop(0)
        while 'UNDECIDED POSITIONS' not in line and lines:
            line = lines.pop(0)
        positions_parse(lines[:12], results['undecided'])
        while 'LOSING POSITIONS' not in line and lines:
            line = lines.pop(0)
        positions_parse(lines[:12], results['losing'])
    return results

def rget(d, key):
    for k in key.split('.'):
        d = d[k]
    return d

if __name__ == '__main__':
    import pprint
    fields = ['games']
    for pt in position_types:
        fields.extend(['{}.{}'.format(pt, gm) for gm in global_metrics[:1]])
        for m in t_metrics:
            fields.extend(['{}.{}.{}'.format(pt, m, sm) for sm in sub_metrics])
        fields.extend(['{}.{}'.format(pt, gm) for gm in global_metrics[1:]])
        for m in cp_metrics:
            fields.extend(['{}.{}.{}'.format(pt, m, sm) for sm in sub_metrics])

    print ','.join(fields)
    for main_dir in sys.argv[1:]:
        for root, dirs, files in os.walk(main_dir):
            for file in files:
                if file == "results.txt":
                    username = root.split("/")[-2]
                    season_part = root.split("/")[-1]
                    league = "tl"
                    if "lonewolf" in season_part:
                        league = "lw"
                    season = season_part.split("-")[-1]
                    file = os.path.join(root, file)
                    #print file
                    results = parse_pgn_spy_file(file)
                    data = [username, "{}{}".format(league,season)] + [unicode(rget(results, k)) for k in fields]
                    print ','.join(data)
