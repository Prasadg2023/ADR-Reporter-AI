from fpdf import FPDF
import tempfile
import os

import re

# Brand names mapping to generic names (focused on Indian clinical practice and commonly reported drugs)
BRAND_TO_GENERIC = {
    # Antipyretics / Analgesics / NSAIDs
    "dolo": "paracetamol",
    "dolo 650": "paracetamol",
    "crocin": "paracetamol",
    "calpol": "paracetamol",
    "pacimol": "paracetamol",
    "panadol": "paracetamol",
    "tylenol": "paracetamol",
    "combiflam": "ibuprofen + paracetamol",
    "advil": "ibuprofen",
    "motrin": "ibuprofen",
    "voveran": "diclofenac",
    "dynapar": "diclofenac",
    "reactin": "diclofenac",
    "zerodol": "aceclofenac",
    "zerodol-sp": "aceclofenac + paracetamol + serratiopeptidase",
    "zerodol sp": "aceclofenac + paracetamol + serratiopeptidase",
    "zerodol-p": "aceclofenac + paracetamol",
    "zerodol p": "aceclofenac + paracetamol",
    "meftal": "mefenamic acid",
    "meftal-pd": "mefenamic acid",
    "meftal pd": "mefenamic acid",
    "meftal-spas": "mefenamic acid + dicyclomine",
    "meftal spas": "mefenamic acid + dicyclomine",
    "nise": "nimesulide",
    "nice": "nimesulide",
    "etorica": "etoricoxib",
    "nucoxia": "etoricoxib",
    "etoshine": "etoricoxib",
    "naprosyn": "naproxen",
    "disprin": "aspirin",
    "ecotrin": "aspirin",
    "loprin": "aspirin",
    "ecosprin": "aspirin",
    "colospa": "mebeverine",
    "celebrex": "celecoxib",
    "spasmonil": "dicyclomine",
    "buscopan": "hyoscine butylbromide",
    "cyclopam": "dicyclomine + paracetamol",
    
    # Antibiotics
    "augmentin": "amoxicillin + clavulanic acid",
    "clavam": "amoxicillin + clavulanic acid",
    "moxikind-cv": "amoxicillin + clavulanic acid",
    "moxikind cv": "amoxicillin + clavulanic acid",
    "moxclav": "amoxicillin + clavulanic acid",
    "mox": "amoxicillin",
    "amoxil": "amoxicillin",
    "azithral": "azithromycin",
    "azee": "azithromycin",
    "zithromax": "azithromycin",
    "taxim": "cefotaxime",
    "taxim-o": "cefixime",
    "taxim o": "cefixime",
    "zifi": "cefixime",
    "ceftum": "cefuroxime",
    "zinnat": "cefuroxime",
    "cefakind": "cefuroxime",
    "monocef": "ceftriaxone",
    "oframax": "ceftriaxone",
    "ciplox": "ciprofloxacin",
    "cifran": "ciprofloxacin",
    "floxip": "ciprofloxacin",
    "zenflox": "ofloxacin",
    "oflox": "ofloxacin",
    "loxof": "levofloxacin",
    "levoflox": "levofloxacin",
    "norflox": "norfloxacin",
    "norbactin": "norfloxacin",
    "metrogyl": "metronidazole",
    "flagyl": "metronidazole",
    "sporidex": "cephalexin",
    "keflex": "cephalexin",
    "linid": "linezolid",
    "lino": "linezolid",
    "vancocin": "vancomycin",
    "meronem": "meropenem",
    "farobact": "faropenem",
    "doxy-1": "doxycycline",
    "doxy1": "doxycycline",
    "mikacin": "amikacin",
    "klarim": "clarithromycin",
    
    # Antifungals
    "diflucan": "fluconazole",
    "syscan": "fluconazole",
    "fluka": "fluconazole",
    "sporanox": "itraconazole",
    "canditral": "itraconazole",
    "itraspor": "itraconazole",
    "nizral": "ketoconazole",
    "ketocip": "ketoconazole",
    "loprox": "ciclopirox",
    "lulifin": "luliconazole",
    "lulisyr": "luliconazole",
    "candid": "clotrimazole",
    
    # Antivirals
    "zovirax": "acyclovir",
    "valcivir": "valacyclovir",
    "tamiflu": "oseltamivir",
    "heptavir": "lamivudine",
    "duovir": "lamivudine + zidovudine",
    "triomune": "lamivudine + stavudine + nevirapine",
    "viread": "tenofovir",
    
    # Antihistamines / Antiallergics
    "avil": "pheniramine",
    "allegra": "fexofenadine",
    "fexo": "fexofenadine",
    "telfast": "fexofenadine",
    "cetzine": "cetirizine",
    "okacet": "cetirizine",
    "levocet": "levocetirizine",
    "1-al": "levocetirizine",
    "1 al": "levocetirizine",
    "montair-lc": "montelukast + levocetirizine",
    "montair lc": "montelukast + levocetirizine",
    "telekast-l": "montelukast + levocetirizine",
    "telekast l": "montelukast + levocetirizine",
    "montair": "montelukast",
    "singulair": "montelukast",
    "montek": "montelukast",
    "montina": "montelukast",
    "atarax": "hydroxyzine",
    "phenergan": "promethazine",
    "benadryl": "diphenhydramine",
    
    # Antidiabetics
    "glycomet": "metformin",
    "glyciphage": "metformin",
    "amaryl": "glimepiride",
    "glimy": "glimepiride",
    "glynase": "glipizide",
    "diamicron": "gliclazide",
    "jalra": "vildagliptin",
    "galvus": "vildagliptin",
    "januvia": "sitagliptin",
    "glyxambi": "empagliflozin + linagliptin",
    "jardiance": "empagliflozin",
    "forxiga": "dapagliflozin",
    "lantus": "insulin glargine",
    "mixtard": "human insulin",
    "lupisulin": "human insulin",
    "humalog": "insulin lispro",
    "novorapid": "insulin aspart",
    "ryzodeg": "insulin degludec + insulin aspart",
    "istamet": "sitagliptin + metformin",
    
    # Antihypertensives
    "amlopin": "amlodipine",
    "stamlo": "amlodipine",
    "amlovas": "amlodipine",
    "telma": "telmisartan",
    "telmikind": "telmisartan",
    "telvas": "telmisartan",
    "cilacar": "cilnidipine",
    "cilanem": "cilnidipine",
    "metolar": "metoprolol",
    "betaloc": "metoprolol",
    "concor": "bisoprolol",
    "cardace": "ramipril",
    "lasix": "furosemide",
    "dytor": "torsemide",
    "aldactone": "spironolactone",
    "arkamin": "clonidine",
    "tenormin": "atenolol",
    "lnipril": "lisinopril",
    
    # Bronchodilators
    "asthalin": "salbutamol",
    "ventolin": "salbutamol",
    "duolin": "levosalbutamol + ipratropium",
    "foracort": "formoterol + budesonide",
    "seroflo": "salmeterol + fluticasone",
    "aerocort": "levosalbutamol + beclomethasone",
    "grilinctus": "levosalbutamol + ambroxol + guaiphenesin",
    "ascoril": "levosalbutamol + ambroxol + guaiphenesin",
    
    # Corticosteroids
    "wysolone": "prednisolone",
    "omnacortil": "prednisolone",
    "medrol": "methylprednisolone",
    "decadron": "dexamethasone",
    "dexona": "dexamethasone",
    "betnesol": "betamethasone",
    "budecort": "budesonide",
    "flomist": "fluticasone",
    
    # Anticoagulants / Antiplatelets
    "clexane": "enoxaparin",
    "clopilet": "clopidogrel",
    "plavix": "clopidogrel",
    "clopivas": "clopidogrel",
    "plagril": "clopidogrel",
    "brilinta": "ticagrelor",
    "eliquis": "apixaban",
    "xarelto": "rivaroxaban",
    "pradaxa": "dabigatran",
    "warfarin": "warfarin",
    "acitrom": "acenocoumarol",
    
    # Proton Pump Inhibitors / Antacids / Antiemetics
    "omez": "omeprazole",
    "omnecip": "omeprazole",
    "omecip": "omeprazole",
    "omez-d": "omeprazole + domperidone",
    "omez d": "omeprazole + domperidone",
    "pantocid": "pantoprazole",
    "pantodac": "pantoprazole",
    "pantocid-d": "pantoprazole + domperidone",
    "pantocid d": "pantoprazole + domperidone",
    "pan-d": "pantoprazole + domperidone",
    "pan d": "pantoprazole + domperidone",
    "pan-40": "pantoprazole",
    "pan 40": "pantoprazole",
    "rabeloc": "rabeprazole",
    "rabeloc-rd": "rabeprazole + domperidone",
    "aciloc": "ranitidine",
    "zantac": "ranitidine",
    "histac": "ranitidine",
    "rantac": "ranitidine",
    "pepcia": "rabeprazole",
    "veloz": "rabeprazole",
    "ondem": "ondansetron",
    "zofer": "ondansetron",
    "vomitabs": "ondansetron",
    "reglan": "metoclopramide",
    "periset": "ondansetron",
    "digene": "magaldrate + simethicone",
    "gelusil": "aluminium hydroxide + magnesium hydroxide + simethicone",
    "mucaine": "oxetacaine + aluminium hydroxide + magnesium hydroxide",
    
    # Vitamin and Mineral Supplements
    "becosules": "vitamin b complex",
    "cobadex": "vitamin b complex",
    "limcee": "vitamin c",
    "shelcal": "calcium + vitamin d3",
    "gemcal": "calcium + vitamin d3",
    "evion": "vitamin e",
    "evion 400": "vitamin e",
    "folvite": "folic acid",
    "autrin": "iron + folic acid + vitamin b12",
    "dexorange": "iron + folic acid + vitamin b12",
    "orofer xt": "ferrous ascorbate + folic acid",
    "neurobion": "vitamin b complex",
    "neurobion forte": "vitamin b complex",
    "calcirol": "cholecalciferol",
    "d3-must": "cholecalciferol",
    "d3 must": "cholecalciferol",
    
    # Hormonal Drugs
    "eltroxin": "levothyroxine",
    "thyronorm": "levothyroxine",
    "thyrox": "levothyroxine",
    "susten": "progesterone",
    "duphaston": "dydrogesterone",
    "meprate": "medroxyprogesterone",
    "novelon": "desogestrel + ethinylestradiol",
    "mala-d": "levonorgestrel + ethinylestradiol",
    "mala d": "levonorgestrel + ethinylestradiol",
    "mala-n": "norethisterone + ethinylestradiol",
    "mala n": "norethisterone + ethinylestradiol",
    
    # Vaccines
    "covishield": "covishield vaccine",
    "covaxin": "covaxin vaccine",
    "rabipur": "rabies vaccine",
    "engerix-b": "hepatitis b vaccine",
    "engerix b": "hepatitis b vaccine",
    "varilrix": "varicella vaccine",
    
    # Antidepressants / Antipsychotics / Antiepileptics
    "zoloft": "sertraline",
    "prozac": "fluoxetine",
    "nexito": "escitalopram",
    "cipralex": "escitalopram",
    "amitone": "amitriptyline",
    "oleanz": "olanzapine",
    "risnia": "risperidone",
    "seroquel": "quetiapine",
    "tegretol": "carbamazepine",
    "encorate": "sodium valproate",
    "valparin": "sodium valproate",
    "dilantin": "phenytoin",
    "epilan": "phenytoin",
    "gardenal": "phenobarbitone",
    "keppra": "levetiracetam",
    "frisium": "clobazam",
    "clonotril": "clonazepam",
    "zapiz": "clonazepam",
    "gabapin": "gabapentin",
    "lyrica": "pregabalin",
    "calmpose": "diazepam",
    "valium": "diazepam",
    
    # Others / Cardiovascular / Lipids
    "lipitor": "atorvastatin",
    "atorva": "atorvastatin",
    "solvin cold": "paracetamol + phenylephrine + chlorpheniramine",
    "wikoryl": "paracetamol + phenylephrine + chlorpheniramine",
    "sinarest": "paracetamol + phenylephrine + chlorpheniramine",
    "alex": "dextromethorphan",
    "tusq-d": "dextromethorphan",
    "tusq d": "dextromethorphan",

    # Newly Added Brands for Expanded Categories
    # Beta-blockers
    "lopresor": "metoprolol",
    "inderal": "propranolol",
    "cardivas": "carvedilol",
    "coreg": "carvedilol",
    "bystolic": "nebivolol",
    "trandate": "labetalol",
    # Calcium Channel Blockers
    "norvasc": "amlodipine",
    "calaptin": "verapamil",
    "dilzem": "diltiazem",
    "depin": "nifedipine",
    "adalat": "nifedipine",
    "procardia": "nifedipine",
    "plendil": "felodipine",
    # ACE Inhibitors
    "lipril": "lisinopril",
    "zestril": "lisinopril",
    "prinivil": "lisinopril",
    "enam": "enalapril",
    "vasotec": "enalapril",
    "lotensin": "benazepril",
    "capoten": "captopril",
    "coversyl": "perindopril",
    # Angiotensin Receptor Blockers (ARBs)
    "losar": "losartan",
    "covance": "losartan",
    "cozaar": "losartan",
    "diovan": "valsartan",
    "olmax": "olmesartan",
    "olmetime": "olmesartan",
    "benicar": "olmesartan",
    "avapro": "irbesartan",
    "atacand": "candesartan",
    # Diuretics
    "aquazide": "hydrochlorothiazide",
    "thalitone": "chlorthalidone",
    "microzide": "hydrochlorothiazide",
    # Statins / Lipid-lowering Drugs
    "lipvas": "atorvastatin",
    "crestor": "rosuvastatin",
    "rosuvas": "rosuvastatin",
    "zocor": "simvastatin",
    "pravachol": "pravastatin",
    "livalo": "pitavastatin",
    "tricor": "fenofibrate",
    "lipicard": "fenofibrate",
    # Benzodiazepines
    "xanax": "alprazolam",
    "alprax": "alprazolam",
    "restyl": "alprazolam",
    "ativan": "lorazepam",
}

