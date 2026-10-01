// Système graphique des fiches de revue documentaire du Cabinet (docx-js).
// Garamond pour le texte courant ; Calibri pour les tableaux et libellés ;
// Arial pour les marqueurs de priorité (glyphes du jeu WGL4, présents partout).

const fs = require('fs');
const {
  Document, Paragraph, TextRun, Table, TableRow, TableCell, ImageRun, Footer, PageNumber, Tab,
  WidthType, BorderStyle, ShadingType, AlignmentType, VerticalAlign, TableLayoutType,
  LineRuleType, HeadingLevel, TabStopType, HeightRule,
} = require('docx');

// ------------------------------------------------------------------ constantes
const C = {
  INK: '1F2328', GRAY_D: '4A5058', GRAY_M: '6B7280', GRAY_L: 'C9CDD2', GRAY_XL: 'E3E6E9',
  GRAY_BG: 'F4F5F6', ORANGE: 'D9730D', GREEN: '1B7A4C', BRICK: 'B03A12', FORME: '8A9096',
};
const F = { SERIF: 'Garamond', SANS: 'Calibri', SYM: 'Arial' };
const PAGE = { W: 11906, H: 16838, TOP: 851, BOTTOM: 1020, SIDE: 992, HEADER: 454, FOOTER: 482 };
const TEXT_W = PAGE.W - 2 * PAGE.SIDE; // 9922 DXA = 17,5 cm
const cm = (x) => Math.round(x * 566.929);

const PRIO = {
  C: { sym: '■', color: C.BRICK, label: 'Critique', plural: 'Critique', caps: 'CRITIQUE' },
  M: { sym: '▲', color: C.ORANGE, label: 'Majeur', plural: 'Majeures', caps: 'MAJEUR' },
  A: { sym: '●', color: C.GREEN, label: 'À corriger', plural: 'À corriger', caps: 'À CORRIGER' },
  F: { sym: '○', color: C.FORME, label: 'Forme', plural: 'De forme', caps: 'FORME' },
};
const PRIO_DEF = {
  C: 'peut rendre le document inexact, contradictoire ou impropre à la transmission',
  M: 'modifie sensiblement le sens, la compréhension ou la crédibilité',
  A: 'à reprendre, sans remise en cause de l’ensemble du document',
  F: 'correction rédactionnelle, typographique ou graphique',
};

// ------------------------------------------------------------------ texte
const NB = '\u00A0';
// Typographie française : espaces insécables (milliers, unités, ponctuation haute, guillemets).
function typo(s) {
  if (!s) return s;
  let t = s;
  let prev;
  do { prev = t; t = t.replace(/(\d) (\d{3})(?!\d)/g, `$1${NB}$2`); } while (t !== prev);
  t = t.replace(/ ([:;!?»%])/g, `${NB}$1`);
  t = t.replace(/« /g, `«${NB}`);
  t = t.replace(/(\d) (t|ha|Mds|Mt|FCFA|kg|pages)(?=[\s.,;:)]|$)/g, `$1${NB}$2`);
  t = t.replace(/ (–|·) /g, `${NB}$1 `);
  t = t.replace(/(§|[Tt]ableaux?|[Pp]oint|[Pp]artie|[Pp]arties|n°) (\d)/g, `$1${NB}$2`);
  t = t.replace(/ et (\d)/g, ` et${NB}$1`);
  t = t.replace(/\b(OBS|A|V)-(\d)/g, '$1\u2011$2'); // converti en <w:noBreakHyphen/> au post-traitement
  return t;
}
// Balisage minimal : **gras**, *italique*, ^exposant^, [[zone à renseigner]].
function parse(s) {
  const out = []; let b = false, i = false, sup = false, ph = false, buf = '';
  const flush = () => { if (buf) out.push({ t: buf, b, i, sup, ph }); buf = ''; };
  for (let k = 0; k < s.length;) {
    if (s.startsWith('[[', k)) { flush(); ph = true; buf = '['; k += 2; continue; }
    if (s.startsWith(']]', k) && ph) { buf += ']'; flush(); ph = false; k += 2; continue; }
    if (s.startsWith('**', k)) { flush(); b = !b; k += 2; continue; }
    if (s[k] === '*') { flush(); i = !i; k += 1; continue; }
    if (s[k] === '^') { flush(); sup = !sup; k += 1; continue; }
    buf += s[k]; k += 1;
  }
  flush();
  return out;
}
const LANG = { value: 'fr-FR' };
function R(text, o = {}) {
  return parse(typo(String(text))).map((sg) => new TextRun({
    text: sg.t,
    font: o.font || F.SERIF,
    size: o.size || 22,
    color: sg.ph ? C.GRAY_M : (o.color || C.INK),
    bold: o.bold || sg.b || undefined,
    italics: o.italics || sg.i || sg.ph || undefined,
    superScript: sg.sup || undefined,
    allCaps: o.caps || undefined,
    characterSpacing: o.spacing || undefined,
    language: LANG,
  }));
}
const sym = (p, size = 18) => new TextRun({ text: PRIO[p].sym, font: F.SYM, size, color: PRIO[p].color, language: LANG });

