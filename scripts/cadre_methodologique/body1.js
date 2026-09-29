// Sections 1 à 4
const { AlignmentType, Paragraph, TextRun, VerticalAlign } = require('docx');
const L = require('./lib');
const { P, PL, B, N, H1, H2, H3, LOGIC, EQ, CAPTION, SOURCE, TABLE, BOX, DEF, SP, C, TINT, FONT } = L;
const { r, sb, sp, ss, fr, sum, br, M, w0 } = require('./mathh');
const { AXES, IND } = require('./indicators');

const W = 9070;

function statusBox() {
  return BOX([
    P('Le présent document distingue trois niveaux de statut, signalés de manière homogène dans chaque chapitre.', { size: 22, after: 80 }),
    B('Les **éléments arrêtés** comprennent les cinq axes, les quinze indicateurs principaux, leurs définitions et leurs formules de calcul. Ils ne sont pas remis en cause ici.', 0, { size: 22 }),
    B('Les **précisions méthodologiques à documenter** portent sur des paramètres de mise en œuvre (composition d\'un panier, période de référence, stade de transformation, liste d\'actes admissibles, etc.) qui doivent être fixés avant le calcul des séries, sans modifier l\'indicateur.', 0, { size: 22 }),
    B('Les **indicateurs complémentaires** sont mentionnés à titre secondaire, pour éclairer la lecture des indicateurs principaux ; ils n\'ont pas vocation à figurer dans le tableau de bord principal.', 0, { size: 22 }),
    P('Lorsqu\'une série n\'a pas pu être vérifiée dans sa source originale, la mention « Disponibilité de la série à vérifier » est portée explicitement. Aucune valeur historique ni aucune cible n\'est avancée dans ce document.', { size: 22, after: 40 }),
  ], { title: 'Convention de lecture' });
}

function chainTable() {
  const steps = ['Nourrir durablement la population', 'Produire de manière compétitive', 'Permettre aux acteurs d\'accéder au financement', 'Sécuriser les droits sur la terre', 'Préserver durablement les ressources productives'];
  const bw = 1534, aw = 350;
  const widths = []; const cells = [];
  steps.forEach((s, i) => {
    widths.push(bw); cells.push({ c: s, fill: TINT, align: AlignmentType.CENTER, valign: VerticalAlign.CENTER, size: 19, color: C, bold: true });
    if (i < steps.length - 1) { widths.push(aw); cells.push({ c: '→', align: AlignmentType.CENTER, valign: VerticalAlign.CENTER, size: 24, color: C }); }
  });
  return TABLE({ widths, rows: [cells], size: 19 });
}

function matrix() {
  const rows = [];
  AXES.forEach((a) => {
    IND.filter((i) => i.axe === a.n).forEach((i, j) => {
      const row = [];
      if (j === 0) row.push({ c: `Axe ${a.n}\n${a.nom}`, rowSpan: 3, fill: TINT, bold: true, color: C, valign: VerticalAlign.CENTER });
      row.push(i.dim);
      row.push(`${a.n}.${i.k}  ${i.nom}`);
      row.push({ c: (i.sens === 'Hausse' ? '↑ ' : '↓ ') + i.sens + ' souhaitée', align: AlignmentType.CENTER, valign: VerticalAlign.CENTER });
      rows.push(row);
    });
  });
  return TABLE({ widths: [2050, 2150, 3470, 1400], head: ['Axe', 'Dimension suivie', 'Indicateur', 'Sens souhaité'], rows, size: 18 });
}

