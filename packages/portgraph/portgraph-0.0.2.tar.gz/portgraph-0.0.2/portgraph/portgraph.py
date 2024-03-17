#!/usr/bin/env python3
# -*- coding:utf8 -*-

import os
import subprocess
import argparse
import sys
from graphviz import Digraph
from pathlib import Path
from typing import Optional, Union


class Port:
    def __init__(self, port: Union[str, Path], localbase: Path, flavor: Optional[str] = None):
        port = str(port)
        self._localbase = localbase
        category, name = port.split(os.sep)[-2:]
        self._category = category
        name_values = name.split("@", 1)
        self._name = name_values[0]
        if flavor is None and len(name_values) == 2:
            self._flavor = name_values[1]
        else:
            self._flavor = flavor

    @property
    def flavor(self) -> Optional[str]:
        return self._flavor

    @property
    def without_flavor(self) -> str:
        return f"{self._category}/{self._name}"

    def __str__(self) -> str:
        result = self.without_flavor
        if self._flavor is not None:
            result = f"{result}@{self._flavor}"
        return result

    def __repr__(self) -> str:
        return str(self)

    def __eq__(self, other) -> bool:
        return str(self) == str(other)

    def path(self, with_flavor=False) -> Path:
        port = self.without_flavor
        if with_flavor:
            port = str(self)
        return self._localbase / port

    def create_category_dir(self):
        Path(self._category).mkdir(exist_ok=True)


class Portgraph:
    def __init__(self, localbase: Path, with_pkg: bool = False, verbose: bool = False, recursion: int = -1, url: Optional[str] = None, suffix: Optional[str] = None,
                 build: bool = True, run: bool = False, showIfAbandoned: bool = True, clean: bool = True):
        self.graph = Digraph(
            format='svg',
            graph_attr=[('rankdir', 'LR')],
            node_attr=[('style', 'filled'), ('fillcolor', '#E1E1E1'), ('fontcolor', '#737373')],
        )
        self.localbase = localbase
        self.with_pkg = with_pkg
        self.verbose = verbose
        self.recursion = recursion
        self.max_recurse = recursion
        if url is not None:
            url_template = f"{url}/{{port}}"
            if suffix is not None:
                url_template = f"{url_template}/{suffix}"
            self.url_template = url_template
        else:
            self.url_template = ""
        self.all_ports = []
        self.PKG = "ports-mgmt/pkg"
        self.build = build
        self.run = run
        self.abandoned = showIfAbandoned
        self.clean = clean

    def build_graph(self, port: Port):
        self.graph.name = str(port)
        self.graph.filename = str(port)
        if self.build:
            self.recurse_ports(port, ['build', '#009999'])
        if self.run:
            self.recurse_ports(port, ['run', '#990000'])
        self.graph.render(str(port), cleanup=self.clean)

    def add_node(self, port: Port):
        node_color = 'black'
        node_style = 'filled'
        if self.abandoned:
            command = ['make', '-C', port, 'maintainer']
            proc_maintainer = subprocess.Popen(command, stdout=subprocess.PIPE)
            maintainer = proc_maintainer.stdout.readline().decode('utf-8').rstrip()
            if maintainer == "ports@FreeBSD.org":
                node_color = 'red'
                node_style = 'bold'

        portname = str(port)
        if portname != self.PKG or (portname == self.PKG and self.with_pkg):
            node_url = self.url_template.format(port=port.without_flavor)
            self.graph.node(portname, URL=node_url, color=node_color, style=node_style)

    def recurse_ports(self, port: Port, depends_args: list[str]):
        if self.max_recurse == 0:
            self.max_recurse = self.recursion
            return

        if self.verbose:
            print(port.path())

        self.add_node(port)
        command = ['make', '-C', port.path(), f'{depends_args[0]}-depends-list', '-DDEPENDS_SHOW_FLAVOR', *([f'FLAVOR={port.flavor}'] if port.flavor else [])]
        proc = subprocess.Popen(command, stdout=subprocess.PIPE)
        dep_ports = (Port(line.rstrip().decode('utf-8'), self.localbase) for line in proc.stdout)
        for dep_port in dep_ports:
            self.all_ports.append(port)
            dep_portname = str(dep_port)
            if dep_portname != self.PKG or (dep_portname == self.PKG and self.with_pkg):
                self.graph.edge(str(port), dep_portname, color=depends_args[1])
            if dep_port not in self.all_ports:
                self.add_node(dep_port)
                self.all_ports.append(dep_port)
                self.max_recurse -= 1
                self.recurse_ports(dep_port, depends_args)


