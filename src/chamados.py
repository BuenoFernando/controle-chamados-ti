from banco import conectar


def cadastrar_chamado(
    solicitante,
    setor,
    categoria,
    descricao,
    prioridade,
    responsavel=None
):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO chamados (
            data_abertura,
            solicitante,
            setor,
            categoria,
            descricao,
            prioridade,
            responsavel
        )
        VALUES (
            datetime('now', 'localtime'),
            ?, ?, ?, ?, ?, ?
        )
    """, (
        solicitante,
        setor,
        categoria,
        descricao,
        prioridade,
        responsavel
    ))

    conexao.commit()

    numero_chamado = cursor.lastrowid

    conexao.close()

    return numero_chamado


def listar_chamados():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            id,
            data_abertura,
            solicitante,
            setor,
            categoria,
            prioridade,
            responsavel,
            status
        FROM chamados
        ORDER BY id DESC
    """)

    chamados = cursor.fetchall()

    conexao.close()

    return chamados

def obter_chamado(id_chamado):
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
        WHERE id = ?
    """, (id_chamado,))

    chamado = cursor.fetchone()

    conexao.close()

    return chamado