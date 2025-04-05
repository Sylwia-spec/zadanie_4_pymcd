import numpy as np
import pandas as pd
from pymcdm.methods import TOPSIS, SPOTIS
from pymcdm.normalizations import minmax_normalization

def rank_preferences(scores, reverse=True):

    return np.argsort(np.argsort(-scores if reverse else scores)) + 1

alternatives = ['Domar', 'BudMax', 'Renovita', 'EkipaPlus']
decision_matrix = np.array([
    [17800, 30, 8.5, 3],
    [16500, 40, 7.0, 2],
    [19000, 25, 9.0, 5],
    [15000, 50, 6.5, 1]
])

weights = [0.4, 0.2, 0.3, 0.1]
types = [-1, -1, 1, 1]

norm_matrix = minmax_normalization(decision_matrix, types)

topsis = TOPSIS()
topsis_scores = topsis(norm_matrix, weights, types)
topsis_ranking = rank_preferences(topsis_scores, reverse=True)


bounds = [(np.min(decision_matrix[:, i]), np.max(decision_matrix[:, i])) for i in range(decision_matrix.shape[1])]
spotis = SPOTIS(bounds)
spotis_scores = spotis(decision_matrix, weights, types)
spotis_ranking = rank_preferences(spotis_scores, reverse=False)

df_results = pd.DataFrame({
    'Firma': alternatives,
    'TOPSIS Wynik': np.round(topsis_scores, 4),
    'TOPSIS Ranking': topsis_ranking,
    'SPOTIS Wynik': np.round(spotis_scores, 4),
    'SPOTIS Ranking': spotis_ranking
})

print("\nRanking wykonawców remontu (TOPSIS i SPOTIS):")
print(df_results.sort_values('TOPSIS Ranking').to_string(index=False))
