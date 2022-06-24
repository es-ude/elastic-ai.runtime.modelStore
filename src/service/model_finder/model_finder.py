from rdflib import Graph, URIRef
from service.store_connection import ModelNotFound

class IllegalGraphException(Exception):
    pass

class ModelFinder:

    def __init__(self):
        self._graph = None

    #todo:statt None Priority
    def _check_triple_for_optional(self, request_graph, p):
        for triple in request_graph.triples((p, None, None)):
            return True
        else:
            return False

    #todo: in case of multiple results, sort by accuracy
    def create_query(self, request_graph, use_optional_requirements=True):
        base_uri = "http://platzhalter.de/service_namespace"
        prefix = "PREFIX service_namespace: <"+ base_uri + ">\n"
        model_query = prefix + "SELECT DISTINCT ?Model\nWHERE {\n"
        base_uri_length = len(base_uri)
        uri_string_in_sparql_syntax = "service_namespace:"
        for s, p, o in request_graph.triples((URIRef("http://platzhalter.de/problem_description"), None, None)):

            p_string = uri_string_in_sparql_syntax+p[base_uri_length:]

            if (not use_optional_requirements) and self._check_triple_for_optional(request_graph, p):
                continue

            if(p_string == "service_namespace:Size"):
                model_query += "\t?Model " + p_string  + " " + "?Size" + " .\n" + "FILTER (?Size <= "+ str(o)  + ")\n"
                continue
            elif(p_string  == "service_namespace:Accuracy"):
                model_query += "\t?Model " + p_string  + " " + "?Accuracy" + " .\n" + "FILTER (?Accuracy >= "+ str(o)  + ")\n"
                continue
            else:
                o_string = uri_string_in_sparql_syntax+o[base_uri_length:]
                model_query += "\t?Model " + p_string + " " + o_string + " .\n"

        model_query += "}"
        return model_query

    def load_graph(self):
        path = "service/model_finder/rdf_graphs/"
        graph_file_1 = open(path+'graph.json','r')
        graph_file_2 = open(path+'graph2.json','r')
        graph_file_3 = open(path+'graph3.json','r')
        graph_file_4 = open(path+'graph4.json','r')

        #+ : Union of both graphs
        model_graph = Graph()
        model_graph = model_graph + Graph().parse(data=graph_file_1.read(), format="json-ld")
        model_graph = model_graph + Graph().parse(data=graph_file_2.read(), format="json-ld")
        model_graph = model_graph + Graph().parse(data=graph_file_3.read(), format="json-ld")
        model_graph = model_graph + Graph().parse(data=graph_file_4.read(), format="json-ld")

        return model_graph
        #todo: soll unabhängig vom gestarteten verzeichnis sein.

    def _set_graph(self, graph):
        self._graph = graph

    def search_for_model(self, serialized_request_graph)->URIRef:
        request_graph = Graph()
        request_graph.parse(data=serialized_request_graph, format="json-ld")

        request_query = self.create_query(request_graph)
        qres = self._graph.query(request_query)


        if len(qres) == 0:
            #try again, this time without optional requirements.
            request_query = self.create_query(request_graph, use_optional_requirements=False)
            qres = self._graph.query(request_query)
            if len(qres) == 0:
                raise ModelNotFound

        for row in qres:
            return row.Model
