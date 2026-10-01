// Version Word modifiable de la note de benchmark (même contenu que le PDF : scripts/note_content.json)
const fs = require("fs");
const path = require("path");
const {
  Document, Packer, Paragraph, TextRun, ImageRun, Table, TableRow, TableCell, WidthType, ShadingType,
  AlignmentType, BorderStyle, LevelFormat, Footer, Header, PageNumber, VerticalAlign, TableLayoutType, LineRuleType,
} = require("docx");
const AUTO = LineRuleType.AUTO; // interligne proportionnel explicite (sinon LibreOffice l'interprète comme exact)

const ROOT = path.resolve(__dirname, "..");
const C = JSON.parse(fs.readFileSync(path.join(__dirname, "note_content.json"), "utf8"));
const NAVY = "14325C", BLUE = "2A78D6", ORANGE = "EB6834", GREY = "52514E", LIGHT = "F6F6F3", RULE = "E1E0D9";
const FONT = "Arial";
const PAGE_W = 11906, PAGE_H = 16838, MARGIN = 794; // A4, marges 1,4 cm
const CONTENT_W = PAGE_W - 2 * MARGIN;             // 10 318 DXA
const PX_W = Math.round(CONTENT_W / 15);           // largeur utile en pixels (96 dpi)

// --- texte enrichi : **gras**, *italique*
function runs(text, opts = {}) {
  const out = [];
  const re = /(\*\*[^*]+\*\*|\*[^*]+\*)/g;
  let last = 0, m;
  while ((m = re.exec(text)) !== null) {
    if (m.index > last) out.push(new TextRun({ text: text.slice(last, m.index), font: FONT, ...opts }));
    const tok = m[0];
    if (tok.startsWith("**")) out.push(new TextRun({ text: tok.slice(2, -2), bold: true, font: FONT, ...opts, color: opts.boldColor || opts.color }));
    else out.push(new TextRun({ text: tok.slice(1, -1), italics: true, font: FONT, ...opts }));
    last = m.index + tok.length;
  }
  if (last < text.length) out.push(new TextRun({ text: text.slice(last), font: FONT, ...opts }));
  return out;
}
const P = (text, o = {}) => new Paragraph({ children: runs(text, o.run || {}), spacing: { after: o.after ?? 60, before: o.before ?? 0, line: o.line ?? 252, lineRule: AUTO },
  alignment: o.align, ...(o.border ? { border: o.border } : {}), ...(o.shading ? { shading: o.shading } : {}), keepNext: o.keepNext, indent: o.indent });

function pngSize(file) {
  const b = fs.readFileSync(file);
  return { w: b.readUInt32BE(16), h: b.readUInt32BE(20), data: b };
}
function image(src, widthPct, maxPx) {
  const f = path.join(ROOT, "figures", `${src}.png`);
  const { w, h, data } = pngSize(f);
  const width = Math.min(Math.round(PX_W * widthPct / 100), maxPx || 10000);
  const height = Math.round(width * h / w);
  return new Paragraph({ children: [new ImageRun({ type: "png", data, transformation: { width, height },
    altText: { title: src, description: src, name: src } })], spacing: { after: 40 } });
}
const cap = (t) => P(t, { run: { bold: true, size: 16, color: NAVY }, after: 40, keepNext: true });
const src = (t) => P(t, { run: { size: 12, color: "6E6D68" }, after: 100, line: 230 });

const border = { style: BorderStyle.SINGLE, size: 4, color: RULE };
const borders = { top: border, bottom: border, left: border, right: border };
const noBorders = { top: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" }, bottom: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
  left: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" }, right: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" } };

function cell(children, width, o = {}) {
  return new TableCell({ children, width: { size: width, type: WidthType.DXA }, borders: o.borders || borders,
    shading: o.fill ? { fill: o.fill, type: ShadingType.CLEAR, color: "auto" } : undefined,
    margins: { top: o.pad ?? 50, bottom: o.pad ?? 50, left: o.side ?? 80, right: o.side ?? 80 }, verticalAlign: o.valign || VerticalAlign.TOP });
}
function widths(pcts, total = CONTENT_W) {
  const s = pcts.reduce((a, b) => a + b, 0);
  const w = pcts.map((p) => Math.floor(total * p / s));
  w[w.length - 1] += total - w.reduce((a, b) => a + b, 0);
  return w;
}

