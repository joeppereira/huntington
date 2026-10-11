"""Dependency-free Okapi BM25.

Lifted from gtm_cloud gtm-workbench/tools/cascade/hybrid_retriever.py (_MiniBM25), the
measured C1-lift component. Kept dependency-free on purpose: the corpus is small enough
for exhaustive scoring, and the query path must stay model- and service-free.
"""

import math
from collections import Counter


class BM25:
    def __init__(self, corpus_tokens: list[list[str]], k1: float = 1.5, b: float = 0.75):
        self.k1, self.b = k1, b
        self.N = len(corpus_tokens)
        self.len = [len(d) for d in corpus_tokens]
        self.avgdl = (sum(self.len) / self.N) if self.N else 0.0
        df: Counter[str] = Counter()
        for d in corpus_tokens:
            df.update(set(d))
        self.idf = {t: math.log(1 + (self.N - n + 0.5) / (n + 0.5)) for t, n in df.items()}
        self.tf = [Counter(d) for d in corpus_tokens]
        self.vocab = set(self.idf)

    def get_scores(self, q_tokens: list[str]) -> list[float]:
        out = [0.0] * self.N
        for i in range(self.N):
            dl = self.len[i] or 1
            s = 0.0
            for t in q_tokens:
                f = self.tf[i].get(t)
                if not f:
                    continue
                s += (
                    self.idf.get(t, 0.0)
                    * f
                    * (self.k1 + 1)
                    / (f + self.k1 * (1 - self.b + self.b * dl / self.avgdl))
                )
            out[i] = s
        return out
