from honeyhive.api.models.evaluations import EvaluationLoggingQuery
import honeyhive
from typing import Dict, List, Any

import pandas as pd
import random
import json


class HoneyHiveEvaluation:
    def __init__(self, project: str, name: str, dataset_name: str = "", description: str = "", metrics_to_compute: List[str] = [], metrics = []):

        ## metrics is overloaded if deprecated, use metrics_to_compute instead
        if metrics != []:
            metrics_to_compute = metrics
            
        self.project = project
        self.name = name
        self.dataset_name = dataset_name
        self.description = description
        self.metrics_to_compute = metrics_to_compute
        self.metrics = metrics_to_compute
        self.configs = []
        self.inputs = []
        self.run = []
        self.completions = []
        self.logged_metrics = []
        self.summary = []
        self.accepted = []
        self.comments = []
        self.is_logged = []
    
    def log_run(
        self,
        config: Dict[str, Any],
        input: Dict[str, Any],
        completion: str,
        metrics: Dict[str, Any],
        accepted: bool = None):
        # check if config is already in self.configs
        # if it is, get the index of it
        # if it isn't, add it to self.configs and get the index of it
        if config not in self.configs:
            self.configs.append(config)
        config_index = self.configs.index(config)

        if len(self.configs) <= 1:
            self.inputs.append(input)
        else:
            # check how many tuples have input as the input
            is_logged = 0
            for log in self.is_logged:
                if json.dumps(input) == log[1]:
                    is_logged += 1
            modulo = is_logged % len(self.configs)
            #print("is_logged", is_logged)
            #print("modulo", modulo)
            if input not in self.inputs or modulo == 0:
                self.inputs.append(input)
        res_list = [i for i, value in enumerate(self.inputs) if value == input]
        input_index = res_list[-1]

        self.is_logged.append((json.dumps(config), json.dumps(input)))
        # add completion to self.completions at config_index, input_index
        if len(self.completions) <= config_index:
            self.completions.append([])
        if len(self.completions[config_index]) <= input_index:
            self.completions[config_index].append([])
        self.completions[config_index][input_index] = completion

        # add metrics to self.logged_metrics at input_index, config_index
        if len(self.logged_metrics) <= input_index:
            self.logged_metrics.append([])
        self.logged_metrics[input_index].append(metrics)

        # add accepted to self.accepted at config_index, input_index
        if len(self.accepted) <= config_index:
            self.accepted.append([])
        if len(self.accepted[config_index]) <= input_index:
            self.accepted[config_index].append([None])
        self.accepted[config_index][input_index] = accepted


    def log_comment(self, comment: str):
        self.comments.append({"text": comment})
    
    def finish(self):
        for config in self.configs:
            if "name" not in config:
                # generate random 5 character string
                config["name"] = ''.join(
                    random.choice('0123456789ABCDEF') for i in range(5)
                )
                config["version"] = config["name"]
                config["task"] = self.project
        
        summary = []

        # get the keys of metrics[0][0]
        # for each key, get the average of that key
        # add that to summary
        keys = list(self.logged_metrics[0][0].keys())
        #print(self.logged_metrics)
        keys.append("Positive Feedback (%)")
        for key in keys:
            summary_entry = {"metric": key}

            for config in self.configs:
                summary_entry[config["name"]] = 0

            # for each input, get the average of that key
            # add that to summary
            if key != "Positive Feedback (%)" and key != "session_id" and key != "generation_id":
                for input_index in range(len(self.logged_metrics)):
                    for config_index in range(len(self.logged_metrics[input_index])):
                        if not isinstance(self.logged_metrics[input_index][config_index][key], str):
                            summary_entry[self.configs[config_index]["name"]] += self.logged_metrics[input_index][config_index][key]

            # for each input, get the average of that key
            for config in self.configs:
                summary_entry[config["name"]] /= len(self.logged_metrics)

            summary.append(summary_entry)
        
        self.summary = summary

        results = []

        i = 0
        j = 0

        # for each input, get the average of that key
        # add that to summary
        for i in range(len(self.inputs)):
            single_result = {}
            j = 0
            for config in self.configs:
                #print("i", i, "j", j)
                single_result[config["name"]] = self.completions[j][i]
                self.logged_metrics[i][j]["prompt"] = config["name"]
                j += 1
            results.append(single_result)
        
        from honeyhive.sdk.init import honeyhive_client
        client = honeyhive_client()

        evaluation = EvaluationLoggingQuery(
                name=self.name,
                task=self.project,
                prompts=self.configs,
                dataset=self.inputs,
                datasetName=self.dataset_name,
                generations=self.completions,
                metrics=self.logged_metrics,
                summary=summary,
                comments=self.comments,
                accepted=self.accepted,
                description=self.description,
                results=results,
                metrics_to_compute=[]
            )
        

        response = client.log_evaluation(evaluation=evaluation)

        url = "https://app.honeyhive.ai/evaluate?id="
        print("Evaluation logged successfully")
        print("View evaluation at", url + response.id)


