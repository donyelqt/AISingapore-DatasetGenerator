import json
import random
from faker import Faker

fake = Faker()

# Define categories and subcategories for diverse data generation
CATEGORIES = {
    "Responsible AI": [
        "Ethical Principles", "Bias Mitigation", "Transparency", "Accountability", 
        "Privacy Protection", "Human-Centered Design", "Governance Frameworks", 
        "Inclusivity", "Risk Management", "Stakeholder Engagement"
    ],
    "Agentic AI": [
        "Autonomy", "Reward Functions", "Goal-Directed Behavior", "Ethical Challenges", 
        "Emergent Behavior", "Multi-Agent Systems", "Uncertainty Handling", 
        "Bounded Rationality", "Learning Mechanisms", "Decision-Making Frameworks", 
        "Social Awareness", "Memory Systems", "Scalable Autonomy"
    ],
    "Prompt Engineering": [
        "Few-Shot Prompting", "Temperature Setting", "Chain-of-Thought", 
        "Effective Prompts", "Zero-Shot Prompting", "Role Prompting", 
        "Context Length", "Prompt Templates", "Prompt Testing", 
        "Explicit vs Implicit Prompting", "Prompt Chaining", "Common Pitfalls"
    ],
    "Foundational Models": [
        "Transfer Learning", "Self-Supervision", "Data Efficiency", 
        "Architectural Components", "Emergent Abilities", "Deployment Challenges", 
        "Multi-Modal Inputs", "Ethical Considerations", "Zero-Shot and Few-Shot Learning", 
        "Scaling Effects", "Contextual Understanding", "Open vs Closed Models"
    ]
}

# Define trap question templates
TRAP_QUESTIONS = {
    "Misleading Context": [
        "Why is {incorrect_concept} considered the best approach for {topic}?",
        "Explain how {incorrect_concept} solves {problem} in {context}."
    ],
    "Outdated Information": [
        "Why is {outdated_concept} still widely used in {field}?",
        "How does {outdated_concept} outperform modern approaches in {context}?"
    ],
    "Confusable Concepts": [
        "Compare {confusable_concept_1} and {confusable_concept_2} for {task}.",
        "Why is {confusable_concept_1} better than {confusable_concept_2} for {context}?"
    ]
}

# Define incorrect, outdated, and confusable concepts
INCORRECT_CONCEPTS = {
    "Responsible AI": ["unrestricted autonomy", "opaque decision-making", "data exploitation"],
    "Agentic AI": ["unbounded rationality", "unsupervised goal-setting", "non-adaptive behavior"],
    "Prompt Engineering": ["overly verbose prompts", "unstructured inputs", "fixed temperature settings"],
    "Foundational Models": ["task-specific training", "small-scale architectures", "non-transferable knowledge"]
}

OUTDATED_CONCEPTS = {
    "Responsible AI": ["rule-based ethics", "static governance frameworks"],
    "Agentic AI": ["deterministic algorithms", "isolated agent systems"],
    "Prompt Engineering": ["manual prompt crafting", "single-shot prompting"],
    "Foundational Models": ["shallow neural networks", "non-scalable architectures"]
}

CONFUSABLE_CONCEPTS = {
    "Responsible AI": ["transparency vs explainability", "fairness vs equality"],
    "Agentic AI": ["autonomy vs automation", "reward functions vs utility functions"],
    "Prompt Engineering": ["few-shot vs zero-shot prompting", "temperature vs top-p sampling"],
    "Foundational Models": ["transfer learning vs fine-tuning", "self-supervision vs semi-supervision"]
}

# Function to generate high-quality questions
def generate_question(category, subcategory):
    topic = random.choice(CATEGORIES[category])
    context = f"in the context of {subcategory}" if random.random() < 0.7 else ""
    instruction = f"Explain the concept of {topic} {context}."
    response = f"{topic} refers to [detailed explanation]. It is important because [reason]. For example, [specific example]."
    return {
        "instruction": instruction,
        "context": context,
        "response": response
    }

# Function to generate trap questions
def generate_trap_question(category):
    trap_type = random.choice(list(TRAP_QUESTIONS.keys()))
    if trap_type == "Misleading Context":
        incorrect_concept = random.choice(INCORRECT_CONCEPTS[category])
        topic = random.choice(CATEGORIES[category])
        problem = fake.sentence()  # Generate a fake problem statement
        context = fake.sentence()  # Generate a fake context
        question = random.choice(TRAP_QUESTIONS[trap_type]).format(
            incorrect_concept=incorrect_concept,
            topic=topic,
            problem=problem,
            context=context
        )
        response = f"This is incorrect because [reason]. The correct approach is [correct_concept]."
    elif trap_type == "Outdated Information":
        outdated_concept = random.choice(OUTDATED_CONCEPTS[category])
        field = category
        context = fake.sentence()  # Generate a fake context
        question = random.choice(TRAP_QUESTIONS[trap_type]).format(
            outdated_concept=outdated_concept,
            field=field,
            context=context
        )
        response = f"This is outdated because [reason]. Modern approaches include [modern_concept]."
    else:
        confusable_pair = random.choice(CONFUSABLE_CONCEPTS[category])
        confusable_concept_1, confusable_concept_2 = confusable_pair.split(" vs ")
        task = random.choice(CATEGORIES[category])
        context = fake.sentence()  # Generate a fake context
        question = random.choice(TRAP_QUESTIONS[trap_type]).format(
            confusable_concept_1=confusable_concept_1,
            confusable_concept_2=confusable_concept_2,
            task=task,
            context=context
        )
        response = f"{confusable_concept_1} focuses on [X], while {confusable_concept_2} focuses on [Y]. The key difference is [difference]."
    return {
        "instruction": question,
        "context": "",
        "response": response
    }

# Function to generate multi-hop reasoning questions
def generate_multi_hop_question(category):
    subcategory_1, subcategory_2 = random.sample(CATEGORIES[category], 2)
    instruction = f"How does {subcategory_1} influence {subcategory_2} in {category}?"
    response = f"{subcategory_1} impacts {subcategory_2} by [mechanism]. For example, [specific example]. This relationship is important because [reason]."
    return {
        "instruction": instruction,
        "context": "",
        "response": response
    }

# Generate 10,000 high-quality rows
with open("high_quality_dataset.jsonl", "w") as f:
    for _ in range(10000):
        category = random.choice(list(CATEGORIES.keys()))
        if random.random() < 0.3:  # 30% trap questions
            entry = generate_trap_question(category)
        elif random.random() < 0.6:  # 30% multi-hop reasoning
            entry = generate_multi_hop_question(category)
        else:  # 40% standard high-quality questions
            entry = generate_question(category, random.choice(CATEGORIES[category]))
        f.write(json.dumps(entry) + "\n")

print("High-quality dataset generated. Validate and fine-tune your model for competition success!")