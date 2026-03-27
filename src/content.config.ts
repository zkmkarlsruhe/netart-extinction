import { defineCollection, reference } from 'astro:content';
import { z } from 'astro/zod';
import { glob } from 'astro/loaders';
import { isFlexibleDate } from '@lib/dates';

const flexDate = z.string().refine(isFlexibleDate, {
  message: 'Date must be YYYY, YYYY-MM, or YYYY-MM-DD',
});

const artworks = defineCollection({
  loader: glob({ pattern: '**/*.md', base: 'src/content/artworks' }),
  schema: z.object({
    title: z.string(),
    artist: z.string(),
    year: z.number().optional(),
    url: z.string().url().optional(),
    medium: z.string().optional(),
    description: z.string().optional(),
    ai_generated: z.boolean().optional(),
  }),
});

const eventType = z.enum([
  'api-shutdown',
  'plugin-eol',
  'browser-change',
  'platform-shutdown',
  'protocol-change',
  'corporate-acquisition',
  'terms-of-service',
  'hardware-obsolescence',
  'sdk-deprecation',
  'os-deprecation',
  'certificate-expiry',
  'data-loss',
  'format-obsolescence',
  'network-shutdown',
  'other',
]);

const severity = z.enum(['total', 'major', 'minor']);

const status = z.enum(['dead', 'degraded', 'restored', 'unknown']);

const fixType = z.enum(['migration', 'emulation', 'archive', 'workaround', 'rebuild', 'none']);

const events = defineCollection({
  loader: glob({ pattern: '**/*.md', base: 'src/content/events' }),
  schema: z.object({
    title: z.string(),
    date: flexDate,
    end_date: flexDate.optional(),
    dependency: z.string(),
    event_type: eventType,
    severity: severity.optional(),
    summary: z.string(),
    ai_generated: z.boolean().optional(),
    links: z.array(z.object({
      url: z.string().url(),
      label: z.string(),
    })).optional(),
    affected_artworks: z.array(z.object({
      artwork: reference('artworks'),
      severity: severity,
      status: status,
      note: z.string().optional(),
    })).optional(),
    fixes: z.array(z.object({
      type: fixType,
      description: z.string(),
      url: z.string().url().optional(),
    })).optional(),
  }),
});

export const collections = { artworks, events };
