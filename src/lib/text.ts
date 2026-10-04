export function fill(text: string, values: Record<string, string | number>): string {
  return text.replace(/\{(\w+)\}/g, (match, key: string) => {
    if (!(key in values)) throw new Error(`Unknown token ${match} in "${text}"`);
    return String(values[key]);
  });
}

export const plural = (count: number, one: string, many: string) => (count === 1 ? one : many);
