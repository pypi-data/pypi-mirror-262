# Copyright (C) 2024 Matthias Nadig


__version__ = '1.0.0'
__author__ = 'Matthias Nadig'


def __getattr__(name):
    str_error = (
        f'Full version of tacotree_lab not available. Cannot access "tacotree_lab.{name}".'
    )
    raise RuntimeError(str_error)