function section1() {
  return [
    H1('1. Introduction'),
    P('La vision agricole de la Côte d\'Ivoire vise une transformation structurelle du secteur, c\'est-à-dire un changement durable dans la manière dont le pays produit, finance, sécurise et préserve son agriculture. Une telle transformation ne peut être appréciée par un indicateur unique. Le dispositif de suivi retenu repose donc sur cinq dimensions complémentaires, chacune éclairant une condition distincte de cette transformation : la souveraineté alimentaire, la compétitivité de l\'agriculture, l\'accès au financement agricole, la sécurisation du foncier rural et la durabilité des systèmes de production.'),
    P('Ces cinq dimensions obéissent à une logique d\'enchaînement. La finalité première est de nourrir durablement la population ; elle suppose un appareil productif compétitif, qui ne peut se développer sans financement ; l\'investissement, en particulier celui de long terme, dépend de la sécurité des droits sur la terre ; l\'ensemble n\'est soutenable que si les ressources naturelles qui conditionnent la production future sont préservées.'),
    chainTable(),
    SP(160),
    P('Trois indicateurs ont été retenus pour chaque dimension, soit quinze indicateurs principaux. Ce nombre résulte d\'un arbitrage explicite entre exhaustivité et lisibilité. Il permet d\'éviter un tableau de bord trop lourd, dont la lecture par le décideur deviendrait incertaine, tout en couvrant, pour chaque axe, trois facettes distinctes et non redondantes du phénomène suivi. Le choix a également privilégié des indicateurs directement interprétables, dont le sens de variation souhaité est univoque, ainsi que des indicateurs pour lesquels une reconstitution historique sur une dizaine d\'années est envisageable. Enfin, chaque fois que cela était pertinent, les définitions ont été alignées sur des normes internationales (FAO, objectifs de développement durable, PDDAA) afin de permettre des comparaisons dans le temps et, lorsque cela a un sens, avec d\'autres pays.'),
    P('Le présent document constitue la référence méthodologique du dispositif. Il a vocation à servir de base à la reconstitution des séries historiques sur la période 2015-2025, à la construction du tableau de bord, à la fixation des valeurs de référence puis des cibles à l\'horizon 2030. Il doit aussi permettre de justifier chaque indicateur devant un décideur, un statisticien, un économiste ou un évaluateur externe. C\'est pourquoi chaque chapitre expose la définition retenue, la logique du choix des indicateurs, leurs formules de calcul et les précautions nécessaires à leur mise en œuvre.'),
    statusBox(),
    SP(),
    P('Le chapitre 2 présente la matrice des quinze indicateurs. Les chapitres 3 à 7 détaillent chaque axe. Le chapitre 8 rassemble les paramètres méthodologiques dans un tableau récapitulatif, le chapitre 9 illustre la cohérence d\'ensemble du dispositif et le chapitre 10 recense les références mobilisées. Une fiche standardisée par indicateur figure en annexe.'),
  ];
}

function section2() {
  return [
    H1('2. Matrice générale des quinze indicateurs'),
    P('La matrice ci-dessous constitue la liste de référence des indicateurs principaux. L\'intitulé et le sens de variation souhaité de chaque indicateur sont arrêtés ; la colonne « dimension suivie » précise la facette de l\'axe que chacun éclaire. La numérotation (axe.indicateur) est reprise dans l\'ensemble du document, y compris dans les fiches de l\'annexe.'),
    CAPTION('Matrice des quinze indicateurs principaux'),
    matrix(),
    SOURCE('Note : ↑ signifie qu\'une hausse de l\'indicateur traduit une amélioration ; ↓ qu\'une baisse traduit une amélioration.'),
    P('Chaque axe est construit selon une progression interne. En souveraineté alimentaire, les indicateurs passent de l\'autonomie à la capacité productive puis à la résilience. En compétitivité, ils suivent la chaîne de valeur, de la parcelle à la transformation. En financement, ils vont de la demande satisfaite à l\'adéquation du financement à l\'investissement. En matière foncière, ils passent de la parcelle au territoire puis aux relations d\'exploitation. En durabilité, ils couvrent les pratiques, les écosystèmes et le climat. Cette construction limite les recouvrements entre indicateurs d\'un même axe et, grâce à des choix de périmètre explicites, entre axes.'),
  ];
}

