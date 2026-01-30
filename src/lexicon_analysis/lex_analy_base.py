import pytesseract, re, unidecode
from PIL import Image
from pathlib import Path
import spacy
from typing import Union, Dict, List
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))  # Adds src/ to path

from data_treatment.EDA.ocr_functions import (
    extract_text_from_image,
    transform_mwes,
    preprocess_text,
    tokenize_text,
    
)

# Customizable sentiment lexicons (Portuguese)
POSITIVE_TERMS = {
    "crescimento": 1.5,
    "alta": 1.0,
    "recuperacao": 1.7,
    "lucro": 1.3,
    "superavit": 1.8,
    "pib": 0.8,
    "banco_central": 0.5,
    "expansao": 1.4,
    "investimento": 1.2,
    "valorizacao": 1.3,
    "estabilidade": 1.0,
    "reducao_de_riscos": 1.2,
    "inovacao": 1.1,
    "oportunidade": 1.0,
    "rentabilidade": 1.5,
    "ganho": 1.2,
    "eficiencia": 1.0,
    "confianca": 1.1
}

NEGATIVE_TERMS = {
    "recessao": -1.8,
    "queda": -1.2,
    "ipca": -1.5,
    "deficit": -1.6,
    "desemprego": -1.7,
    "juros_selic": -0.9,
    "crise": -2.0,
    "defasar": -2.0,
    "instabilidade": -1.2,
    "perda": -1.3,
    "desvalorizacao": -1.5,
    "endividamento": -1.4,
    "inadimplencia": -1.6,
    "colapso": -2.0,
    "problema_fiscal": -1.5,
    "falencia": -2.0,
    "ineficiencia": -1.2,
    "desconfianca": -1.1,
    "quebrar": -1.6,
    "rombo_fiscal": -2
}

# Economic intensifiers (modify adjacent sentiment)
INTENSIFIERS = {
    "muito": 1.5,
    "extremamente": 2.0,
    "ligeiramente": 0.5,
    "quase": 0.3,
    "pifio": 1.3,
    "bem": 1.5,
    "bastante": 1.4,
    "levemente": 0.6,
    "fortemente": 1.8,
    "demasiado": 1.7
}
# Negation terms
NEGATIONS = {"nao", "nem", "sem", "nunca", "jamais", "impossivel"}

def lexicon_sentiment_clauses(
    tokenized_clauses: List[List[str]],
    positive_lex: Dict[str, float] = POSITIVE_TERMS,
    negative_lex: Dict[str, float] = NEGATIVE_TERMS,
    intensifiers: Dict[str, float] = INTENSIFIERS,
    negations: set[str] = NEGATIONS
) -> float:
    """
    Computes sentiment score per clause and aggregates to a general score.

    Args:
        tokenized_clauses: List of clauses, each clause is a list of tokens
        positive_lex / negative_lex: sentiment dictionaries
        intensifiers: weight modifiers for adjacent tokens
        negations: set of negation words

    Returns:
        General sentiment score for the whole text (normalized)
    """
    
    def score_clause(tokens: List[str]) -> float:
        total_score = 0.0
        prev_token = None
        for i, token in enumerate(tokens):
            print(token)
            token_score = 0.0
            # Positive / negative lexicon
            if token in positive_lex:
                token_score = positive_lex[token]
            elif token in negative_lex:
                token_score = negative_lex[token]
            # Intensifiers
            if prev_token in intensifiers:
                token_score *= intensifiers[prev_token]
            # Negations
            if prev_token in negations:
                token_score *= -0.5
            # Contrastive clauses
            if token in {"mas", "porém", "contudo"} and i > 0:
                total_score *= 0.3
            print(total_score)
            total_score += token_score
            print(total_score)
            prev_token = token
        # Normalize by sqrt of token count
        return total_score / (len(tokens) ** 0.5) if tokens else 0.0
    
    

    # Score all clauses
    clause_scores = [score_clause(clause) for clause in tokenized_clauses]

    print(clause_scores)

    # Aggregate: mean of clause scores
    if clause_scores:
        general_score = sum(clause_scores) / len(clause_scores)
    else:
        general_score = 0.0

    return general_score

data = extract_text_from_image('data/tweet_teste_4.png')
   
data2 =  transform_mwes(data)
    
data3 = preprocess_text(data2)
    
data4 = tokenize_text(data3, )

print(data4)


print(lexicon_sentiment_clauses(data4))
