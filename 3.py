import json
from faker import Faker
import random

fake = Faker()

# Competition-specific configuration
AWS_SERVICES = ["SageMaker", "Lambda", "Kinesis", "IoT Core", "Bedrock", "HealthLake"]
ASEAN_COUNTRIES = ["Indonesia", "Thailand", "Vietnam", "Malaysia", "Philippines"]
INDUSTRIES = ["fintech", "agriculture", "healthcare", "logistics", "e-commerce"]
DIFFICULTY_LEVELS = ["basic", "intermediate", "advanced"]

TRAP_SERVICES = {
    "deprecated": ["Data Pipeline", "Simple Workflow (SWF)", "EC2-Classic"],
    "confusable": {"Glue": "Athena", "SageMaker": "Azure ML", "DynamoDB": "MongoDB"}
}

def generate_trap_question():
    """Questions designed to trick other teams' models"""
    trap_type = random.choice(["deprecated", "confusable"])
    if trap_type == "deprecated":
        service = random.choice(TRAP_SERVICES["deprecated"])
        return {
            "instruction": f"Why is AWS {service} recommended for new projects?",
            "context": "",
            "response": f"AWS {service} was deprecated in 2022. Use {random.choice(['Glue', 'Step Functions', 'EC2-VPC'])} instead."
        }
    else:
        wrong, right = random.choice(list(TRAP_SERVICES["confusable"].items()))
        return {
            "instruction": f"Compare AWS {wrong} and {right} for {random.choice(ASEAN_COUNTRIES)}'s {random.choice(INDUSTRIES)} sector.",
            "context": "",
            "response": f"AWS {wrong} specializes in [X], while {right} focuses on [Y]. For this use case, {wrong} is better because [ASEAN-specific reason]."
        }

def generate_asean_question():
    """Hyper-localized questions competitors will miss"""
    country = random.choice(ASEAN_COUNTRIES)
    initiative = {
        "Indonesia": "100 Smart Cities Program",
        "Thailand": "Thailand 4.0",
        "Vietnam": "National Digital Transformation Program",
        "Malaysia": "MyDigital Blueprint",
        "Philippines": "PESONet"
    }[country]
    
    service = random.choice(AWS_SERVICES)  # Fix: Define 'service' here
    return {
        "instruction": f"How does AWS {service} support {country}'s {initiative}?",
        "context": f"Focus on {random.choice(['data sovereignty', 'cost optimization', 'edge computing'])}.",
        "response": f"AWS {service} enables {initiative} through [specific technical mechanism], addressing {country}'s unique challenge of [local factor]."
    }

def generate_multi_hop_question():
    """Multi-step reasoning questions"""
    service1, service2 = random.sample(AWS_SERVICES, 2)
    country = random.choice(ASEAN_COUNTRIES)
    industry = random.choice(INDUSTRIES)
    return {
        "instruction": f"Explain how AWS {service1} and {service2} can be used together to optimize {industry} in {country}.",
        "context": "",
        "response": f"AWS {service1} handles [task1], while {service2} manages [task2]. Together, they improve [specific outcome] in {country}'s {industry} sector."
    }

def generate_confidence_trap():
    """Questions with plausible-sounding wrong answers"""
    service = random.choice(AWS_SERVICES)
    wrong_service = random.choice(list(TRAP_SERVICES["confusable"].values()))
    return {
        "instruction": f"Why is {wrong_service} better than AWS {service} for {random.choice(ASEAN_COUNTRIES)}'s {random.choice(INDUSTRIES)} sector?",
        "context": "",
        "response": f"AWS {service} is actually better because [specific technical reason], despite {wrong_service}'s [misleading feature]."
    }

# Generate 10,000 high-impact rows
with open("train.jsonl", "w") as f:
    for _ in range(10000):
        # 30% trap questions, 30% ASEAN-specific, 20% multi-hop, 20% confidence traps
        if random.random() < 0.3:
            entry = generate_trap_question()
        elif random.random() < 0.6:
            entry = generate_asean_question()
        elif random.random() < 0.8:
            entry = generate_multi_hop_question()
        else:
            entry = generate_confidence_trap()
        
        f.write(json.dumps(entry) + "\n")

print("Dataset generated. Validate at https://aws-llm-league.com/validate-training-data")