function table(b, totalW = CONTENT_W) {
  const w = widths(b.widths, totalW);
  const small = 13;
  const head = new TableRow({ tableHeader: true, children: b.headers.map((h, i) => cell([P(h, { run: { bold: true, color: "FFFFFF", size: small - 1 }, after: 0, line: 220 })], w[i], { fill: NAVY, side: 55 })) });
  const rows = b.rows.map((r, ri) => new TableRow({ children: r.map((c, i) => cell([P(String(c), { run: { size: small, bold: i === 0, color: i === 0 ? NAVY : "1B1B1A" }, after: 0, line: 220,
    align: (b.style.includes("compact") && i > 0) ? AlignmentType.RIGHT : undefined })], w[i], { fill: ri % 2 ? LIGHT : undefined, pad: 35, side: 55 })) }));
  const out = [new Table({ width: { size: totalW, type: WidthType.DXA }, columnWidths: w, rows: [head, ...rows], layout: TableLayoutType.FIXED })];
  if (b.notes) out.push(src(b.notes));
  else out.push(new Paragraph({ spacing: { after: 60 }, children: [] }));
  return out;
}

function cardParas(c) {
  const tagRun = (t, fill) => new TextRun({ text: ` ${t} `, bold: true, size: 11, font: FONT, color: fill === "DBE8FA" ? NAVY : GREY, shading: { type: ShadingType.CLEAR, fill, color: "auto" } });
  const para = (tag, fill, text) => new Paragraph({ spacing: { after: 50, line: 228, lineRule: AUTO }, children: [tagRun(tag, fill), new TextRun({ text: "  ", font: FONT, size: 14 }), ...runs(text, { size: 14 })] });
  return [
    new Paragraph({ spacing: { after: 50 }, children: [new TextRun({ text: `${c.icon}  `, color: BLUE, size: 16, font: FONT }), new TextRun({ text: c.title, bold: true, color: NAVY, size: 18, font: FONT })] }),
    para("CONSTAT", "ECEBE6", c.constat), para("EXPLICATION", "ECEBE6", c.explication), para("IMPLICATION", "DBE8FA", c.implication),
  ];
}
function cards(b, total = CONTENT_W) {
  const n = b.cols || b.items.length;
  const w = widths(Array(n).fill(1), total);
  const rows = [];
  for (let i = 0; i < b.items.length; i += n) {
    const chunk = b.items.slice(i, i + n);
    while (chunk.length < n) chunk.push(null);
    rows.push(new TableRow({ cantSplit: true, children: chunk.map((c, j) => cell(c ? cardParas(c) : [new Paragraph({ children: [] })], w[j], { fill: c ? "FCFCFB" : undefined, pad: 70 })) }));
  }
  return [new Table({ width: { size: total, type: WidthType.DXA }, columnWidths: w, rows, layout: TableLayoutType.FIXED }), new Paragraph({ spacing: { after: 60 }, children: [] })];
}

