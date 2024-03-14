'''
    Ref from FedML: https://github.com/FedML-AI/FedML/blob/master/python/fedml/arguments.py
'''

import argparse
import os

import yaml


def add_args():
    parser = argparse.ArgumentParser(description="CFBench")
    parser.add_argument(
        "--yaml_config_file",
        "--cf",
        help="yaml configuration file",
        type=str,
        default="",
    )

    # default arguments
    parser.add_argument("--run_id", type=str, default="0")

    # default arguments
    parser.add_argument("--rank", type=int, default=0)

    # default arguments
    parser.add_argument("--local_rank", type=int, default=0)

    # For hierarchical scenario
    parser.add_argument("--node_rank", type=int, default=0)

    # default arguments
    parser.add_argument("--role", type=str, default="client")

    args, unknown = parser.parse_known_args()
    return args


class Arguments:
    """Argument class which contains all arguments from yaml config and constructs additional arguments"""

    def __init__(self, cmd_args, training_type=None, comm_backend=None, override_cmd_args=True):
        # set the command line arguments
        cmd_args_dict = cmd_args.__dict__
        for arg_key, arg_val in cmd_args_dict.items():
            setattr(self, arg_key, arg_val)

        self.get_default_yaml_config(cmd_args)
        if not override_cmd_args:
            # reload cmd args again
            for arg_key, arg_val in cmd_args_dict.items():
                setattr(self, arg_key, arg_val)

    def load_yaml_config(self, yaml_path):
        with open(yaml_path, "r") as stream:
            try:
                return yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                raise ValueError("Yaml error - check yaml file")

    def get_default_yaml_config(self, cmd_args):
        self.yaml_paths = [cmd_args.yaml_config_file]
        # Load all arguments from yaml config
        # https://www.cloudbees.com/blog/yaml-tutorial-everything-you-need-get-started
        configuration = self.load_yaml_config(cmd_args.yaml_config_file)

        # Override class attributes from current yaml config
        self.set_attr_from_config(configuration)

        return configuration

    def set_attr_from_config(self, configuration):
        for _, param_family in configuration.items():
            for key, val in param_family.items():
                setattr(self, key, val)


def load_arguments(training_type=None, comm_backend=None):
    cmd_args = add_args()
    # Load all arguments from YAML config file
    args = Arguments(cmd_args, training_type, comm_backend)

    if not hasattr(args, "worker_num"):
        args.worker_num = args.client_num_per_round

    # os.path.expanduser() method in Python is used
    # to expand an initial path component ~( tilde symbol)
    # or ~user in the given path to user’s home directory.
    if hasattr(args, "data_cache_dir"):
        args.data_cache_dir = os.path.expanduser(args.data_cache_dir)
    if hasattr(args, "data_file_path"):
        args.data_file_path = os.path.expanduser(args.data_file_path)
    if hasattr(args, "partition_file_path"):
        args.partition_file_path = os.path.expanduser(args.partition_file_path)
    if hasattr(args, "part_file"):
        args.part_file = os.path.expanduser(args.part_file)

    args.rank = int(args.rank)

    return args
