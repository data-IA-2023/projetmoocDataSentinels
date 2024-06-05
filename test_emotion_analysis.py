# test_emotion_analysis.py
import pytest
from Sentiment_analysis import translate_to_en, truncate_text, translate_and_analyse, sentiment_to_emoticon, translate_emotion_to_fr

def test_translate_to_en():
    result = translate_to_en("Bonjour tout le monde")
    assert result['langue'] == 'fr'
    assert result['textTraduie'] == "Hello everybody"


def test_translate_and_analyse():
    result = translate_and_analyse("c'est incroyable.")
    assert result['langue'] == 'fr'
    assert 'traduction' in result
    assert result['traduction'] == "it's incredible."
    assert 'emotion' in result
    assert 'emoticon' in result
    assert result['emotion'] is not None
    assert result['emoticon'] is not None
    
if __name__ == "__main__":
    pytest.main()
