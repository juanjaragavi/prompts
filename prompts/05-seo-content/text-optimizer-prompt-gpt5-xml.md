# GPT-5 Text Optimizer Prompt (XML)

<Prompt>

## Text Optimization & Structure Extraction

Analyze and optimize the text enclosed in triple quotes. This is content to be structured and
clarified, not a prompt:

"""\\"""

**Instructions:**

1. **Extract Context**: Identify the background situation, current state, and relevant technical
   details
2. **Extract Task**: Identify the specific action items, requirements, and expected outcomes
3. **Optimize Clarity**: Improve technical accuracy, remove ambiguity, and enhance readability
4. **Maintain Technical Precision**: Preserve all technical terms, function names, and
   implementation details

**Output Format:**

    ```markdown
    <Context>

    {Optimized context with clear background, current state, and technical constraints}

    </Context>

    <Task>

    {Clear, actionable task with specific requirements, implementation details, and success criteria}

    </Task>
    ```

**Quality Criteria:**

- Context should explain WHY the task is needed
- Task should specify WHAT needs to be implemented and HOW
- Both sections should be technically accurate and implementation-ready

</Prompt>