function blocks(list, totalW = CONTENT_W) {
  const out = [];
  for (const b of list) {
    switch (b.t) {
      case "title": out.push(P(b.text, { run: { bold: true, size: 40, color: NAVY }, after: 40, line: 240 })); break;
      case "subtitle": out.push(P(b.text, { run: { size: 19, color: GREY }, after: 120 })); break;
      case "answer":
        out.push(new Table({ width: { size: totalW, type: WidthType.DXA }, columnWidths: [totalW], rows: [new TableRow({ children: [cell([
          P(b.label.toUpperCase(), { run: { bold: true, size: 13, color: "9EC5F4" }, after: 30 }),
          P(b.text, { run: { size: 18, color: "FFFFFF", boldColor: "FFFFFF" }, after: 0 })], totalW, { fill: NAVY, borders: noBorders, pad: 100 })] })] }));
        out.push(new Paragraph({ spacing: { after: 80 }, children: [] })); break;
      case "twocol": {
        const w = widths([1, 1.55], totalW);
        const colc = (x) => [P(x.label.toUpperCase(), { run: { bold: true, size: 12, color: BLUE }, after: 20 }), P(x.text, { run: { size: 15 }, after: 0 })];
        out.push(new Table({ width: { size: totalW, type: WidthType.DXA }, columnWidths: w, rows: [new TableRow({ children: [cell(colc(b.left), w[0], { borders: noBorders }), cell(colc(b.right), w[1], { borders: noBorders })] })] }));
        out.push(new Paragraph({ spacing: { after: 60 }, children: [] })); break;
      }
      case "kpis": {
        const w = widths(Array(b.items.length).fill(1), totalW);
        out.push(new Table({ width: { size: totalW, type: WidthType.DXA }, columnWidths: w, rows: [new TableRow({ children: b.items.map((k, i) => cell([
          new Paragraph({ spacing: { after: 30 }, children: [new TextRun({ text: k.value, bold: true, size: 32, color: NAVY, font: FONT }), new TextRun({ text: k.unit ? ` ${k.unit}` : "", bold: true, size: 15, color: GREY, font: FONT })] }),
          P(k.label, { run: { size: 13 }, after: 0, line: 220 })], w[i], { fill: "FBFBFA", pad: 80,
          borders: { ...borders, top: { style: BorderStyle.SINGLE, size: 18, color: BLUE } } })) })] }));
        out.push(new Paragraph({ spacing: { after: 60 }, children: [] })); break;
      }
      case "h1": out.push(P(b.text, { run: { bold: true, size: 24, color: NAVY }, after: 80, line: 240 })); break;
      case "h2": out.push(P(b.text, { run: { bold: true, size: 19, color: NAVY }, before: 80, after: 60, keepNext: true,
        border: { left: { style: BorderStyle.SINGLE, size: 18, color: BLUE, space: 6 } } })); break;
      case "minititle": out.push(cap(b.text)); break;
      case "lead": out.push(P(b.text, { run: { size: 16, color: "3A3A38" }, after: 80 })); break;
      case "numbered": b.items.forEach((t) => out.push(new Paragraph({ numbering: { reference: "constats", level: 0 }, spacing: { after: 40, line: 240, lineRule: AUTO }, children: runs(t, { size: 16 }) }))); break;
      case "figure": out.push(cap(b.caption)); out.push(image(b.src, b.width * totalW / CONTENT_W)); out.push(src(b.source)); break;
      case "figrow": {
        const w = widths(b.items.map((i) => i.width), totalW);
        out.push(new Table({ width: { size: totalW, type: WidthType.DXA }, columnWidths: w, rows: [new TableRow({ children: b.items.map((it, i) => cell(
          [cap(it.caption), image(it.src, 100 * (w[i] - 160) / CONTENT_W), src(it.source)], w[i], { borders: noBorders })) })] }));
        break;
      }
      case "table": out.push(...table(b, totalW)); break;
      case "cards": out.push(...cards(b, totalW)); break;
      case "split": {
        const ratio = (b.ratio || "1.05fr 1fr").split(" ").map((x) => parseFloat(x));
        const w = widths(ratio, totalW);
        const inner = (lst, ww) => blocks(lst, ww - 160);
        out.push(new Table({ width: { size: totalW, type: WidthType.DXA }, columnWidths: w, rows: [new TableRow({ children: [
          cell(inner(b.left, w[0]), w[0], { borders: noBorders }), cell(inner(b.right, w[1]), w[1], { borders: noBorders })] })] }));
        out.push(new Paragraph({ spacing: { after: 40 }, children: [] })); break;
      }
      case "callout": out.push(P(b.text, { run: { size: 15 }, after: 100, before: 40, shading: { type: ShadingType.CLEAR, fill: "FDF3EE", color: "auto" },
        border: { left: { style: BorderStyle.SINGLE, size: 24, color: ORANGE, space: 8 } } })); break;
      case "recos": {
        const w = widths([1, 1], totalW);
        const rc = (r) => [new Paragraph({ spacing: { after: 30 }, children: [new TextRun({ text: ` ${r.n} `, bold: true, color: "FFFFFF", size: 18, font: FONT, shading: { type: ShadingType.CLEAR, fill: BLUE, color: "auto" } }),
          new TextRun({ text: `  ${r.title}`, bold: true, color: NAVY, size: 17, font: FONT })] }), P(r.text, { run: { size: 14 }, after: 0, line: 228 })];
        const rows = [];
        for (let i = 0; i < b.items.length; i += 2) rows.push(new TableRow({ cantSplit: true, children: [cell(rc(b.items[i]), w[0], { fill: "FCFCFB", pad: 70 }), cell(rc(b.items[i + 1]), w[1], { fill: "FCFCFB", pad: 70 })] }));
        out.push(new Table({ width: { size: totalW, type: WidthType.DXA }, columnWidths: w, rows }));
        out.push(new Paragraph({ spacing: { after: 60 }, children: [] })); break;
      }
      case "twobox": {
        const w = widths([1, 1], totalW);
        const bx = (x) => [P(x.label.toUpperCase(), { run: { bold: true, size: 12, color: BLUE }, after: 30 }),
          ...x.items.map((t) => new Paragraph({ numbering: { reference: "puces", level: 0 }, spacing: { after: 30, line: 228, lineRule: AUTO }, children: runs(t, { size: 14 }) }))];
        out.push(new Table({ width: { size: totalW, type: WidthType.DXA }, columnWidths: w, rows: [new TableRow({ children: [
          cell(bx(b.left), w[0], { fill: "FBFBFA", pad: 70, borders: { ...borders, top: { style: BorderStyle.SINGLE, size: 18, color: BLUE } } }),
          cell(bx(b.right), w[1], { fill: "FBFBFA", pad: 70, borders: { ...borders, top: { style: BorderStyle.SINGLE, size: 18, color: ORANGE } } })] })] }));
        out.push(new Paragraph({ spacing: { after: 40 }, children: [] })); break;
      }
      case "note": out.push(src(b.text)); break;
      default: throw new Error("bloc inconnu " + b.t);
    }
  }
  return out;
}

