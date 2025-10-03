from llm import to_llm, remove_tag
import ast

# TODO: add error logging

def _llm_translate(texts: list[str], target_lang: str) -> str:
    prompt = f"""
    ## Tasks:
    Translate the following texts to {target_lang}. 
    Texts are provided in list format.
    If the text is already in {target_lang}, 
    return it directly without any changes.
    You should only return the translated texts in a list format.

    ## Text:
    {texts}

    ## Output Format:
    <Translated>
        [The translated text here, preserving original formatting and style, all output should be in one line]
    </Translated>
    """
    
    return remove_tag(to_llm(prompt), "Translated")

def translate_text(texts: list[str], target_lang: str) -> dict[str, str]:

    translated_texts = _llm_translate(texts, target_lang)

    try:
        translated_list = ast.literal_eval(translated_texts)
    except (ValueError, SyntaxError):
        print(translated_texts)
        return {text: "Translation failed: parsing error" for text in texts}
    
    ret = {}
    for i in range(len(texts)):
        original = texts[i]
        translated = translated_list[i] if i < len(translated_list) else "Translation failed: missing translation"
        ret[original] = translated
        
    return ret