function complement(items) {
  return [H3('Indicateurs complémentaires (à titre secondaire)'),
    P('Les indicateurs suivants peuvent éclairer la lecture des indicateurs principaux. Ils ne font pas partie du tableau de bord principal et ne se substituent à aucun indicateur retenu.'),
    ...items.map((t) => B(t))];
}
function todo(items) {
  return [new Paragraph({ keepNext: true, spacing: { before: 120, after: 80 }, children: [new TextRun({ text: L.fr('Précisions méthodologiques à documenter'), font: FONT, size: 22, bold: true, color: C })] }),
    ...items.map((t) => B(t, 0, { size: 22 }))];
}

function section3() {
  return [
    H1('3. Souveraineté alimentaire'),
    H2('3.1. Définition retenue'),
    DEF('La souveraineté alimentaire est la capacité durable d\'un pays à satisfaire l\'essentiel des besoins alimentaires de sa population à partir d\'une production nationale suffisante, croissante et résiliente, tout en conservant la maîtrise de ses choix de production et en limitant sa vulnérabilité aux approvisionnements extérieurs.'),
    SP(),
    P('Cette définition se distingue de la notion de sécurité alimentaire, telle qu\'arrêtée lors du Sommet mondial de l\'alimentation de 1996, qui s\'attache à l\'accès de chacun à une nourriture suffisante quelle qu\'en soit l\'origine. Elle ne se confond pas davantage avec l\'autosuffisance intégrale, dont la littérature a montré qu\'elle n\'est ni toujours réaliste ni toujours souhaitable pour un pays ouvert aux échanges (Clapp, 2017). La définition retenue met l\'accent sur la capacité de la production nationale à couvrir l\'essentiel des besoins et sur la réduction de la vulnérabilité aux approvisionnements extérieurs.'),
    P('Elle se décompose en trois exigences, auxquelles correspondent les trois indicateurs de l\'axe. La production nationale doit couvrir une part élevée de la consommation (autonomie) ; elle doit être suffisante et croissante au regard de la population (capacité productive) ; elle doit enfin être stable face aux chocs climatiques, sanitaires ou économiques (résilience).'),
    LOGIC('Autonomie  →  capacité productive  →  résilience'),
    P('Les trois indicateurs reposent sur un même panier alimentaire ivoirien et un même système de pondération. Ce choix garantit que les écarts d\'évolution entre indicateurs traduisent des phénomènes économiques distincts et non des différences de périmètre.'),

    H2('3.2. Indicateur 1.1 — Taux de couverture des besoins alimentaires par la production nationale'),
    P('Le dispositif retenu repose sur un panier alimentaire ivoirien commun, constitué des produits qui représentent l\'essentiel de l\'apport calorique de la population. Pour chaque produit *i* et chaque année *t*, le taux de couverture rapporte la production nationale à la consommation apparente.'),
    EQ([M(sb('TC', 'i,t'), '=', fr(sb('P', 'i,t'), sb('C', 'i,t')), '×100')]),
    P('où P_{i,t} représente la production nationale et C_{i,t} la consommation apparente du produit. Lorsque les données le permettent, la consommation apparente est reconstituée à partir de l\'équation d\'emplois et de ressources des bilans alimentaires.'),
    EQ([M(sb('C', 'i,t'), '=', sb('P', 'i,t'), '+', sb('M', 'i,t'), '−', sb('X', 'i,t'), '±Δ', sb('Stocks', 'i,t'))]),
    P('M_{i,t} et X_{i,t} désignent les importations et les exportations. La variation des stocks est retranchée lorsqu\'il y a constitution de stocks et ajoutée en cas de déstockage ; cette convention, identique à celle des bilans alimentaires de la FAO (FAO, 2001), doit être appliquée uniformément à tous les produits. Pour chaque produit, le rapport ainsi défini correspond au taux d\'autosuffisance utilisé par la FAO.'),
    P('L\'indicateur national est la moyenne pondérée des taux par produit.'),
    EQ([M(sb('TC', 't'), '=', sum('i', [w0(), sb('TC', 'i,t')]))]),
    EQ([M(w0(), '=', fr(ss('Consommation', 'i', '0'), sum('j', ss('Consommation', 'j', '0'))))]),
    P('Les poids reflètent la structure de consommation alimentaire de la Côte d\'Ivoire. Pour agréger des produits aussi différents que le riz, le manioc, l\'huile de palme ou le poisson, une unité nutritionnelle commune est nécessaire ; les calories sont privilégiées, car elles expriment directement la contribution de chaque produit à la couverture des besoins énergétiques.'),
    EQ([M(w0(), '=', fr(['kcal provenant du produit ', r('i')], 'kcal totales du panier'))]),
    P('Les pondérations sont calculées sur une période de référence pluriannuelle, afin de neutraliser les fluctuations d\'une année particulière, puis maintenues fixes. Ce choix est essentiel à l\'interprétation. Si les poids étaient recalculés chaque année, l\'indicateur pourrait varier sous le seul effet d\'un changement de régime alimentaire : un déplacement de la consommation vers un produit largement importé augmenterait son poids et ferait baisser le taux agrégé sans que la production nationale ait changé. Avec des poids fixes, toute variation de l\'indicateur traduit une évolution de la couverture nationale des produits du panier, et non une modification de la structure de consommation. Le procédé est celui des indices de Laspeyres utilisés par la FAO pour ses indices de production.'),
    P('La pondération calorique confère en outre à l\'indicateur une propriété de lecture simple. Au cours de la période de référence, et en l\'absence de plafonnement, la moyenne pondérée des taux par produit est égale au rapport entre les calories produites et les calories consommées pour l\'ensemble du panier, puisque chaque terme w_{i}^{0}·TC_{i}^{0} se réduit à la part des calories produites du produit *i* dans les calories totales consommées. Le niveau de référence de l\'indicateur s\'interprète donc comme un taux de couverture calorique global.'),
    ...todo([
      'Composition du panier : liste des produits et seuil de couverture calorique visé, en incluant les produits consommés mais non produits localement (le blé, par exemple), dont le taux de couverture est nul et dont l\'exclusion surestimerait l\'autonomie.',
      'Périmètre des produits animaux et halieutiques, qui relèvent pour partie d\'un autre département ministériel mais pèsent dans la consommation.',
      'Conversion des produits à un stade commun (paddy et riz usiné, tubercules frais et produits transformés) au moyen de coefficients techniques documentés.',
      'Période de référence : moyenne triennale à arrêter, par exemple alignée sur la base 2014-2016 des indices FAOSTAT pour faciliter les contrôles de cohérence.',
      'Traitement analytique des taux supérieurs à 100 % : l\'indicateur retenu les conserve ; un calcul avec plafonnement à 100 % peut être produit en analyse de sensibilité, pour vérifier que l\'excédent d\'un produit ne masque pas le déficit d\'un autre.',
    ]),

    H2('3.3. Indicateur 1.2 — Indice de production vivrière par habitant'),
    P('Le deuxième indicateur mesure la capacité productive. Il utilise exactement le même panier, le même périmètre de produits, le même système de pondération et la même période de référence que le taux de couverture. Pour chaque produit, la production par habitant de l\'année est rapportée à la production moyenne par habitant de la période de référence.'),
    EQ([M(sb('I', 'i,t'), '=', fr(fr(sb('P', 'i,t'), sb('N', 't')), fr(ss('P̄', 'i', '0'), sp('N̄', '0'))), '×100')]),
    P('où N_{t} est la population totale de l\'année *t*, et où les grandeurs surmontées d\'une barre désignent les moyennes de la période de référence. L\'indice agrégé applique les poids caloriques déjà définis.'),
    EQ([M(sb('IPVH', 't'), '=', sum('i', [w0(), sb('I', 'i,t')]))]),
    P('L\'indicateur permet de vérifier si la production alimentaire nationale augmente suffisamment vite relativement à la population. Un niveau supérieur à 100 traduit une amélioration par rapport à la période de référence ; un niveau inférieur signale que la croissance démographique a été plus rapide que celle de la production.'),
    P('La lecture conjointe avec le taux de couverture est instructive. Les deux indicateurs peuvent diverger : la production par habitant peut progresser alors que le taux de couverture recule, si la consommation par habitant croît plus vite, sous l\'effet de la hausse des revenus ou de l\'urbanisation. Le premier renseigne sur l\'effort productif, le second sur son adéquation à la demande.'),
    ...todo([
      'Produits sans production nationale en période de référence : leur indice élémentaire n\'est pas défini (division par zéro). Ils sont exclus de l\'agrégat de l\'IPVH et les poids des autres produits sont renormalisés, selon une règle documentée, tout en restant dans le panier du taux de couverture.',
      'Série de population : utiliser une série homogène, rétropolée après le recensement général de la population et de l\'habitat de 2021, afin d\'éviter une rupture artificielle de l\'indice.',
      'Contrôle de cohérence avec l\'indice FAOSTAT de production alimentaire nette par habitant, dont la pondération (prix internationaux) diffère mais dont la tendance doit être comparable.',
    ]),

    H2('3.4. Indicateur 1.3 — Variabilité de la production vivrière par habitant'),
    P('Le troisième indicateur mesure la résilience du système productif. Il est construit à partir de la même série agrégée que l\'indicateur 1.2, ce qui préserve la cohérence de l\'ensemble : la variabilité mesurée est celle de la grandeur dont on suit par ailleurs le niveau. La procédure comporte trois étapes.'),
    N('Calculer la série annuelle de production vivrière par habitant, y_{t} = IPVH_{t}.'),
    N('Identifier sa tendance, notée ŷ_{t}, et calculer les écarts à la tendance.'),
    N('Calculer la dispersion de ces écarts sur une fenêtre mobile de cinq ans.'),
    EQ([M(sb('e', 't'), '=', sb('y', 't'), '−', sb('ŷ', 't'))]),
    EQ([M(sb('VPROD', 't'), '=SD', br([sb('e', 't−4'), ',…,', sb('e', 't')]))]),
    P('Le retrait de la tendance est indispensable : une production en croissance régulière présenterait sinon un écart type élevé alors qu\'elle est parfaitement stable autour de sa trajectoire. L\'indicateur s\'inscrit dans la logique de l\'indicateur de variabilité de la production alimentaire par habitant publié par la FAO dans sa suite d\'indicateurs de la sécurité alimentaire, qui porte sur la valeur nette de la production alimentaire par habitant à prix internationaux constants. Pour l\'indicateur voisin de variabilité des disponibilités alimentaires, la FAO documente une élimination de la tendance puis un écart type sur cinq ans. La spécification exacte de la tendance utilisée par la FAO pour la série de production devra être vérifiée dans la fiche de métadonnées originale avant publication.'),
    P('Plus l\'indicateur est faible, plus le système productif est stable. Il s\'exprime en points d\'indice, puisque la série de base est l\'IPVH.'),
    ...todo([
      'Méthode d\'estimation de la tendance : tendance linéaire, spline ou filtre, à arrêter une fois pour toutes. Une tendance estimée sur l\'ensemble de la période est révisée à chaque nouvelle année ; la règle de réestimation doit donc être fixée pour éviter une révision permanente des valeurs passées.',
      'Profondeur de série : une valeur pour 2015 exige des données 2011-2015. La série de l\'IPVH doit donc être reconstituée à partir de 2011 au moins.',
      'Une version relative (écart type rapporté à la moyenne de la fenêtre) peut être calculée à titre de contrôle, sans remplacer l\'indicateur retenu.',
    ]),
    ...complement([
      'Prévalence de la sous-alimentation (ODD 2.1.1) et prévalence de l\'insécurité alimentaire modérée ou grave mesurée par l\'échelle FIES (ODD 2.1.2), pour la dimension d\'accès.',
      'Taux de dépendance aux importations de céréales et part des importations alimentaires dans les exportations totales de marchandises (suite d\'indicateurs de la FAO), pour la vulnérabilité extérieure.',
    ]),
  ];
}

