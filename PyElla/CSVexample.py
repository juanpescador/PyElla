#!/usr/bin/python

# Copyright 2010-2012 John Fisher.
    
# This file is part of PyElla.

# PyElla is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# PyElla is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PyElla.  If not, see <http://www.gnu.org/licenses/>.

import sys
import PyElla

def main():
	"""Load CSV file and parse names into three columns"""
	input_path = sys.argv[1]
	try:
		output_path = sys.argv[2]
	except IndexError:
		output_path = None
	try:
	    name_column = sys.argv[3]
	except IndexError:
	    name_column = None
	
	parser = PyElla.ParseNamesCSV(input_path, output_path=output_path, name_column=name_column)
	parser.write_names()

if __name__ == '__main__':
	main()
