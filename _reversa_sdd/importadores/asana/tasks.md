# Importador Asana, Tarefas de Implementação

## Pré-requisitos
- [ ] ArchiveUtils.buildBlockArchive implementado
- [ ] Modelos Block, Board, BoardView, Card, TextBlock disponíveis

## Tarefas

- [ ] T-01, Implementar parsing de argumentos CLI (minimist)
  - Origem no legado: `import/asana/importAsana.ts:34-41`
  - Critério de pronto: `-i` obrigatório; `-o` com default `archive.boardarchive`; exibe help se `-i` ausente
  - Confiança: 🟢

- [ ] T-02, Implementar leitura e parsing do JSON export
  - Origem no legado: `import/asana/importAsana.ts:43-50`
  - Critério de pronto: Valida existência do arquivo; faz parse do JSON; encerra com código 2 se arquivo inexistente
  - Confiança: 🟢

- [ ] T-03, Implementar extração de projetos e seções
  - Origem no legado: `import/asana/importAsana.ts:63-90`
  - Critério de pronto: `getProjects` retorna projetos únicos; `getSections` retorna seções por projectId
  - Confiança: 🟢

- [ ] T-04, Implementar criação do board com propriedade Select
  - Origem no legado: `import/asana/importAsana.ts:106-134`
  - Critério de pronto: Board criado com título do projeto; propriedade "Section" do tipo select com opções coloridas; cores alternam em ciclo
  - Confiança: 🟢

- [ ] T-05, Implementar conversão de tarefas em cards
  - Origem no legado: `import/asana/importAsana.ts:145-178`
  - Critério de pronto: Cada tarefa vira CardBlock com propriedade Section mapeada; notas viram TextBlock filho; contentOrder atualizado
  - Confiança: 🟢

- [ ] T-06, Implementar serialização e saída do archive
  - Origem no legado: `import/asana/importAsana.ts:55-60`
  - Critério de pronto: Chama ArchiveUtils.buildBlockArchive; escreve arquivo de saída; exibe confirmação
  - Confiança: 🟢

## Tarefas de Teste

- [ ] TT-01, Testar importação com JSON de 1 projeto, 3 seções, 5 cards
- [ ] TT-02, Testar com arquivo inexistente (código 2)
- [ ] TT-03, Testar com JSON sem projetos ("No projects found")
- [ ] TT-04, Testar card sem membership (warn, não erro)
- [ ] TT-05, Testar card sem notes (sem TextBlock filho)

## Ordem Sugerida
1. T-01 (CLI)
2. T-02 (leitura)
3. T-03 (extração)
4. T-04 (board + propriedade)
5. T-05 (cards)
6. T-06 (serialização)
