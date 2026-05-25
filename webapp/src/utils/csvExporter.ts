interface ExportCard {
  id: string;
  title: string;
  icon?: string;
  properties?: Record<string, string>;
  createAt: number;
  updateAt: number;
}

export function exportCardsToCSV(cards: ExportCard[], propertyNames: Record<string, string>): string {
  const headers = ["ID", "Title", "Icon", "Created At", "Updated At"];
  const propIds = Object.keys(propertyNames);
  headers.push(...propIds.map((id) => propertyNames[id]));

  const rows = cards.map((card) => {
    const row = [
      card.id,
      `"${(card.title || "").replace(/"/g, '""')}"`,
      card.icon || "",
      new Date(card.createAt).toISOString(),
      new Date(card.updateAt).toISOString(),
    ];
    for (const propId of propIds) {
      row.push(`"${(card.properties?.[propId] || "").replace(/"/g, '""')}"`);
    }
    return row.join(",");
  });

  return [headers.join(","), ...rows].join("\n");
}

export function downloadCSV(csv: string, filename: string) {
  const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.download = filename;
  link.click();
  URL.revokeObjectURL(link.href);
}
