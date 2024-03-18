# Flover: Flexibly Orchestrating RAG Processes for Large Language Models

Flover comes from "Flow" and "Vertex".

Flover is a powerful framework designed to streamline and orchestrate various stages of the Retrieval-Augmented Generation (RAG) process for large language models. It enables developers to efficiently preset and manage tasks such as preprocessing, searching, retrieval, ranking, web scraping, and interfacing with large models, among other functionalities. Built on the foundation of Directed Acyclic Graphs (DAGs), Flover offers a flexible and efficient way to deploy and manage your own RAG services.

Key Features
DAG-based Workflow: Flover leverages Directed Acyclic Graphs to represent and manage the complex dependencies and relationships between different tasks in the RAG process.

Modular Design: The framework is designed with a modular architecture, allowing developers to easily plug in and configure various components for different stages of the RAG process.

Predefined Tasks: Flover comes with predefined tasks for common RAG stages such as preprocessing, search, retrieval, ranking, web page downloading, and interacting with large language models.

Flexibility and Customization: Developers can easily customize and extend Flover to suit their specific requirements and integrate it into their existing workflows.

Efficient Execution: Flover provides efficient task scheduling and execution mechanisms, optimizing the performance of RAG processes.

Getting Started
To get started with Flover, follow these steps:

Install Flover by running 
```bash
pip install flover(comming soon)
```

Define your RAG workflow using the Flover API, specifying the tasks and their dependencies.

Configure the parameters for each task and customize the workflow according to your needs.

Execute the workflow and monitor the progress using the provided tools and interfaces.

Example Usage
Here's a simple example demonstrating how you can define a basic RAG workflow using Flover:

from flover import Flover

# Initialize Flover instance
```python
flover = Flover()
```
# Define tasks for preprocessing, searching, retrieval, etc.
```python
preprocessing_task = flover.add_task("Preprocessing")
search_task = flover.add_task("Search")
retrieval_task = flover.add_task("Retrieval")
```
# Define dependencies between tasks
```python
flover.add_edge(preprocessing_task, search_task)
flover.add_edge(search_task, retrieval_task)
```
# Execute the workflow
```python
flover.execute_workflow()
```
Contributing
We welcome contributions to Flover! If you have ideas for new features, improvements, or bug fixes, please feel free to submit a pull request or open an issue on our GitHub repository.

License
Flover is licensed under the MIT License. See the LICENSE file for more details.

By leveraging the capabilities of Flover, developers can efficiently organize and deploy RAG processes for large language models, enabling them to focus on building innovative applications and services.
