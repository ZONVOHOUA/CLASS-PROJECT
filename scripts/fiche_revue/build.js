// Génère les documents de revue du Cabinet (DOCX) à partir d'un fichier de données :
//   - la fiche de revue et de sécurisation documentaire ;
//   - la fiche de suivi des corrections (seconde version, avec colonne « Statut ») ;
//   - le modèle vierge réutilisable (données : data_modele.js).
// Usage : node build.js [données] [dossier de sortie]
const fs = require('fs');
const path = require('path');
const { Packer, TextRun, VerticalAlign, AlignmentType } = require('docx');
const L = require('./lib');

const ICI = __dirname;
const ARMOIRIES = path.join(ICI, 'assets', 'armoiries_fond_transparent.png');
const STATUTS = ['À CORRIGER', 'CORRIGÉ', 'À VÉRIFIER', 'À ARBITRER', 'MAINTENU'];

function compter(d) {
  if (d.compteurs) return d.compteurs;
  const obs = d.observations;
  const n = (p) => obs.filter((o) => o.prio === p).length;
  return [
    { valeur: obs.length, label: 'Observations' },
    { valeur: n('C'), label: L.PRIO.C.plural, prio: 'C' },
    { valeur: n('M'), label: L.PRIO.M.plural, prio: 'M' },
    { valeur: n('A'), label: L.PRIO.A.plural, prio: 'A' },
    { valeur: n('F'), label: L.PRIO.F.plural, prio: 'F' },
  ];
}

const introSection = (t) => L.P(L.R(t, { size: 21, italics: true, color: L.C.GRAY_D }), { after: 100, keepNext: true });

function largeurs(ws, total) {
  const k = ws.indexOf(0);
  ws[k] = total - ws.reduce((a, b) => a + b, 0);
  return ws;
}

// ------------------------------------------------------------------ fiche de revue
function ficheRevue(d) {
  const W = L.TEXT_W;
  const enfants = [
    L.enTeteInstitutionnel(ARMOIRIES),
    ...L.blocTitre(d.titre, d.sousTitre),
    L.blocIdentification(d.identification),

    // ---------------------------------------------- Niveau 1 : lecture Cabinet
    L.titreSection('Coup d’œil Cabinet', { before: 280 }),
    L.tuiles(compter(d)),
    L.P([], { after: 90 }),
    L.blocStatut(d.synthese),
    L.ligneEtiquetee('Suite proposée', d.synthese.suiteProposee),

    L.titreSection('Points critiques et corrections majeures'),
    L.listeEssentiel(d.essentiel),

    L.titreSection('Arbitrages attendus du Cabinet'),
    L.listeEssentiel(d.arbitragesCourts),

    // ---------------------------------------------- Niveau 2 : lecture technique
    L.titreSection('Observations détaillées', { pageBreakBefore: true, before: 0 }),
    L.legendePriorites(),
    L.P(L.R('Localisation : partie ou section, paragraphe (§) et tableau du document examiné. Les observations sont classées par priorité, puis dans l’ordre du document.',
      { font: L.F.SANS, size: 15, italics: true, color: L.C.GRAY_M }), { before: 90, after: 110 }),
    L.tableauObservations(d.observations),

    L.titreSection('Points nécessitant arbitrage', { before: 300 }),
    introSection('Ces points relèvent d’un choix à effectuer et non d’une erreur à corriger.'),
    L.tableauSimple(['Réf.', 'Sujet', 'Problème', 'Arbitrage attendu'], largeurs([L.cm(1.4), L.cm(3.6), 0, L.cm(5.6)], W),
      d.arbitrages.map((a) => [
        L.cellTexte(a.ref, { bold: true, color: L.C.GREEN }),
        [L.P(L.R(a.sujet, { font: L.F.SANS, size: 18, bold: true }), { line: 240 }), L.P(L.R('Lien : ' + a.lien, { font: L.F.SANS, size: 16, color: L.C.GRAY_M }), { before: 30 })],
        L.cellTexte(a.probleme),
        L.cellTexte(a.arbitrage),
      ])),

    L.titreSection('Vérifications à effectuer', { before: 300 }),
    introSection('Informations qui n’ont pas pu être confirmées avec les pièces disponibles ; elles ne sont pas réputées erronées.'),
    L.tableauSimple(['Réf.', 'Vérification', 'Lien'], largeurs([L.cm(1.4), 0, L.cm(2.2)], W),
      d.verifications.map((v) => [
        L.cellTexte(v.ref, { bold: true, color: L.C.GREEN }),
        L.cellTexte(v.texte),
        L.cellTexte(v.lien, { color: L.C.GRAY_D }),
      ])),

    L.titreSection('Suite à donner', { before: 300 }),
    L.encadre(d.suiteADonner),
    ...(d.guide ? guide(d.guide) : []),
  ];
  return L.document(d.fichier, enfants, L.piedDePage(d.piedDePage.gauche, d.piedDePage.date));
}

