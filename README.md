# ContraBias
⚖️ System prompt plugin for LLMs that mitigates occupational gender bias in English-to-Spanish translation via Counterfactual Prompting.
# ContraBias / NeutrAI: System Prompt Plugin for Gender Bias Mitigation ⚖️

This repository contains a lightweight, system-level prompting plugin designed to mitigate occupational gender bias in LLM-assisted coding and text-generation interfaces (such as **Cursor**, **Cline**, **Claude Desktop**, and **GitHub Copilot**).

## 💡 How It Works
The plugin implements a logical rule system called **Counterfactual Prompting**. Before generating or translating any text involving human subjects, the LLM mentally performs a counterfactual simulation: *"If I change the subject's gender, does the target sentence change?"*.

If the source text does not specify a gender (which is common in English occupations, e.g., "the doctor") but the target language requires grammatical gender marking (such as Spanish), the model detects ambiguity and executes one of two handling actions:
1.  **Neutral Restructuring:** Restructures the output using gender-neutral grammar (e.g., using *"El personal médico"* instead of guessing between *"El médico"* or *"La médica"*).
2.  **Explicit Split Annotation:** Outputs three labeled options for the user: `[Female Version]`, `[Male Version]`, and `[Neutral Version]`.

---

## 🚀 Setup & Installation

### For Cursor IDE 💻
1. Copy the contents of the `.cursorrules` file from this repository.
2. Create a file named `.cursorrules` in the root directory of your project and paste the content.
3. The Cursor AI assistant will automatically apply these rules to all generation, translation, and code-commenting chats.

### For Cline / VS Code Extensions 🧩
1. Copy the contents of the `.clinerules` file from this repository.
2. Create a file named `.clinerules` in the root directory of your workspace and paste the content.

### For Claude Desktop / ChatGPT / API Integrations 🌐
Copy the text inside `system_prompt.txt` and paste it directly into the custom system instructions field of your AI assistant or the `system` role of the LLM completions API.

---

## ⚡ Active Commands
You can trigger specific actions inside your chat window using these commands:
*   `@audit-gender` : Scans the provided text, applies the counterfactual test to human subjects, flags implicit biases, and suggests neutral corrections.
*   `@force-neutral` : Forces the assistant to use only the most natural gender-neutral restructuring, skipping the explicit male/female options.
