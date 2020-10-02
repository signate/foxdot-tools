#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from cmd import Cmd
from FoxDot import execute

class FoxDotInteractiveShell(Cmd):
	prompt = "FoxDot> "

	def default(self, line):
		execute(line)

if __name__ == "__main__":
	FoxDotInteractiveShell().cmdloop()
