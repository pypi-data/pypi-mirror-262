'''
    Ref: https://github.com/FedML-AI/FedML/blob/03a0268c9458bec9f9ede3fb126ff79ebc25a953/python/fedml/ml/aggregator/agg_operator.py#L8
'''

from collections import OrderedDict
from typing import List, Tuple

from fedllm.utils.logger import logger
from fedllm.utils.constants import (
    FEDLLM_FEDERATED_OPTIMIZER_FEDAVG,
    FEDLLM_FEDERATED_OPTIMIZER_FEDPROX,
    FEDLLM_FEDERATED_OPTIMIZER_SCAFFOLD
)

class CFBenchAggOperator:
    @staticmethod
    def agg(args, raw_grad_list: List[Tuple[float, OrderedDict]]) -> OrderedDict:
        training_num = 0
        if args.federated_optimizer == FEDLLM_FEDERATED_OPTIMIZER_FEDAVG:
            for i in range(len(raw_grad_list)):
                local_sample_num, _, _ = raw_grad_list[i]
                training_num += local_sample_num
        else:
            for i in range(len(raw_grad_list)):
                local_sample_num, local_model_params = raw_grad_list[i]
                training_num += local_sample_num

        avg_params = model_aggregator(args, raw_grad_list, training_num)
        return avg_params


def torch_aggregator(args, raw_grad_list, training_num):

    if args.federated_optimizer == FEDLLM_FEDERATED_OPTIMIZER_FEDAVG:
        (num0, avg_params) = raw_grad_list[0]
        for k in avg_params.keys():
            for i in range(0, len(raw_grad_list)):
                local_sample_number, local_model_params = raw_grad_list[i]
                w = local_sample_number / training_num
                if i == 0:
                    avg_params[k] = local_model_params[k] * w
                else:
                    avg_params[k] += local_model_params[k] * w
    elif args.federated_optimizer == FEDLLM_FEDERATED_OPTIMIZER_FEDPROX:
        (num0, avg_params) = raw_grad_list[0]
        for k in avg_params.keys():
            for i in range(0, len(raw_grad_list)):
                local_sample_number, local_model_params = raw_grad_list[i]
                w = local_sample_number / training_num
                if i == 0:
                    avg_params[k] = local_model_params[k] * w
                else:
                    avg_params[k] += local_model_params[k] * w

    elif args.federated_optimizer == FEDLLM_FEDERATED_OPTIMIZER_SCAFFOLD:
        (num0, total_weights_delta, total_c_delta_para) = raw_grad_list[0]
        # avg_params = total_weights_delta
        for k in total_weights_delta.keys():
            for i in range(0, len(raw_grad_list)):
                local_sample_number, weights_delta, c_delta_para = raw_grad_list[i]
                w = local_sample_number / training_num
                # w = local_sample_number / len(raw_grad_list)
                if i == 0:
                    total_weights_delta[k] = weights_delta[k] * w
                    total_c_delta_para[k] = c_delta_para[k]
                else:
                    total_weights_delta[k] += weights_delta[k] * w
                    total_c_delta_para[k] += c_delta_para[k]
            w_c = 1 / args.client_num_in_total
            total_weights_delta[k] = weights_delta[k]
            total_c_delta_para[k] = c_delta_para[k] * w_c
        avg_params = (total_weights_delta, total_c_delta_para)

    return avg_params

def model_aggregator(args, raw_grad_list, training_num):
    return torch_aggregator(args, raw_grad_list, training_num)

