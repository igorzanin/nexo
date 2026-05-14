import { Block, createBlock } from "./block";

export type ContentBlockType =
  | "text"
  | "image"
  | "divider"
  | "checkbox"
  | "h1"
  | "h2"
  | "h3"
  | "list-item"
  | "attachment"
  | "quote"
  | "video";

export const CONTENT_BLOCK_TYPES: ContentBlockType[] = [
  "text",
  "image",
  "divider",
  "checkbox",
  "h1",
  "h2",
  "h3",
  "list-item",
  "attachment",
  "quote",
  "video",
];

export type ContentBlock = Block;

export function createContentBlock(type: ContentBlockType, partial?: Partial<Block>): Block {
  return createBlock({ type, ...partial });
}

export function createTextBlock(partial?: Partial<Block>): Block {
  return createContentBlock("text", partial);
}

export function createImageBlock(partial?: Partial<Block>): Block {
  return createContentBlock("image", partial);
}

export function createCheckboxBlock(partial?: Partial<Block>): Block {
  return createContentBlock("checkbox", partial);
}

export function createDividerBlock(partial?: Partial<Block>): Block {
  return createContentBlock("divider", partial);
}

export function createH1Block(partial?: Partial<Block>): Block {
  return createContentBlock("h1", partial);
}

export function createH2Block(partial?: Partial<Block>): Block {
  return createContentBlock("h2", partial);
}

export function createH3Block(partial?: Partial<Block>): Block {
  return createContentBlock("h3", partial);
}