function P(children, o = {}) {
  return new Paragraph({
    children,
    alignment: o.align,
    spacing: { before: o.before || 0, after: o.after || 0, line: o.line || 252, lineRule: o.exact ? LineRuleType.EXACT : LineRuleType.AUTO },
    keepNext: o.keepNext, keepLines: o.keepLines, indent: o.indent, border: o.border,
    tabStops: o.tabStops, pageBreakBefore: o.pageBreakBefore, heading: o.heading, style: o.style,
  });
}
// Libellé discret (petites capitales espacées).
const label = (text, o = {}) => R(text, { font: F.SANS, size: o.size || 14, bold: true, caps: true, spacing: o.spacing || 20, color: o.color || C.GRAY_M });

// ------------------------------------------------------------------ tableaux
const NONE = { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' };
const line = (size, color) => ({ style: BorderStyle.SINGLE, size, color });
const NO_BORDERS = { top: NONE, bottom: NONE, left: NONE, right: NONE };
const TBL_NO_BORDERS = { ...NO_BORDERS, insideHorizontal: NONE, insideVertical: NONE };

function Cell(children, o = {}) {
  return new TableCell({
    children,
    width: { size: o.w, type: WidthType.DXA },
    columnSpan: o.span,
    verticalAlign: o.valign || VerticalAlign.TOP,
    margins: { top: o.mt ?? 70, bottom: o.mb ?? 70, left: o.ml ?? 90, right: o.mr ?? 90 },
    borders: { ...NO_BORDERS, ...(o.borders || {}) },
    shading: o.fill ? { type: ShadingType.CLEAR, color: 'auto', fill: o.fill } : undefined,
  });
}
function Tbl(rows, widths) {
  return new Table({
    rows,
    width: { size: widths.reduce((a, b) => a + b, 0), type: WidthType.DXA },
    columnWidths: widths,
    layout: TableLayoutType.FIXED,
    borders: TBL_NO_BORDERS,
  });
}
const Row = (cells, o = {}) => new TableRow({
  children: cells, cantSplit: o.cantSplit !== false, tableHeader: o.header || undefined,
  height: o.height ? { value: o.height, rule: HeightRule.ATLEAST } : undefined,
});

// ------------------------------------------------------------------ composants
function enTeteInstitutionnel(armoiriesPng) {
  const wArms = cm(2.45), wText = TEXT_W - wArms;
  // Armoiries : proportions d'origine (500 × 443 px) strictement conservées.
  const largeurPx = (2.05 / 2.54) * 96;
  const hauteurPx = largeurPx * 443 / 500;
  const arms = new ImageRun({
    type: 'png', data: fs.readFileSync(armoiriesPng),
    transformation: { width: largeurPx, height: hauteurPx },
    altText: { name: 'Armoiries', title: 'Armoiries de la République de Côte d’Ivoire', description: 'Armoiries officielles de la République de Côte d’Ivoire' },
  });
  const inner = wText - 200;
  return Tbl([Row([
    Cell([P([arms])], { w: wArms, valign: VerticalAlign.CENTER, ml: 0, mr: 0, mt: 0, mb: 150, borders: { bottom: line(12, C.ORANGE) } }),
    Cell([
      P(R('République de Côte d’Ivoire', { size: 21, bold: true, caps: true, spacing: 16 })),
      P(R('Union – Discipline – Travail', { size: 19, italics: true, color: C.GRAY_D }), { after: 30 }),
      P([], { exact: true, line: 70, after: 70, indent: { right: inner - cm(0.9) }, border: { bottom: line(6, C.ORANGE) } }),
      P(R('Ministère de l’Agriculture, du Développement Rural', { size: 19, bold: true, caps: true, spacing: 6 })),
      P(R('et des Productions Vivrières', { size: 19, bold: true, caps: true, spacing: 6 })),
      P(R('Cabinet du Ministre', { font: F.SANS, size: 16, bold: true, caps: true, spacing: 40, color: C.GREEN }), { before: 60 }),
    ], { w: wText, valign: VerticalAlign.CENTER, ml: 200, mr: 0, mt: 0, mb: 150, borders: { bottom: line(4, C.GRAY_L) } }),
  ])], [wArms, wText]);
}

function blocTitre(titre, sousTitre) {
  return [
    P(R(titre, { size: 33, bold: true, spacing: 10 }), { before: 250, after: 30 }),
    P(R(sousTitre, { size: 23, italics: true, color: C.GRAY_D }), { after: 130 }),
  ];
}

function blocIdentification(id) {
  const n = id.champs.length; const w = Math.floor(TEXT_W / n); const ws = Array(n).fill(w); ws[n - 1] = TEXT_W - w * (n - 1);
  const champ = (c, k) => Cell([
    P(label(c.label), { after: 30 }),
    P(R(c.valeur, { size: 21 })),
    ...(c.note ? [P(R(c.note, { font: F.SANS, size: 15, color: C.GRAY_M }), { before: 20 })] : []),
  ], { w: ws[k], ml: k === 0 ? 0 : 150, mr: 90, mt: 80, mb: 80, borders: { bottom: line(4, C.GRAY_XL), ...(k > 0 ? { left: line(4, C.GRAY_XL) } : {}) } });
  return Tbl([
    Row([Cell([P(label('Document examiné'), { after: 40 }), P(R(id.document, { size: 24, bold: true }), { line: 260 })],
      { w: TEXT_W, span: n, ml: 0, mt: 90, mb: 90, borders: { top: line(8, C.GREEN), bottom: line(4, C.GRAY_XL) } })]),
    Row(id.champs.map(champ)),
    Row([Cell([P(label('Objet'), { after: 30 }), P(R(id.objet, { size: 21 }))],
      { w: TEXT_W, span: n, ml: 0, mt: 80, mb: 90, borders: { bottom: line(4, C.GRAY_L) } })]),
  ], ws);
}

function titreSection(texte, o = {}) {
  return P(R(texte, { font: F.SANS, size: 18, bold: true, caps: true, spacing: 24, color: C.GREEN }), {
    heading: HeadingLevel.HEADING_1, pageBreakBefore: o.pageBreakBefore, keepNext: true, keepLines: true,
    before: o.before ?? 250, after: o.after ?? 100, indent: { left: 130 },
    border: { left: { style: BorderStyle.SINGLE, size: 18, color: C.ORANGE, space: 5 } },
  });
}

function tuiles(stats) {
  const gap = cm(0.3); const n = stats.length;
  const wt = Math.floor((TEXT_W - gap * (n - 1)) / n);
  const widths = []; stats.forEach((_, k) => { widths.push(wt); if (k < n - 1) widths.push(gap); });
  widths[widths.length - 1] += TEXT_W - widths.reduce((a, b) => a + b, 0);
  const cells = [];
  stats.forEach((s, k) => {
    const color = s.prio ? PRIO[s.prio].color : C.INK;
    cells.push(Cell([
      P(R(String(s.valeur), { size: 46, bold: true }), { line: 240 }),
      P([...(s.prio ? [sym(s.prio, 14), new TextRun({ text: NB + NB, size: 14 })] : []), ...label(s.label, { size: 14, color: C.GRAY_D })], { before: 10 }),
    ], { w: widths[cells.length], ml: 40, mr: 40, mt: 50, mb: 70, borders: { top: line(18, color), bottom: line(4, C.GRAY_L) } }));
    if (k < n - 1) cells.push(Cell([P([])], { w: widths[cells.length], ml: 0, mr: 0 }));
  });
  return Tbl([Row(cells)], widths);
}

function blocStatut(s) {
  const w1 = cm(5.4), w2 = TEXT_W - w1;
  return Tbl([Row([
    Cell([
      P(label('Statut global'), { after: 50 }),
      P(R(s.statut, { font: F.SANS, size: 21, bold: true, caps: true, spacing: 6, color: C.BRICK })),
      ...(s.complements ? [P(R(s.complements, { font: F.SANS, size: 16, color: C.GRAY_M }), { before: 50 })] : []),
    ], { w: w1, ml: 170, mt: 90, mb: 90, valign: VerticalAlign.CENTER, borders: { left: line(24, C.BRICK) } }),
    Cell([
      P(label('Appréciation'), { after: 50 }),
      P(R(s.appreciation, { size: 21, italics: true, color: C.GRAY_D }), { line: 264 }),
    ], { w: w2, ml: 220, mt: 90, mb: 90, valign: VerticalAlign.CENTER, borders: { left: line(4, C.GRAY_XL) } }),
  ])], [w1, w2]);
}

function ligneEtiquetee(etiquette, texte, o = {}) {
  return P([...label(etiquette + NB + NB), ...R(texte, { size: 21 })], { before: o.before ?? 120, line: 260, keepLines: true });
}

// Liste compacte (lecture Cabinet) : marqueur + référence | texte.
function listeEssentiel(items) {
  const w1 = cm(2.1), w2 = TEXT_W - w1;
  return Tbl(items.map((it, k) => Row([
    Cell([P([...(it.prio ? [sym(it.prio, 17), new TextRun({ text: NB + NB, size: 17 })] : []),
      ...R(it.ref, { font: F.SANS, size: 18, bold: true, color: it.prio ? C.INK : C.GREEN })])],
    { w: w1, ml: 0, mt: 45, mb: 45, borders: { bottom: line(4, C.GRAY_XL), ...(k === 0 ? { top: line(4, C.GRAY_L) } : {}) } }),
    Cell([P(R(it.texte, { size: 21 }), { line: 252 })],
      { w: w2, ml: 60, mt: 45, mb: 45, borders: { bottom: line(4, C.GRAY_XL), ...(k === 0 ? { top: line(4, C.GRAY_L) } : {}) } }),
  ])), [w1, w2]);
}

function legendePriorites() {
  const w = Math.floor(TEXT_W / 4); const ws = [w, w, w, TEXT_W - 3 * w];
  return Tbl([Row(['C', 'M', 'A', 'F'].map((p, k) => Cell([
    P([sym(p, 15), new TextRun({ text: NB + NB, size: 15 }), ...R(PRIO[p].caps, { font: F.SANS, size: 15, bold: true, spacing: 10, color: C.INK })]),
    P(R(PRIO_DEF[p], { font: F.SANS, size: 15, color: C.GRAY_M }), { before: 20, line: 240 }),
  ], { w: ws[k], ml: k === 0 ? 0 : 110, mr: 60, mt: 40, mb: 40, borders: k > 0 ? { left: line(4, C.GRAY_XL) } : {} })))], ws);
}

const OBS_W = [cm(1.35), cm(2.4), cm(2.0), 0, cm(3.9), cm(1.85)];
OBS_W[3] = TEXT_W - OBS_W.reduce((a, b) => a + b, 0);

function tableauObservations(observations, o = {}) {
  const W = OBS_W;
  const tete = ['Réf.', 'Localisation', 'Catégorie', 'Constat', 'Correction / action attendue', 'Priorité'];
  const rows = [Row(tete.map((t, k) => Cell([P(label(t, { size: 14, color: C.GRAY_D }), { align: k === 5 ? AlignmentType.CENTER : undefined })],
    { w: W[k], ml: k === 0 ? 30 : 80, mr: 80, mt: 40, mb: 60, valign: VerticalAlign.BOTTOM, borders: { bottom: line(8, C.GREEN) } })), { header: true })];
  const groupes = ['C', 'M', 'A', 'F'];
  for (const g of groupes) {
    const obs = observations.filter((x) => x.prio === g);
    if (!obs.length) continue;
    if (o.groupes !== false) {
      const n = obs.length;
      rows.push(Row([Cell([P([sym(g, 15), new TextRun({ text: NB + NB, size: 15 }),
        ...R(PRIO[g].caps, { font: F.SANS, size: 15, bold: true, spacing: 20, color: C.INK }),
        ...R(`${NB}${NB}·${NB}${NB}${n} observation${n > 1 ? 's' : ''}`, { font: F.SANS, size: 15, color: C.GRAY_M })], { keepNext: true })],
      { w: TEXT_W, span: 6, ml: 30, mt: 45, mb: 45, fill: C.GRAY_BG, borders: { bottom: line(4, C.GRAY_L) } })]));
    }
    obs.forEach((x) => {
      const b = { bottom: line(4, C.GRAY_XL) };
      rows.push(Row([
        Cell([P(R(x.id, { font: F.SANS, size: 18, bold: true }))], { w: W[0], ml: 30, mr: 30, mt: 45, mb: 45, borders: b }),
        Cell(x.loc.map((l) => P(R(l, { font: F.SANS, size: 18, color: C.GRAY_D }), { line: 240 })), { w: W[1], ml: 80, mr: 50, mt: 45, mb: 45, borders: b }),
        Cell([P(R(x.cat, { font: F.SANS, size: 18, color: C.GRAY_D }), { line: 240 })], { w: W[2], ml: 80, mr: 30, mt: 45, mb: 45, borders: b }),
        Cell([P(R(x.constat, { font: F.SANS, size: 18 }), { line: 240 })], { w: W[3], ml: 80, mr: 80, mt: 45, mb: 45, borders: b }),
        Cell([P(R(x.action, { font: F.SANS, size: 18 }), { line: 240 })], { w: W[4], ml: 80, mr: 60, mt: 45, mb: 45, borders: b }),
        Cell([P([sym(x.prio, 18)], { align: AlignmentType.CENTER }),
          P(R(PRIO[x.prio].caps, { font: F.SANS, size: 18, bold: true, color: C.INK }), { align: AlignmentType.CENTER, before: 10 })],
        { w: W[5], ml: 40, mr: 40, mt: 45, mb: 45, borders: b }),
      ]));
    });
  }
  return Tbl(rows, W);
}

function tableauSimple(entetes, widths, lignes) {
  const rows = [Row(entetes.map((t, k) => Cell([P(label(t, { size: 14, color: C.GRAY_D }))],
    { w: widths[k], ml: k === 0 ? 30 : 80, mr: 80, mt: 40, mb: 60, valign: VerticalAlign.BOTTOM, borders: { bottom: line(8, C.GREEN) } })), { header: true })];
  lignes.forEach((cells) => rows.push(Row(cells.map((c, k) => Cell(c, { w: widths[k], ml: k === 0 ? 30 : 80, mr: 80, mt: 45, mb: 45, borders: { bottom: line(4, C.GRAY_XL) } })))));
  return Tbl(rows, widths);
}
const cellTexte = (t, o = {}) => [P(R(t, { font: F.SANS, size: o.size || 18, bold: o.bold, color: o.color }), { line: 240 })];

function encadre(texte, o = {}) {
  return Tbl([Row([Cell([P(R(texte, { size: 22 }), { line: 276 })],
    { w: TEXT_W, ml: 230, mr: 200, mt: 130, mb: 130, fill: o.fill || C.GRAY_BG, borders: { left: line(24, o.color || C.GREEN) } })])], [TEXT_W]);
}

function piedDePage(gauche, droite) {
  return new Footer({ children: [P([
    ...R(gauche, { font: F.SANS, size: 14, color: C.GRAY_M }),
    new TextRun({ children: [new Tab()], font: F.SANS, size: 14 }),
    ...R(droite + NB + NB + '·' + NB + NB, { font: F.SANS, size: 14, color: C.GRAY_M }),
    new TextRun({ children: ['Page ', PageNumber.CURRENT, ' / ', PageNumber.TOTAL_PAGES], font: F.SANS, size: 14, color: C.GRAY_D, language: LANG }),
  ], { style: 'PiedDePageCabinet', tabStops: [{ type: TabStopType.RIGHT, position: TEXT_W }], border: { top: { style: BorderStyle.SINGLE, size: 4, color: C.GRAY_L, space: 6 } } })] });
}

function document(meta, children, footer) {
  return new Document({
    creator: 'Cabinet du Ministre – MINADER',
    lastModifiedBy: 'Cabinet du Ministre – MINADER',
    title: meta.titre, subject: meta.sujet, keywords: meta.motsCles, description: meta.description || meta.sujet,
    styles: {
      default: { document: { run: { font: F.SERIF, size: 22, color: C.INK, language: LANG }, paragraph: { spacing: { after: 0, line: 252 } } } },
      paragraphStyles: [{
        id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true,
        run: { font: F.SANS, size: 18, bold: true, color: C.GREEN },
        paragraph: { spacing: { before: 250, after: 100 }, keepNext: true, outlineLevel: 0 },
      }, {
        id: 'PiedDePageCabinet', name: 'Pied de page Cabinet', basedOn: 'Normal', quickFormat: true,
        run: { font: F.SANS, size: 14, color: C.GRAY_D },
      }],
    },
    sections: [{
      properties: { page: {
        size: { width: PAGE.W, height: PAGE.H },
        margin: { top: PAGE.TOP, bottom: PAGE.BOTTOM, left: PAGE.SIDE, right: PAGE.SIDE, header: PAGE.HEADER, footer: PAGE.FOOTER },
      } },
      footers: { default: footer },
      children,
    }],
  });
}

module.exports = {
  C, F, PRIO, TEXT_W, cm, NB, typo, R, P, label, sym, line, Cell, Tbl, Row, NO_BORDERS,
  enTeteInstitutionnel, blocTitre, blocIdentification, titreSection, tuiles, blocStatut, ligneEtiquetee,
  listeEssentiel, legendePriorites, tableauObservations, tableauSimple, cellTexte, encadre, piedDePage, document,
};
