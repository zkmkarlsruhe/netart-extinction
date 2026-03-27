/**
 * Flexible date parsing for YYYY, YYYY-MM, and YYYY-MM-DD formats.
 */

export type DatePrecision = 'year' | 'month' | 'day';

export interface ParsedDate {
  date: Date;
  precision: DatePrecision;
  raw: string;
}

const YEAR_RE = /^\d{4}$/;
const MONTH_RE = /^\d{4}-\d{2}$/;
const DAY_RE = /^\d{4}-\d{2}-\d{2}$/;

export function isFlexibleDate(value: string): boolean {
  return YEAR_RE.test(value) || MONTH_RE.test(value) || DAY_RE.test(value);
}

export function parseFlexibleDate(value: string): ParsedDate {
  if (DAY_RE.test(value)) {
    return { date: new Date(value + 'T00:00:00Z'), precision: 'day', raw: value };
  }
  if (MONTH_RE.test(value)) {
    return { date: new Date(value + '-01T00:00:00Z'), precision: 'month', raw: value };
  }
  if (YEAR_RE.test(value)) {
    return { date: new Date(value + '-01-01T00:00:00Z'), precision: 'year', raw: value };
  }
  throw new Error(`Invalid date format: "${value}". Expected YYYY, YYYY-MM, or YYYY-MM-DD.`);
}

export function endOfPeriod(parsed: ParsedDate): Date {
  const d = new Date(parsed.date);
  switch (parsed.precision) {
    case 'year':
      d.setUTCFullYear(d.getUTCFullYear() + 1);
      d.setUTCMilliseconds(d.getUTCMilliseconds() - 1);
      return d;
    case 'month':
      d.setUTCMonth(d.getUTCMonth() + 1);
      d.setUTCMilliseconds(d.getUTCMilliseconds() - 1);
      return d;
    case 'day':
      d.setUTCHours(23, 59, 59, 999);
      return d;
  }
}

export function formatDate(parsed: ParsedDate): string {
  switch (parsed.precision) {
    case 'year':
      return parsed.date.getUTCFullYear().toString();
    case 'month': {
      const m = parsed.date.toLocaleString('en-US', { month: 'long', timeZone: 'UTC' });
      return `${m} ${parsed.date.getUTCFullYear()}`;
    }
    case 'day': {
      const m = parsed.date.toLocaleString('en-US', { month: 'long', timeZone: 'UTC' });
      return `${parsed.date.getUTCDate()} ${m} ${parsed.date.getUTCFullYear()}`;
    }
  }
}
