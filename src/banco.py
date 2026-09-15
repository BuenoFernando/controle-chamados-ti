import sqlite3
from pathlib import Path


# Localização do banco de dados
BASE_DIR = Path(__file__).resolve().parent.parent
PASTA_BANCO = BASE_DIR / "banco"
ARQUIVO_BANCO = PASTA_BANCO / "chamados.db"


def conectar():
    """Cria e retorna uma conexão com o banco de dados."""
    PASTA_BANCO.mkdir(exist_ok=True)

    conexao = sqlite3.connect(ARQUIVO_BANCO)
    conexao.execute("PRAGMA foreign_keys = ON")

    return conexao


def criar_tabela_chamados():
    """Cria a tabela de chamados caso ela ainda não exista."""

    conexao = conectar()

    conexao.execute("""
        CREATE TABLE IF NOT EXISTS chamados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data_abertura TEXT NOT NULL,
            solicitante TEXT NOT NULL,
            setor TEXT NOT NULL,
            categoria TEXT NOT NULL,
            descricao TEXT NOT NULL,
            prioridade TEXT NOT NULL,
            responsavel TEXT,
            status TEXT NOT NULL DEFAULT 'Aberto',
            solucao TEXT,
            data_encerramento TEXT
        )
    """)

    conexao.commit()
    conexao.close()


def atualizar_chamado(id_chamado, status, solucao=None):
    """Atualiza o status e a solução de um chamado."""

    conexao = conectar()

    if status == "Encerrado":
        conexao.execute("""
            UPDATE chamados
            SET status = ?,
                solucao = ?,
                data_encerramento = datetime('now', 'localtime')
            WHERE id = ?
        """, (status, solucao, id_chamado))

    else:
        conexao.execute("""
            UPDATE chamados
            SET status = ?,
                solucao = ?,
                data_encerramento = NULL
            WHERE id = ?
        """, (status, solucao, id_chamado))

    conexao.commit()
    conexao.close()


def obter_indicadores():
    """Retorna os principais indicadores do sistema."""

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            COUNT(*) AS total,
            SUM(CASE WHEN status = 'Aberto' THEN 1 ELSE 0 END) AS abertos,
            SUM(CASE WHEN status = 'Em atendimento' THEN 1 ELSE 0 END) AS em_atendimento,
            SUM(CASE WHEN status = 'Encerrado' THEN 1 ELSE 0 END) AS encerrados
        FROM chamados
    """)

    resultado = cursor.fetchone()

    conexao.close()

    return {
        "total": resultado[0] or 0,
        "abertos": resultado[1] or 0,
        "em_atendimento": resultado[2] or 0,
        "encerrados": resultado[3] or 0
    }


if __name__ == "__main__":
    criar_tabela_chamados()
    print("Banco de dados criado com sucesso!")