// Mise en forme : helpers de paragraphes, tableaux, encadrés et équations
const {
  Paragraph, TextRun, HeadingLevel, AlignmentType, Table, TableRow, TableCell,
  WidthType, ShadingType, BorderStyle, TabStopType, VerticalAlign, Math: OMath,
} = require('docx');
const { arr } = require('./mathh');

const FONT = 'Garamond';
const C = '1F4E3D';      // vert institutionnel sobre
const TINT = 'EDF3EF';   // teinte claire
const RULE = 'B7C9BE';   // filets
const GREY = '4A4A4A';
const BODY = 22;         // 11 pt… ajusté ci-dessous
const SIZE = 24;         // 12 pt pour Garamond

// Typographie française : apostrophe typographique et espaces insécables
function fr(s) {
  return s
    .replace(/'/g, '’')
    .replace(/ ([:;?!»%])/g, ' $1')
    .replace(/« /g, '« ');
}

// Mini-balisage : **gras**, *italique*, _{indice}, ^{exposant}
function rt(str, base = {}) {
  const out = [];
  const re = /(\*\*[^*]+\*\*|\*[^*]+\*|_\{[^}]*\}|\^\{[^}]*\})/g;
  let last = 0; let m;
  const push = (t, extra = {}) => { if (t) out.push(new TextRun({ text: fr(t), font: FONT, ...base, ...extra })); };
  while ((m = re.exec(str)) !== null) {
    push(str.slice(last, m.index));
    const tok = m[0];
    if (tok.startsWith('**')) push(tok.slice(2, -2), { bold: true });
    else if (tok.startsWith('*')) push(tok.slice(1, -1), { italics: true });
    else if (tok.startsWith('_{')) push(tok.slice(2, -1), { subScript: true });
    else push(tok.slice(2, -1), { superScript: true });
    last = m.index + tok.length;
  }
  push(str.slice(last));
  return out;
}

function P(str, o = {}) {
  return new Paragraph({
    alignment: o.align || AlignmentType.JUSTIFIED,
    spacing: { after: o.after ?? 140, before: o.before ?? 0, line: o.line ?? 276 , lineRule: 'auto'},
    indent: o.indent,
    keepNext: o.keepNext,
    children: typeof str === 'string' ? rt(str, { size: o.size || SIZE, color: o.color, italics: o.italics, bold: o.bold }) : str,
  });
}

// Paragraphe à intitulé intégré (« run-in heading ») en italique
function PL(label, str, o = {}) {
  return new Paragraph({
    alignment: AlignmentType.JUSTIFIED,
    spacing: { after: o.after ?? 140, line: 276 , lineRule: 'auto'},
    children: [new TextRun({ text: fr(label + '. '), font: FONT, size: SIZE, italics: true, color: C }), ...rt(str, { size: SIZE })],
  });
}

function B(str, level = 0, o = {}) {
  return new Paragraph({
    numbering: { reference: o.ref || 'bullets', level },
    alignment: AlignmentType.JUSTIFIED,
    spacing: { after: o.after ?? 80, line: 264 , lineRule: 'auto'},
    children: rt(str, { size: o.size || SIZE }),
  });
}
function N(str, ref = 'steps') {
  return new Paragraph({
    numbering: { reference: ref, level: 0 },
    alignment: AlignmentType.JUSTIFIED,
    spacing: { after: 80, line: 264 , lineRule: 'auto'},
    children: rt(str, { size: SIZE }),
  });
}

function H1(text, o = {}) {
  return new Paragraph({ heading: HeadingLevel.HEADING_1, pageBreakBefore: o.pageBreak !== false, children: [new TextRun({ text: fr(text) })] });
}
function H2(text) { return new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun({ text: fr(text) })] }); }
function H3(text) { return new Paragraph({ heading: HeadingLevel.HEADING_3, children: [new TextRun({ text: fr(text) })] }); }

// Chaîne logique (centrée, italique, couleur institutionnelle)
function LOGIC(text) {
  return new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 120, after: 200 },
    border: { top: { style: BorderStyle.SINGLE, size: 4, color: RULE, space: 6 }, bottom: { style: BorderStyle.SINGLE, size: 4, color: RULE, space: 6 } },
    children: [new TextRun({ text: fr(text), font: FONT, size: SIZE, italics: true, color: C })],
  });
}

// Équations numérotées
let EQN = 0;
function EQ(mathArr, width = 9070) {
  EQN += 1;
  return new Paragraph({
    tabStops: [{ type: TabStopType.CENTER, position: Math.round(width / 2) }, { type: TabStopType.RIGHT, position: width }],
    spacing: { before: 120, after: 160, line: 240, lineRule: 'auto' },
    keepLines: true,
    children: [new TextRun({ text: '\t', font: FONT }), ...mathArr, new TextRun({ text: `\t(${EQN})`, font: FONT, size: 22, color: GREY })],
  });
}
function eqNum() { return EQN; }

