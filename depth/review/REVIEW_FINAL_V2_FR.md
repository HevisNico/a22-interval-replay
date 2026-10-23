# A22 — relecture finale et raccords finis, version 2

Les six préparations prescrites ont passé leurs contrôles finis, leurs contrats de frontière et leur composition avec le théorème de prolongement applicable, au niveau d’une preuve mathématique/source manuelle et de calculs dirigés sous A1–A4. Les cinq frontières homogènes sont à 68 couches, l’interface connectée à 128. La relecture indépendante et la vérification par assistant de preuve ne sont pas revendiquées.

## Résultats effectivement liés

| Préparation | Couches | Diamètre maximal encadré | Écart minimal encadré | Marge locale à la première vague |
| --- | ---: | ---: | ---: | ---: |
| nominal | 68 | 0.1041972138603950301526831306105507684024179278176357277945895604577345491586336309626208156287749121578093908266551016140595715521908277512370674940183930983 | 15.58644714825796112707032832596309805848921143448474290102853485345879245798639276784053185570758049134907176345318109376106165308398201680827240260381570697229 | 86.636253503169763681543059153230266005172333509763798586301542806334 |
| plus | 68 | 0.1041915944088138391074066795395995378661221895420797269914082137465519683850464124674319702594948304873072821386370525480209657780391162618756436311744729306 | 15.58645309532125944483269364845755612545421393206543132239271053289783548315320934487350727593003494553864842396031002869545546013713896357963612357814914401697 | 86.636190816626545991621003923994196115423937212170186102693701818178 |
| minus | 68 | 0.1042028299516005467430595808622984523130466550658354683131657885306303252705327003655144897799331048699740120461489742029058185935638502359136415262775558909 | 15.58644119619362481197131486808391748645475605170951395700222727930548641975549540826391832444575719712608546767477640118108439463240652523023726733870104343539 | 86.636316160653127587872991758204204925539902963835386278268581586222 |
| plus_prefix18 | 68 | 0.1041940270632388483673075910203660123046921252879486191281548591700827666017819630662142179048263196434150634077979105515823364768396626880764262426058229293 | 15.58644702353831390671919723254421874590346534584177041058328838612664593968535779090542703670311358452433963587774123820030032171914486122638033755023483941776 | 86.636190816626545991621003923994196115423937212170186102693701818178 |
| minus_prefix18 | 68 | 0.1042003999584236692584864170781145842020255182101735518623897160192525003874569343227898949627114420920564930265143047242554926905636124039567104156803374193 | 15.58644727296364295069454355198266338352785762106044142245447115653199069773607015898938852612159760457875618817370683825579955729485257103045272679902119696628 | 86.636316160653127587872991758204204925539902963835386278268581586222 |
| interface | 128 | 0.0069639034021228664816347862607786023734293645371174811469385389039466093638304618762645236605748374965224804324588402979048721882238837920904907627693665770 | 15.58670541869413415440733127231869021442736464750711411158654018097682646733707176251361679400034704403739060680459481369923926979628075956485420907623483405371 | 86.636255531405489346249723799793090733345711583565150298679410974854 |

Chaque frontière contient exactement 54 émissions par voie, les 54 cohortes complètes et les 53 écarts sur chacune des 12 voies. Les seuils sont 0.11 pour les cinq frontières à 68, 0.01 pour l’interface, et 15.5 pour tous les écarts. Aucune fin de train n’a été sélectionnée. Les cellules neuves conservent leurs états initiaux prescrits et reçoivent toute l’histoire émise.

Le contrat futur est vérifié pour toute suite sur la source déclarée dont la première date est au moins 1116 et les écarts ultérieurs au moins 20. Les marges locales de FIRST_FUTURE_FINAL_V2.json ferment l’entrée de la première vague dans chacun des six préfixes ; aucun repos global à 1116 n’est supposé. Les conditions de premier seuil, parent masqué, protection des courants bruts, récupération et régénération sont conservées dans les certificats cellule par cellule.

## Les cinq points de l’audit

