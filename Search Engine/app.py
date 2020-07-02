from flask import Flask, render_template, request
from elasticsearch import Elasticsearch
import re
import json

app = Flask(__name__)
es = Elasticsearch('127.0.0.1', port=9200)

@app.route('/')
def home():
    return render_template('search.html')

@app.route('/search/results', methods=['GET', 'POST'])
def search_request():
    sizecommon=500
    isහොඳමගීත=False
    isහොඳමගායකයෝ=False
    search_term = request.form["input"]
    if("ගායකයා"  in search_term):
        search_term = re.sub('ගායකයා$', '', search_term)
        if("හොඳම ගීත"  in search_term):
            search_term = re.sub('ගායකයා හොඳම ගීත$', '', search_term)
            isහොඳමගීත=True
        res = es.search(
        index="sinhala_song_collection", 
        size=sizecommon, 
        body={
            "query": {
                "multi_match" : {
                    
                    "query": search_term, 
                    "fields": [
                        "url", 
                        "artist_name_si"
                    ]
                    }
            }
        }
    )
       # sorted_obj = dict(res) 
        if(isහොඳමගීත):
            
            res["hits"]["hits"] = sorted(res["hits"]["hits"], key=lambda x : int(x["_source"]["track_rating"],16), reverse=True)
            if(hasNumbers(search_term)):
                sizecommonstr=''.join(list(filter(str.isdigit, search_term)))
                int(sizecommonstr)
                a=[]
                for x in range(int(sizecommonstr)):
                    a.append(res["hits"]["hits"][x])
                
                res["hits"]["hits"]=a
    elif("ඇල්බමය"  in search_term):
        search_term = re.sub('ඇල්බමය$', '', search_term)
        if("හොඳම ගීත"  in search_term):
            search_term = re.sub('ඇල්බමය හොඳම ගීත$', '', search_term)
            isහොඳමගීත=True
        if("හොඳම ගායකයෝ"  in search_term):
            search_term = re.sub('ඇල්බමය හොඳම ගායකයෝ$', '', search_term)
            isහොඳමගායකයෝ=True
        res = es.search(
        index="sinhala_song_collection", 
        size=sizecommon, 
        body={
            "query": {
                "multi_match" : {
                    "query": search_term, 
                    "fields": [
                        "url", 
                        "album_name_si"
                    ]
                }
            }
        }
    )
        if(isහොඳමගායකයෝ):
            res["hits"]["hits"] = sorted(res["hits"]["hits"], key=lambda x : int(x["_source"]["artist_rating"],16), reverse=True)
            if(hasNumbers(search_term)):
                sizecommonstr=''.join(list(filter(str.isdigit, search_term)))
                int(sizecommonstr)
                a=[]
                for x in range(int(sizecommonstr)):
                    a.append(res["hits"]["hits"][x])
                
                res["hits"]["hits"]=a
                    
        if(isහොඳමගීත):
            res["hits"]["hits"] = sorted(res["hits"]["hits"], key=lambda x : int(x["_source"]["track_rating"],16), reverse=True)
            if(hasNumbers(search_term)):
                sizecommonstr=''.join(list(filter(str.isdigit, search_term)))
                int(sizecommonstr)
                a=[]
                for x in range(int(sizecommonstr)):
                    a.append(res["hits"]["hits"][x])
                
                res["hits"]["hits"]=a
    elif("ගීතයේ නම"  in search_term):
        res = es.search(
        index="sinhala_song_collection", 
        size=sizecommon, 
        body={
            "query": {
                "multi_match" : {
                    "query": search_term, 
                    "fields": [
                        "url", 
                        "track_name_si"
                    ] 
                }
            }
        }
    )
    elif("සිංදුව"  in search_term ):
        res = es.search(
        index="sinhala_song_collection", 
        size=sizecommon, 
        body={
            "query": {
                "multi_match" : {
                    "query": search_term, 
                    "fields": [
                        "url", 
                        "lyrics"
                    ] 
                }
            }
        }
    )
    elif( "පද රචනය"  in search_term):
        res = es.search(
        index="sinhala_song_collection", 
        size=sizecommon, 
        body={
            "query": {
                "multi_match" : {
                    "query": search_term, 
                    "fields": [
                        "url", 
                        "lyrics"
                    ] 
                }
            }
        }
    )
    elif( "ගීතය"  in search_term):
        res = es.search(
        index="sinhala_song_collection", 
        size=sizecommon, 
        body={
            "query": {
                "multi_match" : {
                    "query": search_term, 
                    "fields": [
                        "url", 
                        "lyrics"
                    ] 
                }
            }
        }
    )
        
    else:
        res = es.search(
        index="sinhala_song_collection", 
        size=500, 
        body={
            "query": {
                "multi_match" : {
                    "query": search_term, 
                    "fields": [
                        "url", 
                        "title", 
                        "track_name_si",
                        "album_name_si",
                        "track_rating",
                        "track_id",
                        "artist_name_si",
                        "artist_rating",
                        "lyrics"
                    ]
                }
            }
        }
        
    )
    return render_template('results.html', res=res )
def hasNumbers(inputString):
     return any(char.isdigit() for char in inputString)
if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(host='0.0.0.0', port=5000)