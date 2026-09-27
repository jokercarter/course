export const tex = String.raw;
export const ref = (file, from, to = from) => ({file, from, to});
export const concept = (title, body) => ({title, body});
export const formula = (label, tex, note) => ({label, tex, note});
export const example = (q, ...steps) => ({q, steps});
export const quiz = (q, hint, a) => ({q, hint, a});
export function lesson(value) {
  return {status: 'ready', ...value};
}
