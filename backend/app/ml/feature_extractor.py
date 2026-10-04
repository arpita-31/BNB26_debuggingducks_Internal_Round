"""
Feature Extractor for ReLearn
Constructs hybrid feature representations using TF-IDF n-grams combined with structural AST signals.
"""
from typing import List, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
import scipy.sparse as sp
from .preprocessor import ResponsePreprocessor

class FeatureExtractor:
    def __init__(self):
        self.preprocessor = ResponsePreprocessor()
        # Word-level TF-IDF for semantic terms
        self.word_vectorizer = TfidfVectorizer(
            ngram_range=(1, 3),
            min_df=1,
            max_features=1500,
            sublinear_tf=True
        )
        # Character-level TF-IDF for short operators, indices, and syntactic fragments
        self.char_vectorizer = TfidfVectorizer(
            analyzer='char_wb',
            ngram_range=(3, 5),
            min_df=1,
            max_features=1500,
            sublinear_tf=True
        )
        self.is_fitted = False

    def fit(self, texts: List[str], codes: List[str] = None):
        """Fits both word and character vectorizers on preprocessed documents."""
        if codes is None:
            codes = ["" for _ in texts]

        prepared_docs = [
            self.preprocessor.prepare_input_string(t, c)
            for t, c in zip(texts, codes)
        ]

        self.word_vectorizer.fit(prepared_docs)
        self.char_vectorizer.fit(prepared_docs)
        self.is_fitted = True
        return self

    def transform(self, texts: List[str], codes: List[str] = None) -> sp.csr_matrix:
        """Transforms input text and code into combined sparse feature matrix."""
        if not self.is_fitted:
            raise ValueError("FeatureExtractor has not been fitted yet.")

        if codes is None:
            codes = ["" for _ in texts]

        prepared_docs = [
            self.preprocessor.prepare_input_string(t, c)
            for t, c in zip(texts, codes)
        ]

        word_feat = self.word_vectorizer.transform(prepared_docs)
        char_feat = self.char_vectorizer.transform(prepared_docs)

        # Concatenate sparse matrices along column axis
        combined = sp.hstack([word_feat, char_feat], format="csr")
        return combined

    def fit_transform(self, texts: List[str], codes: List[str] = None) -> sp.csr_matrix:
        self.fit(texts, codes)
        return self.transform(texts, codes)
