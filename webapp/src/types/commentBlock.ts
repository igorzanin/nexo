import { Block, createBlock } from "./block";

export type CommentBlock = Block;

export function createCommentBlock(partial?: Partial<Block>): Block {
  return createBlock({ type: "comment", ...partial });
}
