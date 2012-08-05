#!/usr/bin/python
# -*- coding: utf-8 -*-

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

"""
A set of classes to help separate Spanish names into each of their parts. The
ParseNamesCSV class implements the reading of a CSV file, replacement of the
column containing the full name with three columns for each component and writing
to a new file.

Limitations are:
 - Not all compound given names are accounted for.
 - Some compound given names can actually be a first surname, e.g Ramón can be
   either a compound given name or a first surname.

The first limitation can be alleviated by adding missing compound given
names to config/compound_tokens_givenname.txt

The second limitation currently has no workaround. Plans are to incorporate a
"problematic" flag to compound given names. When a problematic compound given
name is found it will be stored in a list with its details for review by a
human.

>>> PyElla().parse_name(u"Maria")
[u'Maria', u'', u'']
>>> PyElla().parse_name(u"Maria Jesus")
[u'Maria Jesus', u'', u'']
>>> PyElla().parse_name(u"Maria Jesus Rodriguez")
[u'Maria Jesus', u'Rodriguez', u'']
>>> PyElla().parse_name(u"Maria Jesus Rodriguez Mendez")
[u'Maria Jesus', u'Rodriguez', u'Mendez']
>>> PyElla().parse_name(u"Maria Jesus del Castillo Herrera")
[u'Maria Jesus', u'del Castillo', u'Herrera']
>>> PyElla().parse_name(u"Maria Rodriguez")
[u'Maria', u'Rodriguez', u'']
>>> PyElla().parse_name(u"Maria Rodriguez Benitez")
[u'Maria', u'Rodriguez', u'Benitez']
>>> PyElla().parse_name(u"Maria de los Olivos")
[u'Maria', u'de los Olivos', u'']
>>> PyElla().parse_name(u"Maria de los Olivos Benitez")
[u'Maria', u'de los Olivos', u'Benitez']
>>> PyElla().parse_name(u"Maria de Pilares Benitez Mendez del Pozo")
[u'Maria', u'de Pilares', u'Benitez Mendez del Pozo']
>>> PyElla().parse_name(u"Maria del Mar Batalla Guerrero")
[u'Maria del Mar', u'Batalla', u'Guerrero']
"""

import codecs
import os
import csv

ENCODING = "latin-1"
OUTPUT_ENCODING = "latin-1"

class PyElla:
	"""
	A parser that splits a full Spanish name into its parts. This can be one
	to all of: given name, first surname, second surname.
	"""
	def __init__(self):
		"""
		Create a PyElla object. Define which words signal a compound
		surname and which words signal a compound given name.
		"""
		self.compound_tokens = []
		self.compound_firstnames = []
		self._load_tokens()
	
	def parse_name(self, fullname):
		"""
		Parses the full name and returns a list with one item for each component.
		Items can be empty strings if the component is missing (e.g. no second
		surname).
		"""
		self.firstname = u''
		self.surname1 = u''
		self.surname2 = u''
		self.fullname = fullname

		# Non breaking spaces cause problems, this replaces all white-
		# space chars with regular spaces.
		self.fullname = u' '.join(self.fullname.split())

		components_list = self._create_components()
		self._join_components(components_list)
		
		return [self.firstname, self.surname1, self.surname2]
		
	def _create_components(self):
		"""
		Creates components from a full name. First compound surnames are
		created by searching backwards for compound surname tokens. If one is
		found the token is joined with the word immediately after it.
		Then the compound given names are created by checking front-to-back if
		the	second element in name_components contains one of the given name
		wildcards. If so the first and second element are joined.
		"""
		name_words = self.fullname.split()
		# Go from back to front to check for compound surnames.
		name_words.reverse()
		name_components = []
		for element in name_words[:]:
			if element.lower() in self.compound_tokens:
				name_components[0] = u' '.join([element, name_components[0]])
			else:
				name_components.insert(0, element)
				
		# Go from front to back to check second element for compound given name.
		name_words.reverse()
		
		# The for loop is so the 'for x in y' comparison can be swapped to
		# 'for y in x'. This allows compound given name tokens to be used as
		# wildcards, reducing the amount of tokens needed.
		for compound_firstname in self.compound_firstnames:
			# Compare number of elements to avoid compound surnames which contain
			# a firstname counting as compound firstnames, e.g. given
			# Maria de los Pilares Benitez, de los Pilares should be surname1
			if(len(name_components) > 1):
				if(compound_firstname in name_components[1] and (len(compound_firstname.split()) == len(name_components[1].split()))):
					name_components[0] = u' '.join([name_components[0], name_components[1]])
					name_components.pop(1)
					
		return name_components
	
	def _join_components(self, names_list):
		"""
		Given a list of candidate components, separates them into firstname, surname1
		and surname2 variables.
		Depending on the amount of candidates, creates full Spanish name or partial (no
		second surname)	Spanish name.
		"""
		if(len(names_list) >= 1):
			self.firstname = names_list[0]
			if(len(names_list) >= 2):
				self.surname1 = names_list[1]
			if(len(names_list) >= 3):
				self.surname2 = u' '.join(names_list[2:])

	def __str__(self):
		"""
		Join elements of name together and return as ENCODING string.
		"""
		full_name = self.firstname
		if(self.surname1 is not u''):
			full_name = u'\n'.join([full_name, self.surname1])
		if(self.surname2 is not u''):
			full_name = u'\n'.join([full_name, self.surname2])
		return full_name.encode(ENCODING)
		
	def _load_tokens(self):
		"""
		Loads tokens from config/tokens.cfg and stores them in
		self.compound_tokens and self.compound_firstnames.
		"""
		f = codecs.open(os.path.join(os.getcwd(), "config", "tokens.cfg"), "r", "utf-8")
		
		sections = {}
		in_section = False
		for line in f:
			if line.startswith("["):
				section_name = line
				section_name = section_name.lstrip("[")
				section_name = section_name.rstrip()
				section_name = section_name.rstrip("]")
				in_section = True
			elif in_section:
				if section_name == "given name tokens":
					# Only keep the name, discard the comment. Compare to empty
					# in case of lines that only have a comment.
					token = line.partition("#")[0].strip()
					if token != '':
						self.compound_firstnames.append(token)
				elif section_name == "surname tokens":
					token = line.partition("#")[0].strip()
					if token != '':
						self.compound_tokens.append(token)	
				
		f.close()
		
