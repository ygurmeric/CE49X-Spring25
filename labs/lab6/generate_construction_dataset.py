import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import random
import json

# Define document types and their characteristics
DOCUMENT_TYPES = {
    'Progress Report': {
        'keywords': [
            'completed', 'ongoing', 'milestone', 'schedule', 'progress', 'delay', 
            'ahead', 'percent', 'completion', 'phase', 'achieved', 'target',
            'workforce', 'equipment', 'materials', 'deliverables'
        ],
        'templates': [
            "Monthly Progress Report for {project_name}\nReporting Period: {date}\nOverall Completion: {completion}%\n\nKey Achievements:\n{achievements}\n\nChallenges:\n{challenges}\n\nNext Month's Targets:\n{targets}",
            "Project Status Update\nDate: {date}\nProject: {project_name}\n\nProgress Summary:\n{achievements}\n\nCompletion Status: {completion}% complete\n\nKey Issues:\n{challenges}\n\nPlanned Activities:\n{targets}"
        ]
    },
    'RFI': {
        'keywords': [
            'clarification', 'drawing', 'specification', 'detail', 'confirm',
            'please advise', 'request', 'information', 'query', 'unclear',
            'coordinate', 'dimension', 'method', 'alternative'
        ],
        'templates': [
            "REQUEST FOR INFORMATION\nRFI #: {rfi_number}\nDate: {date}\nProject: {project_name}\n\nSubject: {subject}\n\nQuestion:\n{question}\n\nSuggested Solution:\n{solution}\n\nResponse Required By: {response_date}",
            "RFI Form\nReference: {rfi_number}\nDate Issued: {date}\n\nTopic: {subject}\n\nDescription of Query:\n{question}\n\nProposed Resolution:\n{solution}\n\nUrgency: {urgency}"
        ]
    },
    'Change Order': {
        'keywords': [
            'modification', 'cost', 'scope', 'change', 'additional', 'revision',
            'timeline', 'budget', 'extension', 'variation', 'adjust', 'impact',
            'price', 'duration'
        ],
        'templates': [
            "CHANGE ORDER REQUEST\nCO #: {co_number}\nDate: {date}\nProject: {project_name}\n\nDescription of Change:\n{description}\n\nJustification:\n{justification}\n\nCost Impact: {cost_impact}\nSchedule Impact: {schedule_impact}",
            "Project Change Notice\nReference: {co_number}\nSubmission Date: {date}\n\nChange Details:\n{description}\n\nReason for Change:\n{justification}\n\nImpacts:\nCost: {cost_impact}\nTime: {schedule_impact}"
        ]
    },
    'Safety Incident': {
        'keywords': [
            'incident', 'injury', 'hazard', 'safety', 'PPE', 'accident',
            'near-miss', 'risk', 'emergency', 'violation', 'protective',
            'prevention', 'unsafe', 'immediate'
        ],
        'templates': [
            "SAFETY INCIDENT REPORT\nIncident #: {incident_number}\nDate/Time: {date}\nLocation: {location}\n\nIncident Description:\n{description}\n\nImmediate Actions Taken:\n{actions}\n\nPreventive Measures:\n{prevention}",
            "Safety Event Documentation\nReport #: {incident_number}\nOccurrence: {date}\nSite: {location}\n\nEvent Details:\n{description}\n\nResponse Actions:\n{actions}\n\nFuture Prevention:\n{prevention}"
        ]
    },
    'Quality Inspection': {
        'keywords': [
            'inspection', 'quality', 'compliance', 'standard', 'test',
            'measurement', 'specification', 'tolerance', 'acceptable',
            'defect', 'sample', 'verify', 'check'
        ],
        'templates': [
            "QUALITY INSPECTION REPORT\nInspection #: {inspection_number}\nDate: {date}\nLocation: {location}\n\nItems Inspected:\n{items}\n\nFindings:\n{findings}\n\nRecommendations:\n{recommendations}",
            "Quality Control Check\nReference: {inspection_number}\nInspection Date: {date}\nArea: {location}\n\nScope of Inspection:\n{items}\n\nObservations:\n{findings}\n\nRequired Actions:\n{recommendations}"
        ]
    }
}

# Project phases and roles
PROJECT_PHASES = ['Planning', 'Foundation', 'Structural', 'MEP', 'Finishing']
AUTHOR_ROLES = ['Project Manager', 'Site Engineer', 'Quality Inspector', 'Safety Officer', 'Construction Manager']

def generate_random_date(start_date, end_date):
    """Generate a random date between start_date and end_date"""
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    return start_date + timedelta(days=random_number_of_days)

