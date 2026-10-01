// Données de la fiche de revue : Communication en Conseil des Ministres
// « Redevances de la filière café-cacao au 30 juin 2026 » (version du 12 août 2026).
//
// Sources des observations :
//   - commentaires de relecture présents dans le fichier (relectures des 11 et 20 août 2026) ;
//   - vérification arithmétique de l'ensemble des données du document (voir verif_ccm.py).
// Toutes les valeurs citées proviennent du document examiné ; aucune donnée externe n'est utilisée.
//
// Balisage du texte : **gras**, *italique*, ^exposant^.
// Priorités : C = critique, M = majeur, A = à corriger, F = forme.

module.exports = {
  fichier: {
    titre: 'Fiche de revue documentaire – CCM café-cacao au 30 juin 2026',
    sujet: 'Revue et sécurisation de la Communication en Conseil des Ministres sur les redevances café-cacao au 30 juin 2026',
    motsCles: 'revue documentaire, Cabinet, MINADER, café-cacao, redevances, Conseil des Ministres',
  },
  piedDePage: {
    gauche: 'Cabinet du Ministre  ·  Fiche de revue documentaire  ·  CCM café-cacao au 30 juin 2026',
    date: '1^er^ octobre 2026',
  },

  titre: 'FICHE DE REVUE ET DE SÉCURISATION DOCUMENTAIRE',
  sousTitre: 'Points relevés lors de l’examen du document transmis',

  identification: {
    document: 'Communication en Conseil des Ministres – Informations relatives à la collecte et à l’utilisation des redevances prélevées sur la filière café-cacao au 30 juin 2026',
    champs: [
      { label: 'Structure émettrice', valeur: 'MINADER – MEFB', note: 'Communication conjointe · données du Conseil du Café-Cacao' },
      { label: 'Version / date', valeur: 'Version du 12 août 2026', note: '17 pages' },
      { label: 'Date de revue', valeur: '1^er^ octobre 2026' },
      { label: 'Destinataire final', valeur: 'Conseil des Ministres' },
    ],
    objet: 'Contrôle de la fiabilité des données et de la cohérence du texte avant transmission',
  },

  synthese: {
    statut: 'À corriger avant transmission',
    appreciation: 'Document complet et bien structuré ; les totaux des dix tableaux sont exacts. Les corrections portent sur un montant clé, des incohérences ponctuelles et la forme.',
    suiteProposee: 'Retour à la structure émettrice ; levée prioritaire du point OBS-01 ; arbitrages A-1 et A-2.',
    complements: '2 arbitrages · 4 vérifications',
  },

  // Lecture Cabinet (page 1) : points critiques et majeurs en une ligne.
  essentiel: [
    { ref: 'OBS-01', prio: 'C', texte: '**Revenu brut des producteurs de cacao (janvier-juin 2026).** 1 688,78 Mds annoncés ; les données du document conduisent à 1 642,29 Mds (+51,03 % et non +55,31 %). À confirmer avant transmission.' },
    { ref: 'OBS-02', prio: 'M', texte: '**Production de cacao.** Présentée comme ayant « doublé » : elle a progressé de 58,52 %.' },
    { ref: 'OBS-03', prio: 'M', texte: '**Exportations de café.** Présentées en hausse : il s’agit d’une baisse de 23,22 %.' },
    { ref: 'OBS-04', prio: 'M', texte: '**Objectif de traçabilité.** « Au moins 15 % » : incompatible avec la production déclarée (A-1).' },
    { ref: 'OBS-05', prio: 'M', texte: '**Cumuls éducation.** Nombres en lettres non actualisés (395, 354 et 73 au lieu de 413, 372 et 79).' },
    { ref: 'OBS-06', prio: 'M', texte: '**Hydraulique.** 1 994 pompes posées pour 1 737 forages réalisés : écart de 257 à expliquer.' },
    { ref: 'OBS-07', prio: 'M', texte: '**Dépôts à la BNI.** 47,48 Mds dans le texte, 46,38 Mds au Tableau 10.' },
  ],

  arbitragesCourts: [
    { ref: 'A-1', texte: '**Objectif de traçabilité 2025-2026.** Recalculer le pourcentage, relever l’objectif en volume ou ne conserver que ce dernier.' },
    { ref: 'A-2', texte: '**Échéances postérieures au 30 juin 2026.** Maintenir la rédaction au 30 juin ou l’actualiser.' },
  ],

  observations: [
    // ---------------------------------------------------------------- CRITIQUE
    {
      id: 'OBS-01', prio: 'C', cat: 'Données', objet: 'Revenu brut des producteurs de cacao (janvier-juin 2026)', statut: 'À VÉRIFIER',
      loc: ['1.1 – Prix du cacao, § 1', 'Conclusion, § 2'],
      constat: 'Revenu brut annoncé : 1 688,78 Mds (+55,31 %). Les données de la section 1.1 (879 819 t × 1 867 FCFA/kg) donnent environ 1 642,6 Mds ; le recoupement avec la partie 2 aboutit à 1 642,29 Mds (+51,03 %), la même méthode redonnant exactement le chiffre 2025. Montant repris en conclusion.',
      action: 'Recalculer à partir des données sources et harmoniser la section 1.1 et la conclusion. **À confirmer par la Direction** (V-1).',
    },
    // ---------------------------------------------------------------- MAJEUR
    {
      id: 'OBS-02', prio: 'M', cat: 'Fond', objet: 'Production de cacao présentée comme ayant « doublé »', statut: 'À CORRIGER',
      loc: ['1.1 – Prix du cacao, § 1'],
      constat: 'La hausse du revenu est attribuée à une production qui « a doublé ». La production est passée de 555 030 t à 879 819 t, soit +58,52 %.',
      action: 'Remplacer par « a progressé de 58,52 % ».',
    },
    {
      id: 'OBS-03', prio: 'M', cat: 'Cohérence', objet: 'Exportations de café : hausse ou baisse', statut: 'À CORRIGER',
      loc: ['1.1 – Production du café, § 2'],
      constat: 'Exportations de café : 12 570 t contre 16 372 t, présentées « en hausse de 23,22 % ». Il s’agit d’une baisse ; la conclusion (§ 4) l’indique correctement.',
      action: 'Remplacer « hausse » par « baisse ».',
    },
    {
      id: 'OBS-04', prio: 'M', cat: 'Cohérence', objet: 'Objectif de traçabilité « au moins 15 % »', statut: 'À ARBITRER',
      loc: ['3.1 – SNT, résultats (point 4)'],
      constat: 'Objectif de 300 000 t de cacao tracé « soit au moins 15 % » : ce ratio suppose une production d’environ 2,0 Mt, alors que 2 063 070 t sont déjà déclarées au 30 juin 2026 (partie 2).',
      action: 'Arbitrage requis (A-1).',
    },
    {
      id: 'OBS-05', prio: 'M', cat: 'Cohérence', objet: 'Cumuls éducation : nombres en lettres et en chiffres', statut: 'À CORRIGER',
      loc: ['Partie 3 – Éducation, § 4'],
      constat: 'Cumuls 2012-2026 : les nombres en lettres ne concordent pas avec les chiffres (« trois cent quatre-vingt-quinze (413) » classes ; de même 354 / 372 logements de maîtres et 73 / 79 cantines). Seuls les chiffres semblent actualisés.',
      action: 'Aligner les lettres sur les chiffres actualisés, après confirmation des valeurs (V-3).',
    },
    {
      id: 'OBS-06', prio: 'M', cat: 'Cohérence', objet: 'Pompes posées et forages réalisés (2012-2026)', statut: 'À VÉRIFIER',
      loc: ['Partie 3 – Hydraulique, § 3'],
      constat: '1 994 pompes posées pour 1 737 forages réalisés sur 2012-2026, soit 257 pompes de plus que d’ouvrages. Les 500 pompes réparées, citées à part, n’expliquent pas l’écart.',
      action: 'Expliquer l’écart (pose sur forages existants, par exemple) ou corriger l’un des chiffres. **À confirmer par la Direction** (V-2).',
    },
    {
      id: 'OBS-07', prio: 'M', cat: 'Données', objet: 'Montant logé à la BNI', statut: 'À CORRIGER',
      loc: ['Partie 3 – Soldes bancaires, § 2'],
      constat: 'Dépôts à la BNI : 47,48 Mds dans le texte, contre 46,38 Mds au Tableau 10. Le premier montant correspondrait au total BNI de la communication au 31 mars 2026. La mention « plus de 95 % » reste exacte (96,6 %).',
      action: 'Remplacer 47,48 par 46,38 milliards de FCFA.',
    },
    // ---------------------------------------------------------------- À CORRIGER
    {
      id: 'OBS-08', prio: 'A', cat: 'Cohérence', objet: 'Plan annoncé en introduction', statut: 'À CORRIGER',
      loc: ['Introduction, dernier §'],
      constat: 'Le plan annonce deux parties ; le document en comporte trois. La partie 3 (activités d’appui et soldes bancaires) n’est pas annoncée.',
      action: 'Annoncer la troisième partie ; écrire « deuxième » au lieu de « seconde ».',
    },
    {
      id: 'OBS-09', prio: 'A', cat: 'Institutionnel', objet: 'Dénomination des fonds et programmes', statut: 'À VÉRIFIER',
      loc: ['Introduction ; 1.3', 'Tableaux 2, 3, 7 et 8'],
      constat: 'Les fonds portent des noms différents dans le texte (FIA, Fonds de la relance caféière…) et dans les tableaux (CCC-Investissement, Diversification agricole, Programme 2QC). L’auteur indique que les intitulés de comptes ont été conservés.',
      action: 'Ajouter une note de correspondance entre fonds, programmes et intitulés de comptes (V-4).',
    },
    {
      id: 'OBS-10', prio: 'A', cat: 'Formulation', objet: 'Comparaisons « par rapport à l’année 2025 »', statut: 'À CORRIGER',
      loc: ['1.2, § 2 ; 1.3, § 2', 'Conclusion, § 5'],
      constat: 'Les hausses de janvier-juin 2026 (+60,83 % et +66,67 %) sont rapportées à « l’année 2025 », alors que la comparaison porte sur la même période de 2025.',
      action: 'Écrire « par rapport à la même période de 2025 » dans les trois passages.',
    },
    {
      id: 'OBS-11', prio: 'A', cat: 'Formulation', objet: 'Titre du Tableau 3', statut: 'À CORRIGER',
      loc: ['1.4 – Tableau 3'],
      constat: 'Le titre « Investissements réalisés de janvier à juin 2026 » ne correspond pas au contenu : le tableau présente le cumul d’octobre 2005 à juin 2026.',
      action: 'Corriger le titre : « Investissements réalisés d’octobre 2005 à fin juin 2026 ».',
    },
    {
      id: 'OBS-12', prio: 'A', cat: 'Cohérence', objet: 'Renvoi au Tableau 4 et intitulé de la ligne H', statut: 'À CORRIGER',
      loc: ['1.5, § 1 ; Tableau 4'],
      constat: 'Le solde net de 41,38 Mds est renvoyé au Tableau 4, qui n’affiche que 47,99 Mds ; il figure au Tableau 5. La ligne H du Tableau 4, dite « solde net », inclut la trésorerie (6,61 Mds).',
      action: 'Renvoyer au Tableau 5 ; aligner l’intitulé de la ligne H sur celui du solde bancaire (Tableau 5).',
    },
    {
      id: 'OBS-13', prio: 'A', cat: 'Données', objet: 'Dates erronées ou incomplètes', statut: 'À CORRIGER',
      loc: ['2.1 – Prix du cacao, § 2', 'Tableau 8 ; 3.1'],
      constat: 'Dates erronées ou incomplètes : « octobre 2024 à juin 2026 » (campagne 2024-2025) ; « au 31 juin 2026 » (sacs brousse) ; « entre le 1^er^ octobre et le 30 juin 2026 » (SNT) ; « TOTAL D’OCTOBRE A FIN JUIN 2026 » (Tableau 8).',
      action: 'Lire « juin 2025 », « 30 juin 2026 », « 1^er^ octobre 2025 » et « d’octobre 2025 à fin juin 2026 ».',
    },
    {
      id: 'OBS-14', prio: 'A', cat: 'Données', objet: 'Tableau 9 non aligné sur le Tableau 10', statut: 'À CORRIGER',
      loc: ['Partie 3 – Tableau 9'],
      constat: 'Le Tableau 9 ne concorde pas avec le Tableau 10, dont les totaux par compte sont exacts : 22,75 et 11,94 Mds (comptes CCC-Projets et CCC-Investissement) contre 22,76 et 11,93.',
      action: 'Reprendre 22,76 et 11,93 ; variations 11,04 et 8,86. Totaux inchangés (47,99 et 29,62).',
    },
    {
      id: 'OBS-15', prio: 'A', cat: 'Données', objet: 'Hausse de 66,69 % en conclusion', statut: 'À CORRIGER',
      loc: ['Conclusion, § 5'],
      constat: 'La hausse des redevances d’investissement est chiffrée à 66,69 %, contre 66,67 % au § 1.3 et au Tableau 2 (35,05 / 21,03).',
      action: 'Retenir 66,67 %.',
    },
    // ---------------------------------------------------------------- FORME
    {
      id: 'OBS-16', prio: 'F', cat: 'Forme', objet: 'Accentuation des majuscules', statut: 'À CORRIGER',
      loc: ['En-tête ; titres des parties 1 et 2', 'Tableaux 3 et 8 ; signatures'],
      constat: 'Accentuation des majuscules non harmonisée : « MINISTÈRE » mais « ECONOMIE » ; « ÉVOLUTION » et « EVOLUTION » ; « A FIN JUIN » ; « l’Etat », « l’Economie ». « conseil du café-cacao » en minuscules (3.1).',
      action: 'Accentuer toutes les majuscules (É, À) ; rétablir « Conseil du Café-Cacao ».',
    },
    {
      id: 'OBS-17', prio: 'F', cat: 'Forme', objet: 'Accords et orthographe', statut: 'À CORRIGER',
      loc: ['Introduction ; Tableau 2', '3.1 ; partie 3'],
      constat: 'Accords et orthographe : « demeure supérieure » ; « Il est composé » (la fiscalité) ; « Régénérat° » ; « plants équivalent » ; « a été mis en place » (la Plateforme) ; « recensement… achevée » ; « soixante -six », « vingt -un » ; « cinq cent (500) ».',
      action: 'Lire « supérieur », « Elle est composée », « Régénération », « équivalents », « mise », « achevé », « soixante-six », « vingt et un », « cinq cents ».',
    },
    {
      id: 'OBS-18', prio: 'F', cat: 'Forme', objet: 'Doublons et mots superflus', statut: 'À CORRIGER',
      loc: ['Tableaux 1 et 2', '3.1 ; partie 3'],
      constat: 'Doublons, mots superflus ou manquants : « de construction de construction » ; « pour les pour les » ; « à nouveau » (en-têtes) ; « couvrir de » ; « taux d’exécution est de » ; « démarré également » ; « en lien le rythme » ; point manquant avant « À partir du 1^er^ septembre ».',
      action: 'Supprimer doublons et mots superflus ; lire « en lien avec le rythme » ; rétablir le point.',
    },
    {
      id: 'OBS-19', prio: 'F', cat: 'Forme', objet: 'Écriture des nombres et des unités', statut: 'À CORRIGER',
      loc: ['1.1 ; 2.1 ; 3.1', 'Partie 3'],
      constat: 'Écriture des nombres hétérogène : points comme séparateurs de milliers (593.465 ; 1.000.000 ; 1.101.000 ; 1.994…) ; montants sans unité (7,1 et 2,48 milliards) ; « CFA » au lieu de « FCFA » (2,42 milliards ; 464 millions).',
      action: 'Espace comme séparateur de milliers ; « de FCFA » après chaque montant.',
    },
    {
      id: 'OBS-20', prio: 'F', cat: 'Données', objet: 'Règles d’arrondi', statut: 'À CORRIGER',
      loc: ['Tableau 1 ; 3.1'],
      constat: 'Arrondis non homogènes : taux tronqués (105,01 % pour 105,015 % ; 50,15 % pour 50,155 % ; 92,68 % pour 92,6875 %) ; variations du Tableau 1 non retrouvables à partir des montants affichés (2,91 / 1,88 donne +54,79 %, contre +54,50 % affiché).',
      action: 'Arrondir au plus proche ; préciser en note que les variations portent sur des valeurs non arrondies.',
    },
    {
      id: 'OBS-21', prio: 'F', cat: 'Formulation', objet: 'Période du total d’arrachage (swollen shoot)', statut: 'À CORRIGER',
      loc: ['3.1 – Swollen shoot, § 4'],
      constat: 'Le total de 195 625,4 ha est donné sans période. Les § 1 et 3 établissent qu’il couvre 2018-2025 (105 015,01 + 90 610,39 ha). « Près de » ne convient pas à un chiffre donné à la décimale.',
      action: 'Préciser « sur la période 2018-2025 » (et non 2021-2025) ; supprimer « près de ».',
    },
  ],

  arbitrages: [
    {
      ref: 'A-1', sujet: 'Objectif de traçabilité 2025-2026', lien: 'OBS-04',
      probleme: '« Au moins 300 000 t, soit au moins 15 % » : le ratio suppose une production de 2,0 Mt, déjà dépassée au 30 juin 2026 (2 063 070 t ; 300 000 t n’en représentent que 14,5 %).',
      arbitrage: 'Retenir l’une des options : recalculer le pourcentage sur la production prévisionnelle de la campagne ; relever l’objectif en volume ; ne conserver que l’objectif en volume.',
    },
    {
      ref: 'A-2', sujet: 'Échéances postérieures au 30 juin 2026', lien: '3.1 ; partie 3 ; introduction',
      probleme: 'Le texte présente au futur des échéances aujourd’hui passées : fin de la campagne intermédiaire (31 août 2026), ouverture de la campagne 2026-2027 et digitalisation des achats bord champ (1^er^ septembre 2026), travaux d’électrification (juillet 2026), objectif SNT (30 septembre 2026).',
      arbitrage: 'Maintenir la rédaction arrêtée au 30 juin 2026, en le précisant, ou actualiser ces passages à la date de présentation en Conseil des Ministres.',
    },
  ],

  verifications: [
    { ref: 'V-1', lien: 'OBS-01', texte: 'Confirmer auprès du Conseil du Café-Cacao le revenu brut des producteurs de cacao de janvier à juin 2026 et sa variation, à partir des volumes et prix sources.' },
    { ref: 'V-2', lien: 'OBS-06', texte: 'Obtenir du Conseil du Café-Cacao l’explication de l’écart entre pompes posées (1 994) et forages réalisés (1 737) sur 2012-2026, ou les valeurs corrigées.' },
    { ref: 'V-3', lien: 'OBS-05', texte: 'Confirmer les cumuls 2012-2026 des classes, logements de maîtres et cantines (413, 372 et 79) au 30 juin 2026.' },
    { ref: 'V-4', lien: 'OBS-09', texte: 'Confirmer la correspondance entre fonds, programmes et intitulés de comptes (FIA, Fonds de la relance caféière, Programme 2QC).' },
  ],

  suivi: {
    fichierTitre: 'Fiche de suivi des corrections – CCM café-cacao au 30 juin 2026',
    fichierSujet: 'Suivi des corrections demandées sur la Communication en Conseil des Ministres relative aux redevances café-cacao au 30 juin 2026',
    titre: 'FICHE DE SUIVI DES CORRECTIONS',
    sousTitre: 'Réponse de la structure émettrice aux observations de la fiche de revue du 1^er^ octobre 2026',
    identification: {
      document: 'Communication en Conseil des Ministres – Informations relatives à la collecte et à l’utilisation des redevances prélevées sur la filière café-cacao au 30 juin 2026',
      champs: [
        { label: 'Structure émettrice', valeur: 'MINADER – MEFB', note: 'Communication conjointe' },
        { label: 'Version examinée', valeur: 'Version du 12 août 2026' },
        { label: 'Fiche de revue', valeur: '1^er^ octobre 2026', note: '21 observations · 2 arbitrages' },
        { label: 'Version corrigée', valeur: '[[Date à renseigner]]' },
      ],
      objet: 'Retour, observation par observation, sur la prise en compte des corrections demandées',
    },
    consigne: 'Pour chaque observation, choisir le statut retenu dans la colonne « Statut » (liste déroulante sous Word) et indiquer la suite donnée ou, en cas de maintien de la rédaction initiale, sa justification. Les références OBS et A renvoient à la fiche de revue du 1^er^ octobre 2026.',
    piedDePage: 'Cabinet du Ministre  ·  Fiche de suivi des corrections  ·  CCM café-cacao au 30 juin 2026',
  },

  suiteADonner: 'Il est proposé de retourner le projet de communication à la structure émettrice pour prise en compte des observations ci-dessus avant toute transmission. Le point critique OBS-01 doit être levé en priorité, sur la base des données du Conseil du Café-Cacao. Les arbitrages A-1 et A-2 sont à soumettre à la validation du Cabinet. La version corrigée pourra être accompagnée de la fiche de suivi des corrections dûment renseignée.',
};
