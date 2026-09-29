// Sections 8 à 11
const { Paragraph, TextRun, AlignmentType, Table, TableRow, VerticalAlign, WidthType, ExternalHyperlink } = require('docx');
const L = require('./lib');
const { P, B, H1, H2, H3, CAPTION, SOURCE, TABLE, CELL, SP, C, TINT, FONT, GREY, fr, rt, none } = L;
const { M } = require('./mathh');
const { AXES, IND } = require('./indicators');

const WL = 14570; // largeur utile en paysage

function recapA() {
  const rows = [];
  AXES.forEach((a) => {
    IND.filter((i) => i.axe === a.n).forEach((i, j) => {
      const row = [];
      if (j === 0) row.push({ c: `${a.n}. ${a.nom}`, rowSpan: 3, fill: TINT, bold: true, color: C, valign: VerticalAlign.CENTER });
      row.push({ c: `${a.n}.${i.k} ${i.nom}`, bold: true });
      row.push(i.definition);
      row.push(i.formuleTxt);
      row.push(i.numerateur);
      row.push(i.denominateur);
      row.push(i.unite);
      row.push({ c: (i.sens === 'Hausse' ? '↑ ' : '↓ ') + i.sens, align: AlignmentType.CENTER });
      rows.push(row);
    });
  });
  return TABLE({ widths: [1300, 1900, 2600, 2500, 2000, 2000, 1000, 1270], size: 15, headSize: 16,
    head: ['Axe', 'Indicateur', 'Définition', 'Formule', 'Numérateur', 'Dénominateur', 'Unité', 'Sens souhaité'], rows });
}
function recapB() {
  const rows = IND.map((i) => [
    { c: `${i.axe}.${i.k} ${i.nom}`, bold: true, fill: TINT },
    i.frequence, i.srcP, i.srcS, i.dispo, i.limites, i.comparabilite, i.observations,
  ]);
  return TABLE({ widths: [1800, 1100, 2000, 1900, 2100, 2300, 1700, 1670], size: 15, headSize: 16,
    head: ['Axe et indicateur', 'Fréquence souhaitée', 'Source statistique principale', 'Source secondaire', 'Disponibilité historique', 'Limites méthodologiques', 'Comparabilité internationale', 'Observations'], rows });
}

function section8() {
  return [
    H1('8. Tableau méthodologique final', { pageBreak: false }),
    P('Le tableau méthodologique rassemble, pour les quinze indicateurs, les quinze rubriques qui en fixent le calcul et l\'usage. Pour préserver la lisibilité, il est présenté en deux parties : la première (tableau 8) décrit le contenu de chaque indicateur ; la seconde (tableau 9) en précise les conditions de production et de lecture. Les informations sont strictement identiques à celles des fiches de l\'annexe, qui en constituent la version détaillée. Dans la colonne « disponibilité historique », seuls les éléments vérifiés dans les sources originales sont mentionnés ; les autres portent la mention « disponibilité de la série à vérifier ».', { size: 22 }),
    CAPTION('Tableau méthodologique final (1/2) — contenu des indicateurs'),
    recapA(),
    new Paragraph({ pageBreakBefore: true, children: [] }),
    CAPTION('Tableau méthodologique final (2/2) — production et lecture des indicateurs'),
    recapB(),
    SOURCE('Sigles : voir la liste des sigles et abréviations. Les indices i, t et 0 désignent respectivement le produit ou la filière, l\'année et la période de référence.'),
  ];
}

