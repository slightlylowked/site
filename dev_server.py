#!/usr/bin/env python3
"""Local dev server with hot reload. Run from project root."""
import os
from livereload import Server

root = os.path.dirname(os.path.abspath(__file__))
os.chdir(root)

server = Server()
server.watch("*.html")
server.watch("*.css")
server.serve(root=root, port=3000)