def generate_document_content(doc_type, date):
    """Generate synthetic content for a document based on its type"""
    template_data = DOCUMENT_TYPES[doc_type]
    template = random.choice(template_data['templates'])
    keywords = template_data['keywords']
    
    # Common data
    project_names = ['City Center Tower', 'Harbor Bridge Extension', 'Metro Station Complex', 'Hospital Wing B', 'Shopping Mall Plaza']
    project_name = random.choice(project_names)
    
    if doc_type == 'Progress Report':
        completion = random.randint(0, 100)
        achievements = "\n".join([f"- {random.choice(['Completed', 'Started', 'Continued'])} {random.choice(['excavation', 'concrete work', 'steel installation', 'MEP works', 'finishing works'])}" for _ in range(3)])
        challenges = "\n".join([f"- {random.choice(['Delay in', 'Issue with', 'Coordination needed for'])} {random.choice(['material delivery', 'subcontractor work', 'weather conditions', 'equipment maintenance'])}" for _ in range(2)])
        targets = "\n".join([f"- {random.choice(['Complete', 'Begin', 'Continue'])} {random.choice(['foundation work', 'structural elements', 'electrical installation', 'plumbing works', 'interior finishing'])}" for _ in range(3)])
        return template.format(project_name=project_name, date=date.strftime('%Y-%m-%d'), completion=completion, achievements=achievements, challenges=challenges, targets=targets)
    
    elif doc_type == 'RFI':
        rfi_number = f"RFI-{random.randint(100, 999)}"
        subjects = ['Drawing Clarification', 'Material Specification', 'Construction Method', 'Design Conflict', 'Technical Query']
        subject = random.choice(subjects)
        question = f"Please clarify the {random.choice(['specifications', 'details', 'requirements', 'method'])} for {random.choice(['foundation work', 'structural connection', 'MEP installation', 'finishing detail'])}."
        solution = f"We suggest {random.choice(['modifying the detail', 'using alternative material', 'adjusting the method', 'revising the specification'])} to resolve this issue."
        response_date = (date + timedelta(days=random.randint(3, 10))).strftime('%Y-%m-%d')
        urgency = random.choice(['High', 'Medium', 'Low'])
        return template.format(rfi_number=rfi_number, date=date.strftime('%Y-%m-%d'), project_name=project_name, subject=subject, question=question, solution=solution, response_date=response_date, urgency=urgency)
    
    elif doc_type == 'Change Order':
        co_number = f"CO-{random.randint(100, 999)}"
        description = f"Change in {random.choice(['scope', 'specifications', 'materials', 'method'])} for {random.choice(['structural elements', 'MEP systems', 'architectural features', 'site works'])}."
        justification = f"Due to {random.choice(['site conditions', 'client request', 'regulatory requirements', 'optimization opportunity'])}."
        cost_impact = f"${random.randint(5000, 50000)}"
        schedule_impact = f"{random.randint(1, 30)} days"
        return template.format(co_number=co_number, date=date.strftime('%Y-%m-%d'), project_name=project_name, description=description, justification=justification, cost_impact=cost_impact, schedule_impact=schedule_impact)
    
    elif doc_type == 'Safety Incident':
        incident_number = f"SI-{random.randint(100, 999)}"
        location = random.choice(['Level 1', 'Level 2', 'Basement', 'Exterior', 'Storage Area'])
        description = f"A {random.choice(['near-miss', 'minor incident', 'safety violation', 'hazardous condition'])} was observed involving {random.choice(['equipment operation', 'material handling', 'work at height', 'confined space'])}."
        actions = f"Immediate action taken: {random.choice(['work stopped', 'area secured', 'workers briefed', 'PPE checked'])}."
        prevention = f"Recommended preventive measures include {random.choice(['additional training', 'revised procedures', 'enhanced supervision', 'new safety equipment'])}."
        return template.format(incident_number=incident_number, date=date.strftime('%Y-%m-%d'), location=location, description=description, actions=actions, prevention=prevention)
    
    else:  # Quality Inspection
        inspection_number = f"QI-{random.randint(100, 999)}"
        location = random.choice(['Level 1', 'Level 2', 'Basement', 'Exterior', 'Storage Area'])
        items = "\n".join([f"- {random.choice(['Concrete strength', 'Steel connections', 'MEP installations', 'Finishing work', 'Material storage'])}" for _ in range(3)])
        findings = "\n".join([f"- {random.choice(['Meets specifications', 'Minor deviation noted', 'Requires adjustment', 'Further inspection needed'])}" for _ in range(3)])
        recommendations = "\n".join([f"- {random.choice(['Continue as planned', 'Make minor adjustments', 'Conduct follow-up inspection', 'Update documentation'])}" for _ in range(2)])
        return template.format(inspection_number=inspection_number, date=date.strftime('%Y-%m-%d'), location=location, items=items, findings=findings, recommendations=recommendations)

def generate_dataset(num_documents=1000, output_file='construction_documents.json'):
    """Generate a synthetic dataset of construction project documents"""
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 12, 31)
    
    documents = []
    for _ in range(num_documents):
        doc_type = random.choice(list(DOCUMENT_TYPES.keys()))
        date = generate_random_date(start_date, end_date)
        
        document = {
            'date': date.strftime('%Y-%m-%d'),
            'document_type': doc_type,
            'project_phase': random.choice(PROJECT_PHASES),
            'author_role': random.choice(AUTHOR_ROLES),
            'content': generate_document_content(doc_type, date)
        }
        documents.append(document)
    
    # Save to JSON file
    with open(output_file, 'w') as f:
        json.dump(documents, f, indent=2)
    
    print(f"Generated {num_documents} documents and saved to {output_file}")
    
    # Also create a DataFrame for analysis
    df = pd.DataFrame(documents)
    return df

if __name__ == "__main__":
    # Generate the dataset
    df = generate_dataset()
    
    # Print some statistics
    print("\nDocument type distribution:")
    print(df['document_type'].value_counts())
    
    print("\nProject phase distribution:")
    print(df['project_phase'].value_counts())
    
    print("\nAuthor role distribution:")
    print(df['author_role'].value_counts()) 