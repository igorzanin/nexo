# language: pt
# spec-id: PT-007
# rastreabilidade:
#   process_flows: _reversa_sdd/code-analysis.md §"Módulo: import/ — Importadores de Dados"; _reversa_sdd/migration/target_business_rules.md §"BR-MIGRAR-015"
#   target_architecture: BC-Content / Importadores CLI + import\util\archive.ts
#   paradigma_alvo: OO com DI (python-jose, SQLAlchemy async, Pinia)
#   br_migrar: BR-MIGRAR-015, BR-MIGRAR-016

Funcionalidade: Importação e exportação
  Como operador do sistema
  Quero importar e exportar boards sem perda semântica relevante
  Para migrar dados externos e preservar portabilidade

  @paridade
  Cenário: Exportar board para CSV
    Dado que existe um board com cards e propriedades visíveis na view atual
    Quando o usuário solicita a exportação em CSV
    Então o sistema gera um arquivo compatível com a estrutura tabular esperada
    E os títulos de colunas refletem as propriedades expostas na view exportada

  @paridade @critico @composicao
  Cenário: Exportar board para .boardarchive em NDJSON
    Dado que existe um board com blocos válidos para exportação
    Quando o usuário solicita a exportação em ".boardarchive"
    Então a primeira linha do arquivo contém o header NDJSON com "version" igual a 1 e um campo "date"
    E as linhas seguintes serializam boards e blocks preservando a cardinalidade lógica do board
    E o mesmo contrato observável é mantido quando a exportação usa dados persistidos ou aggregates carregados por dublê equivalente

  @paridade @critico
  Cenário: Importar arquivo .boardarchive
    Dado que existe um arquivo ".boardarchive" válido gerado no formato suportado
    Quando o operador executa a importação desse arquivo
    Então o sistema recria boards e blocks compatíveis com o conteúdo serializado
    E preserva o versionamento do formato sem exigir transformação manual externa

  @paridade
  Cenário: Importar Trello JSON
    Dado que existe um export JSON do Trello compatível com o importador oficial
    Quando o operador executa o importador Trello
    Então listas são convertidas para propriedades selecionáveis e cartões viram cards do board
    E o resultado é serializado no formato ".boardarchive" aceito pelo backend

  @paridade
  Cenário: Validação prévia produz relatório de erros
    Dado que o arquivo de entrada possui dados inválidos ou incompletos
    Quando o operador executa a validação prévia antes da importação final
    Então o sistema retorna um relatório explícito de erros por item inválido
    E a importação final não é executada enquanto o relatório contiver erros bloqueantes
