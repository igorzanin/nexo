import { Block, createBlock } from "./block";

export type AttachmentBlock = Block;

export function createAttachmentBlock(partial?: Partial<Block>): Block {
  return createBlock({ type: "attachment", ...partial });
}
