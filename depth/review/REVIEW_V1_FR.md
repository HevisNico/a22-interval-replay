# A22 — dossier de relecture indépendant, version 1

Ce dossier complète des artefacts immuables. Il ne remplace ni les sources
actives, ni les résultats, ni les checkpoints. Les cinq préparations à 68
couches ont passé leurs contrôles finis et leur composition manuelle sous
A1–A4. L'entrée de l'interface à 128 reste à contrôler. Aucune relecture
indépendante ou vérification par assistant de preuve n'est revendiquée ici.

Les fichiers JSON de ce dossier donnent les chemins et SHA-256 exacts des
résultats concernés. Les conclusions sur les compteurs portent sur les cinq
préfixes complets à 68 et sur l'interface jusqu'à 73 seulement. Elles devront
être étendues à l'interface finale. Les observations instrumentées ont leurs
propres sources, traces et identités ; elles ne sont pas des remplacements
des résultats de production.

## 1. Provenance et application de A1–A2

Le dépôt est fixé au commit
`94f499c85bbc784c08c0d8bdb5e616360dc34863`. L'identité de la nouvelle campagne
est `3ecdb7bd2e618c19fd89ac43f07eca18170865b0f68c1ce1100ba87b96520211`.
`PROVENANCE_V2.json` vérifie les six configurations, le manifeste UPSTREAM,
la correspondance des sources vendues avec le dépôt, et cette identité avant
et après le contrôle. Il décrit séparément l'environnement enregistré dans
les campagnes et une observation actuelle dans un processus isolé utilisant
la même initialisation gelée.

L'environnement observé comprend Python 3.12.14 (interpréteur construit avec
Clang 22.1.3), NumPy 2.3.5 et SciPy 1.17.0. Les extensions ont été compilées
avec GCC/cc Ubuntu 13.3.0, pas avec le compilateur de construction de Python.
Les commandes et versions exactes, ABI, chemins, empreintes de l'interpréteur
et des bibliothèques liées, contextes Decimal et observations de l'arrondi
sont dans le JSON. Le contrôle isolé trouve les contextes dirigés à 160
chiffres, 256 symboles affines, le backend de coefficients natif, les
assertions actives, FE_TONEAREST et la conservation du plus petit subnormal.
Ces sondes ne constituent pas une qualification de toutes les opérations.

Empreintes de production :

- `_a22_native.cpython-312-x86_64-linux-gnu.so` :
  `b968a17f31e85b9b1c8b0db44fd0f93d07bcb77e83f8a8510be1d0ba79f7a26f`.
- `_rounding_native.cpython-312-x86_64-linux-gnu.so` :
  `29b1d226d6576e418c38d476cb050a20b37f6db67b6f70ca734423cac6985c57`.

Le premier est un accélérateur de codage/Merkle exact ; il n'implémente pas
les équations physiques. Le second réalise les primitives binaires des
coefficients et de leurs bornes d'erreur. Leur rôle dans A2 est donc distinct.
La compilation déclarée utilise les scripts fournis, avec `-O3 -std=c11
-shared -fPIC -fno-fast-math -ffp-contract=off`, l'en-tête du Python courant,
`-lm`, et `-lcrypto` pour le module Merkle.

Les reconstructions sont placées exclusivement dans ce dossier. Le premier
essai reproduit exactement le module d'arrondi, mais pas le module Merkle
relocalisé : les macros d'assertion de l'API C Python incorporent le chemin
du fichier C. Cela change `.rodata`, les déplacements et le build-id. Le
chemin historique est encore visible dans le binaire de production. Une
reconstruction séparée, avec ce fichier C inchangé à son chemin d'origine
et une sortie distincte, reproduit **exactement** l'empreinte de production.
`PATH_SENSITIVE_REBUILD.json`, les deux versions du collecteur, les sorties
de compilation et les binaires d'essai sont conservés. L'échec initial de
l'assertion de comparaison des binaires relocalisés n'est pas effacé.

Limite historique : la sortie complète et l'environnement de la compilation
initiale n'avaient pas été conservés comme reçu dédié. La chaîne actuelle
fournit des identités enregistrées dans les campagnes, des métadonnées ELF,
les sources, les commandes de reconstruction et une reproduction exacte.
Elle ne fabrique pas un journal contemporain manquant.

