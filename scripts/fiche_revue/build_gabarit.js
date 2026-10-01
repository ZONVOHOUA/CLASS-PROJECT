// Gabarit d'une page de la fiche de revue, réutilisable pour chaque CCM.
// Reprend les éléments retenus par le Cabinet : en-tête, titre, identification,
// « Coup d'œil Cabinet » et tableau des observations, à remplir.
// Usage : node build_gabarit.js [dossier de sortie]
const path = require('path');
const { TextRun, VerticalAlign, AlignmentType } = require('docx');
const L = require('./lib');
const { ecrire } = require('./build');

const ICI = __dirname;
const ARMOIRIES = path.join(ICI, 'assets', 'armoiries_fond_transparent.png');
const LIGNES = 9; // lignes d'observations vides tenant sur la page
const W = L.TEXT_W;
const OBS_W = [L.cm(1.35), L.cm(2.4), L.cm(2.0), 0, L.cm(3.9), L.cm(1.85)];
OBS_W[3] = W - OBS_W.reduce((a, b) => a + b, 0);

function identification() {
  const half = Math.floor(W / 2);
  const champ = (lab, val, k) => L.Cell([L.P(L.label(lab), { after: 30 }), L.P(L.R(val, { size: 21 }))],
    { w: k ? W - half : half, ml: k ? 150 : 0, mr: 90, mt: 80, mb: 80, borders: { bottom: L.line(4, L.C.GRAY_XL), ...(k ? { left: L.line(4, L.C.GRAY_XL) } : {}) } });
  return L.Tbl([
    L.Row([L.Cell([L.P(L.label('Document examiné'), { after: 40 }), L.P(L.R('Communication en Conseil des Ministres – [[intitulé exact de la CCM]]', { size: 24, bold: true }), { line: 260 })],
      { w: W, span: 2, ml: 0, mt: 90, mb: 90, borders: { top: L.line(8, L.C.GREEN), bottom: L.line(4, L.C.GRAY_XL) } })]),
    L.Row([champ('Structure émettrice', '[[Direction, service ou organisme]]', 0), champ('Destinataire final', 'Conseil des Ministres', 1)]),
    L.Row([L.Cell([L.P([...L.label('Objet' + L.NB.repeat(6)), ...L.R('Contrôle de la fiabilité des données et de la cohérence du texte avant transmission', { size: 21 })])],
      { w: W, span: 2, ml: 0, mt: 90, mb: 90, borders: { bottom: L.line(4, L.C.GRAY_L) } })]),
  ], [half, W - half]);
}

function tableauVide() {
  const tete = ['Réf.', 'Localisation', 'Catégorie', 'Constat', 'Correction / action attendue', 'Priorité'];
  const rows = [L.Row(tete.map((t, k) => L.Cell([L.P(L.label(t, { size: 14, color: L.C.GRAY_D }), { align: k === 5 ? AlignmentType.CENTER : undefined })],
    { w: OBS_W[k], ml: k === 0 ? 30 : 80, mr: 60, mt: 40, mb: 60, valign: VerticalAlign.BOTTOM, borders: { bottom: L.line(8, L.C.GREEN) } })), { header: true })];
  for (let i = 1; i <= LIGNES; i += 1) {
    const b = { bottom: L.line(4, L.C.GRAY_XL) };
    rows.push(L.Row(OBS_W.map((w, k) => L.Cell([k === 0 ? L.P(L.R(`OBS-${String(i).padStart(2, '0')}`, { font: L.F.SANS, size: 18, bold: true })) : L.P([])],
      { w, ml: k === 0 ? 30 : 80, mr: 60, mt: 45, mb: 45, borders: b })), { height: L.cm(1.15) }));
  }
  return L.Tbl(rows, OBS_W);
}

function gabarit() {
  const vide = (prio, lab) => ({ valeur: L.NB, label: lab, prio });
  const enfants = [
    L.enTeteInstitutionnel(ARMOIRIES),
    ...L.blocTitre('FICHE DE REVUE ET DE SÉCURISATION DOCUMENTAIRE', 'Points relevés lors de l’examen du document transmis'),
    identification(),
    L.titreSection('Coup d’œil Cabinet', { before: 240 }),
    L.tuiles([vide(undefined, 'Observations'), vide('C', 'Critique'), vide('M', 'Majeures'), vide('A', 'À corriger'), vide('F', 'De forme')]),
    L.titreSection('Observations détaillées', { before: 240 }),
    L.legendePriorites(),
    L.P(L.R('Localisation : partie ou section, paragraphe (§) et tableau du document examiné. Les observations sont classées par priorité, puis dans l’ordre du document.',
      { font: L.F.SANS, size: 15, italics: true, color: L.C.GRAY_M }), { before: 70, after: 90 }),
    tableauVide(),
  ];
  const meta = { titre: 'Gabarit – Fiche de revue documentaire CCM', sujet: 'Gabarit de fiche de revue et de sécurisation documentaire pour les Communications en Conseil des Ministres', motsCles: 'gabarit, revue documentaire, Cabinet, MINADER, CCM' };
  return L.document(meta, enfants, L.piedDePage('Cabinet du Ministre  ·  Fiche de revue documentaire  ·  CCM', '[[Date]]'));
}

if (require.main === module) {
  const dossier = process.argv[2] || path.join(ICI, '..', '..', 'fiche-revue-documentaire');
  ecrire(gabarit(), path.join(dossier, 'Gabarit_Fiche_Revue_CCM.docx')).catch((e) => { console.error(e); process.exit(1); });
}
module.exports = { gabarit };
