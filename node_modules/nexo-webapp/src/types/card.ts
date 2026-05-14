import { Block, createBlock } from "./block";

export interface CardFields {
  icon: string;
  isTemplate: boolean;
  properties: Record<string, string | string[]>;
  contentOrder: Array<string | string[]>;
}

export type Card = Block & { fields: CardFields };

export function createCard(partial?: Partial<Card>): Card {
  return {
    ...createBlock({ type: "card", ...partial }),
    fields: {
      icon: partial?.fields?.icon ?? "",
      isTemplate: partial?.fields?.isTemplate ?? false,
      properties: partial?.fields?.properties ?? {},
      contentOrder: partial?.fields?.contentOrder ?? [],
    },
  };
}