A1 reste l'hypothèse d'exécution authentique des sources et adaptations
déclarées. Le contrôleur vérifie l'identité avant et après chaque cellule ;
les reçus, comparaisons écriture/lecture et chaînes parentales lient les
artefacts à cette exécution déclarée. A2 reste l'hypothèse de fidélité de
Python/Decimal, du calcul binaire C, de la compilation et du stockage.
Reconstruction et sondes apportent des témoins de correspondance, pas une
preuve du compilateur ou de l'environnement. A3–A4 restent également requis.

## 2. Parent masqué tardif et assertion trop forte

L'assertion historique imposait `right > a_i.upper` pour **tout** parent,
avec `right = min_i(a_i.lower) + 0.999999`. Elle exigeait donc que tous les
parents soient déjà arrivés avant le point choisi près de la première fin
de pulse brut. Cela n'est pas nécessaire pour isoler un premier feu : un
parent peut arriver après ce feu, pendant la protection. L'ancien test
refusait alors un état local physiquement admissible, sans établir une
violation physique. Il n'était pas un lemme du modèle.

Notons `[a_i^-,a_i^+]` les dates parentes relatives à une vague, `[F^-,F^+]`
le premier feu encadré, `l=min_i a_i^-`, et `H=20` l'écart de source minimal.
Les conditions effectivement vérifiées par `certify_contracts.py` sont :

1. Signes dirigés stricts de part et d'autre du premier seuil, gains positifs
   et monotonie de `h` sur les âges `[0,1]`. Le feu précède `l+1`, donc toute
   première fin de courant brut. Il précède aussi `l+1.10`, premier ERROR.
2. Pour un parent déclaré masqué, `a_i^- > F^+`. Il ne contribue donc jamais
   à l'équation du premier feu de cette vague. Pour les autres parents,
   l'équation restreinte conserve les deux signes stricts.
3. Avec `P_min=1+ln(2.5)/1.1` et
   `P_max=1+ln(2.5)/b_entry^-`, chaque ERROR influent finit avant
   `F^-+P_min` : `a_i^++1.25 < F^-+P_min`. Son début est après le feu ;
   il est donc entièrement protégé et son gain ne change pas.
4. Pour **tous** les ports, masqués compris,
   `a_i^++1 < F^-+P_min`. Leurs courants bruts finissent avant toute
   réouverture, indépendamment de leur amplitude admissible.
5. Régénération locale : `F^++P_max < l+H` et
   `max_i a_i^++1.25 < l+H`. La principale et tous les auxiliaires sont donc
   prêts avant la première arrivée possible de la vague suivante.

Les MARK d'un parent tardif peuvent agir pendant la protection et accélérer
la récupération. Cela ne change pas l'équation READY du premier feu ; les
bornes `b_entry^- <= b <= 1.1` couvrent cette adaptation. Comme `b` ne peut
que croître, le même `P_max` reste valable aux vagues suivantes. La phase
FAST dure 1, puis l'intégrale de `b` gouverne la phase SLOW ; ces deux bornes
couvrent les deux phases et les MARK partiels.

Un ERROR **masqué** n'est pas tenu de finir sous protection. Sa partie
éventuellement après la réouverture peut accroître son propre gain, jusqu'à
la butée physique. Elle n'injecte pas directement de charge principale.
Son courant brut est déjà éteint par la condition 4. Après la réouverture,
`q=r` et aucun courant brut ne subsiste : il n'y a donc aucun feu
supplémentaire avant la vague suivante. Les charges auxiliaires achèvent
leur cycle nominal avant cette vague par la condition 5.

Par induction, ce même parent arrive encore après le premier feu de chaque
vague future. L'accroissement de son gain ne peut rendre son courant actif
avant sa propre arrivée. Les gains influents restent fixes ; les gains
masqués peuvent évoluer sans modifier le premier feu. On obtient ainsi
`t_j^p=s_p+d_j` pour toute suite admise, pas seulement pour quatre sondes.
La fin du pulse émis, à `F+1`, est comprise dans la protection minimale.

La régression locale conservée dans `test_future_checker.py` place un parent
influent à 0 et un parent masqué à 1.05. Le premier feu est avant 0.3, tandis
que l'ancien point `right` est inférieur à 1.05. Les conditions réelles
passent. C'est un test local synthétique du vérificateur, pas l'affirmation
que cet état a été appris par l'une des six préparations. Les certificats
finaux contiennent les marges dirigées pour chaque cellule réelle ;
`FIRST_FUTURE_V1.json` lie leurs empreintes et compte 15 ports masqués par
préfixe complet.

