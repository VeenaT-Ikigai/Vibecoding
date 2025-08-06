import speech_recognition as sr
import spacy

# Load medical NER model (use a custom or SciSpacy model for real deployment)
nlp = spacy.load("en_core_web_sm")

def transcribe_audio(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        return ""

def extract_clinical_elements(text):
    doc = nlp(text)
    elements = {
        "diagnoses": [],
        "treatment_plans": [],
        "key_elements": []
    }
    for ent in doc.ents:
        # Placeholder logic: customize for medical entities
        if ent.label_ in ["DISEASE", "CONDITION"]:
            elements["diagnoses"].append(ent.text)
        elif ent.label_ in ["TREATMENT", "PROCEDURE"]:
            elements["treatment_plans"].append(ent.text)
        else:
            elements["key_elements"].append(ent.text)
    return elements

def structure_consultation(audio_file):
    transcript = transcribe_audio(audio_file)
    clinical_data = extract_clinical_elements(transcript)
    structured = {
        "transcript": transcript,
        "diagnoses": clinical_data["diagnoses"],
        "treatment_plans": clinical_data["treatment_plans"],
        "key_elements": clinical_data["key_elements"]
    }
    return structured

if __name__ == "__main__":
    # Example usage
    audio_path = "consultation.wav"
    result = structure_consultation(audio_path)
    print("Transcript:\n", result["transcript"])
    print("\nDiagnoses:", result["diagnoses"])
    print("\nTreatment Plans:", result["treatment_plans"])
    print("\nKey Clinical Elements:", result["key_elements"])