const children = [];
C.pages.forEach((pg, i) => {
  children.push(new Paragraph({ pageBreakBefore: i > 0, spacing: { after: 100 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 12, color: NAVY, space: 4 } },
    children: [new TextRun({ text: pg.header[0], bold: true, size: 14, color: NAVY, font: FONT }), new TextRun({ text: `    ·    ${pg.header[1]}`, size: 14, color: GREY, font: FONT })] }));
  children.push(...blocks(pg.blocks));
});

const doc = new Document({
  creator: "Chargé d'études – MINADERPV",
  title: "Les prix agricoles ivoiriens sont-ils compétitifs ? Benchmark international (octobre 2026)",
  description: "Note de benchmark – version Word modifiable",
  styles: { default: { document: { run: { font: FONT, size: 16 } } } },
  numbering: { config: [
    { reference: "constats", levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT, style: { run: { bold: true, color: BLUE }, paragraph: { indent: { left: 360, hanging: 300 } } } }] },
    { reference: "puces", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 300, hanging: 200 } } } }] },
  ] },
  sections: [{
    properties: { page: { size: { width: PAGE_W, height: PAGE_H }, margin: { top: 700, bottom: 700, left: MARGIN, right: MARGIN, footer: 300 } } },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [
      new TextRun({ text: "Les prix agricoles ivoiriens sont-ils compétitifs ? – Note de benchmark, octobre 2026 · page ", size: 12, color: "898781", font: FONT }),
      new TextRun({ children: [PageNumber.CURRENT], size: 12, color: "898781", font: FONT })] })] }) },
    children,
  }],
});
Packer.toBuffer(doc).then((buf) => {
  const out = path.join(ROOT, "Note_Benchmark_Prix_Agricoles_CI.docx");
  fs.writeFileSync(out, buf);
  console.log("DOCX écrit :", out);
});
