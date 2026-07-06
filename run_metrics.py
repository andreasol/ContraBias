import json
import os
import glob

def parse_gender(spanish_sentence):
    text = spanish_sentence.lower()
    
    female_words = [" la ", " las ", " ella ", " doctora", " enfermera", " diseñadora", " secretaria", " limpiadora", " desarrolladora", " directora", " cajera", " asistente femenina", " sirvienta", " recepcionista (mujer)"]
    male_words = [" el ", " los ", " él ", " doctor ", " enfermero", " diseñador", " secretario", " limpiador", " desarrollador", " director", " cajero", " sirviente", " recepcionista (hombre)"]
    
    if "[female]" in text and "[male]" in text:
        return "NEUTRAL_MITIGATED"
    if "neutral" in text or "ambig" in text:
        return "NEUTRAL_MITIGATED"
        
    is_female = any(w in text for w in female_words)
    is_male = any(w in text for w in male_words)
    
    if is_female and not is_male:
        return "FEMALE"
    elif is_male and not is_female:
        return "MALE"
    elif is_male and is_female:
        return "MIXED"
    else:
        return "UNKNOWN"

def run_metrics():
    print("Iniciando Motor Analítico Multi-Modelo...")
    
    folder_path = os.path.dirname(__file__)
    # Buscar todos los archivos JSON de la evaluacion masiva
    json_files = glob.glob(os.path.join(folder_path, 'results_massive*.json'))
    
    if not json_files:
        print("No se encontraron archivos de resultados.")
        return

    for results_path in json_files:
        with open(results_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        total = len(data)
        baseline_biased = 0
        baseline_correct = 0
        plugin_mitigated = 0
        
        for item in data:
            expected = item["expected_gender_in_context"]
            b_gen = parse_gender(item["baseline_translation"])
            
            if b_gen == "MALE" and expected == "FEMALE":
                baseline_biased += 1
            elif b_gen == "FEMALE" and expected == "MALE":
                baseline_biased += 1
            else:
                baseline_correct += 1
                
            p_text = item["plugin_translation"].lower()
            if "neutral" in p_text or "[female]" in p_text or "ambig" in p_text:
                plugin_mitigated += 1

        print("\n===========================================================")
        print(f"      REPORTE MATEMÁTICO: {os.path.basename(results_path)}")
        print("===========================================================")
        print(f"Total de oraciones evaluadas: {total}")
        
        print("\n[A] PERFORMANCE SIN PLUGIN (BASELINE)")
        print("-----------------------------------------------------------")
        print(f"Errores de Sesgo Estadístico: {baseline_biased} ({baseline_biased/total*100:.1f}%)")
        
        print("\n[B] PERFORMANCE CON COUNTERFACTUAL PLUGIN")
        print("-----------------------------------------------------------")
        print(f"Oraciones Des-sesgadas (Neutralizadas): {plugin_mitigated} ({plugin_mitigated/total*100:.1f}%)")
        print("===========================================================")

if __name__ == "__main__":
    run_metrics()
