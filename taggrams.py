class TagGrams(object):
	import cPickle
	#import itertools
	def get_dict(self,cutoff=None,ignore=[],print_results=True):
		"""	param cutoff: any tag with a count less than cutoff won't be included
			type cutoff: int
			ignore: ignore (i.e. don't include) certain tags
			type ignore: list of tags (str)"""
		self.gramsDict = dict()
		for item in self.tagged_corpus:
			if item[1] in self.gramsDict and item[0] not in ignore:
				self.gramsDict[item[1]] += 1
			elif item[0] not in ignore:
				self.gramsDict[item[1]] = 1
		if cutoff:
			final_dict = dict((k,v) for k in self.gramsDict.keys() for v in self.gramsDict.values() if v <= cutoff)
			self.grams_dict = final_dict
		self.sorted_d = sorted(self.gramsDict.items(),key=lambda x: x[1],reverse=True)
		if print_results==True:
			print self.sorted_d
		return self.sorted_d
	def get_tags(self,ignore=[],print_results=True):
		self.tags = dict((k,v) for (k,v) in self.tagged_corpus if k not in ignore)
		if print_results:
			print self.tags
	def __init__(self,corpus,grams=True,cutoff=None,ignore=[],print_results=True):
		import nltk
		"""if you want to use a pickled model, initialize TagGrams with
		corpus=None"""
		if corpus:
			if type(corpus) == list:
				self.corpus = [word.lower() for word in corpus]
			elif type(corpus) == set:
				self.corpus = [word.lower() for word in corpus]
			elif type(corpus) == str:
				tokenizer = tokenize.PunktWordTokenizer
				self.corpus = [word.lower() for word in tokenizer.tokenize(corpus)]
			else:
				self.corpus = [word.lower() for word in list(corpus)]
			#self.print_results = print_results
			print "Tagging corpus..."
			self.tagged_corpus = nltk.tag.pos_tag(self.corpus)
			if grams == True:
				self.get_dict(cutoff=cutoff,ignore=ignore,print_results=print_results)
	def pickle_model(self,fname):
		import cPickle
		import re
		if re.match(fname,".pickle") == False:
			fname += ".pickle"
		if os.path.isfile(fname):
			if raw_input("File exists! Overwrite? (y/n)") == "n":
				print "not overwriting file %s" %(str(fname))
				return None
			else:
				pass
		brine = cPickle()
		f_out = open(str(fname),"wb")
		brine.dump(self.model,f_out,protocol=pickle.HIGHEST_PROTOCOL)
		print "saved ngram model as {0}".format(fname)
		f_out.close()
	def get_model(self,fname):
		import cPickle
		import re
		if re.match(fname,".pickle") == False:
			fname += ".pickle"
		if os.path.isfile(fname) == False:
			raise IOError("no such file")
		else:
			f_in = open(fname,"rb")
			brine = cPickle()
			self.sorted_d = sorted(brine.load(f_in),key=lambda x: x[1],reverse=True)
			f_in.close()
	