def init(
    project: str,
    name: str = None,
    dataset_name: str = None,
    description: str = None,
    metrics: List[str] = None,
):
    """Initialize an evaluation"""
    import uuid

    # TODO check if project exists
    try:
        is_valid = honeyhive.projects.get(project)
        #print(is_valid)
    except:
        raise Exception("Project does not exist")
    
    return {
        "uuid": str(uuid.uuid4()),
        "project": project,
        "name": name,
        "dataset_name": dataset_name if dataset_name is not None else "",
        "description": description if description is not None else "",
        "metrics": metrics if metrics is not None else [],
    }


def log(
    evaluation: Dict[str, Any],
    configs: List[Dict[str, Any]],
    inputs: List[Dict[str, Any]],
    run: List[List[Dict[str, Any]]],
    completions: List[List[str]] = None,
    metrics: List[List[Dict[str, Any]]] = None,
    accepted: List[List[bool]] = None,
    comments: List[str] = None,
):
    """Log an evaluation"""
    from honeyhive.sdk.init import honeyhive_client
    import random

    client = honeyhive_client()

    import copy

    run = copy.deepcopy(run)

    new_comments = []

    for comment in comments:
        new_comments.append({"text": comment})

    comments = new_comments

    if run:
        # completions is the whole list of list of completions
        # metrics is the whole list of list of metrics except "completion"
        completions = []
        metrics = []
        for i in range(len(run)):
            completion_run = []
            metric_calculation = []
            for j in range(len(run[i])):
                rest_run = run[i][j]
                completion_run.append(rest_run["completion"])
                del rest_run["completion"]
                rest_run["Cost ($)"] = rest_run["cost"]
                del rest_run["cost"]
                rest_run["Latency (ms)"] = rest_run["latency"]
                del rest_run["latency"]
                rest_run["Response Length (tokens)"] = rest_run[
                    "response_length"
                ]
                del rest_run["response_length"]
                metric_calculation.append(rest_run)
            completions.append(completion_run)
            metrics.append(metric_calculation)
    # check if configs have names
    # if they don't, give them random 5 character string
    for config in configs:
        if "name" not in config:
            # generate random 5 character string
            config["name"] = ''.join(
                random.choice('0123456789ABCDEF') for i in range(5)
            )
            config["version"] = config["name"]
            config["task"] = evaluation['project']

    results = []
    summary = []

    # get the keys of metrics[0][0]
    # for each key, get the average of that key
    # add that to summary
    keys = metrics[0][0].keys()
    for key in keys:
        summary_entry = {"metric": key}

        for config in configs:
            summary_entry[config["name"]] = 0

        for i in range(len(metrics)):
            for j in range(len(metrics[i])):
                summary_entry[configs[j]["name"]] += metrics[i][j][key]

        for config in configs:
            summary_entry[config["name"]] /= len(metrics)

        summary.append(summary_entry)

    i = 0
    j = 0
    for input in inputs:
        single_result = {}
        j = 0
        for config in configs:
            single_result[config["name"]] = completions[i][j]
            metrics[i][j]["prompt"] = config["name"]
            j += 1
        i += 1
        results.append(single_result)

    evaluation=EvaluationLoggingQuery(
        name=evaluation['name'],
        task=evaluation['project'],
        prompts=configs,
        dataset=inputs,
        datasetName=evaluation['dataset_name']
        if evaluation['dataset_name'] is not None
        else "",
        generations=completions,
        metrics=metrics,
        summary=summary,
        comments=comments,
        accepted=accepted,
        description=evaluation['description']
        if evaluation['description'] is not None
        else "",
        results=results,
        metrics_to_compute=evaluation['metrics'],
        )


    response = client.log_evaluation(eval
    )
    url = "https://app.honeyhive.ai/evaluate?id="
    print("Evaluation logged successfully")
    print("View evaluation at", url + response.id)

    return response


def log_from_df(
    project: str,
    df: pd.DataFrame,
    name: str = None,
    dataset_name: str = None,
    description: str = None,
    accepted: List[List[bool]] = None,
    comments: List[Dict[str, Any]] = None,
):
    """Log an evaluation from a dataframe"""
    from honeyhive.sdk.init import honeyhive_client

    client = honeyhive_client()
    return client.log_evaluation(
        evaluation=EvaluationLoggingQuery(
            name=name,
            task=project,
            prompts=df["configs"].tolist(),
            dataset=df["inputs"].tolist(),
            dataset_name=dataset_name,
            generations=df["completions"].tolist(),
            metrics=df["metrics"].tolist(),
            comments=comments,
            description=description,
            results=accepted,
        )
    )


__all__ = [
    "init",
    "log",
    "log_from_df",
    "HoneyHiveEvaluation"
]