// Page de consignes (modèle vierge uniquement).
function guide(g) {
  const out = [L.titreSection(g.titre, { pageBreakBefore: true, before: 0 })];
  if (g.intro) out.push(introSection(g.intro));
  g.blocs.forEach((b) => {
    out.push(L.P(L.R(b.titre, { font: L.F.SANS, size: 16, bold: true, caps: true, spacing: 16, color: L.C.GRAY_D }), { before: 180, after: 60, keepNext: true }));
    out.push(L.tableauSimple(b.entetes, largeurs(b.largeurs.map((x) => (x ? L.cm(x) : 0)), L.TEXT_W),
      b.lignes.map((ligne) => ligne.map((t, k) => (typeof t === 'object'
        ? [L.P([L.sym(t.prio, 17), new TextRun({ text: L.NB + L.NB, size: 17 }), ...L.R(t.texte, { font: L.F.SANS, size: 18, bold: true })])]
        : L.cellTexte(t, k === 0 ? { bold: true } : {}))))));
  });
  if (g.regles) {
    out.push(L.P(L.R('Règles de rédaction', { font: L.F.SANS, size: 16, bold: true, caps: true, spacing: 16, color: L.C.GRAY_D }), { before: 200, after: 60, keepNext: true }));
    g.regles.forEach((r) => out.push(L.P([new TextRun({ text: '–' + L.NB + L.NB, font: L.F.SANS, size: 18, color: L.C.ORANGE }), ...L.R(r, { font: L.F.SANS, size: 18 })],
      { indent: { left: 240, hanging: 240 }, after: 40, line: 250 })));
  }
  return out;
}

