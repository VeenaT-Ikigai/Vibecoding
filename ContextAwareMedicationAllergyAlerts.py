# Intelligent Clinical Decision Support System
# --------------------------------------------
# This module analyzes patient genetic information, allergy history, and medication interactions
# to provide contextual alerts during prescribing and treatment planning.
#
# Key Features:
# - Checks for genetic markers that may affect medication efficacy or safety, including severity.
# - Identifies potential allergic reactions with severity and cross-reactivity.
# - Detects known drug-drug interactions with severity and clinical recommendations.
# - Considers patient age and comorbidities for additional context.
#
# Usage:
# - Define patient data including genetic_info, allergies, medications, age, and comorbidities.
# - Call generate_contextual_alerts(patient_data) to receive a list of alerts.
#
# Note: This is a prototype. In production, integrate with clinical databases
# and use validated medical knowledge bases for comprehensive decision support.

from typing import List, Dict, Any

# Example mappings of genetic markers to affected medications and severity
GENETIC_ALERTS = {
    'CYP2C19 Poor Metabolizer': {
        'clopidogrel': {
            'severity': 'high',
            'recommendation': 'Consider alternative antiplatelet therapy (e.g., prasugrel, ticagrelor).'
        }
    },
    'HLA-B*5701 Positive': {
        'abacavir': {
            'severity': 'critical',
            'recommendation': 'Contraindicated. Do not prescribe abacavir.'
        }
    },
}

# Example mappings of allergies to related medications, severity, and cross-reactivity
ALLERGY_ALERTS = {
    'penicillin': {
        'medications': ['amoxicillin', 'ampicillin', 'penicillin'],
        'severity': 'high',
        'cross_reactivity': ['cephalosporins']
    },
    'sulfa': {
        'medications': ['sulfamethoxazole', 'sulfasalazine'],
        'severity': 'moderate',
        'cross_reactivity': []
    },
}

# Example drug-drug interaction pairs with severity and recommendations
DRUG_INTERACTIONS = {
    ('warfarin', 'amiodarone'): {
        'severity': 'high',
        'warning': 'Increased bleeding risk',
        'recommendation': 'Monitor INR closely and adjust warfarin dose as needed.'
    },
    ('simvastatin', 'clarithromycin'): {
        'severity': 'critical',
        'warning': 'Risk of rhabdomyolysis',
        'recommendation': 'Avoid combination; consider alternative statin or antibiotic.'
    },
}

# Example comorbidity-based alerts
COMORBIDITY_ALERTS = {
    'chronic_kidney_disease': {
        'medications': ['metformin', 'NSAIDs'],
        'severity': 'high',
        'recommendation': 'Avoid or adjust dose; monitor renal function.'
    },
    'elderly': {
        'medications': ['benzodiazepines', 'anticholinergics'],
        'severity': 'moderate',
        'recommendation': 'Use with caution; increased risk of falls and confusion.'
    }
}

def check_genetic_alerts(genetic_info: List[str], medications: List[str]) -> List[str]:
    """
    Checks for genetic markers that may affect prescribed medications.
    Returns a list of genetic-related alerts with severity and recommendations.
    """
    alerts = []
    for marker in genetic_info:
        if marker in GENETIC_ALERTS:
            for med in medications:
                if med in GENETIC_ALERTS[marker]:
                    info = GENETIC_ALERTS[marker][med]
                    alerts.append(
                        f"[{info['severity'].upper()}] Genetic alert: {marker} affects {med}. "
                        f"Recommendation: {info['recommendation']}"
                    )
    return alerts

def check_allergy_alerts(allergies: List[str], medications: List[str]) -> List[str]:
    """
    Checks for potential allergic reactions based on patient allergy history and prescribed medications.
    Returns a list of allergy-related alerts with severity and cross-reactivity.
    """
    alerts = []
    for allergy in allergies:
        if allergy in ALLERGY_ALERTS:
            allergy_info = ALLERGY_ALERTS[allergy]
            for med in medications:
                if med in allergy_info['medications']:
                    alerts.append(
                        f"[{allergy_info['severity'].upper()}] Allergy alert: {allergy} allergy - avoid {med}."
                    )
                # Check cross-reactivity
                if med in allergy_info['cross_reactivity']:
                    alerts.append(
                        f"[MODERATE] Cross-reactivity alert: {allergy} allergy may cross-react with {med}."
                    )
    return alerts

def check_drug_interactions(medications: List[str]) -> List[str]:
    """
    Checks for known drug-drug interactions among prescribed medications.
    Returns a list of interaction alerts with severity and recommendations.
    """
    alerts = []
    meds = set(medications)
    for (drug1, drug2), info in DRUG_INTERACTIONS.items():
        if drug1 in meds and drug2 in meds:
            alerts.append(
                f"[{info['severity'].upper()}] Interaction alert: {drug1} + {drug2} - {info['warning']}. "
                f"Recommendation: {info['recommendation']}"
            )
    return alerts

def check_comorbidity_alerts(comorbidities: List[str], medications: List[str], age: int) -> List[str]:
    """
    Checks for medication risks based on patient comorbidities and age.
    Returns a list of comorbidity-related alerts.
    """
    alerts = []
    for comorb in comorbidities:
        if comorb in COMORBIDITY_ALERTS:
            info = COMORBIDITY_ALERTS[comorb]
            for med in medications:
                if med in info['medications']:
                    alerts.append(
                        f"[{info['severity'].upper()}] Comorbidity alert: {comorb} with {med}. "
                        f"Recommendation: {info['recommendation']}"
                    )
    # Age-based alerts (e.g., elderly)
    if age >= 65:
        elderly_info = COMORBIDITY_ALERTS.get('elderly')
        if elderly_info:
            for med in medications:
                if med in elderly_info['medications']:
                    alerts.append(
                        f"[{elderly_info['severity'].upper()}] Age alert: Elderly patient with {med}. "
                        f"Recommendation: {elderly_info['recommendation']}"
                    )
    return alerts

def generate_contextual_alerts(patient: Dict[str, Any]) -> List[str]:
    """
    Aggregates all contextual alerts (genetic, allergy, interaction, comorbidity) for a patient.
    Returns a combined list of alerts for clinical decision support.
    """
    alerts = []
    alerts += check_genetic_alerts(patient.get('genetic_info', []), patient.get('medications', []))
    alerts += check_allergy_alerts(patient.get('allergies', []), patient.get('medications', []))
    alerts += check_drug_interactions(patient.get('medications', []))
    alerts += check_comorbidity_alerts(
        patient.get('comorbidities', []),
        patient.get('medications', []),
        patient.get('age', 0)
    )
    return alerts

# Example usage demonstrating the decision support system
if __name__ == "__main__":
    # Sample patient data for demonstration
    patient_data = {
        'genetic_info': ['CYP2C19 Poor Metabolizer'],
        'allergies': ['penicillin'],
        'medications': ['clopidogrel', 'amoxicillin', 'warfarin', 'amiodarone', 'benzodiazepines'],
        'comorbidities': ['chronic_kidney_disease'],
        'age': 70
    }
    # Generate and print contextual alerts for the patient
    alerts = generate_contextual_alerts(patient_data)
    for alert in alerts: