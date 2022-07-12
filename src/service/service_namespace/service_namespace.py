from rdflib.namespace import Namespace, DefinedNamespace
from rdflib import URIRef

class ServiceNamespace(DefinedNamespace):
    Model: URIRef  # A model.
    ModelName: URIRef  #  Name of the Model

    Input: URIRef  # Input for a Model
    Output: URIRef  # Output of the Model
    Float: URIRef  # Floating Point Value

    Size: URIRef  # Size of the Model

    Predict: URIRef  #  A Model can predict something
    Sine: URIRef  #  Sine function
    Digits: URIRef # MNIST digit classification

    # Evaluation metrics
    Accuracy: URIRef
    MeanAbsoluteError: URIRef

    Optional: URIRef  #  Expressing, that a certain requirement is only optional
    Priority: URIRef  #  for expressing a predicate's priority

    _NS = Namespace("http://platzhalter.de/service_namespace#")
