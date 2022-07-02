import unittest
from service.model_uri_finder import ModelUriFinder, IllegalGraphException
from rdflib import Graph, URIRef, Literal, RDF
from service.service_namespace import ServiceNamespace
from rdflib.namespace import XSD

def clean_string(string):
    string = string.replace(" ", "")
    string = string.replace("\t","")
    string = string.replace("\n","")
    return string

class TestModelFinder(unittest.TestCase):
    def setUp(self):
        self._model_finder = ModelUriFinder()
        self._test_model = URIRef("http://platzhalter.de/problem_description")
        self._graph = Graph()
        self._graph.bind("service_namespace", ServiceNamespace)

    def test_simple_query(self):
        correct_query = """
        PREFIX service_namespace: <http://platzhalter.de/service_namespace>
        SELECT DISTINCT ?Model
        WHERE {
            ?Model service_namespace:Predict service_namespace:Sine .
        }
        ORDER BY DESC(?Accuracy)
        """
        self._graph.add((self._test_model, ServiceNamespace.Predict, ServiceNamespace.Sine))
        test_query_result = self._model_finder.create_query(self._graph)

        correct_query = clean_string(correct_query)
        test_query_result = clean_string(test_query_result)
        self.assertEqual(test_query_result, correct_query)

    def test_query_with_size(self):
        correct_query = """
        PREFIX service_namespace: <http://platzhalter.de/service_namespace>
        SELECT DISTINCT ?Model
        WHERE {
            ?Model service_namespace:Size ?Size .
        FILTER (?Size <= 1500)
        }
        ORDER BY DESC(?Accuracy)
        """
        self._graph.add((self._test_model, ServiceNamespace.Size, Literal(1500, datatype=XSD.integer)))
        test_query_result = self._model_finder.create_query(self._graph)

        correct_query = clean_string(correct_query)
        test_query_result = clean_string(test_query_result)
        self.assertEqual(test_query_result, correct_query)

    def test_query_with_accuracy(self):
        correct_query = """
        PREFIX service_namespace: <http://platzhalter.de/service_namespace>
        SELECT DISTINCT ?Model
        WHERE {
            ?Model service_namespace:Accuracy ?Accuracy .
        FILTER (?Accuracy >= 0.8)
        }
        ORDER BY DESC(?Accuracy)
        """
        self._graph.add((self._test_model, ServiceNamespace.Accuracy, Literal(0.8, datatype=XSD.double)))
        test_query_result = self._model_finder.create_query(self._graph)

        correct_query = clean_string(correct_query)
        test_query_result = clean_string(test_query_result)
        self.assertEqual(test_query_result, correct_query)

    def test_find_model(self):
        #Graph of the known models:
        self._graph.add((self._test_model, RDF.type, ServiceNamespace.Model))
        self._graph.add((self._test_model, ServiceNamespace.Predict, ServiceNamespace.Sine))
        self._graph.add((self._test_model, ServiceNamespace.Input, ServiceNamespace.Float))
        self._graph.add((self._test_model, ServiceNamespace.Output, ServiceNamespace.Float))

        #Graph for the requested model:
        problem_graph = Graph()
        problem_graph.bind("service_namespace", ServiceNamespace)
        problem_description = URIRef("http://platzhalter.de/problem_description")
        problem_graph.add((problem_description, ServiceNamespace.Predict, ServiceNamespace.Sine))
        problem_graph.add((problem_description, ServiceNamespace.Input, ServiceNamespace.Float))
        problem_graph.add((problem_description, ServiceNamespace.Output, ServiceNamespace.Float))
        serialized_graph = problem_graph.serialize(format="json-ld")

        self._model_finder._set_graph(self._graph)
        returned_model_uri = self._model_finder.search_for_model(serialized_graph)

        self.assertEqual(returned_model_uri, self._test_model)

    def test_find_model_with_size_and_accuracy(self):
        #Graph of the known models:
        self._graph.add((self._test_model, RDF.type, ServiceNamespace.Model))
        self._graph.add((self._test_model, ServiceNamespace.Predict, ServiceNamespace.Sine))
        self._graph.add((self._test_model, ServiceNamespace.Input, ServiceNamespace.Float))
        self._graph.add((self._test_model, ServiceNamespace.Output, ServiceNamespace.Float))
        self._graph.add((self._test_model, ServiceNamespace.Size, Literal(1000, datatype=XSD.integer)))
        self._graph.add((self._test_model, ServiceNamespace.Accuracy, Literal(0.9, datatype=XSD.double)))


        #Graph for the requested model:
        problem_graph = Graph()
        problem_graph.bind("service_namespace", ServiceNamespace)
        problem_description = URIRef("http://platzhalter.de/problem_description")
        problem_graph.add((problem_description, ServiceNamespace.Predict, ServiceNamespace.Sine))
        problem_graph.add((problem_description, ServiceNamespace.Input, ServiceNamespace.Float))
        problem_graph.add((problem_description, ServiceNamespace.Output, ServiceNamespace.Float))
        problem_graph.add((problem_description, ServiceNamespace.Size, Literal(1100, datatype=XSD.integer)))
        problem_graph.add((problem_description, ServiceNamespace.Accuracy, Literal(0.8, datatype=XSD.double)))
        serialized_graph = problem_graph.serialize(format="json-ld")

        self._model_finder._set_graph(self._graph)
        returned_model_uri = self._model_finder.search_for_model(serialized_graph)

        self.assertEqual(returned_model_uri, self._test_model)


    def test_retry_find_model_without_optional_parameters(self):
        #Graph of the known models:
        self._graph.add((self._test_model, RDF.type, ServiceNamespace.Model))
        self._graph.add((self._test_model, ServiceNamespace.Predict, ServiceNamespace.Sine))
        self._graph.add((self._test_model, ServiceNamespace.Input, ServiceNamespace.Float))

        #Graph for the requested model:
        problem_graph = Graph()
        problem_graph.bind("service_namespace", ServiceNamespace)
        problem_description = URIRef("http://platzhalter.de/problem_description")
        problem_graph.add((problem_description, ServiceNamespace.Predict, ServiceNamespace.Sine))
        problem_graph.add((problem_description, ServiceNamespace.Input, ServiceNamespace.Float))
        problem_graph.add((problem_description, ServiceNamespace.Output, ServiceNamespace.Float))
        problem_graph.add((ServiceNamespace.Output, ServiceNamespace.Priority, ServiceNamespace.Optional))

        serialized_graph = problem_graph.serialize(format="json-ld")

        self._model_finder._set_graph(self._graph)
        returned_model_uri = self._model_finder.search_for_model(serialized_graph)

        self.assertEqual(returned_model_uri, self._test_model)

    def test_find_model_with_optional_size(self):
        #Graph of the known models:
        self._graph.add((self._test_model, RDF.type, ServiceNamespace.Model))
        self._graph.add((self._test_model, ServiceNamespace.Predict, ServiceNamespace.Sine))
        self._graph.add((self._test_model, ServiceNamespace.Input, ServiceNamespace.Float))
        self._graph.add((self._test_model, ServiceNamespace.Output, ServiceNamespace.Float))
        self._graph.add((self._test_model, ServiceNamespace.Size, Literal(1100, datatype=XSD.integer)))

        #Graph for the requested model:
        problem_graph = Graph()
        problem_graph.bind("service_namespace", ServiceNamespace)
        problem_description = URIRef("http://platzhalter.de/problem_description")
        problem_graph.add((problem_description, ServiceNamespace.Predict, ServiceNamespace.Sine))
        problem_graph.add((problem_description, ServiceNamespace.Input, ServiceNamespace.Float))
        problem_graph.add((problem_description, ServiceNamespace.Output, ServiceNamespace.Float))
        problem_graph.add((problem_description, ServiceNamespace.Size, Literal(900, datatype=XSD.integer)))
        problem_graph.add((ServiceNamespace.Size, ServiceNamespace.Priority, ServiceNamespace.Optional))

        serialized_graph = problem_graph.serialize(format="json-ld")

        self._model_finder._set_graph(self._graph)
        returned_model_uri = self._model_finder.search_for_model(serialized_graph)

        self.assertEqual(returned_model_uri, self._test_model)

    #Assumption: All graphs are correct.
    '''
    def test_find_model_with_illegal_store_graph(self):
        #Graph of the known models:
        self._graph.add((self._test_model, RDF.type, ServiceNamespace.Model))
        self._graph.add((self._test_model, ServiceNamespace.Predict, ServiceNamespace.Sine))
        self._graph.add((self._test_model, ServiceNamespace.Input, ServiceNamespace.Float))
        self._graph.add((self._test_model, ServiceNamespace.Output, ServiceNamespace.Float))
        self._graph.add((ServiceNamespace.Output, ServiceNamespace.Priority, ServiceNamespace.Optional)) #priority does not make sense for the store graph

        #Graph for the requested model:
        problem_graph = Graph()
        problem_graph.bind("service_namespace", ServiceNamespace)
        problem_description = URIRef("http://platzhalter.de/problem_description")
        problem_graph.add((problem_description, ServiceNamespace.Predict, ServiceNamespace.Sine))
        problem_graph.add((problem_description, ServiceNamespace.Input, ServiceNamespace.Float))
        problem_graph.add((problem_description, ServiceNamespace.Output, ServiceNamespace.Float))

        serialized_graph = problem_graph.serialize(format="json-ld")

        self._model_finder._set_graph(self._graph)

        self.assertRaises(IllegalGraphException, self._model_finder.search_store, serialized_graph)

    def test_find_model_with_illegl_problem_graph(self):
        pass
        '''
