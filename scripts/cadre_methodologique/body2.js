// Sections 5 à 7
const L = require('./lib');
const { P, B, H1, H2, LOGIC, EQ, CAPTION, SOURCE, TABLE, DEF, SP } = L;
const { r, sb, ss, fr, sum, br, M } = require('./mathh');
const { complement, todo } = require('./body1');

function section5() {
  return [
    H1('5. Accès au financement agricole'),
    H2('5.1. Définition retenue'),
    DEF('L\'accès au financement agricole est la capacité effective des producteurs et des entreprises agricoles à mobiliser, au moment où ils en ont besoin, des ressources financières suffisantes et adaptées aux cycles, aux risques et aux besoins de leur activité, afin de financer la production, la trésorerie et les investissements agricoles.'),
    SP(),
    P('La définition insiste sur le caractère effectif de l\'accès. Elle s\'appuie sur un acquis ancien de l\'économie du crédit : en présence d\'asymétries d\'information, le marché du crédit peut rationner durablement des emprunteurs solvables (Stiglitz et Weiss, 1981). En agriculture, ce rationnement prend plusieurs formes. Il peut porter sur les quantités, lorsque la demande est refusée ou partiellement servie ; il peut aussi résulter du risque, lorsque les emprunteurs renoncent à solliciter un crédit dont les garanties exigées leur feraient courir un risque excessif (Boucher, Carter et Guirkinger, 2008). Les travaux du CGAP montrent en outre que les besoins financiers des ménages agricoles diffèrent selon leur degré d\'insertion dans des chaînes de valeur structurées (Christen et Anderson, 2013).'),
    P('Les trois indicateurs retenus saisissent trois facettes complémentaires : l\'intensité de la satisfaction de la demande, mesurée en montants ; l\'étendue de l\'accès, mesurée en nombre d\'acteurs ; la qualité du financement, appréciée par sa maturité.'),
    LOGIC('Demande satisfaite  →  acteurs effectivement financés  →  financement adapté à l\'investissement'),

    H2('5.2. Indicateur 3.1 — Taux de couverture de la demande de financement agricole'),
    EQ([M(sb('TCF', 't'), '=', fr(['Montant des financements agricoles effectivement accordés', sb('', 't')], ['Montant total des financements agricoles formellement demandés', sb('', 't')]), '×100')]),
    P('L\'indicateur rapporte des montants et non des nombres de dossiers, afin de saisir aussi le rationnement partiel, lorsque le crédit accordé est inférieur au crédit demandé. Il suppose de distinguer clairement trois notions de demande, dont l\'emboîtement est présenté ci-dessous.'),
    CAPTION('Trois notions de demande de financement agricole'),
    TABLE({ widths: [2000, 3935, 3135], head: ['Notion', 'Contenu', 'Usage dans le dispositif'], size: 19, rows: [
      ['Besoin total de financement', 'Ensemble des ressources nécessaires au financement de la production, de la trésorerie et de l\'investissement, qu\'une demande soit exprimée ou non.', 'Non observable de façon routinière ; estimations ponctuelles par enquête ou modélisation.'],
      ['Demande formellement exprimée', 'Montants sollicités par un dossier déposé auprès d\'une institution financière formelle.', 'Dénominateur opérationnel retenu pour le tableau de bord.'],
      ['Demande éligible ou solvable', 'Part de la demande exprimée qui satisfait les critères d\'éligibilité de l\'institution.', 'Analyse complémentaire des motifs de refus.'],
    ] }),
    SOURCE('Source : analyse des auteurs.'),
    P('Le choix de la demande formellement exprimée comme dénominateur répond à une exigence de mesurabilité : c\'est la seule notion enregistrée par les institutions financières. Il comporte une limite connue, celle des « emprunteurs découragés », c\'est-à-dire des acteurs qui ont un besoin de financement mais ne déposent pas de demande parce qu\'ils anticipent un refus (Kon et Storey, 2003). Si le découragement augmente, le dénominateur diminue et l\'indicateur peut s\'améliorer sans que l\'accès réel progresse. Ce biais justifie la lecture conjointe avec l\'indicateur 3.2, qui porte sur l\'ensemble des acteurs, et l\'introduction dans les enquêtes d\'un module sur les motifs de non-demande.'),
    ...todo([
      'Définition du « financement agricole » : activités de production végétale, animale et halieutique, et, le cas échéant, première transformation.',
      'Dispositif de collecte : aucune série publique des montants demandés n\'a été identifiée ; une déclaration périodique harmonisée des banques et des SFD doit être organisée.',
      'Règle de rattachement temporel : une demande déposée en fin d\'année et accordée l\'année suivante est rattachée à l\'année de la demande.',
    ]),

    H2('5.3. Indicateur 3.2 — Taux d\'accès effectif des acteurs agricoles au financement formel'),
    EQ([M(sb('TAF', 't'), '=', fr('Nombre d\'acteurs agricoles ayant obtenu un financement formel', 'Nombre total d\'acteurs agricoles'), '×100')]),
    P('Le numérateur dénombre, sans double compte, les acteurs ayant obtenu au moins un financement au cours des douze derniers mois auprès d\'une institution formelle réglementée. Sont inclus les financements provenant des banques, des systèmes financiers décentralisés (SFD) et des institutions de microfinance, des dispositifs publics formels et des autres institutions financières réglementées. La période de douze mois est celle du Global Findex de la Banque mondiale, ce qui facilite les rapprochements.'),
    P('La possession d\'un compte, l\'utilisation du mobile money ou les indicateurs généraux d\'inclusion financière ne sont pas assimilés à un accès effectif au financement agricole. Ces indicateurs mesurent la détention d\'un instrument ou l\'usage de services de paiement, non l\'obtention d\'un financement destiné à l\'activité agricole. De même, le crédit fournisseur, les avances des acheteurs et le crédit informel, pour importants qu\'ils soient, ne relèvent pas du financement formel réglementé ; ils peuvent être suivis à titre complémentaire.'),
    ...todo([
      'Unité statistique : exploitation agricole, ménage agricole ou entreprise agricole ; le recensement des exploitants et exploitations agricoles (REEA) 2015-2016 fournit un dénominateur de référence, à actualiser.',
      'Source du numérateur : module harmonisé dans les enquêtes nationales auprès des ménages et des exploitations, à défaut de registre administratif consolidé des emprunteurs.',
      'Ventilations minimales : sexe du responsable, taille de l\'exploitation, filière principale, région.',
    ]),

    H2('5.4. Indicateur 3.3 — Part des financements agricoles à moyen et long terme'),
    EQ([M(sb('PMLT', 't'), '=', fr(['Crédits agricoles à moyen et long terme', sb('', 't')], ['Crédits agricoles totaux', sb('', 't')]), '×100')]),
    P('Cet indicateur distingue le financement de campagne et de trésorerie, principalement à court terme, du financement qui permet la mécanisation, l\'irrigation, le renouvellement des plantations, le stockage et les autres investissements productifs. La transformation structurelle visée par la vision agricole suppose que la part du second progresse ; un système financier qui ne finance que les campagnes entretient une agriculture à faible capital.'),
    P('Les séries de la BCEAO sont examinées en priorité. La Centrale des risques publie, pour la Côte d\'Ivoire, les utilisations de crédits déclarées ventilées par secteur d\'activité (dont la branche « agriculture et chasse » et la branche « sylviculture, exploitation forestière et pêche ») et par terme, dans le Bulletin mensuel des statistiques. Ces données présentent trois limites à documenter. Elles portent sur des encours et non sur des mises en place, et les deux notions ne doivent pas être mélangées dans une même série. Elles ne couvrent que les crédits supérieurs au seuil de déclaration, ce qui sous-représente les petits crédits, notamment ceux des SFD. Enfin, le crédit aux exportateurs et aux agro-industries peut être classé dans le commerce ou l\'industrie et échapper ainsi à la branche agricole.'),
    ...todo([
      'Seuils de durée définissant le court, le moyen et le long terme, à reprendre de la documentation de la BCEAO.',
      'Branches de la nomenclature sectorielle incluses dans le « crédit agricole ».',
      'Intégration des données des SFD, par le biais des statistiques de supervision.',
      'Profondeur historique homogène de la série 2015-2025 : disponibilité de la série à vérifier.',
    ]),
    ...complement([
      'Part du secteur agricole dans l\'encours total des crédits déclarés à la Centrale des risques (BCEAO).',
      'Proportion d\'adultes ayant emprunté auprès d\'une institution financière formelle, en milieu rural (Global Findex), à titre de contexte.',
      'Financements de filière non réglementés (avances des acheteurs, crédit intrants), pour mesurer les substituts au crédit formel.',
    ]),
  ];
}

