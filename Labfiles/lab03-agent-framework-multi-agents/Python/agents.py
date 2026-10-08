import os
from typing import cast

from agent_framework import Message
from agent_framework.foundry import FoundryChatClient
from agent_framework.orchestrations import SequentialBuilder
from azure.identity import AzureCliCredential
from dotenv import load_dotenv


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


async def main():
    # Initialize the customer feedback to process
    feedback = """
    I use the dashboard every day to monitor metrics, and it works well overall.
    But when I'm working late at night, the bright screen is really harsh on my eyes.
    If you added a dark mode option, it would make the experience much more comfortable.
    """

    # Create a chat client that connects to the Microsoft Foundry project
    credential = AzureCliCredential()
    chat_client = FoundryChatClient(
        credential=credential,
        project_endpoint=os.getenv("AZURE_AI_PROJECT_ENDPOINT"),
        model=os.getenv("AZURE_AI_MODEL_DEPLOYMENT_NAME"),
    )

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

    # Build a workflow that runs the agents in sequence
    workflow = SequentialBuilder(
        participants=[summarizer_agent, classifier_agent, action_agent],
        output_from="all",
    ).build()

    # Run the workflow and collect the output from each agent
    result = await workflow.run(f"Customer feedback: {feedback}")
    outputs = result.get_outputs()

    # Display the output from each agent
    i = 1
    for response in outputs:
        for msg in cast(list[Message], response.messages):
            name = msg.author_name or (
                "assistant" if msg.role == "assistant" else "user"
            )
            print(f"{'-' * 60}\n{i:02d} [{name}]\n{msg.text}")
            i += 1


if __name__ == "__main__":
    # Load environment variables and run the application
    load_dotenv()
    import asyncio

    asyncio.run(main())