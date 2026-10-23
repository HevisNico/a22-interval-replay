# Intégrité de la livraison — addendum version 1

Le contrôle de l’enveloppe finale a refusé une copie locale du paquet `A22_plus_prefix18_068_certificate.zip` : son SHA-256 différait du reçu de sauvegarde et le fichier n’était plus un ZIP lisible. Il n’a pas été inclus comme certificat valide ni remplacé silencieusement. Son reçu antérieur, ses octets locaux observés et les deux états d’empreinte sont conservés dans CASE_PACKET_INTEGRITY_INCIDENT_V1.json et CORRUPT_LOCAL_PACKET_FORENSICS_V1.json (copie binaire encodée en base64).

Le nouveau paquet `A22_plus_prefix18_068_certificate_v2_recovered.zip` a été reconstruit exclusivement à partir des sources et checkpoints authentifiés. Son CRC et chaque entrée liée au rapport de composition ont été vérifiés après son enregistrement réussi. CASE_PACKET_RECOVERY_V2.json conserve son identité et son empreinte exactes. L’enveloppe finale version 3 sélectionne cette nouvelle version pour plus_prefix18 ; les cinq autres paquets restent ceux dont les empreintes passent.

Ce défaut concerne une copie locale d’un paquet de relecture. La restauration séparée a authentifié les 468 archives de couche, les 5 616 résultats et leurs reçus parentaux. Les deux ZIP de données des 128 couches de l’interface déjà livrés ont été revérifiés après leur sauvegarde : SHA-256 et CRC passent. Aucun moteur, résultat scientifique ou checkpoint n’a été corrigé pour obtenir ces contrôles.

La cause et la date de la troncature locale restent indéterminées. Les anciens octets distants n’ont pas été relus ; aucune conclusion n’est donnée sur leur intégrité. Cette limite de traçabilité du vieux paquet est maintenue dans le dossier. Les arguments scientifiques restent explicitement conditionnels à A1–A4 et à leur base de confiance ; cet incident ne constitue pas une qualification du stockage, du runtime ou du compilateur. La relecture indépendante reste à faire.

Pour l’examen scientifique, commencer par REVIEW.md et les six rapports de composition, puis utiliser la nouvelle version de paquet indiquée ci-dessus. La copie corrompue est une pièce forensique, pas une donnée acceptée du certificat.
