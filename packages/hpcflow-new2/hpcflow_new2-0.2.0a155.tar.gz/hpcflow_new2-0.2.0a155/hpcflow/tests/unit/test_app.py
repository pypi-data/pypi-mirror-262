import pytest

from hpcflow.app import app as hf


@pytest.fixture
def act_env_1():
    return hf.ActionEnvironment(environment="env_1")


@pytest.fixture
def act_1(act_env_1):
    return hf.Action(
        commands=[hf.Command("<<parameter:p1>>")],
        environments=[act_env_1],
    )


def test_shared_data_from_json_like_with_shared_data_dependency(act_1):
    """Check we can generate some shared data objects where one depends on another."""

    p1 = hf.Parameter("p1")
    p1._set_hash()
    p1_hash = p1._hash_value

    ts1 = hf.TaskSchema(objective="ts1", actions=[act_1], inputs=[p1])
    ts1._set_hash()
    ts1_hash = ts1._hash_value

    env_label = ts1.actions[0].environments[0].environment

    shared_data_json = {
        "parameters": {
            p1_hash: {
                "is_file": p1.is_file,
                "sub_parameters": [],
                "type": p1.typ,
            }
        },
        "task_schemas": {
            ts1_hash: {
                "method": ts1.method,
                "implementation": ts1.implementation,
                "version": ts1.version,
                "objective": ts1.objective.name,
                "inputs": [{"parameter": f"hash:{p1_hash}", "labels": {"": {}}}],
                "outputs": [],
                "actions": [
                    {
                        "_from_expand": False,
                        "script": None,
                        "commands": [
                            {
                                "command": "<<parameter:p1>>",
                                "executable": None,
                                "arguments": None,
                                "stdout": None,
                                "stderr": None,
                                "stdin": None,
                            }
                        ],
                        "input_files": [],
                        "output_files": [],
                        "input_file_generators": [],
                        "output_file_parsers": [],
                        "environments": [
                            {
                                "scope": {"kwargs": {}, "type": "ANY"},
                                "environment": env_label,
                            }
                        ],
                        "rules": [],
                    }
                ],
            }
        },
    }

    sh = hf.template_components_from_json_like(shared_data_json)

    assert sh["parameters"] == hf.ParametersList([p1]) and sh[
        "task_schemas"
    ] == hf.TaskSchemasList([ts1])


def test_get_demo_data_manifest(null_config):
    hf.get_demo_data_files_manifest()


def test_get_demo_data_cache(null_config):
    hf.clear_demo_data_cache_dir()
    hf.cache_demo_data_file("text_file.txt")
    with hf.demo_data_cache_dir.joinpath("text_file.txt").open("rt") as fh:
        contents = fh.read()
    assert contents == "\n".join(f"{i}" for i in range(1, 11)) + "\n"