function section4() {
  return [
    H1('4. Compétitivité de l\'agriculture ivoirienne'),
    H2('4.1. Définition retenue'),
    DEF('La compétitivité de l\'agriculture ivoirienne est la capacité durable de ses chaînes de valeur à produire, transformer et acheminer des produits agricoles répondant aux exigences des marchés, à des niveaux de productivité, de coût, de qualité et de valeur ajoutée permettant de maintenir ou d\'accroître leur position sur les marchés nationaux, régionaux et internationaux face aux produits concurrents.'),
    SP(),
    P('La littérature distingue les mesures de compétitivité fondées sur les résultats commerciaux (parts de marché, avantages comparatifs révélés) et celles qui portent sur ses déterminants, au premier rang desquels la productivité et l\'efficacité (Latruffe, 2010). Le dispositif retient la seconde approche : il suit des leviers sur lesquels la politique agricole a prise, le long de la chaîne de valeur, plutôt que des résultats de marché qui dépendent aussi des prix mondiaux et des taux de change.'),
    LOGIC('Intrants et services  →  production  →  collecte et post-récolte  →  transformation  →  commercialisation'),
    P('Les trois indicateurs se placent aux maillons où se jouent principalement les gains de compétitivité : produire plus efficacement, perdre moins entre le champ et le marché, transformer davantage sur le territoire national.'),
    LOGIC('Produire plus efficacement  →  perdre moins  →  transformer davantage'),

    H2('4.2. Indicateur 2.1 — Indice de productivité des cultures à superficie constante'),
    P('Pour chaque culture *i*, le rendement rapporte la production à la superficie récoltée.'),
    EQ([M(sb('R', 'i,t'), '=', fr(sb('Q', 'i,t'), sb('S', 'i,t')))]),
    P('où Q désigne la production et S la superficie récoltée. Un indice élémentaire est construit par rapport à la période de référence, puis les indices sont agrégés.'),
    EQ([M(sb('IR', 'i,t'), '=', fr(sb('R', 'i,t'), sb('R', 'i,0')), '×100')]),
    EQ([M(sb('IP', 't'), '=', sum('i', [w0(), sb('IR', 'i,t')]))]),
    P('Les pondérations reflètent l\'importance économique relative des cultures. Elles correspondent aux parts de chaque culture dans la valeur de la production végétale, calculées sur la période de référence à prix constants, puis maintenues fixes.'),
    EQ([M(w0(), '=', fr([ss('p', 'i', '0'), ss('Q', 'i', '0')], sum('j', [ss('p', 'j', '0'), ss('Q', 'j', '0')])))]),
    P('Cette pondération justifie l\'intitulé de l\'indicateur. En remplaçant les poids par leur expression et en notant que Q_{i}^{0} = S_{i}^{0}·R_{i}^{0}, on obtient l\'égalité suivante.'),
    EQ([M(sb('IP', 't'), '=', fr(sum('i', [ss('p', 'i', '0'), ss('S', 'i', '0'), sb('R', 'i,t')]), sum('i', [ss('p', 'i', '0'), ss('S', 'i', '0'), ss('R', 'i', '0')])), '×100')]),
    P('L\'indice est donc le rapport entre la valeur de la production qui serait obtenue avec les superficies de la période de référence et les rendements de l\'année, et la valeur de la production de référence. Les superficies étant figées, un accroissement de production résultant uniquement d\'une extension des surfaces ne se traduit par aucun gain de l\'indicateur. Cette propriété est importante pour la Côte d\'Ivoire, où la croissance agricole a longtemps reposé sur l\'extension des superficies, avec les conséquences forestières examinées au chapitre 7.'),
    ...todo([
      'Liste des cultures couvertes (cultures vivrières, d\'exportation et maraîchères principales) et règle d\'entrée ou de sortie en cas de rebasage.',
      'Système de prix : valeur de la production FAOSTAT à prix internationaux constants ou prix nationaux aux producteurs de la période de référence.',
      'Cultures pérennes (cacao, café, hévéa, palmier à huile, anacarde) : utiliser la superficie en production plutôt que la superficie plantée, faute de quoi le renouvellement des vergers ferait baisser artificiellement les rendements.',
      'Aléas climatiques : la série annuelle est publiée telle quelle ; une moyenne mobile peut être présentée pour l\'analyse de tendance.',
    ]),

    H2('4.3. Indicateur 2.2 — Taux de pertes post-récolte'),
    P('Pour un produit donné, le taux de pertes rapporte les quantités perdues après la récolte à la production.'),
    EQ([M(sb('TPR', 'i,t'), '=', fr(['Pertes post-récolte', sb('', 'i,t')], sb('Production', 'i,t')), '×100')]),
    P('Le périmètre couvre les pertes intervenant entre la récolte et l\'entrée en transformation ou la mise sur le marché, c\'est-à-dire lors de la manutention, du stockage et du transport.'),
    LOGIC('Récolte  →  manutention  →  stockage  →  transport  →  entrée en transformation ou mise sur le marché'),
    P('Ce périmètre est cohérent avec celui de l\'indice des pertes alimentaires de la FAO (indicateur ODD 12.3.1a), qui couvre les pertes de la production jusqu\'au commerce de détail exclu (FAO, 2019). L\'agrégation nationale s\'effectue par moyenne pondérée.'),
    EQ([M(sb('TPR', 't'), '=', sum('i', [w0(), sb('TPR', 'i,t')]))]),
    P('Le choix de la pondération appelle un examen particulier, car il détermine ce que l\'indicateur représente. Trois options ont été comparées, sans modifier le principe de l\'indicateur.'),
    CAPTION('Options de pondération du taux de pertes post-récolte'),
    TABLE({ widths: [1900, 3585, 3585], head: ['Pondération', 'Ce que mesure l\'agrégat', 'Appréciation'], size: 19, rows: [
      ['Quantités produites (tonnes)', 'Part des tonnages perdus.', 'À écarter : elle donne un poids excessif aux produits pondéreux et riches en eau (tubercules, plantain) et additionne des grandeurs non homogènes.'],
      ['Calories', 'Part de l\'énergie alimentaire perdue.', 'Pertinente pour une lecture de sécurité alimentaire, mais elle ignore les produits non alimentaires ou peu caloriques à forte valeur (cacao, anacarde).'],
      ['Valeur de la production de référence, à prix constants', 'Part de la valeur économique perdue.', 'Recommandée. Cohérente avec l\'objet de l\'axe (compétitivité) et avec la méthode de la FAO pour l\'ODD 12.3.1a, qui pondère par la valeur de la production à prix constants fixée sur une année de base.'],
    ] }),
    SOURCE('Source : analyse des auteurs ; FAO, métadonnées de l\'indicateur ODD 12.3.1a.'),
    P('La pondération par la valeur de la production de la période de référence est donc recommandée ; une variante calorique peut être publiée en complément pour la lecture de sécurité alimentaire. La mesure elle-même impose trois distinctions. Les pertes quantitatives, qui correspondent à une disparition physique du produit, constituent l\'objet de l\'indicateur. Les pertes qualitatives, qui se traduisent par une dépréciation (moisissures, contamination, déclassement) sans perte de poids, doivent être suivies séparément, en sous-indicateur, car elles ne s\'additionnent pas aux tonnages. Le gaspillage alimentaire au stade de la distribution et de la consommation relève d\'un autre indicateur (ODD 12.3.1b) et n\'entre pas dans ce périmètre.'),
    P('Les travaux de synthèse sur l\'Afrique subsaharienne montrent la forte variabilité des estimations selon les produits, les étapes et les méthodes de mesure (Affognon et al., 2015 ; Hodges et al., 2011). Pour les céréales, le système APHLIS fournit des estimations modélisées par étape ; pour les autres produits, un dispositif d\'enquêtes périodiques est nécessaire.'),
    ...todo([
      'Liste des produits couverts, en cohérence avec les produits à forte valeur de production retenus pour l\'ODD 12.3.1a.',
      'Méthode de mesure par produit (enquêtes, modélisation APHLIS, coefficients de filière) et fréquence des enquêtes approfondies.',
      'Définition opérationnelle des pertes qualitatives pour le sous-indicateur.',
    ]),

    H2('4.4. Indicateur 2.3 — Taux de transformation nationale des produits agricoles'),
    P('Pour chaque produit, le taux de transformation rapporte la quantité transformée en Côte d\'Ivoire à la production nationale disponible pour la transformation.'),
    EQ([M(sb('TT', 'i,t'), '=', fr(['Quantité du produit ', r('i'), ' transformée en Côte d\'Ivoire'], ['Production nationale du produit ', r('i'), ' disponible pour transformation']), '×100')]),
    EQ([M(sb('TT', 't'), '=', sum('i', [w0(), sb('TT', 'i,t')]))]),
    P('La pondération retenue est la part de chaque filière dans la valeur de la production agricole de la période de référence. Elle permet de représenter à la fois les filières d\'exportation, qui dominent la valeur de la production, et les filières tournées vers le marché intérieur, qui pèsent dans l\'emploi et la sécurité alimentaire. Une pondération par les exportations ferait disparaître ces dernières ; une pondération par les tonnages surreprésenterait les produits pondéreux.'),
    P('Le numérateur doit se rapporter à un stade de transformation de référence défini à l\'avance pour chaque filière. Sans cette précaution, l\'indicateur mêlerait des opérations de conditionnement primaire, presque systématiques, et des transformations créatrices de valeur. Le tableau suivant propose une première grille, à valider avec les organes de régulation des filières.'),
    CAPTION('Stades de transformation de référence proposés par filière (à valider)'),
    TABLE({ widths: [1700, 3935, 3435], head: ['Filière', 'Stade de référence proposé', 'Point d\'attention'], size: 19, rows: [
      ['Cacao', 'Broyage des fèves (production de liqueur, beurre, tourteau ou poudre)', 'Aligner campagne et année civile ; exclure les fèves d\'origine étrangère.'],
      ['Anacarde', 'Décorticage des noix brutes en amandes', 'Exprimer le numérateur en équivalent noix brutes.'],
      ['Hévéa', 'Usinage du caoutchouc naturel', 'Exclure le caoutchouc importé des pays voisins.'],
      ['Palmier à huile', 'Extraction de l\'huile brute, puis raffinage (deux sous-taux)', 'Distinguer extraction industrielle et artisanale.'],
      ['Coton', 'Stade postérieur à l\'égrenage (filature, transformation de la fibre)', 'L\'égrenage, quasi systématique, n\'est pas discriminant.'],
      ['Café', 'Torréfaction ou solubilisation', 'Faibles volumes ; forte valeur unitaire.'],
      ['Produits vivriers (manioc, riz, maïs, etc.)', 'Transformation semi-industrielle ou industrielle', 'Données dispersées ; périmètre à arrêter.'],
    ] }),
    SOURCE('Source : proposition méthodologique à valider ; aucun taux n\'est avancé à ce stade.'),
    P('Le dénominateur doit, lui aussi, être défini par filière. La « production disponible pour transformation » exclut l\'autoconsommation et les ventes en frais lorsque la filière n\'a pas vocation à les transformer. Les matières premières importées pour transformation doivent être exclues du numérateur, faute de quoi le taux pourrait dépasser 100 % sans refléter la transformation de la production nationale. Les résultats sont présentés séparément par grande filière dès qu\'ils sont disponibles, l\'agrégat national n\'ayant de sens qu\'accompagné de sa décomposition.'),
    ...todo([
      'Liste des filières couvertes et stade de référence de chacune.',
      'Coefficients de conversion en équivalent matière première.',
      'Méthode d\'identification de l\'origine nationale de la matière première transformée.',
    ]),
    ...complement([
      'Parts de marché mondiales des principaux produits exportés et indice d\'avantage comparatif révélé (Balassa), qui mesurent le résultat commercial.',
      'Productivité totale des facteurs agricoles (USDA ERS, International Agricultural Productivity) et valeur ajoutée agricole par actif.',
      'Part des produits transformés dans la valeur des exportations agricoles.',
    ]),
  ];
}

module.exports = { section1, section2, section3, section4, complement, todo };