# Generic drug mapping to their primary therapeutic categories
GENERIC_TO_CATEGORY = {
    # Antipyretics
    "paracetamol": "Antipyretics",
    "acetaminophen": "Antipyretics",
    
    # Analgesics
    "tramadol": "Analgesics",
    "codeine": "Analgesics",
    "morphine": "Analgesics",
    "fentanyl": "Analgesics",
    "oxycodone": "Analgesics",
    "pethidine": "Analgesics",
    "pentazocine": "Analgesics",
    "buprenorphine": "Analgesics",
    "methadone": "Analgesics",
    "dicyclomine": "Analgesics",
    "mebeverine": "Analgesics",
    "hyoscine butylbromide": "Analgesics",
    
    # NSAIDs
    "ibuprofen": "NSAIDs",
    "diclofenac": "NSAIDs",
    "aceclofenac": "NSAIDs",
    "mefenamic acid": "NSAIDs",
    "nimesulide": "NSAIDs",
    "meloxicam": "NSAIDs",
    "piroxicam": "NSAIDs",
    "ketorolac": "NSAIDs",
    "indomethacin": "NSAIDs",
    "naproxen": "NSAIDs",
    "celecoxib": "NSAIDs",
    "etoricoxib": "NSAIDs",
    "aspirin": "NSAIDs",
    "serratiopeptidase": "NSAIDs",
    
    # Antibiotics
    "amoxicillin": "Antibiotics",
    "clavulanic acid": "Antibiotics",
    "ampicillin": "Antibiotics",
    "cloxacillin": "Antibiotics",
    "piperacillin": "Antibiotics",
    "tazobactam": "Antibiotics",
    "cefadroxil": "Antibiotics",
    "cephalexin": "Antibiotics",
    "cefaclor": "Antibiotics",
    "cefuroxime": "Antibiotics",
    "cefixime": "Antibiotics",
    "cefpodoxime": "Antibiotics",
    "ceftriaxone": "Antibiotics",
    "cefotaxime": "Antibiotics",
    "ceftazidime": "Antibiotics",
    "cefepime": "Antibiotics",
    "azithromycin": "Antibiotics",
    "erythromycin": "Antibiotics",
    "clarithromycin": "Antibiotics",
    "roxithromycin": "Antibiotics",
    "ciprofloxacin": "Antibiotics",
    "levofloxacin": "Antibiotics",
    "ofloxacin": "Antibiotics",
    "norfloxacin": "Antibiotics",
    "moxifloxacin": "Antibiotics",
    "gemifloxacin": "Antibiotics",
    "doxycycline": "Antibiotics",
    "minocycline": "Antibiotics",
    "tetracycline": "Antibiotics",
    "gentamicin": "Antibiotics",
    "gentamycin": "Antibiotics",
    "amikacin": "Antibiotics",
    "neomycin": "Antibiotics",
    "streptomycin": "Antibiotics",
    "tobramycin": "Antibiotics",
    "linezolid": "Antibiotics",
    "vancomycin": "Antibiotics",
    "teicoplanin": "Antibiotics",
    "clindamycin": "Antibiotics",
    "metronidazole": "Antibiotics",
    "tinidazole": "Antibiotics",
    "nitrofurantoin": "Antibiotics",
    "cotrimoxazole": "Antibiotics",
    "sulfamethoxazole": "Antibiotics",
    "trimethoprim": "Antibiotics",
    "imipenem": "Antibiotics",
    "meropenem": "Antibiotics",
    "faropenem": "Antibiotics",
    
    # Antifungals
    "fluconazole": "Antifungals",
    "itraconazole": "Antifungals",
    "ketoconazole": "Antifungals",
    "clotrimazole": "Antifungals",
    "miconazole": "Antifungals",
    "voriconazole": "Antifungals",
    "amphotericin b": "Antifungals",
    "terbinafine": "Antifungals",
    "nystatin": "Antifungals",
    "griseofulvin": "Antifungals",
    "caspofungin": "Antifungals",
    "luliconazole": "Antifungals",
    "ciclopirox": "Antifungals",
    
    # Antivirals
    "acyclovir": "Antivirals",
    "valacyclovir": "Antivirals",
    "ganciclovir": "Antivirals",
    "oseltamivir": "Antivirals",
    "ribavirin": "Antivirals",
    "remdesivir": "Antivirals",
    "favipiravir": "Antivirals",
    "tenofovir": "Antivirals",
    "entecavir": "Antivirals",
    "lamivudine": "Antivirals",
    "zidovudine": "Antivirals",
    "efavirenz": "Antivirals",
    "ritonavir": "Antivirals",
    "lopinavir": "Antivirals",
    "atazanavir": "Antivirals",
    "sofosbuvir": "Antivirals",
    "daclatasvir": "Antivirals",
    
    # Antihistamines
    "cetirizine": "Antihistamines",
    "levocetirizine": "Antihistamines",
    "loratadine": "Antihistamines",
    "desloratadine": "Antihistamines",
    "fexofenadine": "Antihistamines",
    "bilastine": "Antihistamines",
    "diphenhydramine": "Antihistamines",
    "chlorpheniramine": "Antihistamines",
    "pheniramine": "Antihistamines",
    "promethazine": "Antihistamines",
    "hydroxyzine": "Antihistamines",
    "cyproheptadine": "Antihistamines",
    
    # Antiallergics
    "montelukast": "Antiallergics",
    "sodium cromoglycate": "Antiallergics",
    "ketotifen": "Antiallergics",
    
    # Antidiabetics
    "metformin": "Antidiabetics",
    "glimepiride": "Antidiabetics",
    "gliclazide": "Antidiabetics",
    "glipizide": "Antidiabetics",
    "glibenclamide": "Antidiabetics",
    "pioglitazone": "Antidiabetics",
    "sitagliptin": "Antidiabetics",
    "vildagliptin": "Antidiabetics",
    "saxagliptin": "Antidiabetics",
    "linagliptin": "Antidiabetics",
    "teneligliptin": "Antidiabetics",
    "dapagliflozin": "Antidiabetics",
    "empagliflozin": "Antidiabetics",
    "canagliflozin": "Antidiabetics",
    "liraglutide": "Antidiabetics",
    "semaglutide": "Antidiabetics",
    "dulaglutide": "Antidiabetics",
    "acarbose": "Antidiabetics",
    "voglibose": "Antidiabetics",
    "insulin": "Antidiabetics",
    "human insulin": "Antidiabetics",
    "insulin glargine": "Antidiabetics",
    "insulin aspart": "Antidiabetics",
    "insulin lispro": "Antidiabetics",
    "insulin degludec": "Antidiabetics",
    
    # Beta-blockers
    "metoprolol": "Beta-blockers",
    "atenolol": "Beta-blockers",
    "propranolol": "Beta-blockers",
    "bisoprolol": "Beta-blockers",
    "carvedilol": "Beta-blockers",
    "nebivolol": "Beta-blockers",
    "labetalol": "Beta-blockers",
    "sotalol": "Beta-blockers",
    "esmolol": "Beta-blockers",
    
    # Calcium Channel Blockers
    "amlodipine": "Calcium Channel Blockers",
    "nifedipine": "Calcium Channel Blockers",
    "felodipine": "Calcium Channel Blockers",
    "cilnidipine": "Calcium Channel Blockers",
    "diltiazem": "Calcium Channel Blockers",
    "verapamil": "Calcium Channel Blockers",
    "lercanidipine": "Calcium Channel Blockers",
    "benidipine": "Calcium Channel Blockers",
    
    # ACE Inhibitors
    "ramipril": "ACE Inhibitors",
    "enalapril": "ACE Inhibitors",
    "lisinopril": "ACE Inhibitors",
    "perindopril": "ACE Inhibitors",
    "benazepril": "ACE Inhibitors",
    "captopril": "ACE Inhibitors",
    "fosinopril": "ACE Inhibitors",
    
    # Angiotensin Receptor Blockers (ARBs)
    "telmisartan": "Angiotensin Receptor Blockers (ARBs)",
    "losartan": "Angiotensin Receptor Blockers (ARBs)",
    "valsartan": "Angiotensin Receptor Blockers (ARBs)",
    "candesartan": "Angiotensin Receptor Blockers (ARBs)",
    "olmesartan": "Angiotensin Receptor Blockers (ARBs)",
    "irbesartan": "Angiotensin Receptor Blockers (ARBs)",
    "azilsartan": "Angiotensin Receptor Blockers (ARBs)",
    
    # Diuretics
    "furosemide": "Diuretics",
    "torsemide": "Diuretics",
    "hydrochlorothiazide": "Diuretics",
    "chlorthalidone": "Diuretics",
    "spironolactone": "Diuretics",
    "eplerenone": "Diuretics",
    "indapamide": "Diuretics",
    
    # Antihypertensives
    "prazosin": "Antihypertensives",
    "doxazosin": "Antihypertensives",
    "clonidine": "Antihypertensives",
    "methyldopa": "Antihypertensives",
    
    # Bronchodilators
    "salbutamol": "Bronchodilators",
    "albuterol": "Bronchodilators",
    "levosalbutamol": "Bronchodilators",
    "levalbuterol": "Bronchodilators",
    "terbutaline": "Bronchodilators",
    "formoterol": "Bronchodilators",
    "salmeterol": "Bronchodilators",
    "vilanterol": "Bronchodilators",
    "ipratropium": "Bronchodilators",
    "tiotropium": "Bronchodilators",
    "glycopyrronium": "Bronchodilators",
    "theophylline": "Bronchodilators",
    "aminophylline": "Bronchodilators",
    "ambroxol": "Bronchodilators",
    "guaiphenesin": "Bronchodilators",
    
    # Corticosteroids
    "prednisolone": "Corticosteroids",
    "methylprednisolone": "Corticosteroids",
    "dexamethasone": "Corticosteroids",
    "betamethasone": "Corticosteroids",
    "hydrocortisone": "Corticosteroids",
    "triamcinolone": "Corticosteroids",
    "deflazacort": "Corticosteroids",
    "fluticasone": "Corticosteroids",
    "budesonide": "Corticosteroids",
    "mometasone": "Corticosteroids",
    "beclomethasone": "Corticosteroids",
    "ciclesonide": "Corticosteroids",
    
    # Anticoagulants
    "heparin": "Anticoagulants",
    "enoxaparin": "Anticoagulants",
    "dalteparin": "Anticoagulants",
    "warfarin": "Anticoagulants",
    "acenocoumarol": "Anticoagulants",
    "phenindione": "Anticoagulants",
    "dabigatran": "Anticoagulants",
    "rivaroxaban": "Anticoagulants",
    "apixaban": "Anticoagulants",
    "edoxaban": "Anticoagulants",
    
    # Antiplatelets
    "clopidogrel": "Antiplatelets",
    "prasugrel": "Antiplatelets",
    "ticagrelor": "Antiplatelets",
    "ticlopidine": "Antiplatelets",
    "dipyridamole": "Antiplatelets",
    
    # Antidepressants
    "sertraline": "Antidepressants",
    "fluoxetine": "Antidepressants",
    "paroxetine": "Antidepressants",
    "citalopram": "Antidepressants",
    "escitalopram": "Antidepressants",
    "fluvoxamine": "Antidepressants",
    "amitriptyline": "Antidepressants",
    "imipramine": "Antidepressants",
    "clomipramine": "Antidepressants",
    "nortriptyline": "Antidepressants",
    "dosulepin": "Antidepressants",
    "duloxetine": "Antidepressants",
    "venlafaxine": "Antidepressants",
    "desvenlafaxine": "Antidepressants",
    "mirtazapine": "Antidepressants",
    "bupropion": "Antidepressants",
    "trazodone": "Antidepressants",
    
    # Antipsychotics
    "olanzapine": "Antipsychotics",
    "risperidone": "Antipsychotics",
    "quetiapine": "Antipsychotics",
    "aripiprazole": "Antipsychotics",
    "haloperidol": "Antipsychotics",
    "chlorpromazine": "Antipsychotics",
    "trifluoperazine": "Antipsychotics",
    "fluphenazine": "Antipsychotics",
    "clozapine": "Antipsychotics",
    "amisulpride": "Antipsychotics",
    "ziprasidone": "Antipsychotics",
    "lurasidone": "Antipsychotics",
    
    # Antiepileptics
    "carbamazepine": "Antiepileptics",
    "oxcarbazepine": "Antiepileptics",
    "sodium valproate": "Antiepileptics",
    "valproic acid": "Antiepileptics",
    "phenytoin": "Antiepileptics",
    "phenobarbitone": "Antiepileptics",
    "gabapentin": "Antiepileptics",
    "pregabalin": "Antiepileptics",
    "levetiracetam": "Antiepileptics",
    "lamotrigine": "Antiepileptics",
    "topiramate": "Antiepileptics",
    "lacosamide": "Antiepileptics",
    "zonisamide": "Antiepileptics",
    
    # Antacids
    "aluminium hydroxide": "Antacids",
    "magnesium hydroxide": "Antacids",
    "calcium carbonate": "Antacids",
    "sodium bicarbonate": "Antacids",
    "magaldrate": "Antacids",
    "simethicone": "Antacids",
    "oxetacaine": "Antacids",
    
    # Proton Pump Inhibitors
    "omeprazole": "Proton Pump Inhibitors",
    "esomeprazole": "Proton Pump Inhibitors",
    "pantoprazole": "Proton Pump Inhibitors",
    "rabeprazole": "Proton Pump Inhibitors",
    "lansoprazole": "Proton Pump Inhibitors",
    "dexlansoprazole": "Proton Pump Inhibitors",
    "ilaprazole": "Proton Pump Inhibitors",
    "ranitidine": "Proton Pump Inhibitors",
    "famotidine": "Proton Pump Inhibitors",
    "cimetidine": "Proton Pump Inhibitors",
    
    # Antiemetics
    "domperidone": "Antiemetics",
    "metoclopramide": "Antiemetics",
    "ondansetron": "Antiemetics",
    "granisetron": "Antiemetics",
    "palonosetron": "Antiemetics",
    "aprepitant": "Antiemetics",
    "fosaprepitant": "Antiemetics",
    "prochlorperazine": "Antiemetics",
    "dimenhydrinate": "Antiemetics",
    
    # Vitamin and Mineral Supplements
    "multivitamin": "Vitamin and Mineral Supplements",
    "vitamin a": "Vitamin and Mineral Supplements",
    "vitamin b": "Vitamin and Mineral Supplements",
    "vitamin c": "Vitamin and Mineral Supplements",
    "vitamin d": "Vitamin and Mineral Supplements",
    "vitamin e": "Vitamin and Mineral Supplements",
    "vitamin k": "Vitamin and Mineral Supplements",
    "folic acid": "Vitamin and Mineral Supplements",
    "methylcobalamin": "Vitamin and Mineral Supplements",
    "calcium": "Vitamin and Mineral Supplements",
    "iron": "Vitamin and Mineral Supplements",
    "ferrous ascorbate": "Vitamin and Mineral Supplements",
    "ferrous sulfate": "Vitamin and Mineral Supplements",
    "zinc": "Vitamin and Mineral Supplements",
    "magnesium": "Vitamin and Mineral Supplements",
    "calcitriol": "Vitamin and Mineral Supplements",
    "cholecalciferol": "Vitamin and Mineral Supplements",
    "ascorbic acid": "Vitamin and Mineral Supplements",
    "thiamine": "Vitamin and Mineral Supplements",
    "riboflavin": "Vitamin and Mineral Supplements",
    "pyridoxine": "Vitamin and Mineral Supplements",
    "cyanocobalamin": "Vitamin and Mineral Supplements",
    "mecobalamin": "Vitamin and Mineral Supplements",
    "niacinamide": "Vitamin and Mineral Supplements",
    "biotin": "Vitamin and Mineral Supplements",
    "vitamin b-complex": "Vitamin and Mineral Supplements",
    "vitamin b complex": "Vitamin and Mineral Supplements",
    
    # Hormonal Drugs
    "thyroxine": "Hormonal Drugs",
    "levothyroxine": "Hormonal Drugs",
    "progesterone": "Hormonal Drugs",
    "dydrogesterone": "Hormonal Drugs",
    "medroxyprogesterone": "Hormonal Drugs",
    "estrogen": "Hormonal Drugs",
    "estradiol": "Hormonal Drugs",
    "testosterone": "Hormonal Drugs",
    "norethisterone": "Hormonal Drugs",
    "levonorgestrel": "Hormonal Drugs",
    "desogestrel": "Hormonal Drugs",
    "ethinylestradiol": "Hormonal Drugs",
    "octreotide": "Hormonal Drugs",
    "cabergoline": "Hormonal Drugs",
    "clomifene": "Hormonal Drugs",
    "tamoxifen": "Hormonal Drugs",
    "letrozole": "Hormonal Drugs",
    "anastrozole": "Hormonal Drugs",
    
    # Vaccines
    "bcg vaccine": "Vaccines",
    "hepatitis b vaccine": "Vaccines",
    "polio vaccine": "Vaccines",
    "opv": "Vaccines",
    "ipv": "Vaccines",
    "dpt vaccine": "Vaccines",
    "rotavirus vaccine": "Vaccines",
    "measles vaccine": "Vaccines",
    "mmr vaccine": "Vaccines",
    "typhoid vaccine": "Vaccines",
    "tetanus toxoid": "Vaccines",
    "tetanus vaccine": "Vaccines",
    "influenza vaccine": "Vaccines",
    "covid-19 vaccine": "Vaccines",
    "covishield": "Vaccines",
    "covaxin": "Vaccines",
    "rabies vaccine": "Vaccines",
    "varicella vaccine": "Vaccines",
    "hpv vaccine": "Vaccines",
    "meningococcal vaccine": "Vaccines",
    "pneumococcal vaccine": "Vaccines",
    "covishield vaccine": "Vaccines",
    "covaxin vaccine": "Vaccines",
    
    # Statins / Lipid-lowering Drugs
    "atorvastatin": "Statins / Lipid-lowering Drugs",
    "rosuvastatin": "Statins / Lipid-lowering Drugs",
    "simvastatin": "Statins / Lipid-lowering Drugs",
    "pravastatin": "Statins / Lipid-lowering Drugs",
    "pitavastatin": "Statins / Lipid-lowering Drugs",
    "lovastatin": "Statins / Lipid-lowering Drugs",
    "fluvastatin": "Statins / Lipid-lowering Drugs",
    "ezetimibe": "Statins / Lipid-lowering Drugs",
    "fenofibrate": "Statins / Lipid-lowering Drugs",
    "gemfibrozil": "Statins / Lipid-lowering Drugs",

    # Benzodiazepines
    "alprazolam": "Benzodiazepines",
    "diazepam": "Benzodiazepines",
    "lorazepam": "Benzodiazepines",
    "clonazepam": "Benzodiazepines",
    "midazolam": "Benzodiazepines",
    "temazepam": "Benzodiazepines",
    "clobazam": "Benzodiazepines",

    # Others
    "liv.52": "Others",
    "liv 52": "Others",
    "phenylephrine": "Others",
    "dextromethorphan": "Others",
}