1. Provenance : le dossier version 1 contient PROVENANCE_V2.json, les sources et journaux de reconstruction séparés, les empreintes du runtime et des binaires, et l’application explicite de A1–A2. Le module Merkle de production est reproduit octet pour octet avec le chemin C d’origine ; le module d’arrondi l’est aussi. Le journal complet de compilation initiale n’avait pas été archivé : la reconstruction n’est pas présentée comme un reçu historique contemporain. Compilation et runtime restent dans la base de confiance A2.
2. Parent masqué : la section 2 de la version 1 expose précisément pourquoi l’ancienne assertion était trop forte et les inégalités qui la remplacent. Elle couvre les ERROR masqués éventuellement après réouverture, les MARK partiels, les bornes de récupération et l’absence de feu supplémentaire. Cette justification est proposée à la relecture indépendante ; le moteur d’apprentissage n’a pas été modifié.
3. Première source future : les six certificats finaux établissent explicitement 1116. 4096 est l’horizon d’observation des calculs sans source future ; il n’est pas la date minimale revendiquée. Le tableau des marges et les correspondances historiques sont dans FIRST_FUTURE_FINAL_V2.json.
4. Titre : la nouvelle FINITE_TO_INFINITE.md porte le statut des six raccords acquis. Les versions antérieures, dont le titre historique et les pièces déjà liées à leurs empreintes, restent intactes. STATUS_FIELDS_GUIDE.md explique aussi le champ contract_status historique des contrôleurs, que les vérificateurs séparés ne réécrivent pas.
5. Compteurs : COUNTERS_FINAL_V2.json étend l’inventaire aux 5 616 cellules et conserve les profils complets et leurs empreintes. Il distingue les gardes ordinaires des preuves d’ordre particulières. Le rejeu réel instrumenté et le contrôle positif des commutations restent des observations séparées, identifiées dans la version 1.

L’inventaire final trouve 449298 émissions, les comptes ordinaires {"fire": 449298, "ready": 449298}, et 0 commutations réussies enregistrées. La lecture des sources sous A1, les champs présents, la correspondance avec chaque émission et le contrôle positif justifient le sens des zéros ; cela ne compte pas toutes les tentatives refusées.

La version 1 complète est conservée dans A22_review_supplement_v1.zip, à supervision/review_20261023_v1/REVIEW.md. Ses conclusions numériques limitées à l’interface73 sont étendues par les deux inventaires finaux version 2 ; ses résultats et sources ne sont pas remplacés. FINAL_DOCUMENT_BINDINGS_V2.json désigne les résultats exacts auxquels ce présent addendum s’applique.

## Conservation et incident de transport

Les 468 couches complètes, leurs 5 616 résultats et leurs chaînes de reçus parentaux ont été restaurés et authentifiés séparément ; une reprise native avec la barrière de sauvegarde a passé. RECOVERY_FINAL_V1.json lie les archives, reçus, journaux et sources du contrôle. Les sauvegardes régulières et leurs références durables restent nécessaires à la restauration complète.

Une indisponibilité temporaire du transport d’exécution a été signalée immédiatement. Le processus original a survécu ; les sauvegardes 120–121 et l’identité gelée des sources ont été revérifiées avant de reprendre la supervision. TRANSPORT_INTERRUPTION_V1.json conserve ces observations. Aucun remplacement silencieux d’artefact n’a eu lieu.

## Portée et obligations restantes

Les obligations finies des six préparations et leur raccord manuel aux prolongements déclarés sont fermés à ce niveau de preuve. Les préfixes plus_prefix18 et minus_prefix18 rejoignent la même durée nominale que nominal ; les milieux homogènes plus et minus ont leurs durées distinctes ; l’interface a une durée commune aux voies entre les deux bornes, sans identification à leur moyenne arithmétique. Les encadrements exacts sont dans les six rapports de composition.

Restent la relecture indépendante des arguments, et les hypothèses explicites A1–A4, notamment l’exécution authentique et la fidélité du runtime, des primitives natives, de la compilation et du stockage. Il ne s’agit ni d’une preuve vérifiée par assistant formel, ni d’une couverture de toute la boîte initiale A22, ni d’une universalité relativiste. Les corrections documentaires n’ajoutent aucun théorème au-delà des arguments et inégalités identifiés.
