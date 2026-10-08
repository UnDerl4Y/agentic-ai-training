---
lab:
    title: 'Develop a multi-agent solution with Microsoft Agent Framework'
    description: 'Learn to configure multiple agents to collaborate using the Microsoft Agent Framework SDK'
    level: 300
    duration: 30
    islab: true
    status: 'released'
---

# Develop a multi-agent solution with Microsoft Agent Framework

In this exercise, you'll practice using the sequential orchestration pattern in the Microsoft Agent Framework SDK. You'll create a simple pipeline of three agents that work together to process customer feedback and suggest next steps. You'll create the following agents:

- The Summarizer agent will condense raw feedback into a short, neutral sentence.
- The Classifier agent will categorize the feedback as Positive, Negative, or a Feature request.
- Finally, the Recommended Action agent will recommend an appropriate follow-up step.

You'll learn how to use the Microsoft Agent Framework SDK to break down a problem, route it through the right agents, and produce actionable results. Let's get started!

This exercise should take approximately **30** minutes to complete.

## Prerequisites

Before starting this exercise, ensure you have:

- [Visual Studio Code](https://code.visualstudio.com/) installed on your local machine
- An active [Azure subscription](https://azure.microsoft.com/free/)
- [Python 3.12](https://www.python.org/downloads/) installed
- [Git](https://git-scm.com/downloads) installed on your local machine

### Open the Microsoft Foundry Project

1. Open **Microsoft Edge** and go to [**https://ai.azure.com/**](https://ai.azure.com/).

2. Sign in using the credentials provided to you.

3. Open the **Microsoft Foundry project** provided by your instructor.

> [!IMPORTANT]
> Use the **deployed Microsoft Foundry project** provided for this training. You don't need to create a new project or model deployment.

## Get the project endpoint

Before working with the code, open the Microsoft Foundry project at https://ai.azure.com/.

1. On the project **Home** page, locate the **Project endpoint** section.

   > [!NOTE]
   > If you copied the project endpoint in an earlier lab and still have it available, you can skip to **step 2**.

   Select **Copy** next to the project endpoint URL and keep the value available. You'll use this endpoint to configure the application in this lab and in later labs as well.

   The project endpoint will be similar to:

   ```text
   https://<resource-name>.services.ai.azure.com/api/projects/<project-name>
   ```

2. On the same project **Home** page, scroll down to **Recent work** and select **Models**.

   Locate the deployed model provided for the training environment and note its **deployment name**. Keep the value available in a notepad. You'll use it when configuring the application.

## Open the training repository

The Python application and supporting files are available in the training repository.

> [!NOTE]
> If you downloaded and extracted the training repository in an earlier lab, you can skip to **step 4** and continue from there.

1. Open **Microsoft Edge** and go to:

   https://github.com/UnDerl4Y/agentic-ai-training

2. On the repository page, select the green **`<> Code`** button, then select **Download ZIP**.

3. When the download finishes, open your **Downloads** folder and extract the ZIP file.

4. Open **PowerShell**.

5. Copy the Lab 3 folder to your Desktop:

   ```powershell
   Copy-Item "C:\Users\agenticuser\Downloads\agentic-ai-training-main\agentic-ai-training-main\Labfiles\lab03-agent-framework-multi-agents" -Destination "$env:USERPROFILE\Desktop\" -Recurse
   ```

6. Open the copied Lab 3 folder in Visual Studio Code:

   ```powershell
   code "$env:USERPROFILE\Desktop\lab03-agent-framework-multi-agents"
   ```

> [!NOTE]
> The folder is copied to the Desktop to avoid issues with long file paths. The Lab 3 codebase is now open in Visual Studio Code.

## Understand the lab files

The `Python` folder contains the files needed to run the application.

```text
Python
├── .env
├── agents.py
└── requirements.txt
```

Here is what each file is used for:

* **`.env`** stores the Microsoft Foundry project endpoint and model deployment name.
* **`agents.py`** contains the code for the three agents and the sequential workflow.
* **`requirements.txt`** lists the Python packages required by the application.

## Understand the Python application

The `agents.py` file already contains the application code. You don't need to add or modify the code.

The application contains four main parts:

1. Agent instructions
2. Microsoft Foundry chat client
3. Three agents
4. Sequential orchestration

### Define the agent instructions

The application starts by defining instructions for each agent.

```python
# Define the instructions for each agent
summarizer_instructions = """
You summarize customer feedback into one short, neutral sentence.
Focus on the main point of the feedback.
Do not add information that is not included in the feedback.
"""

classifier_instructions = """
You classify customer feedback into one of these categories:
- Positive
- Negative
- Feature request

Return only the category name.
"""

action_instructions = """
You recommend an appropriate follow-up action based on the customer feedback.
Keep the recommendation short and practical.
"""
```

Each instruction defines the task for one agent.

The **summarizer** focuses on the main point of the feedback. The **classifier** assigns a category. The **action** agent recommends a follow-up step.

### Initialize the customer feedback

The application contains sample customer feedback that will be processed by the agents.

```python
# Initialize the customer feedback to process
feedback = """
I use the dashboard every day to monitor metrics, and it works well overall.
But when I'm working late at night, the bright screen is really harsh on my eyes.
If you added a dark mode option, it would make the experience much more comfortable.
"""
```

The feedback describes a customer request for a dark mode option.

### Create the chat client

The application creates a chat client that connects to the Microsoft Foundry project.

```python
# Create a chat client that connects to the Microsoft Foundry project
credential = AzureCliCredential()
chat_client = FoundryChatClient(
    credential=credential,
    project_endpoint=os.getenv("AZURE_AI_PROJECT_ENDPOINT"),
    model=os.getenv("AZURE_AI_MODEL_DEPLOYMENT_NAME"),
)
```

`AzureCliCredential()` uses the Azure account you signed in to with the Azure CLI.

`FoundryChatClient` uses the project endpoint and model deployment name from the `.env` file to connect to the Microsoft Foundry project.

### Create the agents

The application creates three agents using the chat client.

```python
# Create the agents that will process the customer feedback
summarizer_agent = chat_client.as_agent(
    name="summarizer",
    instructions=summarizer_instructions,
)

classifier_agent = chat_client.as_agent(
    name="classifier",
    instructions=classifier_instructions,
)

action_agent = chat_client.as_agent(
    name="action",
    instructions=action_instructions,
)
```

Each agent has a name and its own instructions.

The agents have different responsibilities:

* **summarizer** summarizes the customer feedback.
* **classifier** categorizes the feedback.
* **action** recommends a follow-up action.

### Build the sequential workflow

The three agents are connected using `SequentialBuilder`.

```python
# Build a workflow that runs the agents in sequence
workflow = SequentialBuilder(
    participants=[summarizer_agent, classifier_agent, action_agent],
    output_from="all",
).build()
```

The `participants` list defines the order in which the agents are used:

```text
summarizer → classifier → action
```

The `output_from="all"` setting makes the output from all three agents available after the workflow runs.

### Run the workflow

The application sends the customer feedback to the workflow.

```python
# Run the workflow and collect the output from each agent
result = await workflow.run(f"Customer feedback: {feedback}")
outputs = result.get_outputs()
```

The `workflow.run()` method starts the sequential workflow with the customer feedback.

The `get_outputs()` method retrieves the outputs from the workflow.

### Display the agent outputs

The application displays the responses from the agents in the terminal.

```python
# Display the output from each agent
i = 1
for response in outputs:
    for msg in cast(list[Message], response.messages):
        name = msg.author_name or (
            "assistant" if msg.role == "assistant" else "user"
        )
        print(f"{'-' * 60}\n{i:02d} [{name}]\n{msg.text}")
        i += 1
```

The code loops through the workflow outputs and displays each message with the corresponding agent name.

This makes it possible to review the contribution from each agent.

## Configure the environment

The application reads the Microsoft Foundry project details from the `.env` file.

1. In Visual Studio Code, open the **`Python`** folder.

2. Open the **`.env`** file.

3. Replace `your_project_endpoint_here` with the project endpoint you copied from Microsoft Foundry.

4. Replace `your_model_deployment_name_here` with the model deployment name provided for your training environment.

   The file will look similar to:

   ```text
   # Environment configuration
   # Replace the values below with your Microsoft Foundry project details.


   # Microsoft Foundry project endpoint
   # Copy this from the project overview page in the Microsoft Foundry portal.
   # Your project endpoint will be similar to:
   # https://<resource-name>.services.ai.azure.com/api/projects/<project-name>
   AZURE_AI_PROJECT_ENDPOINT=your_project_endpoint_here


   # Model deployment name
   # Enter the name of the model deployment provided for your training environment.
   AZURE_AI_MODEL_DEPLOYMENT_NAME=your_model_deployment_name_here
   ```

5. Save the `.env` file.

## Create a Python environment

1. In Visual Studio Code, select **Terminal > New Terminal**.

2. Navigate to the **Python** folder:

   ```powershell
   cd Python
   ```

3. Create a Python virtual environment:

   ```powershell
   python -m venv labenv
   ```

4. Activate the virtual environment:

   ```powershell
   .\labenv\Scripts\Activate.ps1
   ```

5. Install the required packages:

   ```powershell
   pip install -r requirements.txt
   ```

> [!NOTE]
> The package installation may take **3 to 4 minutes** to complete. The terminal may appear to be stuck for a while, but the installation is still running and downloading the required packages. Please wait for the command to finish before continuing.

## Sign in to Azure

The application uses your Azure CLI credentials to authenticate with Microsoft Foundry.

1. In the integrated terminal, run:

   ```powershell
   az login
   ```

> [!TIP]
> If you have trouble signing in with Azure CLI, see [**Azure CLI sign-in troubleshooting**](https://github.com/UnDerl4Y/agentic-ai-training/blob/main/Instructions/Troubleshooting/az-loign.md).

2. Sign in using the credentials provided for the training environment.

3. Verify your active Azure account:

   ```powershell
   az account show
   ```

> [!TIP]
> If you have access to multiple Azure subscriptions, make sure the subscription containing your Microsoft Foundry project is selected.

## Test the application

Now you can run the application and review how the agents process the customer feedback.

1. In the same terminal (in the **Python** folder, with the virtual environment active), run the application:

   ```powershell
   python agents.py
   ```

2. Review the output in the terminal.

   Your output will be similar to:

   ```output
   ------------------------------------------------------------
   01 [summarizer]
   User requests a dark mode option for more comfortable nighttime use.
   ------------------------------------------------------------
   02 [classifier]
   Feature request
   ------------------------------------------------------------
   03 [action]
   Consider adding a dark mode option to improve comfort during nighttime use.
   ```

3. Review the output from each agent.

   The **summarizer** provides a short summary, the **classifier** identifies the feedback category, and the **action** agent recommends a follow-up step.

> [!NOTE]
> AI-generated responses may differ slightly between agents and runs. Your responses will be similar to those shown in this lab, but the wording and level of detail may vary.

## Try different feedback

You can test the orchestration with different customer feedback.

1. In **`agents.py`**, replace the current `feedback` value with:

   ```text
   I reached out to your customer support yesterday because I couldn't access my account. The representative responded almost immediately, was polite and professional, and fixed the issue within minutes. Honestly, it was one of the best support experiences I've ever had.
   ```

2. Save the file.

3. Run the application again in the same terminal:

   ```powershell
   python agents.py
   ```

4. Review how each agent processes the new feedback.

   The agents will summarize the feedback, classify it, and suggest an appropriate action.

> [!NOTE]
> AI-generated responses may differ slightly between agents and runs. The wording and level of detail may vary.

## Summary

In this exercise, you created a multi-agent solution that processes customer feedback using sequential orchestration.

You learned how to:

* Connect a Python application to a Microsoft Foundry project.
* Configure multiple agents with different instructions.
* Use `SequentialBuilder` to run agents in sequence.
* Collect and display the output from each agent.
* Test the orchestration with different customer feedback.