Relecture indépendante demandée : contrôler le caractère de premier seuil,
la séparation influent/masqué, la validité des deux bornes de récupération
avec MARK partiels, et l'induction excluant tout feu additionnel. Les
conditions de remplacement sont plus précises qu'une simple suppression
d'assertion ; aucune branche du moteur d'apprentissage n'a été modifiée.

## 3. Première source future : borne acquise 1116 pour les cinq préfixes

Les cinq fichiers `contracts_v2_from_1116_through_068.json` déclarent
explicitement `first_future_source_lower=1116`, et des écarts ultérieurs
de source au moins 20. `FIRST_FUTURE_V1.json` authentifie ces fichiers et
leurs compositions. Leur marge locale minimale est supérieure à 86.636.
4096 est le temps d'observation du **rejeu sans aucune source future**.
Ce n'est ni une remise à zéro, ni une exigence d'attendre 4096 avant la
première source future.

Pour chaque cellule `v`, soit `L_v` sa dernière émission d'apprentissage et
`A_v` la dernière arrivée d'apprentissage parmi tous ses parents. Le contrôle
calcule, avec bornes supérieures dirigées,

    Q_v = max(L_v+1+ln(2.5)/0.08, A_v+1.25, L_v+1).

La dernière récupération est finie au plus tard à la première borne, car
`b>=0.08` pendant tout l'apprentissage. Tous les courants bruts et auxiliaires
ont fini à la deuxième borne. L'histoire complète certifiée exclut un feu
oublié après `L_v`. La cellule est donc READY et sans courant après `Q_v`.
Sur cet intervalle courant-libre, `q'=kappa(r-q)`. Son état exact `q(4096)=r`
implique `q=r` sur tout cet intervalle, puisque l'exponentielle du flot ne
s'annule pas. Les gains et `b` ont aussi cessé de varier après la fin des
derniers courants auxiliaires ; les auxiliaires sont à leur repos exact.

Le vérificateur exige `Q_v < 4096` et

    Q_v < 1116 + min_parent(d_parent.lower).

Une induction sur les couches établit que la première vague future ne
modifie aucun événement d'apprentissage déjà enregistré : elle atteint
chaque cellule après son propre `Q_v`. Puis la régénération locale de la
section 2 traite toutes les vagues suivantes. D'autres cellules peuvent
encore traiter l'apprentissage lorsque la source émet à 1116 ; cette preuve
n'exige pas de repos global à cette date.

Dans les cinq préfixes à 68, les bornes locales maximales sont même
inférieures à 1049. Ce fait numérique propre à ces préfixes n'est pas
extrapolé à l'interface profonde. Pour l'interface à 128, les mêmes
inégalités devront être contrôlées sur son histoire réelle avant de
revendiquer 1116. Son contrôle préliminaire à 30 n'est pas une validation
à 128.

Harmonisation versionnée : le prototype gelé `contracts.py` et le texte
historique `ADAPTATION_PROOF.md` utilisaient la borne plus faible 4096.
Ils restent inchangés et identifiables. Les anciennes pièces ne sont pas
réétiquetées comme si elles avaient établi 1116. Le présent addendum et
le tableau de correspondance JSON désignent précisément les certificats
qui établissent la borne renforcée. Les sondes ponctuelles de la théorie
à 4096 ne sont pas utilisées comme preuve universelle.

## 4. Titre et statut des documents

La copie actualisée `FINITE_TO_INFINITE.md` de ce dossier porte le statut
effectivement acquis : cinq raccords finis passent ; l'interface à 128
reste en attente. Son ancienne version exacte est conservée dans
`original_sources/FINITE_TO_INFINITE.md`. La version à l'emplacement gelé
initial reste intacte, car ses empreintes sont référencées par les cinq
compositions et paquets déjà sauvegardés. L'addendum corrige leur contexte
documentaire sans casser ni remplacer ces liens de provenance.

Cette correction de titre ne ferme aucune obligation mathématique par
elle-même. Le niveau reste une preuve source manuelle et des inégalités
dirigées sous A1–A4 ; ni qualification indépendante ni formalisation n'a
été ajoutée par un changement de titre.

## 5. Sens des compteurs et contrôle de leur enregistrement

