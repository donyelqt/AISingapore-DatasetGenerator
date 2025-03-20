import json
from faker import Faker
import random

fake = Faker()

# Competition-specific configuration
AWS_SERVICES = ["SageMaker", "Lambda", "Kinesis", "IoT Core", "Bedrock", "HealthLake", "Glue", "DynamoDB"]
ASEAN_COUNTRIES = ["Indonesia", "Thailand", "Vietnam", "Malaysia", "Philippines"]
INDUSTRIES = ["fintech", "agriculture", "healthcare", "logistics", "e-commerce"]
DIFFICULTY_LEVELS = ["basic", "intermediate", "advanced"]
FOCUSES = ["data sovereignty", "cost optimization", "edge computing"]

# Specific technical mechanisms and local factors
TECHNICAL_MECHANISMS = {
    "SageMaker": ["pre-trained models via JumpStart", "real-time inference endpoints", "distributed training"],
    "Lambda": ["serverless event-driven processing", "auto-scaling compute", "microservices orchestration"],
    "Kinesis": ["real-time data streaming", "shard-based scalability", "data ingestion pipelines"],
    "IoT Core": ["MQTT-based edge processing", "device shadow management", "Greengrass integration"],
    "Bedrock": ["foundation model customization", "private model hosting", "low-latency inference"],
    "HealthLake": ["FHIR-compliant data storage", "healthcare analytics pipelines", "structured data extraction"],
    "Glue": ["ETL job automation", "data cataloging", "serverless data integration"],
    "DynamoDB": ["low-latency NoSQL queries", "auto-scaling throughput", "global tables"]
}

LOCAL_FACTORS = {
    "Indonesia": ["archipelagic connectivity gaps", "rapid urbanization", "data residency laws"],
    "Thailand": ["rural digital divide", "tourism-driven economy", "smart city initiatives"],
    "Vietnam": ["limited rural internet", "export-driven growth", "multilingual needs"],
    "Malaysia": ["cloud-first policy", "urban-rural disparity", "data protection regulations"],
    "Philippines": ["high rural banking costs", "frequent natural disasters", "mobile-first population"]
}

TRAP_SERVICES = {
    "deprecated": ["Data Pipeline", "Simple Workflow (SWF)", "EC2-Classic"],
    "confusable": {"Glue": "Athena", "SageMaker": "Azure ML", "DynamoDB": "MongoDB"}
}

SPECIFIC_OUTCOMES = {
    "fintech": ["transaction security", "fraud detection", "customer onboarding speed"],
    "agriculture": ["crop yield prediction", "supply chain efficiency", "soil monitoring"],
    "healthcare": ["patient record interoperability", "telemedicine latency", "disease prediction"],
    "logistics": ["real-time tracking", "route optimization", "demand forecasting"],
    "e-commerce": ["personalized recommendations", "inventory management", "customer support automation"]
}

def generate_trap_question():
    """Questions designed to trick other teams' models"""
    trap_type = random.choice(["deprecated", "confusable"])
    if trap_type == "deprecated":
        service = random.choice(TRAP_SERVICES["deprecated"])
        replacement = random.choice(['Glue', 'Step Functions', 'EC2-VPC'])
        return {
            "instruction": f"Why is AWS {service} recommended for new projects?",
            "context": "",
            "response": f"AWS {service} was deprecated in 2022. Use {replacement} instead for modern, scalable solutions."
        }
    else:
        wrong, right = random.choice(list(TRAP_SERVICES["confusable"].items()))
        country = random.choice(ASEAN_COUNTRIES)
        industry = random.choice(INDUSTRIES)
        mechanism = random.choice(TECHNICAL_MECHANISMS.get(wrong, ["generic capability"]))
        local_factor = random.choice(LOCAL_FACTORS[country])
        return {
            "instruction": f"Compare AWS {wrong} and {right} for {country}'s {industry} sector.",
            "context": "",
            "response": f"AWS {wrong} specializes in {mechanism}, while {right} focuses on alternative approaches. For {country}'s {industry} sector, {wrong} is better due to its alignment with {local_factor}."
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
    
    service = random.choice(AWS_SERVICES)
    focus = random.choice(FOCUSES)
    mechanism = random.choice(TECHNICAL_MECHANISMS[service])
    local_factor = random.choice(LOCAL_FACTORS[country])
    return {
        "instruction": f"How does AWS {service} support {country}'s {initiative}?",
        "context": f"Focus on {focus}.",
        "response": f"AWS {service} enables {initiative} through {mechanism}, addressing {country}'s unique challenge of {local_factor}. For {focus}, it provides scalable, secure solutions tailored to regional needs."
    }

def generate_multi_hop_question():
    """Multi-step reasoning questions"""
    service1, service2 = random.sample(AWS_SERVICES, 2)
    country = random.choice(ASEAN_COUNTRIES)
    industry = random.choice(INDUSTRIES)
    task1 = random.choice(TECHNICAL_MECHANISMS[service1])
    task2 = random.choice(TECHNICAL_MECHANISMS[service2])
    outcome = random.choice(SPECIFIC_OUTCOMES[industry])
    return {
        "instruction": f"Explain how AWS {service1} and {service2} can be used together to optimize {industry} in {country}.",
        "context": "",
        "response": f"AWS {service1} handles {task1}, while {service2} manages {task2}. Together, they improve {outcome} in {country}'s {industry} sector by leveraging complementary strengths."
    }

def generate_confidence_trap():
    """Questions with plausible-sounding wrong answers"""
    service = random.choice(AWS_SERVICES)
    wrong_service = random.choice(list(TRAP_SERVICES["confusable"].values()))
    country = random.choice(ASEAN_COUNTRIES)
    industry = random.choice(INDUSTRIES)
    mechanism = random.choice(TECHNICAL_MECHANISMS[service])
    misleading_feature = random.choice(["ease of use", "broad compatibility", "lower initial cost"])
    return {
        "instruction": f"Why is {wrong_service} better than AWS {service} for {country}'s {industry} sector?",
        "context": "",
        "response": f"AWS {service} is actually better because its {mechanism} delivers superior performance, despite {wrong_service}'s {misleading_feature}."
    }

def generate_generative_ai_question():
    """Questions showcasing generative AI capabilities"""
    country = random.choice(ASEAN_COUNTRIES)
    industry = random.choice(INDUSTRIES)
    outcome = random.choice(SPECIFIC_OUTCOMES[industry])
    local_factor = random.choice(LOCAL_FACTORS[country])
    return {
        "instruction": f"How can AWS SageMaker JumpStart use generative AI to improve {industry} in {country}?",
        "context": "Focus on underserved communities.",
        "response": f"AWS SageMaker JumpStart leverages pre-trained LLMs, fine-tuned on {country}'s {industry} data, to generate {outcome}-focused solutions (e.g., chatbots, predictions). For underserved communities, it addresses {local_factor} by enabling low-cost, scalable AI deployment."
    }

# Generate 10,000 high-impact rows
with open("train.jsonl", "w") as f:
    for _ in range(10000):
        rand = random.random()
        if rand < 0.25:  # 25% trap questions
            entry = generate_trap_question()
        elif rand < 0.50:  # 25% ASEAN-specific
            entry = generate_asean_question()
        elif rand < 0.70:  # 20% multi-hop
            entry = generate_multi_hop_question()
        elif rand < 0.90:  # 20% confidence traps
            entry = generate_confidence_trap()
        else:  # 10% generative AI focus
            entry = generate_generative_ai_question()
        
        f.write(json.dumps(entry) + "\n")

print("Dataset generated. Validate at https://aws-llm-league.com/validate-training-data")