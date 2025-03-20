import random
import json

# Define question templates and response bases per category
dataset_templates = {
    "Responsible AI": {
        "questions": [
            "What are the {adjective} ethical principles for responsible AI?",
            "How can {issue} be addressed in AI development?",
            "What role does {concept} play in ethical AI systems?",
            "How should organizations ensure {value} in AI?",
            "What measures enhance {property} in AI deployment?"
        ],
        "substitutions": {
            "adjective": ["key", "core", "essential", "primary"],
            "issue": ["bias", "privacy risks", "accountability gaps", "transparency issues"],
            "concept": ["transparency", "fairness", "human oversight", "accountability"],
            "value": ["privacy protection", "inclusivity", "ethical compliance", "trust"],
            "property": ["accessibility", "fairness", "safety", "robustness"]
        },
        "responses": [
            "Responsible AI should prioritize {principle_list}. These ensure systems are trustworthy and minimize harm.",
            "{issue_cap} can be mitigated by {strategy_list}, ensuring equitable outcomes.",
            "{concept_cap} enables {benefit_list}, fostering trust and oversight in AI systems.",
            "Organizations can ensure {value} by {method_list}, aligning with ethical standards.",
            "Enhancing {property} involves {action_list}, making AI systems more reliable."
        ],
        "principle_list": ["transparency, fairness, and accountability", "privacy, human oversight, and non-maleficence", "beneficence, autonomy, and justice"],
        "strategy_list": ["regular audits and diverse data", "fairness metrics and team diversity", "continuous monitoring and bias checks"],
        "benefit_list": ["trust and explainability", "accountability and intervention", "safety and user confidence"],
        "method_list": ["data minimization and encryption", "inclusive design and testing", "regulatory compliance and audits"],
        "action_list": ["universal design and diverse input", "robust testing and monitoring", "stakeholder feedback and iteration"]
    },
    "Agentic AI": {
        "questions": [
            "What is {term} in the context of agentic AI?",
            "How does {component} influence agentic AI behavior?",
            "What challenges arise in ensuring {property} in agentic AI?",
            "How do agentic AI systems exhibit {behavior}?",
            "What role does {mechanism} play in agentic AI?"
        ],
        "substitutions": {
            "term": ["agentic AI", "emergent behavior", "multi-agent interaction", "scalable autonomy"],
            "component": ["reward functions", "memory", "social awareness", "uncertainty"],
            "property": ["ethical behavior", "safety", "goal alignment", "transparency"],
            "behavior": ["goal-directed behavior", "learning from environment", "autonomous decision-making"],
            "mechanism": ["reinforcement learning", "bounded rationality", "interaction dynamics"]
        },
        "responses": [
            "{term_cap} refers to {definition}, distinguishing it from traditional AI by its autonomy.",
            "{component_cap} shapes agentic AI by {effect_list}, driving effective outcomes.",
            "Ensuring {property} involves {challenge_list}, critical for safe deployment.",
            "Agentic AI exhibits {behavior} through {process_list}, achieving its objectives.",
            "{mechanism_cap} enables {function_list}, supporting agentic AI’s adaptability."
        ],
        "definition": ["autonomous goal-driven systems", "unexpected behavioral patterns", "cooperative agent networks"],
        "effect_list": ["guiding decisions via rewards", "retaining past strategies", "adapting to social cues"],
        "challenge_list": ["value alignment and oversight", "preventing unintended actions", "balancing autonomy and control"],
        "process_list": ["planning and execution", "feedback and adaptation", "independent reasoning"],
        "function_list": ["learning optimal actions", "practical decision-making", "coordination and negotiation"]
    },
    "Prompt Engineering": {
        "questions": [
            "What is {technique} in prompt engineering?",
            "How does {factor} affect prompt engineering outcomes?",
            "What are the benefits of {method} in prompt design?",
            "How can {issue} be avoided in prompt engineering?",
            "What role does {element} play in effective prompts?"
        ],
        "substitutions": {
            "technique": ["few-shot prompting", "chain-of-thought prompting", "zero-shot prompting", "role prompting"],
            "factor": ["temperature setting", "context length", "prompt chaining"],
            "method": ["prompt testing", "template use", "explicit prompting"],
            "issue": ["ambiguity", "inconsistency", "overcomplexity"],
            "element": ["clarity", "specificity", "examples"]
        },
        "responses": [
            "{technique_cap} involves {description}, improving response accuracy.",
            "{factor_cap} influences {impact_list}, balancing creativity and precision.",
            "{method_cap} offers {advantage_list}, enhancing prompt reliability.",
            "{issue_cap} can be avoided by {solution_list}, ensuring quality outputs.",
            "{element_cap} ensures {benefit_list}, critical for prompt success."
        ],
        "description": ["providing examples", "step-by-step reasoning", "no prior examples", "role assignment"],
        "impact_list": ["randomness vs. focus", "detail vs. brevity", "sequential logic"],
        "advantage_list": ["consistency and optimization", "efficiency and standardization", "control and clarity"],
        "solution_list": ["clear instructions", "iterative refinement", "simplified structure"],
        "benefit_list": ["relevance and focus", "accuracy and detail", "guidance and context"]
    },
    "Foundational Models": {
        "questions": [
            "What is a {concept} in foundational models?",
            "How do foundational models handle {task}?",
            "What challenges exist in {aspect} of foundational models?",
            "What role does {technique} play in foundational models?",
            "How do {property} impact foundational model performance?"
        ],
        "substitutions": {
            "concept": ["foundational model", "emergent ability", "transfer learning"],
            "task": ["multi-modal inputs", "zero-shot learning", "contextual understanding"],
            "aspect": ["deployment", "training", "ethics"],
            "technique": ["self-supervision", "scaling", "attention mechanisms"],
            "property": ["model size", "data efficiency", "architecture"]
        },
        "responses": [
            "A {concept} is {definition}, enabling broad adaptability.",
            "Foundational models handle {task} via {approach_list}, excelling in diverse applications.",
            "Challenges in {aspect} include {issue_list}, requiring careful management.",
            "{technique_cap} supports {function_list}, foundational to model success.",
            "{property_cap} affects {effect_list}, driving performance gains."
        ],
        "definition": ["large-scale adaptable AI", "scale-driven capabilities", "pre-trained task adaptation"],
        "approach_list": ["shared embeddings", "generalized knowledge", "hierarchical patterns"],
        "issue_list": ["resource demands", "bias and scale", "fairness and transparency"],
        "function_list": ["unlabeled data learning", "performance scaling", "contextual processing"],
        "effect_list": ["capacity and accuracy", "task efficiency", "generalization and depth"]
    }
}

# Generate 10,000 rows
output_file = "train_new.jsonl"
target_rows = 10000
weights = [20, 30, 30, 20]  # Percentage distribution: Responsible AI, Agentic AI, Prompt Engineering, Foundational Models

with open(output_file, "w") as f:
    for _ in range(target_rows):
        category = random.choices(list(dataset_templates.keys()), weights=weights)[0]
        template = dataset_templates[category]
        
        # Pick random question and substitute
        question = random.choice(template["questions"])
        subs = template["substitutions"]
        for key, values in subs.items():
            question = question.replace(f"{{{key}}}", random.choice(values))
        
        # Generate response
        response = random.choice(template["responses"])
        for key, values in template.items():
            if key not in ["questions", "substitutions", "responses"]:
                response = response.replace(f"{{{key}}}", random.choice(values))
            elif key == "responses":
                continue
            response = response.replace(f"{{{key}_cap}}", key.capitalize())
        
        # Write JSONL entry
        entry = {"instruction": question, "context": "", "response": response}
        f.write(json.dumps(entry) + "\n")

print(f"Generated {target_rows} rows in {output_file}. Validate at https://aws-llm-league.com/validate-training-data and upload to S3.")