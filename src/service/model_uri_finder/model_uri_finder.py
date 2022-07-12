from cmath import e
import os

from rdflib import Graph, URIRef
from rdflib.namespace import Namespace

from service.errors import ModelUriNotFound
from service.service_namespace import ServiceNamespace


URI_STRING_IN_SPARQL_SYNTAX = "service_namespace:"
import time


class ModelUriFinder:

    def __init__(self):
        self._base_uri = "http://platzhalter.de/service_namespace#"
        self._base_uri_length = len(self._base_uri)
        self._namespace = Namespace(self._base_uri)

        self._type_graph = self._build_type_graph()
        self._model_graph = None

    def _build_type_graph(self):
        ns = self._namespace
        graph = Graph()

        graph.add((ns.Digits, ns.ModelType, ns.Classification))
        graph.add((ns.Sine, ns.ModelType, ns.Regression))

        return graph

    def _check_triple_for_optional(self, request_graph, p):
        for triple in request_graph.triples((p, ServiceNamespace.Priority, ServiceNamespace.Optional)):
            return True
        return False

    def _initialize_query_string(self):
        prefix = "PREFIX service_namespace: <"+ self._base_uri + ">\n"
        model_query = prefix + "SELECT DISTINCT ?Model\nWHERE {\n"
        return model_query

    def _query_add_size(self, model_query, p_string, size):
        model_query += "\t?Model " + p_string  + " " + "?Size" + " .\n" + "FILTER (?Size <= "+ str(size)  + ")\n"
        return model_query

    def _query_add_accuracy(self, model_query, p_string, accuracy):
        model_query += "\t?Model " + p_string  + " " + "?Accuracy" + " .\n" + "FILTER (?Accuracy >= "+ str(accuracy)  + ")\n"
        return model_query

    def _query_add_mae(self, model_query, p_string, mae):
        model_query += f"\t?Model {p_string} ?MeanAbsoluteError .\n"
        model_query += f"FILTER (?MeanAbsoluteError <= {mae})\n"
        return model_query

    def _query_add_regular_requirement(self, model_query, p_string, o_string):
        model_query += "\t?Model " + p_string + " " + o_string + " .\n"
        return model_query

    def _query_get_uri_in_sparql_syntax(self, uri:str):
        return URI_STRING_IN_SPARQL_SYNTAX+uri[self._base_uri_length:]

    def _query_add_end(self, model_query, model_type):
        model_query += "}"
        if model_type == self._namespace.Regression:
            model_query += "ORDER BY ASC(?MeanAbsoluteError)"
        else:
            model_query += "ORDER BY DESC(?Accuracy)"
        return model_query

    def create_query(self, request_graph, use_optional_requirements=True):
        model_query = self._initialize_query_string()
        model_type = None

        for s, p, o in request_graph.triples((URIRef("http://platzhalter.de/problem_description"), None, None)):

            p_string = self._query_get_uri_in_sparql_syntax(p)

            if (not use_optional_requirements):
                if self._check_triple_for_optional(request_graph,p):
                    continue

            if(p_string == "service_namespace:Size"):
                model_query = self._query_add_size(model_query, p_string, o)
                continue
            elif(p_string  == "service_namespace:Accuracy"):
                model_query = self._query_add_accuracy(model_query, p_string, o)
                continue
            elif p_string == "service_namespace:MeanAbsoluteError":
                model_query = self._query_add_mae(model_query, p_string, o)
                continue
            else:
                if p_string == "service_namespace:Predict":
                    model_type = next(self._type_graph.objects(o, self._namespace.ModelType), None)

                o_string = self._query_get_uri_in_sparql_syntax(o)
                model_query = self._query_add_regular_requirement(model_query, p_string, o_string)

        model_query = self._query_add_end(model_query, model_type)

        return model_query

    def load_json_graphs(self, graphs: list[str]):
        full_graph = Graph()
        for graph in graphs:
            full_graph += Graph().parse(data=graph, format="json-ld")

        print(f"finder loading graph: {full_graph.serialize()}")
        self._model_graph = full_graph

    def search_for_model(self, serialized_request_graph)->URIRef:
        request_graph = Graph()
        request_graph.parse(data=serialized_request_graph, format="json-ld")
        print(f"finder searching graph: {request_graph.serialize()}")

        request_query = self.create_query(request_graph)
        print(f" query: {request_query}")
        qres = self._model_graph.query(request_query)


        if len(qres) == 0:
            #try again, this time without optional requirements.
            request_query = self.create_query(request_graph, use_optional_requirements=False)
            qres = self._model_graph.query(request_query)
            if len(qres) == 0:
                raise ModelUriNotFound

        #Only the first result will be returned. Allways the one with the highest Accuracy
        for row in qres:
            time.sleep(1)
            return row.Model