// ─────────────── Section 9 : schéma de cohérence
function section9() {
  const axes = [
    ['SOUVERAINETÉ ALIMENTAIRE', 'Nourrir durablement la population', '1.1 · 1.2 · 1.3'],
    ['COMPÉTITIVITÉ', 'Produire efficacement, réduire les pertes et transformer', '2.1 · 2.2 · 2.3'],
    ['FINANCEMENT', 'Permettre aux acteurs d\'investir', '3.1 · 3.2 · 3.3'],
    ['FONCIER', 'Sécuriser les droits nécessaires à l\'investissement de long terme', '4.1 · 4.2 · 4.3'],
    ['DURABILITÉ', 'Préserver le capital naturel qui permet la production future', '5.1 · 5.2 · 5.3'],
  ];
  const widths = [2900, 520, 4250, 1400];
  const rows = [];
  axes.forEach((a, i) => {
    rows.push(new TableRow({ cantSplit: true, children: [
      CELL(a[0], { w: widths[0], fill: C, color: 'FFFFFF', bold: true, size: 20, align: AlignmentType.CENTER, valign: VerticalAlign.CENTER, borders: { top: none, bottom: none, left: none, right: none } }),
      CELL('→', { w: widths[1], size: 26, color: C, align: AlignmentType.CENTER, valign: VerticalAlign.CENTER, borders: { top: none, bottom: none, left: none, right: none } }),
      CELL(a[1], { w: widths[2], fill: TINT, size: 21, italics: true, valign: VerticalAlign.CENTER, borders: { top: none, bottom: none, left: none, right: none } }),
      CELL(a[2], { w: widths[3], fill: TINT, size: 18, color: C, align: AlignmentType.CENTER, valign: VerticalAlign.CENTER, borders: { top: none, bottom: none, left: none, right: none } }),
    ] }));
    if (i < axes.length - 1) {
      rows.push(new TableRow({ children: [
        CELL('▼', { w: widths[0], size: 16, color: C, align: AlignmentType.CENTER, borders: { top: none, bottom: none, left: none, right: none } }),
        CELL('', { w: widths[1] + widths[2] + widths[3], span: 3, borders: { top: none, bottom: none, left: none, right: none } }),
      ] }));
    }
  });
  const scheme = new Table({ width: { size: 9070, type: WidthType.DXA }, columnWidths: widths, rows });

  return [
    H1('9. Schéma de cohérence des cinq axes', { pageBreak: false }),
    P('Les cinq axes ne constituent pas cinq tableaux de bord juxtaposés. Ils décrivent les conditions successives et interdépendantes d\'une même transformation. Le schéma ci-dessous en présente la logique d\'ensemble ; la colonne de droite rappelle les indicateurs rattachés à chaque axe.'),
    CAPTION('Logique d\'ensemble du dispositif'),
    scheme,
    SP(200),
    P('La lecture verticale du schéma ne doit pas masquer les relations transversales entre axes. Plusieurs d\'entre elles se lisent directement dans les indicateurs, ce qui justifie une analyse croisée lors de chaque exercice de suivi. Les liens présentés ci-dessous sont des hypothèses de lecture fondées sur la littérature ; le dispositif ne prétend pas en mesurer l\'intensité causale.'),
    CAPTION('Principales interdépendances entre les axes'),
    TABLE({ widths: [1900, 4870, 2300], head: ['Relation', 'Mécanisme attendu', 'Indicateurs à lire ensemble'], size: 19, rows: [
      ['Foncier → financement', 'Des droits formalisés allongent l\'horizon d\'investissement et peuvent faciliter la garantie des prêts ; la littérature invite à la prudence sur ce second canal en Afrique (Lawry et al., 2017).', '4.1, 4.3 et 3.2, 3.3'],
      ['Financement → compétitivité', 'Le crédit de moyen et long terme finance la mécanisation, le stockage, le renouvellement des vergers et la transformation.', '3.3 et 2.1, 2.2, 2.3'],
      ['Compétitivité → souveraineté', 'Des rendements plus élevés et des pertes moindres accroissent la production disponible par habitant.', '2.1, 2.2 et 1.1, 1.2'],
      ['Compétitivité ↔ durabilité', 'Les gains de rendement réduisent la pression sur les forêts (découplage), mais l\'intensification peut accroître certaines émissions.', '2.1 et 5.2, 5.3'],
      ['Foncier → durabilité', 'La sécurité des droits, y compris des exploitants non propriétaires, favorise les investissements de long terme dans les sols et l\'agroforesterie.', '4.1, 4.3 et 5.1'],
      ['Durabilité → souveraineté', 'La préservation des sols, des forêts et du climat conditionne la stabilité de la production future.', '5.1, 5.2 et 1.3'],
    ] }),
    SOURCE('Source : analyse des auteurs.'),
    P('Cette architecture explique aussi les choix de périmètre destinés à éviter les doubles comptes : les émissions liées à la déforestation sont exclues de l\'intensité des émissions (5.3) parce qu\'elles sont saisies par le taux de déforestation (5.2) ; l\'axe durabilité se limite à la dimension environnementale parce que les dimensions économique et sociale sont couvertes par les axes 2 à 4 ; les contrats d\'exploitation sont exclus du taux de couverture foncière (4.1) parce qu\'ils font l\'objet d\'un indicateur propre (4.3).'),
  ];
}

