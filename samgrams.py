class Samgrams(object):
	from nltk import tokenize,tag
	import cPickle			
	import os.path
	import re
# 	def __len__(self,x=None):
# 		if x == None:
# 			self.len = 0
# 		else:
# 			self.len = len(x)
	def grams(self,n,print_results,text=None):
		""":param words: a list of words"""
		if n == 0:
			raise ValueError("n must be greater than 0")
		else:
			d = dict()
			start_index = 0
			end_index = n
			while end_index <= (len(text)):
				gram = "".join((" "+word) for word in text[start_index:(end_index)])
				#print gram
				if gram in d.keys():
					d[gram] += 1
				else:
					d[gram] = 1
				start_index += 1
				end_index += 1
			self.sorted_d = sorted(d.items(),key=lambda x: x[1],reverse=True)
			#sorted_d = sorted(d.items(), key=lambda item: item[1])
			#sorted_d.reverse()
			if print_results == True:
				print self.sorted_d
			return self.sorted_d		
	def gramsDict(self,n,print_results,text=None):
		""" :param text: the text to be analyzed for n-grams
			:type text: a str or a list"""
		if not text:
			text = self.words
		else:
			if type(text) == str:
				self.words = nltk.tokenize.wordpunct_tokenize(text)
			elif type(text) == set:
				self.words = list(text)
			elif type(text) == list:
				self.words = text
			else:
				raise TypeError("text must be str or list")
		print "training model..."
		self.model = dict()
		i = 1
		while i <= n:
			self.model[i] = self.grams(i,print_results,text)
			#print ngramsDict[i]
			i += 1
		if print_results == True:
			print self.model
		#return self.model
	def get_model(self,fname,part,n=0):
		import re
		"""	NOTE: to prevent misidentification of pickled components, the n-gram model and n-gram frequencies
			should be pickled and retrieved separately.
			:param fname: name of the file containing the pickled item to be retrieved
			:type fname: str
			:param part: what part of the model is being retrieved:
				grams:	self.model[n] (will raise a ValueError if there's no corresponding self.model[n])
				model:	self.model
				freq:	self.ngramsFreqDict[n] (will raise a ValueError if there's no corresponding self.ngramsFreqDict[n])
				freqs:	self.ngramsFreqDict
			:type part:	str
			:param n:	if part == grams or freq, picks out which slice is being unpickled
			:type n:	int"""
		if re.match(fname,".pickle") == False:
			fname += ".pickle"
		if os.path.isfile(fname) == False:
			raise IOError("no such file")
		else:
			f_in = open(fname,"rb")
			brine = cPickle()
			if part == "model":
				self.model = brine.load(f_in)
			elif part == "freqs":
				self.ngramsFreqDict = brine.load(f_in)
			elif part == "grams":
				if n == 0:
					raise ValueError("n must be greater than 0")
				else:
					if self.model:
						if n in self.model.keys():
							if raw_input("{0}-gram model found. Overwrite? (y/n)".format(n)) == "n":	
								self.model[n] = brine.load(f_in)
							elif raw_input("{0}-gram model found. Overwrite? (y/n)".format(n)) == "y":
								print "not overwriting {0}-gram model".format(n)
								return None	
					else:
						self.model = dict()
						self.model[n] = brine.load(f_in)
			elif part == "freq":
				if n == 0:
					raise ValueError("n must be greater than 0")
				else:
					if self.ngramsFreqDict:
						if n in self.ngramsFreqDict.keys():
							if raw_input("{0}-gram frequencies found. Overwrite? (y/n)".format(n)) == "n":	
								self.model[n] = brine.load(f_in)
							elif raw_input("{0}-gram frequencies found. Overwrite? (y/n)".format(n)) == "y":
								print "not overwriting {0}-gram frequencies".format(n)
								return None	
					else:
						self.ngramsFreqDict = dict()
						self.ngramsFreqDict[n] = brine.load(f_in)
			else:
				raise ValueError("invalid choice. part must be grams, model, freq, or freqs")
	def __init__(self,text,n=0):
		"""if you want to load (parts of) a model from pre-existing .pickle files, instantiate a new Samgrams object
		with text=None, then call get_model"""
		if text != None:
			if type(text) == str:
				self.words = nltk.tokenize.wordpunct_tokenize(text)
			elif type(text) == set:
				self.words = list(text)
			elif type(text) == list:
				self.words = text
			else:
				try:
					self.words = list(text)
				except TypeError:
					raise TypeError("text must be iterable")
			if n != 0:
				self.gramsDict(n,False,text=None)	
			else:
				raise ValueError("n must be greater than 0")
		
	def gramFreqs(self,print_results):
		""":param ngrams: an n-gram dictionary as produced by get_gramsDict"""
		self.ngramsFreqDict = dict()
		for d in self.model:
			total = 0
			for x in self.model[d]:
				total += x[1]
			if total == 0:
				raise ValueError("%d-gram dictionary appears to be empty" %(d))
				continue
			else:
				fd = dict()
				for x in self.model[d]:
					fd[x[0]] = (x[1] * 1.0) / total
			self.ngramsFreqDict[d] = fd
		if print_results == True:
			print self.ngramsFreqDict
	def get_grams(self,n):
		"""print the chosen n-gram model"""
		if self.model:
			if n in self.model.keys():
				return self.model[n]
			else:
				raise IndexError("n has to be equal to a set of trained ngrams (1-{0})".format(len(self.model.keys())))
		else:
			raise AttributeError("""no trained model. please load a pickled model with get_model
			 or train a new one with gramsdict""")
	def get_gramsDict(self):
		"""print the n-grams model"""
		if self.model:
			return self.model
		else:
			raise AttributeError("""no trained model. please load a pickled model with get_model
			 or train a new one with gramsdict""")
	def get_gramFreqs(self,n):
		"""print the frequency dictionary for the chosen n-gram"""
		if self.ngramsFreqDict:
			if n in self.ngramsFreqDict.keys():
				return self.ngramsFreqDict[n]
			else:
				raise IndexError("n has to be equal to a set of frequencies for trained ngrams (1-{0})".format(len(self.ngramsFreqDict.keys())))
		else:
			raise AttributeError("""no frequencies found. please load a pickled set of frequencies with get_model
			or train a new one with gramFreqs""")
	def get_allFreqs(self):
		"""print self.ngramsFreqDict"""
		if self.ngramsFreqDict:
			return self.ngramsFreqDict
		else:
			raise AttributeError("""no frequencies found. please load a pickled set of frequencies with get_model
			or train a new one with gramFreqs""")
	def pickle_model(self,fname,cuke,n=0):
		import re
		"""	NOTE: to prevent misidentification of pickled components, the n-gram model and n-gram frequencies
			should be pickled and retrieved separately.
			:param fname: name of the file to be output to
			:param fname: str
			:param cuke: what you want to pickle
			:type cuke:	grams: self.model[n] (will raise a ValueError if there's no corresponding self.model[n])
						model:	self.model
						freq:	self.ngramsFreqDict[n] (will raise a ValueError if there's no corresponding self.ngramsFreqDict[n])
						freqs:	self.ngramsFreqDict
			:param n: if cuke == grams or freq, picks out which slice to pickle
			:type n: int"""
		if re.match(fname,".pickle") == False:
			fname += ".pickle"
		if os.path.isfile(fname):
			if raw_input("File exists! Overwrite? (y/n)") == "n":
				print "not overwriting file %s" %(str(fname))
				return None
			else:
				pass
		choice = cuke
		brine = cPickle()
		f_out = open(str(fname),"wb")
		if choice == "model":
			brine.dump(self.model,f_out,protocol=pickle.HIGHEST_PROTOCOL)
			print "saved ngram model as {0}".format(fname)
		elif choice == "freqs":
			brine.dump(self.ngramsFreqDict,f_out,protocol=pickle.HIGHEST_PROTOCOL)
			print "saved ngram frequencies as {0}".format(fname)
		elif choice == "grams":
			if n == 0:
				raise ValueError("n must be greater than 0")
			elif n in self.model.keys():
				brine.dump(self.model[n],f_out,protocol=pickle.HIGHEST_PROTOCOL)
				print "saved {0}-grams as {1}".format(n,fname)
			else:
				raise IndexError("n has to be equal to a set of trained ngrams (1-{0})".format(len(self.model.keys())))
		elif choice == "freq":
			if n == 0:
				raise ValueError("n must be greater than 0")
			elif n in self.model.keys():
				brine.dump(self.ngramFreqDict[n],f_out,protocol=pickle.HIGHEST_PROTOCOL)
				print "saved {0}-gram frequencies as {1}".format(n,fname)
			else:
				raise IndexError("n has to be equal to a set of trained ngrams (1-{0})".format(len(self.model.keys())))
		else:
			raise ValueError("invalid choice. options are grams, model, freq, or freqs.")
		f_out.close()
				
# 	 def gen_sent(self,length):
#  		import re
#  		import random
#  		self.str_out = ""
#  		self.start_p = re.compile(r'^[.?!\n]?')
#  		self.end_p = re.compile(r'[.?!\n]?$')
#  		self.starts = {}
#  		#self.ends = {}
#  		for d in self.ngramsFreqDict:
#  			self.starts[d] = []
#  			for item in d:
# 				if re.match(self.start_p,item[0])
#  					self.starts[d].append(item)
# #  			self.ends[d] = []
# #  			for item in d:
# #  				if re.search(self.end_p,item[0])
#  		
#  		while len(self.str_out) <= length or not re.match(self.end_p,self.str_out):
 				
				
#if __name__ == "__main__":
# from nltk.corpus import brown
# t = list(brown.words(categories="adventure"))
# n = get_gramsDict(t,3,False)
# y = get_gramFreqs(n,True)