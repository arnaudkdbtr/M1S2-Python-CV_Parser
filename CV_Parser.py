import requests
import json
from pathlib import Path
import PyPDF2
import re
import os
import sys

# Clé API Mistral
MISTRAL_API_KEY = "VOTRE_CLE"

# URL de l'API Mistral
API_URL = "https://api.mistral.ai/v1/chat/completions"

# Chemin d'accès au fichier PDF
chemin_pdf = None
if len(sys.argv) > 1:
    chemin_pdf = Path(sys.argv[1])
else:
    chemin_pdf = Path(r"C:\Users\DIRECTORY\CV.pdf")


def extraire_texte_pdf(chemin_pdf):
    """
    Extrait le texte d'un fichier PDF
    
    Args:
        chemin_pdf (Path): Chemin vers le fichier PDF
        
    Returns:
        str: Texte extrait du PDF
    """
    try:
        texte = ""
        with open(chemin_pdf, 'rb') as fichier:
            lecteur_pdf = PyPDF2.PdfReader(fichier)
            for page in lecteur_pdf.pages:
                texte += page.extract_text() + "\n"
        return texte
    except Exception as e:
        print(f"Erreur lors de l'extraction du texte du PDF: {e}")
        return None


def generer_json_avec_mistral(texte_cv):
    """
    Envoie le texte du CV à l'API Mistral pour générer directement le JSON
    
    Args:
        texte_cv (str): Texte du CV extrait du PDF
        
    Returns:
        str: JSON généré par Mistral
    """
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {MISTRAL_API_KEY}"
    }
    
    # Liste des compétences techniques et soft skills à rechercher pour aider le modèle
    liste_competences = """
    Exemples de compétences techniques à identifier (UNIQUEMENT les outils concrets et langages de programmation):
    
    # Langages de programmation
    Python, R, Java, C, C++, C#, JavaScript, TypeScript, PHP, Ruby, Swift, Kotlin, Go, Rust, SQL, Scala, Perl, Shell, Bash, PowerShell, MATLAB, VBA
    
    # Data Science et ML (outils uniquement)
    TensorFlow, PyTorch, Keras, Scikit-learn, Pandas, NumPy, SciPy, NLTK, spaCy, Matplotlib, Seaborn
    
    # Web et Frontend
    HTML, CSS, Bootstrap, React, Angular, Vue.js, jQuery, REST API, GraphQL, Node.js, Express
    
    # Bases de données
    MySQL, PostgreSQL, SQLite, Oracle, MongoDB, Redis, Elasticsearch, NoSQL, SQL Server, MariaDB
    
    # DevOps et Cloud
    AWS, Azure, GCP, Docker, Kubernetes, Git, GitHub, GitLab, CI/CD, Jenkins, Linux, Unix, Windows, MacOS
    
    # Bureautique et outils
    Microsoft Office, Microsoft 365, Office 365, Suite Office, Excel, Word, PowerPoint, Access, Outlook, OneNote, SharePoint, OneDrive, Teams, Microsoft Teams, Microsoft Exchange, Dynamics 365, Visio, Publisher, Google Workspace, Google Docs, Google Sheets, Google Slides, LibreOffice, OpenOffice, Tableau, Power BI, SAP, Salesforce, Jira, Confluence, Trello, MS Project, Adobe Acrobat, Adobe PDF
    
    # Autres outils techniques
    LaTeX, RStudio, Jupyter, Orange, SAS, SPSS
    
    ATTENTION: N'inclus PAS les domaines de connaissances ou sujets théoriques comme compétences techniques.
    Par exemple, n'inclus PAS: Économie, Microéconomie, Macroéconomie, Comptabilité, Finance, Droit, Mathématiques, 
    Statistiques théoriques, Machine Learning théorique, etc. 
    
    Inclus UNIQUEMENT les outils et langages concrets que la personne sait utiliser.
    
    IMPORTANT: Assure-toi d'inclure tous les logiciels de la suite Microsoft Office ou Microsoft 365 mentionnés dans le CV, comme Excel, Word, PowerPoint, Outlook, OneNote, etc. 
    Ces compétences bureautiques sont essentielles et doivent être listées individuellement en plus de la mention globale "Microsoft Office" ou "Microsoft 365" si elle est présente.
    
    Exemples de soft skills à identifier:
    Communication, leadership, travail d'équipe, résolution de problèmes, gestion de projet, organisation, autonomie, adaptabilité, créativité, esprit critique, négociation, intelligence émotionnelle, gestion du temps, gestion du stress, écoute active, empathie, flexibilité, prise de décision, persuasion, présentation, prise de parole en public
    
    Exemples de certifications:
    Permis B, Permis BVA, TOEIC, TOEFL, IELTS, Cambridge Certificate, DELF, DALF, HSK, PIX, Google Analytics, Certification Microsoft, Certification Microsoft Office Specialist (MOS), Certification Microsoft 365, Certification Azure, AWS, Google Cloud, ITIL, PMP, PRINCE2
    """
    
    # Construire le prompt pour Mistral
    prompt = f"""
    Voici le texte complet d'un CV extrait d'un fichier PDF. Analyse-le et convertis-le directement en JSON avec la structure suivante:

    ```json
    {{
      "prenom_nom": "string",
      "email": "string",
      "telephone": "string",
      "linkedin": "string (seulement le nom d'utilisateur, pas l'URL complète, ou vide si non présent)",
      "github": "string (seulement le nom d'utilisateur, pas l'URL complète, ou vide si non présent)",
      "competences_techniques": [
        "compétence technique 1",
        "compétence technique 2"
      ],
      "soft_skills": [
        "soft skill 1",
        "soft skill 2"
      ],
      "langues": [
        "string (langue et niveau)"
      ],
      "certifications": [
        "string (certification 1)",
        "string (certification 2)"
      ],
      "formation": [
        {{
          "titre": "string (diplôme et spécialité)",
          "etablissement": "string (nom de l'école/université)",
          "periode": "string (dates de début et fin)",
          "details": [
            "string (enseignements, mentions, etc.)"
          ]
        }}
      ],
      "experience": [
        {{
          "titre": "string (intitulé du poste)",
          "entreprise": "string (nom de l'entreprise)",
          "lieu": "string (ville/pays ou télétravail)",
          "periode": "string (dates de début et fin)",
          "details": [
            "string (responsabilités, accomplissements)"
          ]
        }}
      ]
    }}
    ```

    Instructions spéciales:
    - Inclus TOUJOURS les champs "linkedin" et "github" dans le JSON, même s'ils sont vides ("").
    - Pour LinkedIn, si tu trouves une URL comme "linkedin.com/in/nom-utilisateur", n'inclus que "nom-utilisateur". Si tu trouves directement "/linkedin-innom-utilisateur", n'inclus que "nom-utilisateur".
    - Pour GitHub, si tu trouves une URL comme "github.com/nom-utilisateur", n'inclus que "nom-utilisateur". Si tu trouves directement "/githubnom-utilisateur", n'inclus que "nom-utilisateur".
    - Si aucun profil LinkedIn ou GitHub n'est mentionné dans le CV, laisse ces champs vides: "linkedin": "", "github": "".
    
    - IMPORTANT: Pour les compétences techniques, inclus UNIQUEMENT les langages de programmation, logiciels, et outils concrets.
      * Ne pas inclure dans cette section les domaines de connaissances théoriques comme l'économie, la finance, les mathématiques, etc.
      * Limite-toi aux compétences techniques concrètes et opérationnelles (langages, logiciels, frameworks, etc.)
      * Sois particulièrement attentif à identifier tous les logiciels bureautiques mentionnés comme Excel, Word, PowerPoint, Microsoft Office, Microsoft 365, etc.
    
    - Identifie et liste toutes les soft skills (compétences personnelles, interpersonnelles et transversales).
    
    - CERTIFICATIONS:
      * Recherche et inclus toutes les certifications mentionnées dans le CV.
      * Permis de conduire (B, BVA, etc.), certifications de langue (TOEIC, TOEFL, etc.), certifications informatiques (PIX, Microsoft Office Specialist, etc.)
      * Si aucune certification n'est mentionnée, laisse la liste vide: []
    
    - Tu dois ABSOLUMENT inclure les champs "competences_techniques", "soft_skills" et "certifications" dans le JSON final, même s'ils sont vides.

    {liste_competences}

    Texte du CV:
    {texte_cv}

    Retourne UNIQUEMENT le JSON sans aucun autre commentaire. Assure-toi que le format est valide.
    """
    
    # Préparer la requête pour l'API
    payload = {
        "model": "mistral-small-latest",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2  # Température plus basse pour respecter plus strictement le format demandé
    }
    
    try:
        # Envoyer la requête à l'API Mistral
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        
        # Extraire la réponse
        resultat = response.json()
        reponse_mistral = resultat["choices"][0]["message"]["content"]
        
        # Extraire uniquement le JSON de la réponse (au cas où Mistral ajoute des commentaires)
        json_pattern = r"```json\s*([\s\S]*?)\s*```|^\s*(\{[\s\S]*\})\s*$"
        match = re.search(json_pattern, reponse_mistral)
        
        if match:
            json_str = match.group(1) or match.group(2)
            
            # Vérifier que le JSON est valide
            try:
                json_obj = json.loads(json_str)
                
                # Post-traitement pour s'assurer que les compétences bureautiques sont correctement identifiées
                if "competences_techniques" in json_obj:
                    # Liste des termes bureautiques à rechercher dans le texte du CV (insensible à la casse)
                    bureautique_terms = [
                        "Microsoft Office", "MS Office", "Office", "Suite Office", 
                        "Microsoft 365", "Office 365", "M365", "O365",
                        "Excel", "Word", "PowerPoint", "PPT", "Access", "Outlook",
                        "OneNote", "SharePoint", "OneDrive", "Teams", "Microsoft Teams",
                        "Visio", "Publisher", "Microsoft Exchange"
                    ]
                    
                    # Vérifier si ces termes sont dans le texte du CV mais pas dans les compétences
                    found_terms = set()
                    for term in bureautique_terms:
                        pattern = re.compile(r'\b' + re.escape(term) + r'\b', re.IGNORECASE)
                        if pattern.search(texte_cv):
                            # Normaliser le nom de la compétence (première lettre de chaque mot en majuscule)
                            normalized_term = ' '.join(word.capitalize() for word in term.split())
                            found_terms.add(normalized_term)
                    
                    # Ajouter les termes trouvés qui ne sont pas déjà dans les compétences
                    for term in found_terms:
                        if not any(comp.lower() == term.lower() for comp in json_obj["competences_techniques"]):
                            json_obj["competences_techniques"].append(term)
                
                # Vérifier que tous les champs requis sont présents, sinon les ajouter
                champs_requis = ["linkedin", "github", "competences_techniques", "soft_skills", "certifications"]
                for champ in champs_requis:
                    if champ not in json_obj:
                        if champ in ["linkedin", "github"]:
                            json_obj[champ] = ""
                        elif champ in ["competences_techniques", "soft_skills", "certifications"]:
                            json_obj[champ] = []
                
                return json.dumps(json_obj, ensure_ascii=False, indent=2)
            except json.JSONDecodeError as e:
                print(f"Erreur lors du décodage du JSON: {e}")
                print(f"JSON reçu: {json_str}")
                return None
        else:
            # Si Mistral n'a pas utilisé de balises de code, essayons de parser directement
            try:
                json_obj = json.loads(reponse_mistral)
                
                # Post-traitement pour s'assurer que les compétences bureautiques sont correctement identifiées
                if "competences_techniques" in json_obj:
                    # Liste des termes bureautiques à rechercher dans le texte du CV (insensible à la casse)
                    bureautique_terms = [
                        "Microsoft Office", "MS Office", "Office", "Suite Office", 
                        "Microsoft 365", "Office 365", "M365", "O365",
                        "Excel", "Word", "PowerPoint", "PPT", "Access", "Outlook",
                        "OneNote", "SharePoint", "OneDrive", "Teams", "Microsoft Teams",
                        "Visio", "Publisher", "Microsoft Exchange"
                    ]
                    
                    # Vérifier si ces termes sont dans le texte du CV mais pas dans les compétences
                    found_terms = set()
                    for term in bureautique_terms:
                        pattern = re.compile(r'\b' + re.escape(term) + r'\b', re.IGNORECASE)
                        if pattern.search(texte_cv):
                            # Normaliser le nom de la compétence (première lettre de chaque mot en majuscule)
                            normalized_term = ' '.join(word.capitalize() for word in term.split())
                            found_terms.add(normalized_term)
                    
                    # Ajouter les termes trouvés qui ne sont pas déjà dans les compétences
                    for term in found_terms:
                        if not any(comp.lower() == term.lower() for comp in json_obj["competences_techniques"]):
                            json_obj["competences_techniques"].append(term)
                
                # Vérifier que tous les champs requis sont présents, sinon les ajouter
                champs_requis = ["linkedin", "github", "competences_techniques", "soft_skills", "certifications"]
                for champ in champs_requis:
                    if champ not in json_obj:
                        if champ in ["linkedin", "github"]:
                            json_obj[champ] = ""
                        elif champ in ["competences_techniques", "soft_skills", "certifications"]:
                            json_obj[champ] = []
                
                return json.dumps(json_obj, ensure_ascii=False, indent=2)
            except json.JSONDecodeError:
                print("Impossible d'extraire un JSON valide de la réponse Mistral")
                print(f"Réponse reçue: {reponse_mistral}")
                return None
    
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la communication avec l'API Mistral: {e}")
        return None


