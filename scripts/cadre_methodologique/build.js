const fs = require('fs');
const {
  Document, Packer, Paragraph, TextRun, AlignmentType, Footer, Header, PageNumber,
  TableOfContents, LevelFormat, PageOrientation, BorderStyle, SectionType, TabStopType,
} = require('docx');
const L = require('./lib');
const { FONT, C, GREY, SIZE, fr, P, TABLE, H1 } = L;
const { section1, section2, section3, section4 } = require('./body1');
const { section5, section6, section7 } = require('./body2');
const { section8, section9, section10, section11 } = require('./body3');

const TITLE = 'CADRE MÉTHODOLOGIQUE DES INDICATEURS DE SUIVI DE LA VISION AGRICOLE';
const SUB = 'Définitions, indicateurs, méthodes de calcul et fondements scientifiques';
const DATE = 'Septembre 2026';

const A4 = { width: 11906, height: 16838 };
const marginsP = { top: 1418, bottom: 1304, left: 1418, right: 1418, header: 709, footer: 624 };
const marginsL = { top: 1134, bottom: 1134, left: 1134, right: 1134, header: 567, footer: 510 };

function header(width) {
  return new Header({ children: [new Paragraph({
    tabStops: [{ type: TabStopType.RIGHT, position: width }],
    border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: 'B7C9BE', space: 4 } },
    children: [
      new TextRun({ text: fr('Cadre méthodologique des indicateurs de la vision agricole'), font: FONT, size: 17, color: GREY, smallCaps: true }),
      new TextRun({ text: fr('\tDocument méthodologique de travail'), font: FONT, size: 17, color: GREY, italics: true }),
    ],
  })] });
}
function footer() {
  return new Footer({ children: [new Paragraph({
    alignment: AlignmentType.CENTER,
    children: [new TextRun({ children: [PageNumber.CURRENT], font: FONT, size: 20, color: GREY })],
  })] });
}

function cover() {
  const line = (o = {}) => new Paragraph({ spacing: { before: o.before || 0, after: o.after || 0 }, border: { bottom: { style: BorderStyle.SINGLE, size: o.size || 12, color: C, space: 1 } }, children: [] });
  return [
    new Paragraph({ spacing: { before: 2600, after: 0 }, children: [] }),
    line({ size: 18, after: 360 }),
    new Paragraph({ spacing: { after: 360, line: 300 , lineRule: 'auto'}, children: [new TextRun({ text: fr(TITLE), font: FONT, size: 50, bold: true, color: C })] }),
    new Paragraph({ spacing: { after: 360 }, children: [new TextRun({ text: fr(SUB), font: FONT, size: 30, italics: true, color: GREY })] }),
    line({ size: 6, after: 0 }),
    new Paragraph({ spacing: { before: 4300 }, children: [new TextRun({ text: fr('Document méthodologique de travail'), font: FONT, size: 26, color: '222222' })] }),
    new Paragraph({ spacing: { before: 120 }, children: [new TextRun({ text: 'Côte d’Ivoire', font: FONT, size: 26, bold: true, color: C })] }),
    new Paragraph({ spacing: { before: 120 }, children: [new TextRun({ text: DATE, font: FONT, size: 24, color: GREY })] }),
  ];
}