# Therapeutic categories sorted by clinical priority for ADR reporting
CATEGORY_PRIORITY = [
    "Vaccines",
    "Anticoagulants",
    "Antiplatelets",
    "Antibiotics",
    "Antifungals",
    "Antivirals",
    "Antidiabetics",
    "Beta-blockers",
    "Calcium Channel Blockers",
    "ACE Inhibitors",
    "Angiotensin Receptor Blockers (ARBs)",
    "Diuretics",
    "Antihypertensives",
    "Statins / Lipid-lowering Drugs",
    "Corticosteroids",
    "NSAIDs",
    "Analgesics",
    "Antipyretics",
    "Benzodiazepines",
    "Antiepileptics",
    "Antipsychotics",
    "Antidepressants",
    "Hormonal Drugs",
    "Bronchodilators",
    "Antihistamines",
    "Antiallergics",
    "Proton Pump Inhibitors",
    "Antiemetics",
    "Antacids",
    "Vitamin and Mineral Supplements",
    "Others"
]

def string_similarity(s1, s2):
    """Calculates Levenshtein similarity between two strings."""
    s1 = s1.lower().strip()
    s2 = s2.lower().strip()
    if s1 == s2:
        return 1.0
    if not s1 or not s2:
        return 0.0
        
    m, n = len(s1), len(s2)
    if m > n:
        s1, s2 = s2, s1
        m, n = n, m
        
    current_row = list(range(m + 1))
    for i in range(1, n + 1):
        previous_row = current_row
        current_row = [i] + [0] * m
        for j in range(1, m + 1):
            add = previous_row[j] + 1
            delete = current_row[j - 1] + 1
            change = previous_row[j - 1]
            if s1[j - 1] != s2[i - 1]:
                change += 1
            current_row[j] = min(add, delete, change)
            
    lev_dist = current_row[m]
    max_len = max(m, n)
    return 1.0 - (lev_dist / max_len)