// ─────────────── Section 10 : références
const REFS = [
  ['Cadres de référence transversaux', [
    'Union africaine (2025). *Kampala CAADP Declaration on Building Resilient and Sustainable Agrifood Systems in Africa* et *CAADP Strategy and Action Plan 2026-2035*. Adoptés lors du Sommet extraordinaire de Kampala, 9-11 janvier 2025. https://au.int/en/pressreleases/20250506/au-launches-caadp-strategy-action-plan-2026-2035-caadp-kampala-declaration (consulté le 29 septembre 2026).',
    'ReSAKSS (2025). *Kampala CAADP Declaration & CAADP Strategy and Action Plan (2026-2035)*. Regional Strategic Analysis and Knowledge Support System, IFPRI / AKADEMIYA2063. https://www.resakss.org/node/6927 (consulté le 29 septembre 2026).',
    'Union africaine (2014). *Déclaration de Malabo sur la croissance et la transformation accélérées de l\'agriculture en Afrique pour une prospérité partagée et de meilleures conditions de vie*. Commission de l\'Union africaine, Addis-Abeba.',
    'FAO. *FAOSTAT*, base de données statistique de l\'Organisation des Nations unies pour l\'alimentation et l\'agriculture. https://www.fao.org/faostat/ (consulté le 29 septembre 2026).',
  ]],
  ['Axe 1 — Souveraineté alimentaire', [
    'FAO (2001). *Food Balance Sheets – A Handbook*. Rome, Organisation des Nations unies pour l\'alimentation et l\'agriculture. https://www.fao.org/4/x9892e/x9892e00.htm (consulté le 29 septembre 2026).',
    'FAO. *FAO indices of agricultural production*, note méthodologique du domaine FAOSTAT « Production indices ». https://files-faostat.fao.org/production/QI/QI_e.pdf (consulté le 29 septembre 2026).',
    'FAO. *Suite of Food Security Indicators*, FAOSTAT (indicateurs de variabilité de la production et des disponibilités alimentaires par habitant). https://www.fao.org/faostat/en/#data/FS (consulté le 29 septembre 2026).',
    'Clapp, J. (2017). Food self-sufficiency: Making sense of it, and when it makes sense. *Food Policy*, 66, 88-96.',
  ]],
  ['Axe 2 — Compétitivité de l\'agriculture', [
    'Latruffe, L. (2010). *Competitiveness, Productivity and Efficiency in the Agricultural and Agri-Food Sectors*. OECD Food, Agriculture and Fisheries Papers, n° 30, OCDE, Paris. https://doi.org/10.1787/5km91nkdt6d6-en.',
    'FAO (2019). *The State of Food and Agriculture 2019. Moving forward on food loss and waste reduction*. Rome. https://www.fao.org/3/ca6030en/ca6030en.pdf (consulté le 29 septembre 2026).',
    'FAO. *Indicateur ODD 12.3.1 – Pertes alimentaires mondiales* (indice des pertes alimentaires, 12.3.1a), portail des indicateurs ODD de la FAO. https://www.fao.org/sustainable-development-goals-data-portal/data/indicators/1231-global-food-losses/en/ (consulté le 29 septembre 2026).',
    'Affognon, H., Mutungi, C., Sanginga, P. et Borgemeister, C. (2015). Unpacking postharvest losses in sub-Saharan Africa: A meta-analysis. *World Development*, 66, 49-68.',
    'Hodges, R. J., Buzby, J. C. et Bennett, B. (2011). Postharvest losses and waste in developed and less developed countries: opportunities to improve resource use. *The Journal of Agricultural Science*, 149(S1), 37-45.',
    'Barrett, C. B., Reardon, T., Swinnen, J. et Zilberman, D. (2022). Agri-food value chain revolutions in low- and middle-income countries. *Journal of Economic Literature*, 60(4), 1316-1377.',
    'Banque mondiale (2013). *Growing Africa: Unlocking the Potential of Agribusiness*. Washington, D.C.',
    'USDA Economic Research Service. *International Agricultural Productivity – Documentation and Methods*. https://ers.usda.gov/data-products/international-agricultural-productivity/documentation-and-methods (consulté le 29 septembre 2026).',
  ]],
  ['Axe 3 — Accès au financement agricole', [
    'Stiglitz, J. E. et Weiss, A. (1981). Credit rationing in markets with imperfect information. *American Economic Review*, 71(3), 393-410.',
    'Kon, Y. et Storey, D. J. (2003). A theory of discouraged borrowers. *Small Business Economics*, 21(1), 37-49.',
    'Boucher, S. R., Carter, M. R. et Guirkinger, C. (2008). Risk rationing and wealth effects in credit markets: Theory and implications for agricultural development. *American Journal of Agricultural Economics*, 90(2), 409-423.',
    'Christen, R. P. et Anderson, J. (2013). *Segmentation of Smallholder Households: Meeting the Range of Financial Needs in Agricultural Families*. Focus Note n° 85, CGAP, Washington, D.C. https://www.cgap.org/research/publication/segmentation-of-smallholder-households (consulté le 29 septembre 2026).',
    'Banque mondiale (2025). *The Global Findex Database 2025: Connectivity and Financial Inclusion in the Digital Economy*. Washington, D.C. https://www.worldbank.org/en/publication/globalfindex/report (consulté le 29 septembre 2026).',
    'BCEAO. *Bulletin mensuel des statistiques* (utilisations de crédits déclarées à la Centrale des risques, par secteur d\'activité et par terme), éditions successives. https://www.bceao.int (consulté le 29 septembre 2026).',
    'BCEAO. *Base de données économiques et financières EDEN*. https://edenpub.bceao.int/ (consulté le 29 septembre 2026).',
  ]],
  ['Axe 4 — Sécurisation du foncier rural', [
    'République de Côte d\'Ivoire. Loi n° 98-750 du 23 décembre 1998 relative au domaine foncier rural, modifiée par les lois n° 2004-412 du 14 août 2004, n° 2013-655 du 13 septembre 2013 et n° 2019-868 du 14 octobre 2019. Texte initial : FAOLEX, https://www.fao.org/faolex/results/details/en/c/LEX-FAOC015631/ (consulté le 29 septembre 2026).',
    'République de Côte d\'Ivoire. Décret n° 2016-590 du 3 août 2016 portant création, attributions, organisation et fonctionnement de l\'Agence foncière rurale (AFOR).',
    'République de Côte d\'Ivoire. Décret n° 2019-263 du 27 mars 2019 portant définition de la procédure de délimitation des territoires des villages (abrogeant le décret n° 2013-296 du 2 mai 2013).',
    'République de Côte d\'Ivoire. Décret n° 2024-850 du 30 septembre 2024 fixant les règles relatives à l\'opération intégrée de sécurisation foncière rurale.',
    'République de Côte d\'Ivoire. Ordonnance n° 2025-85 du 12 février 2025 portant création, attributions, organisation et fonctionnement du Système d\'information foncière rurale (SIFOR). Intitulé exact et loi de ratification à confirmer au Journal officiel.',
    'Ministère d\'État, ministère de l\'Agriculture, du Développement rural et des Productions vivrières (2023). *Stratégie nationale et Programme national de sécurisation foncière rurale 2023-2033*, adoptés par le Gouvernement le 15 juin 2023. Document diffusé par l\'AFOR : https://www.afor.ci (consulté le 29 septembre 2026).',
    'FAO (2012). *Directives volontaires pour une gouvernance responsable des régimes fonciers applicables aux terres, aux pêches et aux forêts dans le contexte de la sécurité alimentaire nationale*. Rome, Comité de la sécurité alimentaire mondiale. https://www.fao.org/4/i2801f/i2801f.pdf (consulté le 29 septembre 2026).',
    'Commission de l\'Union africaine, Commission économique pour l\'Afrique et Banque africaine de développement (2010). *Cadre et lignes directrices sur les politiques foncières en Afrique*. Addis-Abeba. https://au.int/en/documents/20110131/framework-and-guidelines-land-policy-africa (consulté le 29 septembre 2026).',
    'Besley, T. (1995). Property rights and investment incentives: Theory and evidence from Ghana. *Journal of Political Economy*, 103(5), 903-937.',
    'Lawry, S., Samii, C., Hall, R., Leopold, A., Hornby, D. et Mtero, F. (2017). The impact of land property rights interventions on investment and agricultural productivity in developing countries: a systematic review. *Journal of Development Effectiveness*, 9(1), 61-81. https://doi.org/10.1080/19439342.2016.1160947.',
    'Colin, J.-Ph. (2013). Securing rural land transactions in Africa. An Ivorian perspective. *Land Use Policy*, 31, 430-440. https://www.sciencedirect.com/science/article/abs/pii/S0264837712001482.',
    'ObservaTerra. *Observatoire de la sécurisation foncière rurale en Côte d\'Ivoire*. https://www.observaterra.ci (consulté le 29 septembre 2026).',
  ]],
  ['Axe 5 — Durabilité des systèmes de production', [
    'FAO. *Indicateur ODD 2.4.1 – Proportion de la superficie agricole exploitée de manière productive et durable*, métadonnées et portail des indicateurs. https://www.fao.org/sustainable-development-goals-data-portal/data/indicators/Indicator2.4.1-proportion-of-agricultural-area-under-productive-and-sustainable-agriculture/en (consulté le 29 septembre 2026).',
    'FAO (2020). *Global Forest Resources Assessment 2020: Main report*. Rome. https://doi.org/10.4060/ca9825en.',
    'FAO. *FAOSTAT domain Emission indicators – Methodological note*, octobre 2023. https://files-faostat.fao.org/production/EM/EM_en.pdf (consulté le 29 septembre 2026).',
    'GIEC (2006). *Lignes directrices 2006 du GIEC pour les inventaires nationaux de gaz à effet de serre*, volume 4 : Agriculture, foresterie et autres affectations des terres ; et *Refinement 2019*. IGES, Japon.',
    'Tubiello, F. N., Salvatore, M., Rossi, S., Ferrara, A., Fitton, N. et Smith, P. (2013). The FAOSTAT database of greenhouse gas emissions from agriculture. *Environmental Research Letters*, 8(1), 015009.',
    'République de Côte d\'Ivoire (2022). *Contribution déterminée au niveau national (CDN) révisée*, soumise à la CCNUCC. Référence FAOLEX : https://www.fao.org/faolex/results/details/en/c/LEX-FAOC219858/ (consulté le 29 septembre 2026).',
    'Hansen, M. C. et al. (2013). High-resolution global maps of 21st-century forest cover change. *Science*, 342(6160), 850-853.',
    'Curtis, P. G., Slay, C. M., Harris, N. L., Tyukavina, A. et Hansen, M. C. (2018). Classifying drivers of global forest loss. *Science*, 361(6407), 1108-1111.',
    'Pendrill, F. et al. (2022). Disentangling the numbers behind agriculture-driven tropical deforestation. *Science*, 377(6611), eabm9267.',
    'Vancutsem, C. et al. (2021). Long-term (1990–2019) monitoring of forest cover changes in the humid tropics. *Science Advances*, 7(10), eabe1603.',
    'Kalischek, N., Lang, N., Renier, C. et al. (2023). Cocoa plantations are associated with deforestation in Côte d\'Ivoire and Ghana. *Nature Food*, 4, 384-393. https://doi.org/10.1038/s43016-023-00751-8.',
    'Puyravaud, J.-P. (2003). Standardizing the calculation of the annual rate of deforestation. *Forest Ecology and Management*, 177(1-3), 593-596.',
    'Pretty, J. et al. (2018). Global assessment of agricultural system redesign for sustainable intensification. *Nature Sustainability*, 1, 441-446.',
    'ARSO (2021). *ARS 1000 – Cacao durable*, norme régionale africaine (série ARS 1000), rendue obligatoire en Côte d\'Ivoire par décret du 8 juin 2022 (numéro à confirmer au Journal officiel).',
    'Union européenne (2023). Règlement (UE) 2023/1115 du Parlement européen et du Conseil du 31 mai 2023 relatif aux produits sans déforestation. *Journal officiel de l\'Union européenne*, L 150. https://eur-lex.europa.eu/eli/reg/2023/1115/oj.',
  ]],
];