function section6() {
  return [
    H1('6. Sécurisation du foncier rural'),
    H2('6.1. Définition retenue'),
    DEF('La sécurisation du foncier rural est le processus par lequel les droits légitimes de propriété, de détention et d\'usage des terres rurales sont clairement identifiés, délimités, formalisés, enregistrés et protégés, de manière à garantir aux propriétaires comme aux exploitants la stabilité de leurs droits et à prévenir les conflits fonciers.'),
    SP(),
    P('Cette définition s\'inscrit dans le cadre juridique et institutionnel ivoirien. La loi n° 98-750 du 23 décembre 1998 relative au domaine foncier rural, modifiée par les lois n° 2004-412 du 14 août 2004, n° 2013-655 du 13 septembre 2013 et n° 2019-868 du 14 octobre 2019, organise la constatation des droits coutumiers par le certificat foncier et leur consolidation par l\'immatriculation. L\'Agence foncière rurale (AFOR), créée par le décret n° 2016-590 du 3 août 2016, est chargée de sa mise en œuvre. La Stratégie nationale de sécurisation foncière rurale (SNSFR) et le Programme national de sécurisation foncière rurale (PNSFR) 2023-2033, adoptés par le Gouvernement le 15 juin 2023, fixent le cadre programmatique. Le Système d\'information foncière rurale (SIFOR), institué par l\'ordonnance n° 2025-85 du 12 février 2025, constitue le registre numérique des opérations et des droits.'),
    P('Sur le plan international, la définition est cohérente avec le Cadre et lignes directrices sur les politiques foncières en Afrique (Commission de l\'Union africaine, Commission économique pour l\'Afrique et Banque africaine de développement, 2010) et avec les Directives volontaires pour une gouvernance responsable des régimes fonciers (FAO, 2012), qui insistent sur la reconnaissance de l\'ensemble des droits légitimes, y compris coutumiers et secondaires.'),
    P('Le lien entre sécurisation foncière et investissement est bien établi sur le plan théorique (Besley, 1995), mais les résultats empiriques sont plus nuancés en Afrique. La revue systématique de Lawry et al. (2017) conclut à des gains de productivité liés à la reconnaissance des droits, plus limités en Afrique qu\'en Asie ou en Amérique latine, et ne trouve pas de preuve d\'un effet passant par le crédit. C\'est l\'une des raisons pour lesquelles le dispositif mesure la sécurisation à trois échelles complémentaires.'),
    LOGIC('Sécuriser les parcelles  →  sécuriser les territoires  →  sécuriser les relations d\'exploitation'),

    H2('6.2. Indicateur 4.1 — Taux de couverture du domaine foncier rural par des droits fonciers formalisés'),
    EQ([M(sb('TCDF', 't'), '=', fr('Superficie cumulée couverte par des droits fonciers formalisés', 'Superficie totale du domaine foncier rural'), '×100')]),
    P('La superficie est privilégiée par rapport au nombre de certificats. Un certificat collectif peut couvrir plusieurs centaines d\'hectares, un certificat individuel quelques hectares : compter les actes reviendrait à additionner des objets de taille très différente et ne dirait rien de la part du territoire effectivement sécurisée. Les actes admissibles doivent être définis de façon limitative.'),
    CAPTION('Actes admissibles au numérateur de l\'indicateur 4.1 (à confirmer)'),
    TABLE({ widths: [2900, 1300, 4870], head: ['Acte', 'Statut proposé', 'Observation'], size: 19, rows: [
      ['Certificat foncier individuel', 'Admis', 'Acte de constatation des droits coutumiers au sens de la loi n° 98-750.'],
      ['Certificat foncier collectif', 'Admis', 'Superficie totale comptée une fois ; ventilation distincte recommandée.'],
      ['Titre foncier issu de l\'immatriculation d\'une terre du domaine rural', 'Admis', 'Se substitue au certificat lorsqu\'il en est issu : la parcelle n\'est pas comptée deux fois.'],
      ['Contrats d\'exploitation (location, prêt, planter-partager)', 'Non admis', 'Relèvent de l\'indicateur 4.3.'],
      ['Attestations et documents non prévus par la loi', 'Non admis', 'Peuvent faire l\'objet d\'un suivi descriptif distinct.'],
    ] }),
    SOURCE('Source : proposition établie à partir de la loi n° 98-750 modifiée ; statut définitif à arrêter avec l\'AFOR.'),
    P('Le double comptage est évité en raisonnant par parcelle et non par acte. Chaque parcelle dispose d\'un identifiant unique dans le SIFOR ; elle est comptée une seule fois dès lors qu\'elle est couverte par au moins un acte admissible, quel que soit le nombre d\'actes successifs qui la concernent. Le numérateur s\'écrit alors comme une somme de superficies de parcelles.'),
    EQ([M(sb('SDF', 't'), '=', sum('p', [sb('a', 'p'), '·', sb('𝟙', 'p,t')]))]),
    P('où a_{p} est la superficie de la parcelle *p* et où l\'indicatrice vaut 1 si la parcelle est couverte par au moins un acte admissible à la date *t*, 0 sinon.'),
    ...todo([
      'Superficie de référence du domaine foncier rural : le PNSFR 2023-2033 retient un ordre de grandeur de 23 millions d\'hectares à sécuriser ; la valeur officielle doit être confirmée dans le document adopté et maintenue fixe.',
      'Situation des certificats fonciers dont le délai de demande d\'immatriculation serait échu : règle de maintien ou de retrait du numérateur à arrêter au regard de la loi modifiée.',
      'Ventilation par sexe des titulaires, conformément aux Directives volontaires.',
    ]),

    H2('6.3. Indicateur 4.2 — Taux de délimitation juridiquement achevée des territoires villageois'),
    EQ([M(sb('TDV', 't'), '=', fr('Nombre de territoires villageois dont la délimitation est juridiquement achevée', 'Nombre total de villages officiels'), '×100')]),
    P('La délimitation des territoires villageois fixe les limites à l\'intérieur desquelles s\'opèrent ensuite la reconnaissance des droits et la certification des parcelles. Sa procédure a été définie par le décret n° 2013-296 du 2 mai 2013, abrogé et remplacé par le décret n° 2019-263 du 27 mars 2019, qui a confié un rôle central à l\'AFOR. Le décret n° 2024-850 du 30 septembre 2024 a ensuite institué une opération intégrée de sécurisation foncière rurale, qui enchaîne la délimitation des territoires et la reconnaissance des parcelles coutumières.'),
    P('Un territoire « bouclé-borné » n\'est pas automatiquement un territoire dont la délimitation est juridiquement achevée. Le bornage matérialise les limites sur le terrain ; la délimitation n\'acquiert sa portée juridique qu\'avec l\'acte administratif définitif qui la consacre. Les bilans publiés par l\'AFOR distinguent d\'ailleurs les villages délimités et bornés de ceux dont la délimitation a été consacrée par arrêté. L\'indicateur retient ce niveau juridiquement achevé. Les étapes intermédiaires sont suivies comme sous-indicateurs opérationnels, sous la forme d\'un entonnoir.'),
    CAPTION('Sous-indicateurs opérationnels de la délimitation (entonnoir)'),
    TABLE({ widths: [700, 4185, 4185], head: ['Étape', 'Sous-indicateur', 'Usage'], size: 19, rows: [
      ['1', 'Villages dont l\'opération de délimitation est ouverte', 'Mesure l\'engagement des opérations.'],
      ['2', 'Villages dont les limites ont été identifiées contradictoirement et levées', 'Mesure l\'avancement technique.'],
      ['3', 'Villages bouclés-bornés', 'Mesure la matérialisation des limites.'],
      ['4', 'Villages dont le dossier de délimitation est validé et transmis', 'Mesure l\'instruction administrative.'],
      ['5', 'Villages dont la délimitation est consacrée par l\'acte définitif', 'Numérateur de l\'indicateur principal.'],
    ] }),
    SOURCE('Source : proposition à aligner sur la dénomination et l\'ordre exacts des étapes de la procédure en vigueur.'),
    ...todo([
      'Nature exacte de l\'acte définitif dans la procédure issue du décret n° 2024-850 et articulation avec le décret n° 2019-263.',
      'Liste officielle des villages servant de dénominateur, arrêtée à une date de référence avec le ministère chargé de l\'Intérieur et l\'AFOR ; règle de mise à jour en cas de création de villages.',
    ]),

    H2('6.4. Indicateur 4.3 — Taux de formalisation des relations foncières d\'exploitation'),
    EQ([M(sb('TFR', 't'), '=', fr('Nombre de relations d\'exploitation non-propriétaire couvertes par un contrat écrit enregistré', 'Nombre total de relations d\'exploitation non-propriétaire identifiées'), '×100')]),
    P('En Côte d\'Ivoire, une part importante des terres est exploitée par des personnes qui n\'en détiennent pas les droits coutumiers, dans le cadre d\'arrangements souvent oraux. Les travaux de Colin (2013) ont montré que ces transactions constituent une source majeure d\'insécurité et de conflits, lorsque leur contenu ou leur durée sont contestés. Sécuriser les parcelles sans sécuriser ces relations laisserait sans protection une large partie des exploitants.'),
    P('Les relations pertinentes comprennent la location, le prêt, les droits d\'usage, le planter-partager et les autres formes reconnues. L\'unité de compte est la relation, c\'est-à-dire le couple formé par une parcelle et un exploitant non propriétaire ; un renouvellement de contrat n\'est pas compté comme une nouvelle relation.'),
    P('Le dénominateur n\'est vraisemblablement pas disponible en série historique. Dans ce cas, un indicateur transitoire peut être suivi, le nombre cumulé de contrats enregistrés. Cet indicateur transitoire ne remplace pas l\'indicateur principal : il mesure l\'activité de formalisation mais non la part des relations couvertes, et il pourrait progresser alors même que le nombre de relations informelles augmente plus vite. Le dénominateur peut être estimé à partir des enquêtes foncières réalisées lors des opérations de sécurisation, qui identifient les occupants des parcelles, et des enquêtes agricoles renseignant le mode de faire-valoir.'),
    ...todo([
      'Définition de « enregistré » : inscription dans le SIFOR, visa du comité villageois de gestion foncière rurale ou enregistrement fiscal.',
      'Typologie des relations et correspondance avec les modèles de contrats mis à disposition par l\'AFOR.',
      'Méthode d\'estimation du dénominateur et périodicité des enquêtes.',
    ]),
    ...complement([
      'Proportion de la population adulte disposant de droits fonciers documentés et percevant ses droits comme sûrs (ODD 1.4.2).',
      'Part des femmes parmi les titulaires de certificats fonciers (ODD 5.a.1, en partie).',
      'Nombre de conflits fonciers enregistrés par les instances de règlement.',
    ]),
  ];
}

