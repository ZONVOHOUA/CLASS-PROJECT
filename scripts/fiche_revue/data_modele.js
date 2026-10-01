// Modèle vierge de la fiche de revue documentaire du Cabinet.
// Les zones [[…]] apparaissent en italique gris et sont à remplacer ; la dernière page
// (guide de renseignement) est à supprimer avant transmission.

const doc = '[[Document examiné]]';

module.exports = {
  fichier: {
    titre: 'Modèle – Fiche de revue documentaire du Cabinet',
    sujet: 'Modèle de fiche de revue et de sécurisation documentaire du Cabinet du Ministre',
    motsCles: 'modèle, revue documentaire, Cabinet, MINADER',
  },
  piedDePage: { gauche: `Cabinet du Ministre  ·  Fiche de revue documentaire  ·  ${doc}`, date: '[[Date]]' },

  titre: 'FICHE DE REVUE ET DE SÉCURISATION DOCUMENTAIRE',
  sousTitre: 'Points relevés lors de l’examen du document transmis',

  identification: {
    document: '[[Titre exact du document examiné]]',
    champs: [
      { label: 'Structure émettrice', valeur: '[[Direction, service ou organisme]]' },
      { label: 'Version / date', valeur: '[[Version ou date]]', note: '[[Nombre de pages]]' },
      { label: 'Date de revue', valeur: '[[Date]]', note: 'Échéance : [[à préciser]]' },
      { label: 'Destinataire final', valeur: '[[Destinataire]]', note: 'Confidentialité : [[mention officielle, s’il en existe une]]' },
    ],
    objet: '[[Objet très court de l’examen]]',
  },

  compteurs: [
    { valeur: '[[n]]', label: 'Observations' },
    { valeur: '[[n]]', label: 'Critique', prio: 'C' },
    { valeur: '[[n]]', label: 'Majeures', prio: 'M' },
    { valeur: '[[n]]', label: 'À corriger', prio: 'A' },
    { valeur: '[[n]]', label: 'De forme', prio: 'F' },
  ],
  synthese: {
    statut: '[[Statut global]]',
    appreciation: '[[Appréciation d’ensemble en une ou deux phrases, fondée sur la gravité réelle des observations.]]',
    suiteProposee: '[[Suite proposée, en une ligne.]]',
    complements: '[[n]] arbitrage(s) · [[n]] vérification(s)',
  },

  essentiel: [
    { ref: 'OBS-01', prio: 'C', texte: '**[[Intitulé court.]]** [[Constat en une phrase et conséquence pour le document.]]' },
    { ref: 'OBS-02', prio: 'M', texte: '**[[Intitulé court.]]** [[Constat en une phrase.]]' },
  ],
  arbitragesCourts: [
    { ref: 'A-1', texte: '**[[Sujet.]]** [[Décision attendue, en une phrase.]]' },
  ],

  observations: [
    { id: 'OBS-01', prio: 'C', cat: '[[Catégorie]]', loc: ['[[Page – §]]'], objet: '[[Objet]]', statut: 'À CORRIGER',
      constat: '[[Ce que dit le document, où, et pourquoi cela pose difficulté. Citer seulement l’extrait nécessaire.]]',
      action: '[[Correction établie avec certitude, ou « À confirmer par la Direction ».]]' },
    { id: 'OBS-02', prio: 'M', cat: '[[Catégorie]]', loc: ['[[Page – §]]'], objet: '[[Objet]]', statut: 'À CORRIGER',
      constat: '[[Constat précis et exploitable.]]', action: '[[Correction ou action attendue.]]' },
    { id: 'OBS-03', prio: 'A', cat: '[[Catégorie]]', loc: ['[[Page – §]]'], objet: '[[Objet]]', statut: 'À CORRIGER',
      constat: '[[Constat précis et exploitable.]]', action: '[[Correction ou action attendue.]]' },
    { id: 'OBS-04', prio: 'F', cat: '[[Catégorie]]', loc: ['[[Page – §]]'], objet: '[[Objet]]', statut: 'À CORRIGER',
      constat: '[[Constat précis et exploitable.]]', action: '[[Correction ou action attendue.]]' },
  ],

  arbitrages: [
    { ref: 'A-1', sujet: '[[Sujet]]', lien: '[[OBS-xx]]',
      probleme: '[[Nature du choix à effectuer.]]',
      arbitrage: '[[Décision attendue : validation politique, choix institutionnel, choix de chiffres, positionnement du Ministère ou formulation finale.]]' },
  ],
  verifications: [
    { ref: 'V-1', lien: '[[OBS-xx]]', texte: '[[Information à confirmer, et auprès de quelle structure.]]' },
  ],

  suiteADonner: '[[Proposition adaptée au niveau réel des corrections. Exemples : « Il est proposé de retourner le document à la Direction pour prise en compte des observations ci-dessus avant transmission au Cabinet. » ; « Le document peut être finalisé après intégration des corrections identifiées. » ; « Les points critiques doivent être levés avant toute transmission. »]]',

  guide: {
    titre: 'Guide de renseignement',
    intro: 'Page de consignes, à supprimer avant transmission de la fiche.',
    blocs: [
      {
        titre: 'Niveaux de priorité', entetes: ['Niveau', 'Critère'], largeurs: [3.4, 0],
        lignes: [
          [{ prio: 'C', texte: 'Critique' }, 'Le point peut rendre le document faux, juridiquement risqué, contradictoire ou impropre à la transmission.'],
          [{ prio: 'M', texte: 'Majeur' }, 'Le point modifie significativement le sens, la compréhension ou la crédibilité du document.'],
          [{ prio: 'A', texte: 'À corriger' }, 'Le point doit être repris mais ne remet pas en cause le document dans son ensemble.'],
          [{ prio: 'F', texte: 'Forme' }, 'Correction rédactionnelle ou graphique.'],
        ],
      },
      {
        titre: 'Catégories', entetes: ['Catégorie', 'Champ'], largeurs: [3.4, 0],
        lignes: [
          ['Fond', 'Erreur factuelle, raisonnement incorrect, conclusion non démontrée.'],
          ['Cohérence', 'Contradiction entre deux passages, chiffres incompatibles, logique interne défaillante.'],
          ['Données', 'Valeur erronée, non sourcée, obsolète ou incohérente.'],
          ['Source', 'Absence de référence, source inadaptée ou preuve insuffisante.'],
          ['Institutionnel', 'Erreur sur un texte, une compétence, une institution, une procédure ou une terminologie officielle.'],
          ['Formulation', 'Phrase ambiguë, trop complexe ou susceptible d’être mal interprétée.'],
          ['Forme', 'Orthographe, typographie, mise en page, numérotation, alignement, appellation.'],
          ['À vérifier', 'Élément dont l’exactitude n’a pas pu être confirmée et qui appelle une vérification par la Direction.'],
        ],
      },
      {
        titre: 'Statut global', entetes: ['Statut', 'Repère indicatif'], largeurs: [5.4, 0],
        lignes: [
          ['À corriger avant transmission', 'Un point critique au moins, ou des points majeurs portant sur des éléments essentiels.'],
          ['Révision ciblée nécessaire', 'Points majeurs localisés, sans point critique.'],
          ['Corrections mineures', 'Points « à corriger » ou « forme » uniquement.'],
        ],
      },
    ],
    regles: [
      'Une observation par ligne, référencée OBS-01, OBS-02… ; classement par priorité, puis dans l’ordre du document.',
      'Localiser précisément (page ou section, paragraphe, tableau) et ne citer que l’extrait strictement nécessaire.',
      'Rédiger un constat exploitable : ce que dit le document, où, et pourquoi cela pose difficulté.',
      'Ne proposer une correction que si elle est établie avec certitude ; à défaut, écrire « À confirmer par la Direction ».',
      'Placer dans « Points nécessitant arbitrage » ce qui relève d’un choix, et non d’une erreur.',
      'Une information non vérifiable avec les pièces disponibles n’est pas déclarée fausse : elle figure dans « Vérifications à effectuer ».',
      'Distinguer l’erreur interne au document de l’erreur confirmée par vérification externe.',
      'Ton neutre et constructif : « ne concorde pas avec… », « doit être vérifié au regard de… ».',
      'Fixer le statut global selon la gravité réelle des observations, jamais selon leur seul nombre.',
    ],
  },
};
