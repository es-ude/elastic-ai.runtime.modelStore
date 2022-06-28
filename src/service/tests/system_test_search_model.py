import unittest
import monitor
import threading
import paho.mqtt.subscribe as subscribe
import paho.mqtt.publish as publish
import time
from .helper_model_store_test import SetUpModelStore
from pathlib import Path
import _thread
import requests
from rdflib import Graph, URIRef, Literal, RDF
from service.service_namespace import ServiceNamespace
from rdflib.namespace import XSD

CLIENT_ID = 1
PUBLIC_HOSTNAME = "broker.hivemq.com"
THIS_DIR = Path(__file__).resolve().parent
TEST_MLFLOW_URI = "http://localhost:6000"

class SystemTestSearchModel(unittest.TestCase):
    def setUp(self):
        self._monitor = monitor.Monitor(TEST_MLFLOW_URI)
        self._received_model_uri = False

    def _start_service(self):
        _thread.start_new_thread(self._monitor.run, ())

    def _subscribe_to_public_broker(self, callback):
        subscribe.callback(callback, "/"+str(CLIENT_ID), hostname=PUBLIC_HOSTNAME, )

    def _start_client_with_callback(self, callback):
        _thread.start_new_thread(self._subscribe_to_public_broker, (callback,))

    def _deliver(self, client, userdata, message):
        #todo: checken, on die gesendete URI die richtige ist.
        self.assertEqual("http://platzhalter.de/hello_world_model_3", bytes.decode(message.payload))
        self._received_model_uri = True
        _thread.exit()

    def _request_search_for_model(self):
        #create graph for the problem:
        problem_graph = Graph()
        problem_graph.bind("service_namespace", ServiceNamespace)
        problem_description = URIRef("http://platzhalter.de/problem_description")
        problem_graph.add((problem_description, ServiceNamespace.Predict, ServiceNamespace.Sine))
        problem_graph.add((problem_description, ServiceNamespace.Input, ServiceNamespace.Float))
        problem_graph.add((problem_description, ServiceNamespace.Output, ServiceNamespace.Float))
        problem_graph.add((problem_description, ServiceNamespace.Size, Literal(1100, datatype=XSD.integer)))
        problem_graph.add((problem_description, ServiceNamespace.Accuracy, Literal(0.9, datatype=XSD.double)))
        serialized_graph = problem_graph.serialize(format="json-ld")

        message = str(CLIENT_ID) + "$" + serialized_graph
        publish.single("/service/searchModel", message, hostname=PUBLIC_HOSTNAME)


    def test_start_monitor_and_send_search_request(self):
        self._start_service()
        self._start_client_with_callback(self._deliver)
        time.sleep(0.5)

        self._request_search_for_model()
        time.sleep(0.5)
        self.assertTrue(self._received_model_uri)

    def tearDown(self) -> None:
        pass