function section7() {
  return [
    H1('7. Durabilité des systèmes de production'),
    H2('7.1. Définition retenue'),
    DEF('La durabilité des systèmes de production agricole est la capacité de l\'agriculture à maintenir durablement sa production et les services qu\'elle procure, tout en préservant les sols, les forêts, l\'eau, la biodiversité et le climat, et en renforçant sa capacité à résister aux changements climatiques et aux autres pressions environnementales.'),
    SP(),
    P('La durabilité comporte, dans son acception habituelle, des dimensions économique, sociale et environnementale ; c\'est le cas de l\'indicateur ODD 2.4.1 de la FAO, qui combine onze sous-indicateurs relevant de ces trois dimensions. Pour éviter les doubles comptes avec les autres axes, qui couvrent déjà la productivité, les revenus, le financement et le foncier, le tableau de bord se concentre ici principalement sur la dimension environnementale et climatique.'),
    P('Les références principales sont les travaux de la FAO sur l\'agriculture durable et l\'indicateur ODD 2.4.1, la Stratégie et le Plan d\'action du PDDAA 2026-2035 adoptés avec la Déclaration de Kampala en janvier 2025, la Contribution déterminée au niveau national (CDN) de la Côte d\'Ivoire révisée en 2022, ainsi que les politiques forestières et climatiques nationales, dont le Code forestier et la stratégie REDD+.'),
    LOGIC('Produire autrement  →  préserver les écosystèmes  →  réduire l\'empreinte climatique'),

    H2('7.2. Indicateur 5.1 — Part de la superficie agricole sous pratiques de production durable'),
    EQ([M(sb('PAD', 't'), '=', fr(['Superficie agricole sous pratiques de production durable', sb('', 't')], ['Superficie agricole totale', sb('', 't')]), '×100')]),
    P('L\'indicateur repose sur une liste nationale harmonisée de pratiques reconnues, établie à partir du cadre de la FAO et des documents ivoiriens, notamment la norme africaine ARS 1000 sur le cacao durable, rendue obligatoire en Côte d\'Ivoire. Le tableau suivant présente les pratiques à examiner ; les critères minimaux d\'application doivent être arrêtés pour chacune.'),
    CAPTION('Pratiques à examiner pour la liste nationale harmonisée'),
    TABLE({ widths: [2600, 6470], head: ['Pratique', 'Critère d\'application à préciser'], size: 19, rows: [
      ['Agroforesterie', 'Densité minimale d\'arbres d\'ombrage ou d\'essences associées par hectare.'],
      ['Rotations culturales', 'Succession de cultures de familles différentes sur une période définie.'],
      ['Associations culturales', 'Présence simultanée de cultures complémentaires sur la parcelle.'],
      ['Couverture des sols', 'Part minimale de sol couverte (paillage, plantes de couverture) hors période de culture.'],
      ['Agriculture de conservation', 'Travail minimal du sol, couverture permanente et diversification.'],
      ['Gestion raisonnée des engrais', 'Doses fondées sur une recommandation ou une analyse de sol.'],
      ['Lutte intégrée contre les ravageurs', 'Recours prioritaire aux méthodes non chimiques et traitement sur seuil.'],
      ['Restauration des sols', 'Apport organique, amendements, aménagements antiérosifs.'],
      ['Irrigation économe', 'Techniques d\'irrigation à faible consommation d\'eau.'],
      ['Autres pratiques reconnues', 'Pratiques certifiées (ARS 1000, agriculture biologique, autres référentiels), après examen.'],
    ] }),
    SOURCE('Source : liste indicative à valider ; critères à définir avec les services techniques et l\'ANADER.'),
    P('Une même parcelle peut appliquer plusieurs pratiques. Le numérateur est donc calculé comme l\'union des superficies concernées et non comme la somme des superficies par pratique, qui pourrait dépasser la superficie agricole totale. Les hectares couverts sont privilégiés par rapport au nombre d\'exploitations, car une exploitation peut n\'appliquer une pratique que sur une fraction de ses parcelles.'),
    EQ([M(sb('SPD', 't'), '=', sum('p', [sb('a', 'p'), '·', sb('𝟙', 'p,t')]))]),
    P('où l\'indicatrice vaut 1 si au moins une pratique reconnue est appliquée sur la parcelle *p* au cours de l\'année *t*. Les superficies par pratique, y compris leurs recouvrements, sont suivies comme sous-indicateurs.'),
    ...todo([
      'Liste nationale harmonisée et critères minimaux d\'application.',
      'Périmètre du dénominateur : superficie cultivée (terres arables et cultures permanentes) ou superficie agricole incluant les pâturages, en cohérence avec le champ du numérateur.',
      'Articulation avec l\'ODD 2.4.1, qui évalue la durabilité par exploitation à partir de seuils et pourrait fournir un contrôle externe.',
    ]),

    H2('7.3. Indicateur 5.2 — Taux de déforestation imputable à l\'expansion agricole'),
    EQ([M(sb('TDA', 't'), '=', fr(['Superficie forestière convertie en terres agricoles', sb('', 't')], ['Superficie forestière au début de la période', sb('', 't')]), '×100')]),
    P('Seule est retenue la déforestation dont le changement d\'usage final est agricole. La conversion des forêts résulte aussi de l\'urbanisation, des infrastructures, de l\'exploitation forestière, des incendies ou d\'autres causes ; ces causes doivent être distinguées dans la matrice de changement d\'occupation des terres. La mesure porte sur la déforestation brute : les reboisements ne viennent pas en déduction, car ils ne compensent ni la perte de biodiversité ni le carbone des forêts anciennes.'),
    P('Les travaux récents confirment la pertinence de l\'indicateur. À l\'échelle mondiale, l\'agriculture est le principal moteur de la déforestation tropicale (Curtis et al., 2018 ; Pendrill et al., 2022). En Côte d\'Ivoire, la cartographie des plantations de cacao par imagerie satellitaire a mis en évidence l\'association entre cacaoculture et perte forestière, y compris dans les aires protégées (Kalischek et al., 2023). Le règlement (UE) 2023/1115 relatif aux produits sans déforestation confère en outre à cette mesure une portée commerciale directe.'),
    P('Lorsque les cartes d\'occupation des terres ne sont disponibles qu\'à des dates espacées, le taux doit être annualisé. Pour une période allant de t_{1} à t_{2}, le taux annuel moyen s\'écrit comme suit ; la formule de Puyravaud (2003), fondée sur un taux composé, peut être utilisée en contrôle.'),
    EQ([M(sb('TDA', 'annuel'), '=', fr(sb('SFA', [sb('t', '1'), '→', sb('t', '2')]), [sb('SF', sb('t', '1')), '×', br([sb('t', '2'), '−', sb('t', '1')])]), '×100')]),
    P('L\'objectif de long terme est un découplage entre la croissance de la production agricole et la conversion forestière. La lecture conjointe de cet indicateur et de l\'indice de productivité à superficie constante (indicateur 2.1) permet de vérifier si la croissance provient de gains de rendement plutôt que de nouvelles surfaces.'),
    ...todo([
      'Définition de la forêt : définition nationale retenue pour les rapports REDD+ ou définition de la FAO, à fixer et à conserver.',
      'Classement de l\'agroforesterie cacaoyère, qui peut être confondue avec la forêt dans certains produits satellitaires.',
      'Source de référence : cartographie nationale ou produits mondiaux (Hansen et al., 2013 ; Vancutsem et al., 2021), avec méthode d\'attribution de l\'usage final.',
    ]),

    H2('7.4. Indicateur 5.3 — Intensité des émissions de gaz à effet de serre de la production agricole'),
    EQ([M(sb('IC', 't'), '=', fr(['Émissions agricoles', sb('', 't')], ['Valeur réelle de la production agricole', sb('', 't')]))]),
    P('ou, selon la série statistique la plus robuste :'),
    EQ([M(sb('IC', 't'), '=', fr(['Émissions agricoles', sb('', 't')], ['Valeur ajoutée agricole réelle', sb('', 't')]))]),
    P('L\'unité est la tonne d\'équivalent CO₂ par million de FCFA constants. Plus l\'indicateur diminue, plus la production agricole devient sobre en carbone. Le dénominateur doit être exprimé à prix constants : à prix courants, une hausse des prix agricoles ferait baisser l\'intensité sans aucun changement des pratiques.'),
    P('Pour éviter un double comptage avec l\'indicateur 5.2, les émissions directement associées au changement d\'affectation des terres et à la déforestation sont exclues, lorsque cela est méthodologiquement possible. Le numérateur correspond ainsi à la catégorie des émissions « à la ferme » (farm gate) de FAOSTAT, qui distingue ces émissions de celles liées au changement d\'affectation des terres et de celles des étapes situées en amont et en aval de la production. Il comprend notamment les émissions des sols agricoles, la fertilisation, la fermentation entérique de l\'élevage, la riziculture, la gestion des déjections, le brûlage des résidus agricoles et les autres sources comprises dans les inventaires agricoles établis selon les lignes directrices du GIEC.'),
    P('FAOSTAT publie une intensité d\'émissions par valeur de la production agricole, qui fournit une base de comparaison internationale. L\'inventaire national, établi pour les rapports à la Convention-cadre des Nations unies sur les changements climatiques, reste la source de référence dès lors qu\'il est disponible sous forme de série annuelle homogène.'),
    ...todo([
      'Choix définitif du dénominateur (valeur de la production ou valeur ajoutée), en veillant à la cohérence de périmètre : si la valeur ajoutée inclut la sylviculture et la pêche, les émissions correspondantes doivent être traitées de manière symétrique.',
      'Jeu de potentiels de réchauffement global (FAOSTAT utilise ceux du cinquième rapport d\'évaluation du GIEC), à maintenir fixe sur toute la série.',
      'Rapprochement entre inventaire national et FAOSTAT, et documentation des écarts.',
    ]),
    ...complement([
      'Émissions agricoles absolues, car une baisse de l\'intensité peut coexister avec une hausse des émissions totales.',
      'Indicateur ODD 2.4.1 (proportion de la superficie agricole exploitée de manière productive et durable).',
      'Consommation d\'engrais minéraux par hectare cultivé et superficie forestière totale.',
    ]),
  ];
}

module.exports = { section5, section6, section7 };
