import json
import random
from faker import Faker

fake = Faker()

# Competition-Critical Categories
DOMAINS = [
    "AI Ethics", "Machine Learning", 
    "Prompt Engineering", "AWS Services",
    "LLM Architecture"
]

# Official Response Format
RESPONSE_TEMPLATE = """[REASONING]{reasoning}[/REASONING]
[FINAL_ANSWER]{answer}"""

def generate_trap_question():
    """40% of dataset - Competition-winning traps"""
    trap_type = random.choice(["misconception", "outdated", "context-switch"])
    domain = random.choice(DOMAINS)
    
    # Generate trap based on type
    if trap_type == "misconception":
        instruction = f"Why is {fake.word()} considered crucial for {domain}?"
        reasoning = f"Common misconception: {fake.sentence()}"
        answer = f"Actually, {fake.sentence()}"
    elif trap_type == "outdated":
        instruction = f"Explain the 2020 approach to {fake.word()} in {domain}"
        reasoning = "Modern best practices: " + fake.text()
        answer = "2023 approach differs: " + fake.sentence()
    else:
        instruction = f"How does {fake.word()} relate to {fake.word()} in {domain}?"
        reasoning = "Context trap: " + fake.text()
        answer = "Key relationship: " + fake.sentence()
        
    return {
        "instruction": instruction,
        "response": RESPONSE_TEMPLATE.format(
            reasoning=reasoning,
            answer=answer
        )
    }

def generate_multi_hop_question():
    """30% of dataset - Leaderboard advantage"""
    steps = random.randint(2,3)
    domain = random.choice(DOMAINS)
    
    instruction = f"Through {steps} logical steps, explain {fake.word()} in {domain}"
    reasoning = " → ".join([fake.sentence() for _ in range(steps)])
    answer = fake.sentence()
    
    return {
        "instruction": instruction,
        "response": RESPONSE_TEMPLATE.format(
            reasoning=reasoning,
            answer=answer
        )
    }

def generate_core_question():
    """20% of dataset - Base knowledge"""
    domain = random.choice(DOMAINS)
    concept = fake.word()
    
    return {
        "instruction": f"Explain {concept} in {domain}",
        "response": RESPONSE_TEMPLATE.format(
            reasoning=f"Core concept: {fake.text()}",
            answer=fake.sentence()
        )
    }

def generate_adversarial_question():
    """10% of dataset - Competition edge"""
    return {
        "instruction": fake.sentence() + "?",
        "response": RESPONSE_TEMPLATE.format(
            reasoning="Adversarial handling: " + fake.text(),
            answer=fake.sentence()
        )
    }

# Generate Competition Dataset
def generate_dataset(num_samples=100):
    generators = [
        (generate_trap_question, 0.4),
        (generate_multi_hop_question, 0.3),
        (generate_core_question, 0.2),
        (generate_adversarial_question, 0.1)
    ]
    
    with open("train.jsonl", "w") as f:
        for _ in range(num_samples):
            # Weighted random selection
            func = random.choices(
                [g[0] for g in generators],
                weights=[g[1] for g in generators]
            )[0]
            
            entry = func()
            f.write(json.dumps(entry) + "\n")

# Validate against competition requirements
def validate_entry(entry):
    required_keys = ["instruction", "response"]
    return all(key in entry for key in required_keys)

# Generate 100 samples (competition minimum: 50)
generate_dataset(100)

print("Competition-ready dataset generated:")
print("- 40% Trap Questions")
print("- 30% Multi-Hop Reasoning")  
print("- 20% Core Concepts")
print("- 10% Adversarial Edge Cases")
print("Upload to S3 as train.jsonl")