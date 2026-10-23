# Interprétation des statuts conservés

Les champs des contrôleurs de calcul et ceux des vérificateurs ont des rôles distincts.

- `runs/*_v1/progress.json` indique la progression du calcul et de sa sauvegarde. Le champ historique `contract_status: NOT_YET_CHECKED` est écrit à la fin du calcul par `campaign.py` ; les vérificateurs séparés ne le réécrivent pas.
- `supervision/boundary_jobs/CASE.json` donne les codes de sortie des trois contrôles séparés.
- `runs/CASE_v1/contracts_v2_from_1116_through_DEPTH.json` identifie le contrat effectivement vérifié, sa profondeur, ses marges et ses sources.
- `audits/CASE_finite_to_infinite.json` lie ce contrat et l’audit de provenance au théorème de prolongement manuel sous A1–A4.

Un ancien champ de contrôleur ou un ancien titre n’annule pas un certificat ultérieur, et ne doit pas servir à revendiquer un contrat absent. La nouvelle enveloppe de relecture lie les empreintes exactes des pièces finales et actualise les titres sans remplacer les artefacts historiques. Son constructeur refuse de produire un paquet final tant que les six raccords et les inventaires finaux ne passent pas.

Les arrêts volontaires du superviseur de sauvegarde portent `pause_only: true` et ne sont pas des refus du moteur. Ils permettent de changer uniquement la cadence des nouvelles ou le superviseur de persistance. Le calcul physique et ses fichiers sources restent inchangés.
