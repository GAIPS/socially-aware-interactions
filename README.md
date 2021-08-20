# Socially Aware Interactions: From dialogue trees to natural language dialogue systems

Tree-based dialogue training tools, such as the [Dialogue Trainer Software](https://www.dialoguetrainer.com/en), generally include easy-to-use authoring interfaces. Nevertheless, the following disadvantages are still present:
- Dialogue is not self-made: players are unable to learn relevant communication skills
- Dialogue is predetermined: agent does not need to adapt to changes in the context
- Dialogue tree is very large: editor may have trouble managing the dialogue

On the other hand, natural language dialogue systems are flexible, allow users to write their own input, and are also able to manage errors in the conversation. However, in these systems, authoring interfaces are usually not available to create and edit scenarios, or they are simply made for a specific scenario, being difficult to generalize to other contexts.

Therefore, our main goal was to find a middle-ground between these two types of systems, focusing on the flexibility, robustness and authoring requirements of the dialogue. The agent should then adapt to the context of the dialogue by employing a simple and general deliberation mechanism, and dialogue scenarios should be simple to create and configure in an authoring tool. In order to fulfil these requirements, we created a prototype of a dialogue system based on the [Cognitive Social Frames](https://arxiv.org/pdf/2001.07142.pdf) model and the theory of social practices. The dialogue system's interface and deliberation mechanism were implemented in [Python](https://www.python.org/) and the dialogue scenarios were authored in [Twine](https://twinery.org/).

# Agent Architecture
<img src="https://user-images.githubusercontent.com/25940883/130188525-8f263aca-5a52-418d-afa6-a71257183658.png" alt="architecture" width=600>

# Application Snapshot
<img src="https://user-images.githubusercontent.com/25940883/130191553-ab11beef-9088-4900-a1d1-9ce90c9d1f95.png" alt="app snapshot" width=600>

# Getting Started
1. Download or clone this repository 
2. Download and install [Twine](https://twinery.org/)
3. Open Twine and add the [Twison](https://lazerwalker.com/twison/format.js) add-on by adding a new format and pointing to its url 
4. Create a new story (scenario), or import to Twine the file "AnamnesisScenario.html", which is in the folder "scenarios/Twine" of the repository, editing it if you want to
5. Play the story and a webpage will open with the story in a JSON format
6. Copy all the text from that webpage
7. Open the "scenarios/JSON" folder, which already contains 2 examples of JSON files
8. Create a new JSON text file in the folder and paste the JSON text you copied earlier to that file
9. Run the "dialogueSystem.exe" file of the "exe" folder, select the JSON file of your preference and click on the start button

## Scenario Configuration in Twine

<details><summary><b>Roles</b></summary>
  
  Create passage with tag "roles" – the user role is defined inside {{user}} {{/user}}, and the same logic applies for the agent role ({{agent}} {{/agent}}).
  
  <img src="https://user-images.githubusercontent.com/25940883/130190666-7e169c4d-4678-4f23-baa3-e6e734c0baf2.png" label="roles">

</details>

<details><summary><b>Frames</b></summary>
  
  Create passage with tag "frame" and add any other context and knowledge tags you want. Connect it to another frame by writing their name between double square brackets ([[Introduction]]).
  
  <img src="https://user-images.githubusercontent.com/25940883/130190601-9572e317-a8c4-4113-94a8-063d1b186242.png" alt="frame specific">
  
  This is an overview of the connected frames in Twine.
  
  <img src="https://user-images.githubusercontent.com/25940883/130190698-8346a75a-c490-430e-805b-2ff87a0fc0b0.png" alt="frame general" width=600>    

</details>

<details><summary><b>Resources</b></summary>
  
  Create passage with a title that corresponds to the resource’s utterance. Add tags that match the tags of existing frames, since resources are connected to the frames. Add the role of the resource as a tag if it is necessary (according to the roles defined in the roles passage). Connect the resource to another, if you want, by using double square brackets. Add knowledge if it is the case - the "add to knowledge base" property is defined inside {{addKnowledge}} {{/addKnowledge}}.
  
  This is an example of a resource passage without any role defined and not connected to any other resource passage.
  
  <img src="https://user-images.githubusercontent.com/25940883/130190367-882e6b12-dc5b-4154-8024-edfa5b7ab418.png" alt="resource specific">
  
  This is an example of a resource passage with a defined role (patient), connected to one other resource passage and that updates knowledge base.
  
  <img src="https://user-images.githubusercontent.com/25940883/130190475-6cf3dbf5-4545-46bf-8c97-d43c9c1d2030.png" alt="resource specific knowledge base"> 
  
  This is an overview of the dialogue trees with one or more utterances in Twine.

  <img src="https://user-images.githubusercontent.com/25940883/130190130-0765cc31-23ba-45eb-b2a9-25e0537f8173.png" label="resources general" width=400>    
  
</details>

<details><summary><b>Timeout</b></summary>
  
  If you'd like the agent to detect that the user has not responded for a defined amount of time, create a passage with the tags "frame" and "timeout". The time, in seconds, of the timeout can be specified, within the frame, inside {{timer}} {{/timer}}. This frame is not linked to any other frame and its resources are defined just like the resources associated with the other frames.
  
  <img src="https://user-images.githubusercontent.com/25940883/130190638-17fe50b1-8c53-4d68-aac3-0a301587b6ad.png" alt="timeout frame">
  
</details>

# Future Work
In the future, we hope to be able to improve this prototype, fulfiling the following points:
- Manage more errors in the dialogue, besides the timeout error
- Allow the system to create dialogues with no speaking turns specified
- Map the user inputs to appropriate context tags, and extract relevant knowledge from them
- Attempt to create dialogue scenarios with crowdsourced data
