#!/usr/bin/env node
import { Command } from "commander";
import { createClient } from "./client";
import { run as importTrello } from "./trello";
import { run as importJira } from "./jira";
import { run as importAsana } from "./asana";
import { run as importTodoist } from "./todoist";
import { run as importNotion } from "./notion";
import { run as importDeck } from "./nextcloud-deck";

const program = new Command();

program
  .name("nexo-import")
  .description("Import data from external services into nexo")
  .version("1.0.0");

function addCommonOptions(cmd: Command): Command {
  return cmd
    .requiredOption("--board <id>", "Target nexo board ID")
    .option("--api <url>", "Nexo API base URL", "http://localhost:8000")
    .requiredOption("--token <jwt>", "Nexo JWT auth token");
}

addCommonOptions(
  program
    .command("trello")
    .description("Import from a Trello JSON export file")
    .requiredOption("--file <path>", "Path to Trello JSON export file")
).action(async (opts) => {
  const client = createClient(opts.api, opts.token);
  await importTrello(opts.file, opts.board, client);
});

addCommonOptions(
  program
    .command("jira")
    .description("Import from a Jira XML export file")
    .requiredOption("--file <path>", "Path to Jira XML export file")
).action(async (opts) => {
  const client = createClient(opts.api, opts.token);
  await importJira(opts.file, opts.board, client);
});

addCommonOptions(
  program
    .command("asana")
    .description("Import from an Asana JSON export file")
    .requiredOption("--file <path>", "Path to Asana JSON export file")
).action(async (opts) => {
  const client = createClient(opts.api, opts.token);
  await importAsana(opts.file, opts.board, client);
});

addCommonOptions(
  program
    .command("todoist")
    .description("Import from a Todoist JSON export file")
    .requiredOption("--file <path>", "Path to Todoist JSON export file")
).action(async (opts) => {
  const client = createClient(opts.api, opts.token);
  await importTodoist(opts.file, opts.board, client);
});

addCommonOptions(
  program
    .command("notion")
    .description("Import from a Notion CSV export (file or folder)")
    .requiredOption("--file <path>", "Path to Notion CSV file or export folder")
).action(async (opts) => {
  const client = createClient(opts.api, opts.token);
  await importNotion(opts.file, opts.board, client);
});

addCommonOptions(
  program
    .command("nextcloud-deck")
    .description("Import from a Nextcloud Deck instance via API")
    .requiredOption("--url <url>", "Nextcloud server base URL")
    .requiredOption("--user <username>", "Nextcloud username")
    .requiredOption("--pass <password>", "Nextcloud password")
    .requiredOption("--deck-board <id>", "Source board ID in Nextcloud Deck", parseInt)
).action(async (opts) => {
  const client = createClient(opts.api, opts.token);
  await importDeck(
    { url: opts.url, user: opts.user, pass: opts.pass, deckBoard: opts.deckBoard },
    opts.board,
    client
  );
});

program.parseAsync(process.argv).catch((err: Error) => {
  console.error("Error:", err.message);
  process.exit(1);
});