def clean_drug_name(name):
    """Cleans drug name input by removing strengths and dosage forms."""
    if not name:
        return ""
    name = name.lower().strip()
    
    # Remove common dosage forms
    dosage_forms = [
        r'\btablet\b', r'\btablets\b', r'\bcapsule\b', r'\bcapsules\b', r'\bcaps\b', 
        r'\binjection\b', r'\binj\b', r'\bsyrup\b', r'\bsuspension\b', r'\bdrops\b',
        r'\bcream\b', r'\bointment\b', r'\bgel\b', r'\binhaler\b', r'\brotacap\b', r'\brotacaps\b'
    ]
    for pattern in dosage_forms:
        name = re.sub(pattern, ' ', name)
        
    # Remove strengths (e.g., 500mg, 650 mg, 10mcg, 1g) and frequency codes
    name = re.sub(r'\b\d+\s*(mg|g|mcg|ml|od|bd|tds|hs|prn)\b', ' ', name)
    
    # Remove stand-alone numbers except when part of specific brand names like Liv.52 or 1-AL
    if 'liv.52' not in name and 'liv 52' not in name and '1-al' not in name and '1 al' not in name:
        name = re.sub(r'\b\d+\b', ' ', name)
        
    # Remove extra spaces
    name = re.sub(r'\s+', ' ', name).strip()
    return name