// ------------------------------------------------------------------ fiche de suivi
function ficheSuivi(d) {
  const s = d.suivi;
  const W = L.TEXT_W;
  const ws = largeurs([L.cm(1.45), L.cm(5.0), L.cm(1.85), L.cm(2.45), 0], W);
  const tete = ['Réf.', 'Objet et localisation', 'Priorité', 'Statut', 'Suite donnée par la structure émettrice'];
  const rows = [L.Row(tete.map((t, k) => L.Cell([L.P(L.label(t, { size: 14, color: L.C.GRAY_D }), { align: k === 2 || k === 3 ? AlignmentType.CENTER : undefined })],
    { w: ws[k], ml: k === 0 ? 30 : 80, mr: 60, mt: 40, mb: 60, valign: VerticalAlign.BOTTOM, borders: { bottom: L.line(8, L.C.GREEN) } })), { header: true })];
  const b = { bottom: L.line(4, L.C.GRAY_XL) };
  const ligne = (ref, objet, loc, prio, statut) => L.Row([
    L.Cell([L.P(L.R(ref, { font: L.F.SANS, size: 18, bold: true, color: prio ? L.C.INK : L.C.GREEN }))], { w: ws[0], ml: 30, mr: 30, mt: 60, mb: 60, borders: b }),
    L.Cell([L.P(L.R(objet, { font: L.F.SANS, size: 18 }), { line: 240 }), ...(loc ? [L.P(L.R(loc, { font: L.F.SANS, size: 16, color: L.C.GRAY_M }), { before: 20, line: 240 })] : [])],
      { w: ws[1], ml: 80, mr: 60, mt: 60, mb: 60, borders: b }),
    L.Cell(prio
      ? [L.P([L.sym(prio, 16)], { align: AlignmentType.CENTER }), L.P(L.R(L.PRIO[prio].caps, { font: L.F.SANS, size: 16, bold: true }), { align: AlignmentType.CENTER })]
      : [L.P(L.R('Arbitrage', { font: L.F.SANS, size: 16, bold: true, color: L.C.GREEN }), { align: AlignmentType.CENTER })],
    { w: ws[2], ml: 30, mr: 30, mt: 60, mb: 60, borders: b }),
    // Statut : liste déroulante Word (contrôle de contenu inséré au post-traitement).
    L.Cell([L.P(L.R(`§§STATUT:${statut}§§`, { font: L.F.SANS, size: 18, bold: true }), { align: AlignmentType.CENTER })],
      { w: ws[3], ml: 40, mr: 40, mt: 60, mb: 60, valign: VerticalAlign.CENTER, fill: L.C.GRAY_BG, borders: b }),
    L.Cell([L.P([])], { w: ws[4], ml: 100, mr: 60, mt: 60, mb: 60, borders: b }),
  ], { height: L.cm(1.05) });
  d.observations.forEach((o) => rows.push(ligne(o.id, o.objet, o.loc.join(' ; '), o.prio, o.statut)));
  d.arbitrages.forEach((a) => rows.push(ligne(a.ref, a.sujet, 'Lien : ' + a.lien, null, 'À ARBITRER')));

  const wv = Math.floor(W / 2);
  const visa = (titre, w) => L.Cell([
    L.P(L.label(titre, { color: L.C.GRAY_D }), { after: 60 }),
    L.P(L.R('Nom, fonction et date', { font: L.F.SANS, size: 16, color: L.C.GRAY_M }), { after: 900 }),
    L.P(L.R('Visa', { font: L.F.SANS, size: 16, color: L.C.GRAY_M })),
  ], { w, ml: 160, mr: 120, mt: 120, mb: 120, borders: { top: L.line(8, L.C.GREEN), bottom: L.line(4, L.C.GRAY_L), left: L.line(4, L.C.GRAY_XL), right: L.line(4, L.C.GRAY_XL) } });

  const enfants = [
    L.enTeteInstitutionnel(ARMOIRIES),
    ...L.blocTitre(s.titre, s.sousTitre),
    L.blocIdentification(s.identification),
    L.titreSection('Consignes', { before: 260 }),
    L.P(L.R(s.consigne, { size: 21 }), { line: 264, after: 60 }),
    L.P([...L.label('Statuts' + L.NB + L.NB), ...L.R(STATUTS.join('  ·  '), { font: L.F.SANS, size: 16, bold: true, color: L.C.GRAY_D })], { after: 40 }),
    L.titreSection('Suivi des observations', { before: 260 }),
    L.Tbl(rows, ws),
    L.titreSection('Visas', { before: 320 }),
    L.Tbl([L.Row([visa('Pour la structure émettrice', wv), visa('Pour le Cabinet – contrôle des corrections', W - wv)])], [wv, W - wv]),
  ];
  return L.document({ ...d.fichier, titre: s.fichierTitre, sujet: s.fichierSujet }, enfants, L.piedDePage(s.piedDePage, d.piedDePage.date));
}

async function ecrire(doc, sortie) {
  fs.mkdirSync(path.dirname(sortie), { recursive: true });
  fs.writeFileSync(sortie, await Packer.toBuffer(doc));
  console.log('écrit :', sortie);
}

async function main() {
  const donnees = process.argv[2] || path.join(ICI, 'data_ccm_30juin2026.js');
  const dossier = process.argv[3] || path.join(ICI, '..', '..', 'fiche-revue-documentaire');
  const d = require(path.resolve(donnees));
  await ecrire(ficheRevue(d), path.join(dossier, 'Fiche_Revue_Documentaire_Cabinet.docx'));
  if (d.suivi) await ecrire(ficheSuivi(d), path.join(dossier, 'Fiche_Suivi_Corrections_Cabinet.docx'));
  const modele = require(path.join(ICI, 'data_modele.js'));
  await ecrire(ficheRevue(modele), path.join(dossier, 'Modele_Fiche_Revue_Documentaire_Cabinet.docx'));
}

if (require.main === module) main().catch((e) => { console.error(e); process.exit(1); });
module.exports = { ficheRevue, ficheSuivi, ecrire, compter, STATUTS };
