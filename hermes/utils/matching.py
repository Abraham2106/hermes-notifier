import difflib

def categorize_match(keyword: str, text: str, threshold: float = 0.75) -> str:
    """Categoriza la similitud de un texto con respecto a una palabra clave.
    
    Args:
        keyword (str): La palabra clave a buscar.
        text (str): El texto donde se buscara la palabra (ej. asunto del correo).
        threshold (float): Ratio minimo de similitud para considerarse 'SIMILAR'.
        
    Returns:
        str: "EXACT" si existe coincidencia exacta (case-insensitive).
             "SIMILAR" si existe coincidencia difusa (plurales, typos).
             "NONE" si no hay coincidencia.
    """
    if not text or not keyword:
        return "NONE"
        
    kw_lower = keyword.lower().strip()
    text_lower = text.lower()
    
    # Busqueda exacta
    if kw_lower in text_lower:
        return "EXACT"
        
    # Busqueda difusa (fuzzy)
    words = text_lower.split()
    for word in words:
        # Limpiar signos de puntuacion comunes a los bordes
        clean_word = word.strip(".,;:()[]{}!?\"'")
        if not clean_word:
            continue
            
        ratio = difflib.SequenceMatcher(None, kw_lower, clean_word).ratio()
        if ratio >= threshold:
            return "SIMILAR"
            
    return "NONE"
