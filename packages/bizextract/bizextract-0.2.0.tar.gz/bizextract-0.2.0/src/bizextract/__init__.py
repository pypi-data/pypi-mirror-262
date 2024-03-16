from base64 import b64decode
import csv
import json
from pathlib import Path
from tabulate import tabulate
import tika
import re


# { 'regions': [...], 'companies': {...} }
configuration = 'eyJyZWdpb25zIjogWyJBbWVyaWNhcyIsICJFdXJvcGUiLCAiQXNpYSBQYWNpZmljIl0sICJjb21wYW5pZXMiOiB7ImEiOiAiQW5kcmV3cyIsICJiIjogIkJhbGR3aW4iLCAiYyI6ICJDaGVzdGVyIiwgImQiOiAiRGlnYnkiLCAiZSI6ICJFcmllIiwgImYiOiAiRmVycmlzIn0sICJoZWFkZXJzIjogWyJQZXJpb2QiLCAiR3JvdXAiLCAiU2VnbWVudCIsICJSZWdpb24iLCAiQ29tcGFueSIsICJOYW1lIiwgIlVuaXRzIFNvbGQiLCAiUHJpY2UiLCAiQ3VzdG9tIFNhdGlzZmFjdGlvbiIsICJBY2N5IiwgIlNwZWVkIiwgIlNlcnZpY2UgTGlmZSIsICJBZ2UiLCAiUmVnaW9uIEtpdCIsICJNYXRlcmlhbCBDb3N0cyIsICJMYWJvciBDb3N0cyIsICJDb250cmliLiBNYXJnaW4iXX0='
CONFIG = json.loads(b64decode(configuration.encode()).decode())

CONVERSION = dict(map(lambda r: (r, 1), CONFIG['regions']))



def process_report(segment, group, report):
    year = int(report[1][7:12])
    data = []
    region = None
    for line in report[26:]:
        if len(line) == 0:
            continue

        items = line.split(' ')
        if len(items) == 13 and items[0] in CONFIG['regions']:
            region = items[0]
            items = items[1:]
        elif len(items) == 14 and items[0] == b64decode(b'QXNpYQ==').decode():
            region = f'{items[0]} {items[1]}'
            items = items[2:]

        price = items[2].replace('S$', '').replace('€', '').replace('$', '')
        price = float(price) / CONVERSION[region]
        items[2] = price
        company = CONFIG['companies'][items[0][0].lower()]
        items = [f'12/1/{year}', group, segment, region, company] + items
        data.append(items)

    return data


def list_reports(path: Path, pattern: str = b64decode(b'R0ROQUdsb2JlKg==').decode()) -> list[Path]:
    return list(path.glob(pattern))


def parse_reports(pattern: str | None = None) -> list[list[str]]:
    tika.initVM()
    from tika import parser

    analysis = []
    if pattern is None:
        reports = list_reports(Path('.'))
    else:
        reports = list_reports(Path('.'), pattern)
    for path in reports:
        parsed = parser.from_file(str(path))
        content = parsed['content']

        page_pattern = re.compile('([A-Z]+\\d{6}_?\\d*) Page (\\d+)')
        group = None
        pages = {}
        page = 0
        for line in content.split('\n'):
            m = page_pattern.match(line)
            if m:
                group = m.group(1)
                page = int(m.group(2))
            if page not in pages:
                pages[page] = []
            pages[page].append(line)

        performance_analysis = None
        budget_analysis = None
        for page in pages:
            # print(f'Page {page}: ~{pages[page][8]}~')
            if pages[page][8] == 'Top Products In Budget':
                budget_analysis = pages[page]
            if pages[page][8] == 'Top Products In Performance':
                performance_analysis = pages[page]

        # for lineno in range(len(budget_analysis)):
        #    print(f'{lineno}: {budget_analysis[lineno]}')
        analysis.extend(process_report('Budget', group, budget_analysis))
        analysis.extend(process_report('Performance', group, performance_analysis))

    return analysis


def print_table(analysis: list[list[str]]):
    print(tabulate(analysis, headers=CONFIG['headers']))


def write_table(analysis: list[list[str]], outpath: Path = Path('out.csv')):
    with open(outpath, 'w', newline='') as fd:
        writer = csv.writer(fd)
        writer.writerow(CONFIG['headers'])
        writer.writerows(analysis)