def enregistrer_json(json_str, chemin_pdf):
    """
    Enregistre le JSON dans un fichier au même emplacement que le PDF
    
    Args:
        json_str (str): JSON à enregistrer
        chemin_pdf (Path): Chemin vers le fichier PDF source
    """
    try:
        # Créer le chemin pour le fichier JSON basé sur le chemin du PDF
        nom_fichier = chemin_pdf.stem  # Obtient le nom du fichier sans extension
        chemin_json = chemin_pdf.parent / f"{nom_fichier}.json"
        
        with open(chemin_json, 'w', encoding='utf-8') as fichier:
            fichier.write(json_str)
        print(f"JSON enregistré dans {chemin_json}")
    except Exception as e:
        print(f"Erreur lors de l'enregistrement du JSON: {e}")


def main():
    print("=" * 60)
    print("CONVERSION DE CV PDF VERS JSON AVEC MISTRAL AI")
    print("=" * 60)
    
    # Vérifier si le fichier PDF existe
    if not chemin_pdf.exists():
        print(f"Erreur: Le fichier {chemin_pdf} n'existe pas.")
        return
    
    # Étape 1: Extraire le texte du PDF
    print(f"Extraction du texte du PDF: {chemin_pdf}")
    texte_cv = extraire_texte_pdf(chemin_pdf)
    if not texte_cv:
        print("Échec de l'extraction du texte. Arrêt du programme.")
        return
    
    # Étape 2: Envoyer à Mistral pour générer directement le JSON
    print("Envoi du texte à Mistral AI pour génération du JSON...")
    json_str = generer_json_avec_mistral(texte_cv)
    if not json_str:
        print("Échec de la génération du JSON. Arrêt du programme.")
        return
        
    # Étape 3: Enregistrer le JSON au même endroit que le PDF
    enregistrer_json(json_str, chemin_pdf)
    
    print("\nTraitement terminé !")


if __name__ == "__main__":
    main()