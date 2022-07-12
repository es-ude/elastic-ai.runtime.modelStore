import mlflow
from rdflib import RDF, Graph, Literal, URIRef
from rdflib.namespace import DefinedNamespace, Namespace


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


def register_model(model_uri, name):
    version = mlflow.register_model(model_uri, name)

    client = mlflow.tracking.MlflowClient()
    run = client.get_run(version.run_id)

    if "hash" not in run.data.tags:
        raise Exception("Can't register model without hash")

    client.set_model_version_tag(version.name, version.version, "hash", run.data.tags["hash"])
    model_uri = f"model:{run.data.tags['hash']}"
    model_ref = URIRef(model_uri)

    graph = Graph()
    graph.add((model_ref, RDF.type, ServiceNamespace.Model))
    graph.add((model_ref, ServiceNamespace.ModelName, Literal(name)))

    if "size" in run.data.tags:
        graph.add((model_ref, ServiceNamespace.Size, Literal(int(run.data.tags["size"]))))
    if "accuracy" in run.data.metrics:
        graph.add((model_ref, ServiceNamespace.Accuracy, Literal(run.data.metrics["accuracy"])))
    if "mae" in run.data.metrics:
        graph.add((model_ref, ServiceNamespace.MeanAbsoluteError, Literal(run.data.metrics["mae"])))
    if "graph" in run.data.tags:
        user_graph = Graph().parse(data=run.data.tags["graph"], format="json-ld")
        for _, predicate, object in user_graph.triples((URIRef("model:placeholder"), None, None)):
            graph.add((model_ref, predicate, object))

    graph_json = graph.serialize(format="json-ld")
    client.set_model_version_tag(version.name, version.version, "graph", graph_json)


def log_predicate(predicate, object):
    client = mlflow.tracking.MlflowClient()
    active_run = client.get_run(mlflow.tracking.fluent._get_or_start_run().info.run_id)
    graph = Graph()
    if "graph" in active_run.data.tags:
        graph.parse(data=active_run.data.tags["graph"], format="json-ld")

    graph.add((URIRef("model:placeholder"), predicate, object))
    client.set_tag(active_run.info.run_id, "graph", graph.serialize(format="json-ld"))