def find_closest_match(term, candidates, threshold=0.82):
    """Finds the closest string match using Levenshtein distance."""
    best_candidate = None
    best_score = 0.0
    for cand in candidates:
        if len(cand) < 3 and term != cand:
            continue
        score = string_similarity(term, cand)
        if score > best_score:
            best_score = score
            best_candidate = cand
            
    if best_score >= threshold:
        return best_candidate, best_score
    return None, 0.0

def detect_drug_category(drug_name):
    """Automatically detects drug category based on predefined lists, supporting generic and brand names,
    combination medicines, spelling mistake tolerance, and priority ranking.
    """
    if not drug_name:
        return "Others (Low Confidence)"
        
    cleaned_name = clean_drug_name(drug_name)
    if not cleaned_name:
        return "Others (Low Confidence)"
        
    # Split combination drugs on common separators: +, &, and, with, /
    ingredients = re.split(r'\s*(?:\+|\band\b|&|/|\bwith\b)\s*', cleaned_name)
    
    detected_categories = []
    
    for ingredient in ingredients:
        ingredient = ingredient.strip()
        if not ingredient:
            continue
            
        resolved_generic = None
        
        # 1. Exact check in BRAND_TO_GENERIC
        if ingredient in BRAND_TO_GENERIC:
            resolved_generic = BRAND_TO_GENERIC[ingredient]
        else:
            # 2. Spelling check in BRAND_TO_GENERIC (high threshold for brand names)
            best_brand, brand_score = find_closest_match(ingredient, BRAND_TO_GENERIC.keys(), threshold=0.85)
            if best_brand:
                resolved_generic = BRAND_TO_GENERIC[best_brand]
                
        # If it was a brand name, it might have mapped to a combination (e.g., "ibuprofen + paracetamol")
        sub_ingredients = []
        if resolved_generic:
            sub_ingredients = [x.strip() for x in re.split(r'\s*(?:\+|\band\b|&|/|\bwith\b)\s*', resolved_generic)]
        else:
            sub_ingredients = [ingredient]
            
        for sub_ing in sub_ingredients:
            # 3. Exact check in GENERIC_TO_CATEGORY
            if sub_ing in GENERIC_TO_CATEGORY:
                detected_categories.append(GENERIC_TO_CATEGORY[sub_ing])
                continue
                
            # 4. Spelling check in GENERIC_TO_CATEGORY
            best_gen, gen_score = find_closest_match(sub_ing, GENERIC_TO_CATEGORY.keys(), threshold=0.80)
            if best_gen:
                detected_categories.append(GENERIC_TO_CATEGORY[best_gen])
                continue
                
            # 5. Substring / Word overlap check in GENERIC_TO_CATEGORY
            matched_category = None
            sub_ing_words = set(sub_ing.split())
            for gen_name, cat in GENERIC_TO_CATEGORY.items():
                gen_words = set(gen_name.split())
                if sub_ing_words.intersection(gen_words):
                    overlapping_words = sub_ing_words.intersection(gen_words)
                    if any(len(w) >= 4 for w in overlapping_words):
                        matched_category = cat
                        break
            
            if matched_category:
                detected_categories.append(matched_category)
            else:
                detected_categories.append("Others (Low Confidence)")
                
    if not detected_categories:
        return "Others (Low Confidence)"
        
    # Resolve multiple categories using priority ranking
    best_category = None
    best_priority_index = len(CATEGORY_PRIORITY) + 2
    
    for cat in detected_categories:
        if cat == "Others (Low Confidence)":
            priority_index = len(CATEGORY_PRIORITY) + 1
        elif cat in CATEGORY_PRIORITY:
            priority_index = CATEGORY_PRIORITY.index(cat)
        else:
            priority_index = CATEGORY_PRIORITY.index("Others")
            
        if priority_index < best_priority_index:
            best_priority_index = priority_index
            best_category = cat
            
    if best_category == "Others (Low Confidence)":
        return "Others (Low Confidence)"
        
    return best_category

