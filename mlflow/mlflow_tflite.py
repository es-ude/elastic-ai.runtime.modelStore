import hashlib
import os
import sys

import mlflow
from mlflow.models import Model
from mlflow.tracking.artifact_utils import _download_artifact_from_uri
from mlflow.utils.environment import (
    _CONDA_ENV_FILE_NAME,
    _CONSTRAINTS_FILE_NAME,
    _REQUIREMENTS_FILE_NAME,
    _process_conda_env,
    _process_pip_requirements,
)
from mlflow.utils.file_utils import write_to
from mlflow.utils.model_utils import (
    _get_flavor_configuration,
    _validate_and_prepare_target_save_path,
)
import yaml


FLAVOR_NAME = "tflite"

mlflow_tflite = sys.modules[__name__]


def get_default_pip_requirements():
    return mlflow.tensorflow.get_default_pip_requirements()


def get_default_conda_env():
    return mlflow.tensorflow.get_default_conda_env()


def log_model(tflite_model, artifact_path, registered_model_name=None, await_registration_for=300, **kwargs):
    Model.log(
        artifact_path, mlflow_tflite, tflite_model=tflite_model, **kwargs
    )
    if registered_model_name is not None:
        run_id = mlflow.tracking.fluent.active_run().info.run_id
        version = mlflow.register_model(
            "runs:/%s/%s" % (run_id, artifact_path),
            registered_model_name,
            await_registration_for=await_registration_for,
        )

        model_hash = hashlib.sha256(tflite_model).digest()
        client = mlflow.tracking.MlflowClient()
        client.set_model_version_tag(version.name, version.version, "hash", model_hash.hex())


def save_model(
    tflite_model,
    path,
    mlflow_model=None,
    conda_env=None,
    pip_requirements=None,
    extra_pip_requirements=None,
):
    _validate_and_prepare_target_save_path(path)

    if mlflow_model is None:
        mlflow_model = Model()

    model_data_subpath = "model.tflite"
    model_data_path = os.path.join(path, model_data_subpath)

    with open(model_data_path, "wb") as file:
        file.write(tflite_model)

    mlflow_model.add_flavor(FLAVOR_NAME, data=model_data_subpath)
    mlflow_model.save(os.path.join(path, "MLmodel"))

    if conda_env is None:
        if pip_requirements is None:
            default_reqs = get_default_pip_requirements()
            inferred_reqs = mlflow.models.infer_pip_requirements(
                path, FLAVOR_NAME, fallback=default_reqs
            )
            default_reqs = sorted(set(inferred_reqs).union(default_reqs))
        else:
            default_reqs = None

        conda_env, pip_requirements, pip_constraints = _process_pip_requirements(
            default_reqs, pip_requirements, extra_pip_requirements
        )
    else:
        conda_env, pip_requirements, pip_constraints = _process_conda_env(conda_env)

    with open(os.path.join(path, _CONDA_ENV_FILE_NAME), "w") as file:
        yaml.safe_dump(conda_env, stream=file, default_flow_style=False)

    if pip_constraints:
        write_to(os.path.join(path, _CONSTRAINTS_FILE_NAME), "\n".join(pip_constraints))

    write_to(os.path.join(path, _REQUIREMENTS_FILE_NAME), "\n".join(pip_requirements))


def load_model(model_uri, dst_path=None):
    local_model_path = _download_artifact_from_uri(model_uri, dst_path)
    flavor_conf = _get_flavor_configuration(local_model_path, FLAVOR_NAME)
    tflite_model_file_path = os.path.join(local_model_path, flavor_conf.get("data", "model.tflite"))

    with open(tflite_model_file_path, "rb") as model_file:
        model = model_file.read()

    return model