def graph4allports(localbase: Path, flavor: str, with_pkg: bool, verbose: bool, recursion: int, url: str, suffix: str, build: bool, run: bool, abandoned: bool, clean: bool = True):
    subdirs = ('Mk', 'distfiles', 'Tools', 'Templates', 'Keywords', 'base')
    port_paths = (
        port_path
        for category_path in localbase.iterdir()
        for port_path in category_path.iterdir()
        if category_path.is_dir() and category_path.name not in subdirs and port_path.is_dir()
    )
    for port_path in port_paths:
        graph4port(port_path, localbase, flavor, with_pkg, verbose, recursion, url, suffix, build, run, abandoned, clean)


def graph4port(port: str, localbase: Path, flavor: str, with_pkg: bool, verbose: bool, recursion: int, url: str, suffix: str, build: bool, run: bool, abandoned: bool, clean: bool = True):
    portgraph = Portgraph(localbase, with_pkg, verbose, recursion, url, suffix, build, run, abandoned, clean)
    portgraph.build_graph(Port(port, localbase, flavor))


def main():
    parser = argparse.ArgumentParser(description="portgraph produces a graph representing the dependencies needed for a given port")

    parser.add_argument('-v', '--verbose', action='store_true', help="be verbose")
    parser.add_argument('-l', '--localbase', type=str, default="/usr/ports", help="Localbase where ports are located (/usr/ports by default)")
    parser.add_argument('-p', '--port', type=str, default="ports-mgmt/portgraph", help="the port to produce the graph (ports-mgmt/portgraph by default).")
    parser.add_argument('-f', '--flavor', type=str, help="Sets the flavor for ports")
    parser.add_argument('-c', '--recursion', type=int, default=-1, help="Sets the maximum recursion.")
    parser.add_argument('-u', '--url', type=str, help="Adds a link on each node. Ex: url/ports-mgmt/portgraph")
    parser.add_argument('-s', '--url-suffix', dest="suffix", type=str, help="Adds a suffix to the url on each node. Ex: url/ports-mgmt/portgraph.svg")
    parser.add_argument('-w', '--with-pkg', dest='with_pkg', action='store_true', help="Since pkg is always required, this is disabled by default. You can enable it with this option.")
    parser.add_argument('-a', '--all', dest='allports', action='store_true', help="Build a graph for each port")
    parser.add_argument('-b', '--build', action='store_true', help="Build depends list. If -b or -r is not present, -b is actived by default")
    parser.add_argument('-r', '--run', action='store_true', help="Run depends list. If -b or -r is not present, -b is actived by default")
    parser.add_argument('-t', '--abandoned', action='store_true', help="Show abandoned ports with a particular style. You should Take maintainership ;)")
    parser.add_argument('-C', '--clean', action='store_true', help="Delete the source file (dot graph) after rendering")

    args = parser.parse_args()
    args.build = not args.build and not args.run

    graph_args = [
        Path(args.localbase),
        args.flavor,
        args.with_pkg,
        args.verbose,
        args.recursion,
        args.url,
        args.suffix,
        args.build,
        args.run,
        args.abandoned,
        args.clean,
    ]
    if args.allports:
        graph_it = graph4allports
    else:
        graph_it = graph4port
        graph_args.insert(0, args.port)

    graph_it(*graph_args)

if __name__ == "__main__":
    main()
