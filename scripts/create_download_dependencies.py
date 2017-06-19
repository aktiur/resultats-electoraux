import os
import sys
import json


RULE = """
{target}: DL_{target}

.PHONY: DL_{target} 
DL_{target}: |dist/raw
\tif [ -e "{target}" ]; then curl -o "{target}" -z "{target}" "{url}"; else curl -o "{target}" "{url}"; fi 
"""


def create_dependencies(source_files, out):
    for name, url in source_files.items():
        filename = os.path.join('dist', 'raw', name + '.csv')

        out.write(RULE.format(target=filename, url=url))


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python scripts/create_download_dependencies.py config > dest")
        sys.exit(1)

    with open(sys.argv[1]) as f:
        config = json.load(f)

    create_dependencies(config['sources'], sys.stdout)