class ParseNamesCSV:
	"""
	Parses names from a CSV file. If name_column isn't specified the CSV file
	is checked for a header called either "Nombre" or "Name". If found, it is
	assumed to be the column holding the names to be parsed. If no output path
	is specified it writes to a new file, appending ' - names parsed'	to the filename.

	Known issue:
	Doesn't work when the CSV file contains a single column. The dialect sniffer
	thinks it's a newline-separated-values file and the end result is one column with
	each component on a separate line.
	"""
	def __init__(self, input_path, output_path=None, name_column=None):
		try:
			input_file = open(input_path, "rb")
		except IOError:
			print "Couldn't open file '" + input_path + "'."
			exit()
			
		try:
			if output_path is not None:
				output_file = open(output_path, "wb")
			else:
				output_path = input_path.rpartition(".")[0] + " - names parsed." + input_path.rpartition(".")[2]
				output_file = open(output_path, "wb")
		except IOError:
			print "Couldn't create file '" + output_path + "'."
			exit()
		
		dialect = csv.Sniffer().sniff(input_file.read(1024))
		input_file.seek(0)
		
		self.csv_reader = csv.reader(input_file, dialect=dialect)
		
		fieldnames = self.csv_reader.next()
		input_file.seek(0)
		self.csv_reader = csv.DictReader(input_file, dialect=dialect)
		if name_column is not None:
			try:
				name_col_index = fieldnames.index(name_column)
			except ValueError:
				print "Column " + name_column + " does not exist."
				exit()
			self.name_col = name_column
		else:
			try:
				name_col_index = fieldnames.index("Name")
			except ValueError:
				try:
					name_col_index = fieldnames.index("Nombre")
				except ValueError:
					print "Can't find column with names"
					exit()
				self.name_col = "Nombre"
			self.name_col = "Name"
		
		# Delete old column where the full name was
		fieldnames.pop(name_col_index)
		# Inserted in reverse order so the given name column is where the full name was
		fieldnames.insert(name_col_index, "Second Surname")
		fieldnames.insert(name_col_index, "First Surname")
		fieldnames.insert(name_col_index, "Given Name")
			
		self.csv_writer = csv.DictWriter(output_file, fieldnames=fieldnames, \
			dialect=dialect, extrasaction="ignore")
			
	def write_names(self):
		self.csv_writer.writeheader()
		pyella = PyElla()
		for row in self.csv_reader:
			name_components = pyella.parse_name(row[self.name_col].decode('latin-1'))
			row['Given Name'] = name_components[0].encode(OUTPUT_ENCODING)
			if name_components[1] is not u'': 
				row['First Surname'] = name_components[1].encode(OUTPUT_ENCODING)
			if name_components[2] is not u'': 
				row['Second Surname'] = name_components[2].encode(OUTPUT_ENCODING)
			self.csv_writer.writerow(row)
	
if __name__ == '__main__':
	import doctest
	doctest.testmod()
