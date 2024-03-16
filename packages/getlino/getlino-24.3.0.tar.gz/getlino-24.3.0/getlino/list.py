# Copyright 2021-2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

import os
import shutil
import secrets
import click

from os.path import join
from importlib import import_module

from .utils import KNOWN_REPOS

KNOWN_APPS = [r for r in KNOWN_REPOS if r.settings_module]


@click.command()
@click.pass_context
def list(ctx):
    """
    List the available choices for getlino startsite.

    """

    for r in KNOWN_APPS:
        # r: nickname package_name git_repo settings_module front_end
        # print(r.settings_module)
        if r.public_url:
            click.echo("{r.nickname} : {r.public_url}".format(**locals()))
        else:
            m = import_module(r.settings_module)
            s = m.Site
            click.echo(
                "{r.nickname} : {s.verbose_name} : {s.description}".format(
                    **locals()))
        # if s.description:
        #     click.echo("\n" + s.description.strip() + "\n")
        # if r.git_repo:
        #     print("(`Source repository <{r.git_repo}>`__)".format(**locals()))
