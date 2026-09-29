// Helpers for OMML equations with docx-js
const { Math: OMath, MathRun, MathFraction, MathSubScript, MathSuperScript,
  MathSubSuperScript, MathSum, MathRoundBrackets } = require('docx');

const arr = (x) => {
  if (x === undefined || x === null) return [];
  if (Array.isArray(x)) return x.flatMap(arr);
  if (typeof x === 'string') return [new MathRun(x)];
  return [x];
};
const r = (t) => new MathRun(t);
const sb = (b, s) => new MathSubScript({ children: arr(b), subScript: arr(s) });
const sp = (b, s) => new MathSuperScript({ children: arr(b), superScript: arr(s) });
const ss = (b, s, p) => new MathSubSuperScript({ children: arr(b), subScript: arr(s), superScript: arr(p) });
const fr = (n, d) => new MathFraction({ numerator: arr(n), denominator: arr(d) });
const sum = (idx, body) => new MathSum({ children: arr(body), subScript: arr(idx) });
const br = (x) => new MathRoundBrackets({ children: arr(x) });
const M = (...parts) => new OMath({ children: arr(parts) });

// frequently used
const w0 = () => ss('w', 'i', '0');
module.exports = { arr, r, sb, sp, ss, fr, sum, br, M, w0 };
