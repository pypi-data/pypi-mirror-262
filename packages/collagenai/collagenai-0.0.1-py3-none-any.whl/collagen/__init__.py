from datetime import datetime
from collagen.utils.arguments import load_arguments, Arguments
from loguru import logger
import random
import numpy as np
import torch
import socket
import os
import wandb

PROJECT_START_DATETIME = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")

def init(args=None):
    # TODO not be used currently

    # Setup project start datetime in format %Y-%m-%d_%H:%M:%S
    global PROJECT_START_DATETIME

    # Load arguments
    if args is None:
        args = load_arguments()

    args = Arguments(args)
    logger.info(f"System arguments: {vars(args)}")

    # Setup experiment environment
    if hasattr(args, "random_seed"):
        init_random_seed(args.random_seed)
    else:
        raise ValueError("random_seed is not defined in arguments")

    # Setup logger
    init_print_logger(args, args.console_log_save_dir, args.console_log_file_name)

    manage_profiling_args(args)

    return args

def init_random_seed(seed):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True

def init_print_logger(args, log_dir, log_file_name):
    """
    Logger setting
    :return:
    """

    log_run_name = f"{args.project_name}_{args.dataset}_{args.baseline_name}_{args.federated_optimizer}"

    # update log_dir here
    new_log_dir = os.path.join(log_dir, log_run_name, PROJECT_START_DATETIME)

    new_log_file_name = f"{socket.gethostname()}_{args.dataset}_{args.baseline_name}_{args.federated_optimizer}_{args.partition_method}_{args.partition_alpha}_{log_file_name}"

    log_file_path = os.path.join(new_log_dir, new_log_file_name)

    logger.add(log_file_path, format="{time}|{level}|{message}", level=args.console_log_save_level, rotation=args.console_log_save_file_rotation)


def manage_profiling_args(args):

    if hasattr(args, "enable_wandb") and args.enable_wandb:
        wandb_only_server = getattr(args, "wandb_only_server", None)
        if (wandb_only_server and args.rank == 0 and args.process_id == 0) or not wandb_only_server:
            wandb_entity = getattr(args, "wandb_entity", None)
            if wandb_entity is not None:
                wandb_args = {
                    "entity": args.wandb_entity,
                    "project": args.wandb_project,
                    "config": args,
                }
            else:
                wandb_args = {
                    "project": args.wandb_project,
                    "config": args,
                }

            if hasattr(args, "run_name"):
                # wandb_args["name"] = args.run_name
                # Personalize the run name
                # wandb_args["name"] = str(args.baseline_name) + "_" + str(args.scenario) + "_" + str(
                #     socket.gethostname()) + "_" + str(
                #     args.dataset) + "_" + str(args.federated_optimizer) + "_" + str(args.partition_method) + ":" + str(
                #     args.partition_alpha) + "_init-cls:" + str(args.first_task_num_of_class) + "_cls-per-task:" + str(
                #     args.num_of_class_increment_per_task)

                wandb_args["name"] = str(args.baseline_name) + "_" + str(args.scenario) + "_" +str(socket.gethostname()) + "_" + str(
                    args.dataset) + "_" + str(args.federated_optimizer) + "_" + str(args.partition_method) + ":" + str(
                    args.partition_alpha)

                if hasattr(args, "fedprox_mu"):
                    wandb_args["name"] += "_mu:" + str(args.fedprox_mu)

            if hasattr(args, "wandb_group_id"):
                wandb_args["group"] = args.wandb_group_id
                # wandb_args["group"] = "Test1"
                wandb_args["name"] = f"Client {args.rank}"
                wandb_args["job_type"] = str(args.rank)

            if hasattr(args, "wandb_mode"):
                # online / offline
                # if str(args.wandb_mode) == "online":
                #     if hasattr(args, "wandb_key"):
                #         wandb.login(key=args.wandb_key)
                wandb_args["mode"] = str(args.wandb_mode)

            wandb.init(**wandb_args)


__all__ = [
    "data",
    "device",
    "PROJECT_START_DATETIME",
]