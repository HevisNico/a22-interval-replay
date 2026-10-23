A22 — rejeu de vérification, paquet unique

Contenu : neuf archives recalculées (minus 67–68 ; plus_prefix18 66–68 ; minus_prefix18 65–68), rapport JSON de comparaison, rapport d’environnement, reçus et provenances de référence des 36 cellules de production à la couche 68.

Résultat : 36/36 concordances exactes pour state, emissions et time_dependencies. Les empreintes de provenance brute restent différentes. La provenance normalisée retire UNIQUEMENT le champ parents : les 36 empreintes production/rejeu concordent. Chaque valeur normalisée et les deux SHA-256 figurent dans comparison_report.json. Cette normalisation ne prouve pas à elle seule l’identité des données parentales.

Vérification indépendante après extraction : python3 -B VERIFY.py
Le script utilise uniquement la bibliothèque standard. Il relit les archives, contrôle leurs empreintes, les charges utiles, les liens entre reçus du rejeu, et recalcule les provenances brutes et normalisées. Il compare les trois autres empreintes scientifiques inscrites dans les reçus, sans réexécuter le moteur.

Les neuf archives sont reprises octet pour octet du rejeu effectué ; aucun nouveau calcul scientifique ni modification de reçu. BUILD.py documente l’assemblage dans l’espace de travail original et n’est pas requis pour VERIFY.py.
