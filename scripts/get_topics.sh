
langpipe readlines -f ../raw_transcriptions_8000.txt \
	sentences replace -f replacements.csv \
	words filter-length-gte -m 3 \
	remove-stopwords -f stop_words.txt trace \
	filter-pos -p 'NN' -p 'NNP' -p 'NNS' -p 'NNPS' \
	trace