// Légende de tableau numérotée
let TABN = 0;
function CAPTION(text) {
  TABN += 1;
  return new Paragraph({
    keepNext: true,
    spacing: { before: 200, after: 80 },
    children: [
      new TextRun({ text: `Tableau ${TABN}. `, font: FONT, size: 21, bold: true, color: C }),
      new TextRun({ text: fr(text), font: FONT, size: 21, italics: true, color: GREY }),
    ],
  });
}
function SOURCE(text) {
  return new Paragraph({ spacing: { before: 60, after: 200 }, children: rt(text, { size: 18, italics: true, color: GREY }) });
}

const thin = { style: BorderStyle.SINGLE, size: 4, color: RULE };
const none = { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' };

// Contenu de cellule : chaîne (lignes séparées par \n ; « - » en début = puce) ou tableau d'objets
function cellParas(content, o) {
  if (Array.isArray(content)) return content;
  const lines = String(content).split('\n');
  return lines.map((l) => {
    const bullet = l.startsWith('- ');
    return new Paragraph({
      alignment: o.align || AlignmentType.LEFT,
      spacing: { after: 30, before: 30, line: 240 , lineRule: 'auto'},
      indent: bullet ? { left: 170, hanging: 170 } : undefined,
      children: rt(bullet ? '– ' + l.slice(2) : l, { size: o.size, bold: o.bold, color: o.color, italics: o.italics }),
    });
  });
}
function CELL(content, o = {}) {
  return new TableCell({
    width: { size: o.w, type: WidthType.DXA },
    columnSpan: o.span, rowSpan: o.rowSpan,
    verticalAlign: o.valign || VerticalAlign.TOP,
    shading: o.fill ? { type: ShadingType.CLEAR, color: 'auto', fill: o.fill } : undefined,
    margins: { top: 50, bottom: 50, left: 90, right: 90 },
    borders: o.borders || { top: thin, bottom: thin, left: thin, right: thin },
    children: cellParas(content, o),
  });
}

// Tableau générique : head = [..] ; rows = [[cell|{c, span, rowSpan, fill, bold}]]
function TABLE({ widths, head, rows, size = 18, headSize, zebra = false, firstBold = false }) {
  const total = widths.reduce((a, b) => a + b, 0);
  const trs = [];
  if (head) {
    trs.push(new TableRow({
      tableHeader: true, cantSplit: true,
      children: head.map((h, j) => CELL(h, { w: widths[j], fill: C, color: 'FFFFFF', bold: true, size: headSize || size, valign: VerticalAlign.CENTER })),
    }));
  }
  rows.forEach((row, i) => {
    let col = 0;
    trs.push(new TableRow({
      cantSplit: true,
      children: row.map((c) => {
        const spec = (c && typeof c === 'object' && !Array.isArray(c) && 'c' in c) ? c : { c };
        const span = spec.span || 1;
        const w = widths.slice(col, col + span).reduce((a, b) => a + b, 0);
        const isFirst = col === 0;
        col += span;
        return CELL(spec.c, {
          w, span: spec.span, rowSpan: spec.rowSpan, size: spec.size || size,
          fill: spec.fill || (zebra && i % 2 === 1 ? 'F6F8F7' : undefined),
          bold: spec.bold ?? (firstBold && isFirst), color: spec.color, italics: spec.italics,
          align: spec.align, valign: spec.valign,
        });
      }),
    }));
  });
  return new Table({ width: { size: total, type: WidthType.DXA }, columnWidths: widths, rows: trs });
}

// Encadré : filet vertical à gauche, fond teinté
function BOX(children, { width = 9070, title } = {}) {
  const kids = [];
  if (title) kids.push(new Paragraph({ spacing: { after: 80 }, children: [new TextRun({ text: fr(title), font: FONT, size: 22, bold: true, color: C })] }));
  children.forEach((c) => kids.push(typeof c === 'string' ? P(c, { size: 22, after: 80 }) : c));
  return new Table({
    width: { size: width, type: WidthType.DXA }, columnWidths: [width],
    rows: [new TableRow({ cantSplit: true, children: [new TableCell({
      width: { size: width, type: WidthType.DXA },
      shading: { type: ShadingType.CLEAR, color: 'auto', fill: TINT },
      margins: { top: 140, bottom: 100, left: 220, right: 220 },
      borders: { top: none, bottom: none, right: none, left: { style: BorderStyle.SINGLE, size: 24, color: C } },
      children: kids,
    })] })],
  });
}

// Citation de définition retenue
function DEF(text) {
  return BOX([new Paragraph({
    alignment: AlignmentType.JUSTIFIED, spacing: { after: 40, line: 276 , lineRule: 'auto'},
    children: [new TextRun({ text: fr('« ' + text + ' »'), font: FONT, size: SIZE, italics: true })],
  })]);
}

const SP = (after = 120) => new Paragraph({ spacing: { after }, children: [] });

module.exports = { FONT, C, TINT, RULE, GREY, SIZE, fr, rt, P, PL, B, N, H1, H2, H3, LOGIC, EQ, eqNum, CAPTION, SOURCE, CELL, TABLE, BOX, DEF, SP, thin, none };
