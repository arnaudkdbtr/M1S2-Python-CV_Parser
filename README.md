![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue)
![LLM](https://img.shields.io/badge/LLM-Mistral-orange)
![Platform](https://img.shields.io/badge/Platform-CLI-green)

# 📄 CV Parser - Mistral AI

Un outil en ligne de commande qui extrait automatiquement les informations d'un CV au format PDF et les convertit en JSON structuré à l'aide de l'API Mistral AI.

## 🔍 Objectif

Extraire efficacement les données pertinentes d'un CV depuis un fichier PDF et les structurer en format JSON pour faciliter leur traitement et analyse.

## 🤖 Pourquoi un LLM ?

Les approches traditionnelles basées sur des expressions régulières sont souvent:
- Peu fiables face à des mises en page variées
- Fragiles et difficiles à maintenir
- Limitées pour comprendre le contexte

L'utilisation de Mistral AI permet une extraction plus intelligente et adaptative qui comprend la sémantique du contenu et s'adapte à différents formats de CV.

## ⚙️ Fonctionnalités

- Lecture de fichiers PDF avec PyPDF2
- Traitement du texte extrait via l'API Mistral AI
- Génération d'un JSON structuré avec les sections:
  - `prenom_nom`, `email`, `telephone`, `linkedin`, `github`
  - `competences_techniques`, `soft_skills`, `langues`, `certifications`
  - `formation`, `experience`
- Post-traitement pour garantir la détection des compétences bureautiques
- Vérification et validation du JSON généré
- Sauvegarde du résultat au même emplacement que le fichier PDF source

Le programme générera un fichier JSON (`CV_Exemple.json`) au même emplacement que le PDF source.

## 🔑 Configuration de l'API

Le programme utilise une clé API Mistral. Pour configurer votre propre clé API:

```python
MISTRAL_API_KEY = "votre_clé_api_ici"
```

Pour obtenir une clé API:
1. Créer un compte sur https://console.mistral.ai/
2. Générer une clé API dans votre compte Mistral
3. Remplacer la valeur de MISTRAL_API_KEY dans le code par votre clé API

Dans un environnement de production, il est recommandé de:
1. Définir cette clé comme variable d'environnement
2. La stocker dans un gestionnaire de secrets
3. Ne pas l'inclure directement dans le code source

## 📊 Structure du JSON généré

```json
{
  "prenom_nom": "string",
  "email": "string",
  "telephone": "string",
  "linkedin": "string (utilisateur uniquement)",
  "github": "string (utilisateur uniquement)",
  "competences_techniques": [
    "compétence technique 1",
    "compétence technique 2"
  ],
  "soft_skills": [
    "soft skill 1",
    "soft skill 2"
  ],
  "langues": [
    "langue et niveau"
  ],
  "certifications": [
    "certification 1",
    "certification 2"
  ],
  "formation": [
    {
      "titre": "diplôme et spécialité",
      "etablissement": "nom de l'école/université",
      "periode": "dates de début et fin",
      "details": [
        "enseignements, mentions, etc."
      ]
    }
  ],
  "experience": [
    {
      "titre": "intitulé du poste",
      "entreprise": "nom de l'entreprise",
      "lieu": "ville/pays ou télétravail",
      "periode": "dates de début et fin",
      "details": [
        "responsabilités, accomplissements"
      ]
    }
  ]
}
```

## 🧠 Modèle utilisé

| Modèle | Statut | API utilisée |
|--------|--------|--------------|
| Mistral Small | ✅ Testé | `https://api.mistral.ai/v1/chat/completions` |

## 🔄 Comment ça fonctionne

1. **Extraction du texte**: Le programme utilise PyPDF2 pour extraire le texte brut du fichier PDF
2. **Préparation du prompt**: Construction d'une requête structurée pour Mistral AI avec des instructions détaillées
3. **Appel API**: Envoi du texte extrait à l'API Mistral AI
4. **Post-traitement**: Vérification et enrichissement du JSON généré
5. **Sauvegarde**: Enregistrement du résultat dans un fichier JSON

## 📝 Limitations

- La qualité de l'extraction dépend de la lisibilité du PDF
- Les PDF scannés ou protégés ne peuvent pas être traités correctement
- La performance peut varier selon la structure et le format du CV

## 🔮 Améliorations possibles

- Support pour d'autres formats (DOCX, HTML, etc.)
- Interface graphique pour faciliter l'utilisation
- Gestion sécurisée de la clé API
- Options de configuration supplémentaires
- Support multilingue amélioré
