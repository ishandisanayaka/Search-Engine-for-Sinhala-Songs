#Scrapy project is python scrapy project that used for crawl web sites and extract songs.
It can be run using that command:   
	scrapy crawl lyrics -o output.json

#Data set folder contain final Data set that used to search engine as a .json file

#Insert to Elasticsearch is used to insert .json file to the elasticsearch index.
It can be run using that command:
	python bulk_insert.py

#search engine folder contain python search project including the user interfaces
It can be run using that command:
	python app.py
