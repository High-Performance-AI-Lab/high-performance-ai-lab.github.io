import { defineCollection } from "astro:content";
import { glob } from "astro/loaders";
import { z } from "astro/zod";

const projects = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/projects" }),
  schema: z.object({
    title: z.string(),
    tagline: z.string(),
    eyebrow: z.string(),
    description: z.string(),
    url: z.url().optional(),
    category: z.enum(["systems", "tools", "education", "proofs"]),
    tags: z.array(z.string()),
    order: z.number(),
    stackOrder: z.number(),
    stackAction: z.string(),
    stackRole: z.string(),
    accent: z.enum(["oxide", "cobalt", "citron", "violet", "moss", "amber", "teal", "cyan", "rose"]),
    icon: z.enum(["lattice", "checkpoint", "proof", "curriculum", "neural-die", "trace"]),
    status: z.string(),
    metric: z.string().optional(),
    metricLabel: z.string().optional(),
    command: z.string().optional(),
    featured: z.boolean().default(false),
  }),
});

const products = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/products" }),
  schema: z.object({
    name: z.string(),
    tagline: z.string(),
    description: z.string(),
    eyebrow: z.string(),
    category: z.string().default("Product"),
    url: z.url().optional(),
    command: z.string().optional(),
    features: z.array(
      z.object({
        code: z.string(),
        label: z.string(),
        detail: z.string(),
      }),
    ).default([]),
    metrics: z.array(
      z.object({
        value: z.string(),
        label: z.string(),
      }),
    ).default([]),
    accent: z.enum(["teal", "cyan", "violet", "amber", "rose"]).default("teal"),
    order: z.number().default(0),
    featured: z.boolean().default(false),
  }),
});

const articles = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/articles" }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    publishedAt: z.coerce.date(),
    kind: z.enum(["article", "news", "field-note"]),
    author: z.string(),
    tags: z.array(z.string()),
    readingTime: z.string(),
    featured: z.boolean().default(false),
    homepageExcerpt: z.array(z.string()).min(2).max(3),
    socialImage: z.object({
      src: z.string(),
      alt: z.string(),
      width: z.number().int().positive(),
      height: z.number().int().positive(),
      type: z.enum(["image/jpeg", "image/png", "image/webp"]),
    }).optional(),
    url: z.url().optional(),
  }),
});

const team = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/team" }),
  schema: z.object({
    name: z.string(),
    role: z.string(),
    bio: z.string(),
    initials: z.string().min(2).max(3),
    portrait: z.string(),
    location: z.string().optional(),
    order: z.number(),
    accent: z.enum(["oxide", "cobalt", "citron", "violet", "moss", "amber"]),
    github: z.url().optional(),
    website: z.url().optional(),
  }),
});

export const collections = { projects, products, articles, team };
