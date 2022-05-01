from bson import ObjectId
from elasticsearch import Elasticsearch
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http.response import HttpResponse
import json
import pymongo

class NodeInfo(APIView):

    def get(self, request, *args, **kwargs):
        es = Elasticsearch("http://127.0.0.1:9200")
        id=kwargs['id']
        res = es.nodes.info(node_id=id)
        return Response(str(res))
class Health(APIView):

    def get(self, request, *args, **kwargs):
        es = Elasticsearch("http://127.0.0.1:9200")
        # id=kwargs['id']
        res = es.cluster.health()
        return Response(str(res))
class Stats(APIView):

    def get(self, request, *args, **kwargs):
        es = Elasticsearch("http://127.0.0.1:9200")
        # id=kwargs['id']
        res = es.cluster.stats()
        return Response(str(res))

class Indices(APIView):

    def get(self, request, *args, **kwargs):
        es = Elasticsearch("http://127.0.0.1:9200")
        # id=kwargs['id']
        res = es.indices.get_alias().keys()
        return Response(str(res))

class BackendList(APIView):

    def get(self, request, *args, **kwargs):
        #  Mongodb Connection

        client = pymongo.MongoClient()
        mydb = client["URL"]
        mycol = mydb["reqUrl"]

        if 'id' in kwargs:

            id = kwargs['id']
            single = mycol.find_one({"_id": ObjectId(id)})
            if not single:
                return Response("Wrong ID or ID not Found")
            else:
                return Response(str(single))
        else:
            res = mycol.find({})
            result = []
            for x in res:
                result.append(x)
            return Response(str(result))

    def post(self, request, format=None):

        obj1 = request.body.decode('utf-8')
        data = json.loads(obj1)
        ip = data['ip']
        portint = data['port']
        port = str(data['port'])
        un = data['username']
        pas = data['password']
        use_ssl = data['use_ssl']
        if use_ssl == "False":
            url = "http://" + ip + ":" + port
        else:
            url = "https://" + ip + ":" + port
        try:
            # Elasticsearch Connection

            es = Elasticsearch(url)
            res = es.info()
            # Mongodb Connection

            client = pymongo.MongoClient()
            mydb = client["URL"]
            mycol = mydb["reqUrl"]
            retrive = mycol.find_one({"ip": ip, "port": portint})
            if not retrive:
                mycol.insert_one(data)
                return Response(res)
            else:
                return Response(res)

        except Exception as e:
            return HttpResponse(e, status=400)

    def delete(self, request, *args, **kwargs):
        # Mongodb Connection

        client = pymongo.MongoClient()
        mydb = client["URL"]
        mycol = mydb["reqUrl"]
        if 'id' in kwargs:
            id = kwargs['id']
            presence = mycol.find_one({"_id": ObjectId(id)})
            if not presence:
                return Response("Data of that ID not available")
            else:
                mycol.delete_one({"_id": ObjectId(id)})
                return Response("deleted")
        else:
            mycol.delete_many({})
            return Response("All Data Deleted Successfully")

    def put(self, request, *args, **kwargs):

        obj1 = request.body.decode('utf-8')
        data = json.loads(obj1)
        # Mongodb Connection

        client = pymongo.MongoClient()
        mydb = client["URL"]
        mycol = mydb["reqUrl"]

        id = kwargs['id']
        presence = mycol.find_one({"_id": ObjectId(id)})
        if not presence:
            return Response("Data of that ID not available")
        else:
            mycol.delete_one({"_id": ObjectId(id)})
            mycol.insert_one(data)
            return Response("updated successfully")