Le champ `recorded_guard_counts` de l'ancien audit est construit uniquement
à partir de `relative_order_proofs`. Un dictionnaire vide signifie aucune
**preuve d'ordre particulière enregistrée**, pas aucune garde ordinaire.
Le champ distinct `width_profile.guard_dates` contient les comptes ordinaires.
L'inventaire passif complet trouve, sur 4 956 cellules, **413 658 feux
enregistrés et 413 658 récupérations**, chacun en correspondance exacte
avec les émissions conservées. Les champs attendus sont présents ; une clé
absente n'est pas interprétée comme zéro.

`COUNTERS_V1.json` conserve les profils, comptes et empreintes de chaque
résultat concerné. Aucune commutation réussie, aucun no-fire-cover réussi
et aucun group-recovery réussi n'y est enregistré. Cela ne compte pas les
tentatives refusées, ni toutes les permutations explorées. Le champ des
plus grandes augmentations est tronqué pour l'affichage ; la liste
`relative_order_proofs` exportée, elle, n'est pas tronquée.

Le lien source est explicite : `unit` initialise `PROFILE=Profile(inputs)`
avant les événements et exporte ce même objet. Le code de chaque sortie
réussie des trois mécanismes précités ajoute un enregistrement dès que
`PROFILE` n'est pas `None`. Les anciens lanceurs qui mettent PROFILE à None
ne sont pas appelés par ce contrôleur. L'identité des sources effectives,
le lien des globals de `unit` avec le module du modèle et les champs
conservés sont des témoins de cette lecture sous A1.

Deux contrôles séparés complètent l'inventaire :

- `REPLAY_LOGGING_V1.json` : rejeu observé de la vraie cellule nominale
  `(68,0)` avec ses parents authentifiés. Ses états, émissions, dépendances
  de temps et provenance ont exactement les mêmes empreintes scientifiques
  que la production. Les 823 appels d'advance observés trouvent PROFILE
  actif ; 54 feux et 54 récupérations sont enregistrés ; aucune commutation
  n'est appelée. Les métriques de durée/RSS, non déterministes, ne sont pas
  comparées entre exécutions.
- `POSITIVE_LOGGING_V1.json` : une fixture synthétique originale déclenche
  deux commutations réussies et conserve leurs deux enregistrements. Elle
  vérifie le fonctionnement positif du canal de diagnostic. Elle n'est pas
  une trajectoire d'apprentissage certifiée et ses événements raw_on ne sont
  pas ajoutés à la campagne ni à ses obligations de couverture.

Ces contrôles ont leurs propres sources et traces, et aucun observateur
n'a été installé dans les processus de production. Le zéro de production
reste une conclusion sur l'exécution déclarée sous A1, pas une attestation
externe de chaque instruction exécutée. L'inventaire final de l'interface
doit encore être étendu des couches 74 à 128.

## Corrections documentaires et obligations restantes

Corrections documentaires acquises : distinction des deux familles de
compteurs, statut du titre, tableau 1116/4096 et identification du nouveau
binaire. Les pièces historiques restent immuables.

Obligations mathématiques traitées au niveau manuel : parent masqué tardif,
protection de tous les courants bruts, éventuelle plasticité masquée,
régénération et absence de second feu ; entrée locale de la première vague
à 1116, avec ses contrôles dirigés effectués pour les cinq préfixes à 68.
La relecture indépendante de ces arguments reste à faire.

Restent ouverts : atteindre et auditer l'interface à 128 ; y vérifier les
54 cohortes, le diamètre 0.01, tous les écarts, le contrat futur et l'entrée
locale à 1116 ; étendre l'inventaire des compteurs à ce préfixe complet ;
composer ensuite le théorème connecté. A1–A4 demeurent des hypothèses
d'exécution. Aucune preuve du compilateur, qualification du runtime,
universalité sur toute la boîte initiale ou universalité relativiste n'est
revendiquée.

Enfin, un défaut d'ordonnancement du superviseur de sauvegarde a été isolé :
un marqueur de calcul pouvait déclencher un paquet périodique avant que le
nouveau checkpoint soit offert à la sauvegarde. Le garde-fou a refusé le
paquet 75 ; aucune avance sans reçu durable ni perte de checkpoint n'en a
résulté. Une nouvelle version identifiée du superviseur déclenche les
paquets sur les couches acquittées durables. Sources avant/après et motif
sont dans `supervisor_change_v2.json`. Cette correction de persistance
n'affecte pas les équations, les ordres d'événements ou les résultats du
moteur actif.
