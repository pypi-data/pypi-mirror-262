# HoneyHive Python SDK

<div align="center">
   <img src="https://user-images.githubusercontent.com/6267663/220803812-cd7e27bd-06cb-49b0-87c1-d85fe21a3557.png" />
   <p>HoneyHive is a model observability and evaluation platform that helps you continuously improve your models in production. We help you evaluate, deploy, monitor and fine-tune both closed and open-source large language models for production use-cases, allowing you to optimize model performance & align your models with your users’ preferences.</p>
   <a href="https://docs.honeyhive.ai/introduction"><img src="https://img.shields.io/static/v1?label=Docs&message=API Ref&color=fc9434&style=for-the-badge" /></a>
</div> 


## SDK Installation

```bash
pip install honeyhive
```

## Authentication

After signing up on the app, you can find your API key in the [Settings page](https://app.honeyhive.ai/settings/account).

```python
import honeyhive
honeyhive.api_key = "HONEYHIVE_API_KEY"
honeyhive.openai_api_key = "OPENAI_API_KEY"
```

## Usage

Here we are assuming that you have a project setup in HoneyHive. If you don't, you can create one [here](https://app.honeyhive.ai/) by clicking on the `New Project` button.

### Generating a text completion via HoneyHive


#### Custom Prompt

Adding HoneyHive is as simple as changing `openai.Completions.create` to `honeyhive.Completions.create`. Just make sure to specify which project associated with the generation.

It's recommended to move the prompt to a template in our platform so that we can analyze user input distributions better.

```python
response = honeyhive.Completions.create(
  project="Sandbox - Email Writer",
  model="text-davinci-003",
  prompt="Write an email to a colleague named Jill congratulating her on her promotion. The tone should be warm yet professional. Mention how you admire the work she's been putting in.  Include a joke about how her pet lizard Max enjoys eating grasshoppers. Mention how you're looking forward to the team off-site next week.",
  temperature=0,
  max_tokens=256,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
)

generation_id = response.generation_id
```


#### Deployed Prompt

Assuming you have a prompt deployed for your project, you can generate it by calling `honeyhive.generations.generate(`

```python
response = honeyhive.generations.generate(
    task="PROJECT_NAME",
    input={
        "EXAMPLE1": "input",
        "EXAMPLE2": "input"
    }
)
```

#### Specific Prompt

If you want to generate a completion for a specific prompt, you can do so by calling `honeyhive.generations.generate(`

```python
response = honeyhive.generations.generate(
    task="PROJECT_NAME",
    input={
        "EXAMPLE1": "input",
        "EXAMPLE2": "input"
    },
    prompts=["PROMPT_NAME"]
)
```

### Evaluating a text completion via HoneyHive

For providing feedback on a generation, you can call `honeyhive.feedback(`

```python
response = honeyhive.feedback(
    task="PROJECT_NAME",
    generation_id=generation_id,
    feedback={
        "EXAMPLE1": "feedback",
        "EXAMPLE2": True,
    }
)
```


## SDK Capabilities

### Completions
`honeyhive.Completions.create` - calls OpenAI and logs the generation in HoneyHive

### Generations
`honeyhive.generations.generate` - generates a completion via HoneyHive
`honeyhive.generations.get_generations` - gets a pandas dataframe of all generations for a project

### Feedback
`honeyhive.feedback` - provides feedback on a generation

### Projects
`honeyhive.tasks.get_tasks` - gets a list of all projects
`honeyhive.tasks.get_task` - gets a specific project
`honeyhive.tasks.create_task` - creates a new project
`honeyhive.tasks.update_task` - updates a project
`honeyhive.tasks.delete_task` - deletes a project

### Prompts
`honeyhive.prompts.get_prompts` - gets a list of all prompts for a project
`honeyhive.prompts.create_prompt` - creates a new prompt for a project
`honeyhive.prompts.update_prompt` - updates a prompt for a project
`honeyhive.prompts.delete_prompt` - deletes a prompt for a project

### Metrics
`honeyhive.metrics.get_metrics` - gets a list of all metrics for a project
`honeyhive.metrics.create_metric` - creates a new metric for a project
`honeyhive.metrics.delete_metric` - deletes a metric for a project

### Datasets
`honeyhive.datasets.get_datasets` - gets a list of all datasets for a project
`honeyhive.datasets.get_dataset` - gets a specific dataset for a project
`honeyhive.datasets.create_dataset` - creates a new dataset for a project
`honeyhive.datasets.delete_dataset` - deletes a dataset for a project