function tocAndAcronyms() {
  const t = (s) => new Paragraph({ spacing: { after: 240 }, children: [new TextRun({ text: fr(s), font: FONT, size: 32, bold: true, color: C })] });
  const sigles = [
    ['ADERIZ', 'Agence pour le développement de la filière riz'], ['AFAT', 'Agriculture, foresterie et autres affectations des terres'],
    ['AFD', 'Agence française de développement'], ['AFOR', 'Agence foncière rurale'],
    ['ANADER', 'Agence nationale d\'appui au développement rural'], ['ANStat', 'Agence nationale de la statistique'],
    ['APHLIS', 'African Postharvest Losses Information System'], ['ARS', 'African Regional Standard (norme régionale africaine)'],
    ['BCEAO', 'Banque centrale des États de l\'Afrique de l\'Ouest'], ['BNETD-CCT', 'Bureau national d\'études techniques et de développement – Centre de cartographie et de télédétection'],
    ['CCNUCC', 'Convention-cadre des Nations unies sur les changements climatiques'], ['CDN', 'Contribution déterminée au niveau national'],
    ['CGAP', 'Consultative Group to Assist the Poor'], ['CVGFR', 'Comité villageois de gestion foncière rurale'],
    ['EHCVM', 'Enquête harmonisée sur les conditions de vie des ménages'], ['FAO', 'Organisation des Nations unies pour l\'alimentation et l\'agriculture'],
    ['FIES', 'Food Insecurity Experience Scale (échelle de mesure de l\'insécurité alimentaire vécue)'], ['FRA', 'Global Forest Resources Assessment (évaluation des ressources forestières mondiales)'],
    ['GES', 'Gaz à effet de serre'], ['GIEC', 'Groupe d\'experts intergouvernemental sur l\'évolution du climat'],
    ['ICCO', 'Organisation internationale du cacao'], ['IFPRI', 'Institut international de recherche sur les politiques alimentaires'],
    ['JRC TMF', 'Centre commun de recherche de la Commission européenne – Tropical Moist Forest'], ['ODD', 'Objectifs de développement durable'],
    ['PDDAA', 'Programme détaillé pour le développement de l\'agriculture africaine (CAADP)'], ['PNSFR', 'Programme national de sécurisation foncière rurale'],
    ['REDD+', 'Réduction des émissions dues à la déforestation et à la dégradation des forêts'], ['REEA', 'Recensement des exploitants et exploitations agricoles'],
    ['ReSAKSS', 'Regional Strategic Analysis and Knowledge Support System'], ['RGPH', 'Recensement général de la population et de l\'habitat'],
    ['SEP-REDD+', 'Secrétariat exécutif permanent de la REDD+'], ['SFD', 'Systèmes financiers décentralisés'],
    ['SIFOR', 'Système d\'information foncière rurale'], ['SNSFR', 'Stratégie nationale de sécurisation foncière rurale'],
    ['tCO₂e', 'Tonne d\'équivalent dioxyde de carbone'], ['UEMOA', 'Union économique et monétaire ouest-africaine'],
    ['USDA ERS', 'Economic Research Service du département de l\'Agriculture des États-Unis'], ['VGGT', 'Directives volontaires pour une gouvernance responsable des régimes fonciers (FAO)'],
  ];
  return [
    t('Table des matières'),
    new TableOfContents('Table des matières', { hyperlink: true, headingStyleRange: '1-2' }),
    new Paragraph({ pageBreakBefore: true, spacing: { after: 240 }, children: [new TextRun({ text: fr('Sigles et abréviations'), font: FONT, size: 32, bold: true, color: C })] }),
    TABLE({ widths: [1900, 7170], rows: sigles.map(([a, b]) => [{ c: a, bold: true, color: C }, b]), size: 20 }),
  ];
}

const portrait = { page: { size: { ...A4, orientation: PageOrientation.PORTRAIT }, margin: marginsP } };
const landscape = { page: { size: { width: A4.width, height: A4.height, orientation: PageOrientation.LANDSCAPE }, margin: marginsL } };

const main1 = [...section1(), ...section2(), ...section3(), ...section4(), ...section5(), ...section6(), ...section7()];
const s8 = section8();
const rest = [...section9(), ...section10(), ...section11()];

const doc = new Document({
  creator: 'Cabinet du Ministre de l’Agriculture',
  title: 'Cadre méthodologique des indicateurs de suivi de la vision agricole',
  description: SUB,
  features: { updateFields: true },
  styles: {
    default: { document: { run: { font: FONT, size: SIZE }, paragraph: { spacing: { line: 276 , lineRule: 'auto'} } } },
    paragraphStyles: [
      { id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true,
        run: { font: FONT, size: 36, bold: true, color: C },
        paragraph: { spacing: { before: 120, after: 280 }, outlineLevel: 0, keepNext: true,
          border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: C, space: 6 } } } },
      { id: 'Heading2', name: 'Heading 2', basedOn: 'Normal', next: 'Normal', quickFormat: true,
        run: { font: FONT, size: 27, bold: true, color: C },
        paragraph: { spacing: { before: 320, after: 140 }, outlineLevel: 1, keepNext: true, keepLines: true } },
      { id: 'Heading3', name: 'Heading 3', basedOn: 'Normal', next: 'Normal', quickFormat: true,
        run: { font: FONT, size: 24, bold: true, italics: true, color: '333333' },
        paragraph: { spacing: { before: 240, after: 100 }, outlineLevel: 2, keepNext: true } },
    ],
  },
  numbering: { config: [
    { reference: 'bullets', levels: [
      { level: 0, format: LevelFormat.BULLET, text: '–', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 400, hanging: 260 } }, run: { color: C } } },
      { level: 1, format: LevelFormat.BULLET, text: '·', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 800, hanging: 260 } } } },
    ] },
    { reference: 'steps', levels: [
      { level: 0, format: LevelFormat.DECIMAL, text: '%1.', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 400, hanging: 300 } }, run: { color: C, bold: true } } },
    ] },
  ] },
  sections: [
    { properties: { ...portrait }, children: cover() },
    { properties: { ...portrait, type: SectionType.NEXT_PAGE, page: { ...portrait.page, pageNumbers: { start: 1 } } },
      headers: { default: header(9070) }, footers: { default: footer() }, children: [...tocAndAcronyms(), ...main1] },
    { properties: { ...landscape, type: SectionType.NEXT_PAGE },
      headers: { default: header(14570) }, footers: { default: footer() }, children: s8 },
    { properties: { ...portrait, type: SectionType.NEXT_PAGE },
      headers: { default: header(9070) }, footers: { default: footer() }, children: rest },
  ],
});

const out = process.argv[2] || 'Cadre_methodologique_15_indicateurs_Vision_Agricole_CIV.docx';
Packer.toBuffer(doc).then((buf) => { fs.writeFileSync(out, buf); console.log('OK', out, buf.length); });