function refPara(t) {
  return new Paragraph({
    alignment: AlignmentType.LEFT,
    spacing: { after: 100, line: 252 , lineRule: 'auto'},
    indent: { left: 360, hanging: 360 },
    children: rt(t, { size: 21 }),
  });
}

function section10() {
  const out = [
    H1('10. Références scientifiques et institutionnelles'),
    P('Les références sont regroupées par axe ; les cadres transversaux sont présentés en premier. Priorité a été donnée aux textes réglementaires, aux documents gouvernementaux, aux publications des institutions internationales et aux articles de revues à comité de lecture. Les adresses électroniques ont été vérifiées à la date indiquée. Deux références législatives récentes portent la mention « à confirmer » : leur existence est établie, mais leur intitulé exact doit être contrôlé au Journal officiel avant diffusion externe.', { size: 22 }),
  ];
  REFS.forEach(([title, list]) => {
    out.push(H3(title));
    list.forEach((t) => out.push(refPara(t)));
  });
  return out;
}

// ─────────────── Section 11 : fiches
function fiche(i, idx) {
  const axe = AXES.find((a) => a.n === i.axe);
  const W1 = 2500, W2 = 6570;
  const rowsSpec = [
    ['Nom de l\'indicateur', `${i.nom} (${i.code})`],
    ['Axe', `Axe ${axe.n} — ${axe.nom}`],
    ['Finalité', i.finalite],
    ['Question à laquelle il répond', i.question],
    ['Définition', i.definition],
    ['Formule', 'MATH'],
    ['Variables nécessaires', i.variables],
    ['Unité', i.unite],
    ['Sens souhaité', (i.sens === 'Hausse' ? '↑ ' : '↓ ') + i.sens],
    ['Périodicité', i.frequence],
    ['Sources possibles', `Principale : ${i.srcP}\nSecondaires : ${i.srcS}`],
    ['Méthode d\'agrégation', i.agregation],
    ['Pondérations éventuelles', i.ponderations],
    ['Précautions méthodologiques', i.precautions],
    ['Limites', i.limites],
    ['Référence scientifique principale', i.reference],
    ['Disponibilité pour la Côte d\'Ivoire', i.dispo],
    ['Travaux restant à conduire', i.travaux],
  ];
  const rows = rowsSpec.map(([k, v]) => {
    let content;
    if (v === 'MATH') {
      content = [
        new Paragraph({ alignment: AlignmentType.LEFT, spacing: { before: 60, after: 60 }, children: i.math() }),
        new Paragraph({ spacing: { after: 30 }, children: rt('Numérateur : ' + i.numerateur, { size: 18 }) }),
        new Paragraph({ spacing: { after: 30 }, children: rt('Dénominateur : ' + i.denominateur, { size: 18 }) }),
      ];
    } else content = v;
    return new TableRow({ cantSplit: true, children: [
      CELL(k, { w: W1, fill: TINT, bold: true, color: C, size: 18 }),
      CELL(content, { w: W2, size: 18 }),
    ] });
  });
  return [
    new Paragraph({ heading: 'Heading2', pageBreakBefore: idx > 0, children: [new TextRun({ text: fr(`Fiche ${i.axe}.${i.k} — ${i.nom}`) })] }),
    new Table({ width: { size: W1 + W2, type: WidthType.DXA }, columnWidths: [W1, W2], rows }),
  ];
}

function section11() {
  return [
    H1('11. Annexe — Fiches indicateurs'),
    P('Chaque fiche présente, selon une structure identique, les éléments nécessaires au calcul, à l\'interprétation et à la mise à jour d\'un indicateur. Les fiches reprennent exactement les définitions, formules et paramètres des chapitres 3 à 8. Elles distinguent les éléments arrêtés (définition, formule, sens souhaité) des travaux restant à conduire, qui portent sur des paramètres de mise en œuvre et sur la disponibilité des données.'),
    P('Aucune valeur historique ni aucune cible n\'y figure. Les valeurs de référence et les cibles 2030 seront établies dans un document distinct, une fois les séries reconstituées selon la présente méthodologie.'),
    ...IND.flatMap(fiche),
  ];
}

module.exports = { section8, section9, section10, section11, WL };
