import click
from typing import List,Any

def progressbar(items: List[Any], label=None):
    template='│%(bar)s│ %(info)s'
    if label is not None:
        template='%(label)s │%(bar)s│ %(info)s'
    return click.progressbar(iterable=items, length=len(items), label=label, fill_char='█', empty_char=' ', width=0, bar_template=template)