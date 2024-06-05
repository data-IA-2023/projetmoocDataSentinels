import deep_translator  # Importation de la bibliothèque pour la traduction
from transformers import RobertaTokenizerFast, TFRobertaForSequenceClassification, pipeline  # Importation des composants de Hugging Face Transformers
from langdetect import detect  # Importation de la fonction detect de la bibliothèque langdetect

# Initialisation du tokenizer pour RoBERTa avec gestion de la troncation
tokenizer = RobertaTokenizerFast.from_pretrained("arpanghoshal/EmoRoBERTa", truncation=True, max_length=512)

# Initialisation du modèle RoBERTa pour la classification de séquences
model = TFRobertaForSequenceClassification.from_pretrained("arpanghoshal/EmoRoBERTa")

# Initialisation du pipeline pour l'analyse de sentiment avec le modèle RoBERTa
emotion_analysis = pipeline('sentiment-analysis', model=model, tokenizer=tokenizer)

# Fonction pour traduire un texte en anglais
def translate_to_en(text=""):
    """
    Cette fonction prend en entrée un texte et le traduit en anglais.
    Elle détecte d'abord la langue du texte, puis le traduit en anglais.

    Args:
        text (str): Le texte à traduire. Par défaut, c'est une chaîne vide.

    Returns:
        dict: Un dictionnaire contenant la langue détectée et le texte traduit en anglais.
    """
    langue = detect(text)
    translated_text = deep_translator.GoogleTranslator(source='auto', target='en').translate(text)
    return {'langue': langue, 'textTraduie': translated_text}

# Fonction pour tronquer les textes trop longs
def truncate_text(text, max_length=512):
    """
    Cette fonction tronque le texte à une longueur maximale de tokens.

    Args:
        text (str): Le texte à tronquer.
        max_length (int): La longueur maximale du texte après troncation.

    Returns:
        str: Le texte tronqué.
    """
    tokens = tokenizer.encode(text, truncation=True, max_length=max_length)
    return tokenizer.decode(tokens, skip_special_tokens=True)

# Fonction pour traduire un texte en anglais et l'analyser pour l'émotion
def translate_and_analyse(text):
    """
    Cette fonction prend un texte en entrée, le traduit en anglais, puis analyse son émotion dominante.

    Args:
        text (str): Le texte à analyser.

    Returns:
        dict: Un dictionnaire contenant le texte d'origine, sa traduction en anglais, l'émotion détectée, 
              la langue d'origine et une émoticône correspondant à l'émotion détectée.
    """
    trad = translate_to_en(text)
    truncated_text = truncate_text(trad['textTraduie'])
    emo = emotion_analysis(truncated_text)[0]['label']
    
    return {'text': text, 'traduction': trad['textTraduie'], "emotion": translate_emotion_to_fr(emo), "langue": trad["langue"], 'emoticon': sentiment_to_emoticon(emo)}

def sentiment_to_emoticon(sentiment):
    """
    Cette fonction prend un sentiment en entrée et renvoie une émoticône équivalente.

    Args:
        sentiment (str): Le sentiment à traduire en émoticône.

    Returns:
        str: L'émoticône équivalente au sentiment. Si aucun sentiment correspondant n'est trouvé, la fonction renvoie None.
    """
    emoticon_dict = {
        "admiration": "😍",
        "amusement": "😄",
        "anger": "😠",
        "annoyance": "😒",
        "approval": "👍",
        "caring": "❤️",
        "confusion": "😕",
        "curiosity": "🤔",
        "desire": "😏",
        "disappointment": "😞",
        "disapproval": "👎",
        "disgust": "🤢",
        "embarrassment": "😳",
        "excitement": "😃",
        "fear": "😨",
        "gratitude": "🙏",
        "grief": "😢",
        "joy": "😊",
        "love": "😍",
        "nervousness": "😬",
        "optimism": "😊",
        "pride": "😊",
        "realization": "😲",
        "relief": "😌",
        "remorse": "😔",
        "sadness": "😔",
        "surprise": "😮",
        "neutral": "😐"
    }

    return emoticon_dict.get(sentiment.lower(), None)

def translate_emotion_to_fr(emotion):
    """
    Cette fonction prend une émotion en anglais en entrée et la traduit en français.

    Args:
        emotion (str): L'émotion à traduire.

    Returns:
        str: L'émotion traduite en français. Si aucune traduction n'est disponible, la fonction renvoie None.
    """
    # Dictionnaire pour traduire les émotions en français
    emotion_dict = {
        "admiration": "admiration",
        "amusement": "amusement",
        "anger": "colère",
        "annoyance": "agacement",
        "approval": "approbation",
        "caring": "sollicitude",
        "confusion": "confusion",
        "curiosity": "curiosité",
        "desire": "désir",
        "disappointment": "déception",
        "disapproval": "désapprobation",
        "disgust": "dégoût",
        "embarrassment": "embarras",
        "excitement": "excitation",
        "fear": "peur",
        "gratitude": "gratitude",
        "grief": "chagrin",
        "joy": "joie",
        "love": "amour",
        "nervousness": "nervosité",
        "optimism": "optimisme",
        "pride": "fierté",
        "realization": "réalisation",
        "relief": "soulagement",
        "remorse": "remords",
        "sadness": "tristesse",
        "surprise": "surprise",
        "neutral": "neutre"
    }
    try:
        return emotion_dict[emotion.lower()]
    except:
        return None

if __name__ == "__main__":
    # Exemple d'utilisation de la fonction translate_and_analyse avec le texte "c'est incroyable."
    emotion_labels = translate_and_analyse("c'est incroyable.")
    print(emotion_labels)