def generate_report_pdf(report_data):
    """Generates a highly structured, professional PDF file for an ADR report in WHO-PvPI format."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_margins(15, 15, 15)
    
    # Draw a thin decorative border around the page
    pdf.set_draw_color(60, 60, 60)
    pdf.set_line_width(0.5)
    pdf.rect(10, 10, 190, 277)
    
    # Title Banner
    pdf.set_fill_color(33, 158, 188) # Premium teal color matching the app theme
    pdf.rect(15, 15, 180, 15, style='F')
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", style="B", size=13)
    pdf.cell(180, 15, txt="ADVERSE DRUG REACTION REPORT (PvPI STYLE)", ln=True, align='C')
    pdf.ln(5)
    
    pdf.set_text_color(0, 0, 0)
    
    # Helper functions to print section headers
    def print_section_header(title):
        pdf.set_font("Helvetica", style="B", size=10)
        pdf.set_fill_color(240, 240, 240)
        pdf.set_draw_color(200, 200, 200)
        pdf.cell(180, 8, txt=f" {title}", ln=True, fill=True, border='B')
        pdf.ln(3)

    # Helper function to print key-value rows side-by-side safely
    def print_row(label1, val1, label2=None, val2=None):
        pdf.set_font("Helvetica", style="B", size=9)
        pdf.cell(35, 7, txt=f"{label1}:", ln=False)
        pdf.set_font("Helvetica", size=9)
        
        safe_val1 = str(val1) if val1 is not None and val1 != "" else "N/A"
        safe_val1 = safe_val1.encode('latin-1', 'replace').decode('latin-1')
        
        if label2:
            pdf.cell(55, 7, txt=safe_val1, ln=False)
            pdf.set_font("Helvetica", style="B", size=9)
            pdf.cell(35, 7, txt=f"{label2}:", ln=False)
            pdf.set_font("Helvetica", size=9)
            
            safe_val2 = str(val2) if val2 is not None and val2 != "" else "N/A"
            safe_val2 = safe_val2.encode('latin-1', 'replace').decode('latin-1')
            pdf.cell(55, 7, txt=safe_val2, ln=True)
        else:
            pdf.multi_cell(145, 7, txt=safe_val1)

    # 1. Report Metadata
    print_row("Report ID", report_data.get('report_id', 'New'), "Submission Date", report_data.get('submission_timestamp', 'N/A'))
    pdf.ln(2)
    
    # 2. Section A: Patient Information
    print_section_header("1. PATIENT INFORMATION")
    print_row("Patient Name", report_data.get('patient_name'), "Age / Gender", f"{report_data.get('age', 'N/A')} yrs / {report_data.get('gender', 'N/A')}")
    print_row("Weight", f"{report_data.get('weight_kg', 'N/A')} kg" if report_data.get('weight_kg') else "N/A", "Mobile Number", report_data.get('patient_mobile'))
    print_row("Email Address", report_data.get('patient_email'))
    pdf.ln(4)
    
    # 3. Section B: Suspected Medicine Information
    print_section_header("2. SUSPECTED DRUG(S) INFORMATION")
    print_row("Drug Name", report_data.get('drug_name'), "Therapeutic Category", report_data.get('final_drug_category'))
    print_row("Strength / Dose", report_data.get('strength'), "Frequency", report_data.get('frequency'))
    print_row("Route of Admin", report_data.get('route_of_administration'), "Indication", report_data.get('indication'))
    print_row("Batch Number", report_data.get('batch_number'), "Expiry Date", report_data.get('expiry_date'))
    print_row("Date Started", report_data.get('medicine_start_date'), "Date Stopped", report_data.get('medicine_stop_date'))
    pdf.ln(4)
    
    # 4. Section C: Adverse Event Information
    print_section_header("3. ADVERSE DRUG REACTION DETAILS")
    print_row("Reaction Started", report_data.get('reaction_start_date'), "Reaction Ended", report_data.get('reaction_end_date'))
    print_row("Action Taken", report_data.get('action_taken'))
    
    # Long text for reaction description
    pdf.set_font("Helvetica", style="B", size=9)
    pdf.cell(180, 6, txt="Adverse Reaction Description:", ln=True)
    pdf.set_font("Helvetica", size=9)
    desc = report_data.get('reaction_description', 'N/A')
    desc = str(desc).encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(180, 5, txt=desc, border=1)
    pdf.ln(4)
    
    # 5. Section D: Physician / Healthcare Professional Details
    print_section_header("4. ASSOCIATED PHYSICIAN DETAILS")
    print_row("Physician Name", report_data.get('physician_name'), "Physician Contact", report_data.get('physician_contact'))
    pdf.ln(15)
    
    # Footer Signatures
    pdf.set_draw_color(150, 150, 150)
    pdf.line(15, 260, 75, 260)
    pdf.line(135, 260, 195, 260)
    
    pdf.set_font("Helvetica", style="I", size=8)
    pdf.set_xy(15, 261)
    pdf.cell(60, 5, txt="Reporter / Patient Signature", ln=False, align='C')
    pdf.set_xy(135, 261)
    pdf.cell(60, 5, txt="Reviewing Pharmacist Signature", ln=True, align='C')
    
    # Save to a temporary file
    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, f"ADR_Report_{report_data.get('report_id', 'new')}.pdf")
    pdf.output(file_path)
    
    return file_path

MONTHS_MAP = {
    # English
    "january": 1, "jan": 1,
    "february": 2, "feb": 2,
    "march": 3, "mar": 3,
    "april": 4, "apr": 4,
    "may": 5,
    "june": 6, "jun": 6,
    "july": 7, "jul": 7,
    "august": 8, "aug": 8,
    "september": 9, "sep": 9, "sept": 9,
    "october": 10, "oct": 10,
    "november": 11, "nov": 11,
    "december": 12, "dec": 12,
    
    # Hindi / Marathi
    "जनवरी": 1, "जानेवारी": 1, "जनवर": 1,
    "फरवरी": 2, "फेब्रुवारी": 2, "फ़रवरी": 2,
    "मार्च": 3,
    "अप्रैल": 4, "एप्रिल": 4,
    "मई": 5, "मे": 5,
    "जून": 6,
    "जुलाई": 7, "जुलै": 7,
    "अगस्त": 8, "ऑगस्ट": 8,
    "सितंबर": 9, "सप्टेंबर": 9, "सितम्बर": 9,
    "अक्टूबर": 10, "ऑक्टोबर": 10, "अक्टुबर": 10,
    "नवंबर": 11, "नोव्हेंबर": 11, "नवम्बर": 11,
    "दिसंबर": 12, "डिसेंबर": 12, "दिसम्बर": 12
}

def normalize_date_string(date_str):
    """Normalizes spoken or written dates in English, Hindi, and Marathi to YYYY-MM-DD."""
    import datetime
    if not date_str:
        return None
        
    s = str(date_str).strip().lower()
    
    # Check if the string is already a formatted ISO date or a special ongoing/taking/skip status
    special_terms = ["still taking", "still ongoing", "unknown", "none", "skip"]
    if any(term in s for term in special_terms):
        return date_str
        
    # Standardize Devanagari numbers to English digits
    devanagari_to_english = {
        '०': '0', '१': '1', '२': '2', '३': '3', '४': '4',
        '५': '5', '६': '6', '७': '7', '८': '8', '९': '9'
    }
    for d, e in devanagari_to_english.items():
        s = s.replace(d, e)
        
    # Strip suffixes like "st", "nd", "rd", "th" from day numbers (e.g. 11th -> 11)
    s = re.sub(r'\b(\d+)(st|nd|rd|th)\b', r'\1', s)
        
    # Standardize separators to spaces
    s = re.sub(r'[,.\-\/]', ' ', s)
    s = re.sub(r'\s+', ' ', s).strip()
    
    parts = s.split()
    day, month, year = None, None, None
    
    try:
        if len(parts) == 3:
            # Format: YYYY MM DD (e.g. 2026 06 10)
            if len(parts[0]) == 4 and parts[0].isdigit():
                year = int(parts[0])
                if parts[1].isdigit() and parts[2].isdigit():
                    month = int(parts[1])
                    day = int(parts[2])
            # Format: DD MM YYYY or MM DD YYYY
            elif len(parts[2]) == 4 and parts[2].isdigit():
                year = int(parts[2])
                # Case 1: Month name in middle (e.g. 10 June 2026 / १० जून २०२६)
                if parts[1] in MONTHS_MAP:
                    month = MONTHS_MAP[parts[1]]
                    if parts[0].isdigit():
                        day = int(parts[0])
                # Case 2: Month name at start (e.g. June 10 2026)
                elif parts[0] in MONTHS_MAP:
                    month = MONTHS_MAP[parts[0]]
                    if parts[1].isdigit():
                        day = int(parts[1])
                # Case 3: All digits (default to DD MM YYYY)
                elif parts[0].isdigit() and parts[1].isdigit():
                    day = int(parts[0])
                    month = int(parts[1])
            # Format: DD MM YY (e.g. 10 06 26)
            elif len(parts[2]) == 2 and parts[2].isdigit():
                year = 2000 + int(parts[2])
                if parts[1] in MONTHS_MAP:
                    month = MONTHS_MAP[parts[1]]
                    if parts[0].isdigit():
                        day = int(parts[0])
                elif parts[0].isdigit() and parts[1].isdigit():
                    day = int(parts[0])
                    month = int(parts[1])
                    
        elif len(parts) == 2:
            # Format: MM YYYY or Month YYYY (e.g. 12/2028 or June 2026)
            # Or formatted like "106 2026" / "1006 2026" where space/separator is missing between DD and MM
            if parts[1].isdigit():
                if len(parts[1]) == 4:
                    year = int(parts[1])
                else:
                    year = 2000 + int(parts[1])
                
                if parts[0] in MONTHS_MAP:
                    month = MONTHS_MAP[parts[0]]
                    day = 1
                elif parts[0].isdigit():
                    if len(parts[0]) == 3:
                        # Split 3 digits into DD and M (assuming DD/M because of Indian clinical standard)
                        # e.g., 106 -> day 10, month 6
                        # e.g., 211 -> day 21, month 1
                        d_part = int(parts[0][0:2])
                        m_part = int(parts[0][2])
                        if 1 <= d_part <= 31 and 1 <= m_part <= 12:
                            day = d_part
                            month = m_part
                        else:
                            # Try D and MM
                            d_part = int(parts[0][0])
                            m_part = int(parts[0][1:3])
                            if 1 <= d_part <= 31 and 1 <= m_part <= 12:
                                day = d_part
                                month = m_part
                    elif len(parts[0]) == 4:
                        # Split 4 digits into DD and MM
                        # e.g., 1006 -> day 10, month 6
                        d_part = int(parts[0][0:2])
                        m_part = int(parts[0][2:4])
                        if 1 <= d_part <= 31 and 1 <= m_part <= 12:
                            day = d_part
                            month = m_part
                    else:
                        month = int(parts[0])
                        day = 1
                        
        elif len(parts) == 1 and parts[0].isdigit():
            # Format: DDMMYYYY or YYYYMMDD
            if len(parts[0]) == 8:
                # Check if first 4 digits form a reasonable year (1900 to 2100)
                y_candidate_1 = int(parts[0][0:4])
                y_candidate_2 = int(parts[0][4:8])
                if 1900 <= y_candidate_1 <= 2100:
                    year = y_candidate_1
                    month = int(parts[0][4:6])
                    day = int(parts[0][6:8])
                elif 1900 <= y_candidate_2 <= 2100:
                    year = y_candidate_2
                    day = int(parts[0][0:2])
                    month = int(parts[0][2:4])
            # Format: YYYYMM (e.g. 202606)
            elif len(parts[0]) == 6:
                year = int(parts[0][0:4])
                month = int(parts[0][4:6])
                day = 1
                
        if year and month and day:
            # Validate values form a real calendar date
            dt = datetime.date(year, month, day)
            return f"{dt.year:04d}-{dt.month:02d}-{dt.day:02d}"
    except Exception:
        pass
        
    return None
