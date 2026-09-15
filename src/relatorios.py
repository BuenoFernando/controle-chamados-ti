from banco import conectar


def obter_total_chamados():
    """Retorna o total de chamados cadastrados."""

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM chamados
    """)

    total = cursor.fetchone()[0]

    conexao.close()

    return total


def obter_chamados_por_status():
    """Retorna a quantidade de chamados agrupados por status."""

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            status,
            COUNT(*) AS quantidade
        FROM chamados
        GROUP BY status
        ORDER BY quantidade DESC
    """)

    resultado = cursor.fetchall()

    conexao.close()

    return resultado


def obter_chamados_por_prioridade():
    """Retorna a quantidade de chamados agrupados por prioridade."""

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            prioridade,
            COUNT(*) AS quantidade
        FROM chamados
        GROUP BY prioridade
        ORDER BY quantidade DESC
    """)

    resultado = cursor.fetchall()

    conexao.close()

    return resultado


def obter_chamados_por_categoria():
    """Retorna a quantidade de chamados agrupados por categoria."""

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            categoria,
            COUNT(*) AS quantidade
        FROM chamados
        GROUP BY categoria
        ORDER BY quantidade DESC
    """)

    resultado = cursor.fetchall()

    conexao.close()

    return resultado

def exportar_relatorio_excel():
    """Exporta os chamados para um arquivo Excel."""

    from openpyxl import Workbook
    from pathlib import Path

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            id,
            data_abertura,
            solicitante,
            setor,
            categoria,
            descricao,
            prioridade,
            responsavel,
            status,
            solucao,
            data_encerramento
        FROM chamados
        ORDER BY id DESC
    """)

    chamados = cursor.fetchall()

    conexao.close()

    # Pasta onde o relatório será salvo
    pasta_relatorios = Path(__file__).resolve().parent.parent / "relatorios"
    pasta_relatorios.mkdir(exist_ok=True)

    arquivo = pasta_relatorios / "relatorio_chamados.xlsx"

    # Criação do arquivo Excel
    workbook = Workbook()
    planilha = workbook.active
    planilha.title = "Chamados"

    # Cabeçalhos
    cabecalhos = [
        "ID",
        "Data de Abertura",
        "Solicitante",
        "Setor",
        "Categoria",
        "Descrição",
        "Prioridade",
        "Responsável",
        "Status",
        "Solução",
        "Data de Encerramento"
    ]

    planilha.append(cabecalhos)

    # Dados
    for chamado in chamados:
        planilha.append(chamado)

    # Ajuste das larguras das colunas
    larguras = {
        "A": 8,
        "B": 20,
        "C": 20,
        "D": 20,
        "E": 18,
        "F": 45,
        "G": 15,
        "H": 20,
        "I": 18,
        "J": 45,
        "K": 20
    }

    for coluna, largura in larguras.items():
        planilha.column_dimensions[coluna].width = largura

    # Congela a primeira linha
    planilha.freeze_panes = "A2"

    workbook.save(arquivo)

    return arquivo


if __name__ == "__main__":
    print("Total de chamados:", obter_total_chamados())

    print("\nChamados por status:")
    for status, quantidade in obter_chamados_por_status():
        print(f"- {status}: {quantidade}")

    print("\nChamados por prioridade:")
    for prioridade, quantidade in obter_chamados_por_prioridade():
        print(f"- {prioridade}: {quantidade}")

    print("\nChamados por categoria:")
    for categoria, quantidade in obter_chamados_por_categoria():
        print(f"- {categoria}: {quantidade}")