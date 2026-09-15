import tkinter as tk
from tkinter import ttk, messagebox

from banco import (
    criar_tabela_chamados,
    obter_indicadores,
    atualizar_chamado
)

from chamados import (
    cadastrar_chamado,
    listar_chamados,
    obter_chamado
)

from relatorios import (
    obter_chamados_por_status,
    obter_chamados_por_prioridade,
    obter_chamados_por_categoria,
    exportar_relatorio_excel
)


# ============================================================
# CONFIGURAÇÕES
# ============================================================

LARGURA = 850
ALTURA = 600

STATUS = [
    "Aberto",
    "Em atendimento",
    "Encerrado"
]

PRIORIDADES = [
    "Baixa",
    "Média",
    "Alta",
    "Crítica"
]

CATEGORIAS = [
    "Computador",
    "Sistema",
    "Rede",
    "Impressora",
    "Acesso",
    "Outro"
]

SETORES = [
    "Administrativo",
    "Financeiro",
    "RH",
    "Produção",
    "TI",
    "Comercial",
    "Logística",
    "Outro"
]


# ============================================================
# CENTRALIZA JANELA
# ============================================================

def centralizar_janela(janela, largura, altura):
    janela.update_idletasks()

    largura_tela = janela.winfo_screenwidth()
    altura_tela = janela.winfo_screenheight()

    pos_x = (largura_tela - largura) // 2
    pos_y = (altura_tela - altura) // 2

    janela.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")


# ============================================================
# ATUALIZA INDICADORES
# ============================================================

def atualizar_indicadores():
    indicadores = obter_indicadores()

    lbl_total.config(text=str(indicadores["total"]))
    lbl_abertos.config(text=str(indicadores["abertos"]))
    lbl_atendimento.config(text=str(indicadores["em_atendimento"]))
    lbl_encerrados.config(text=str(indicadores["encerrados"]))


# ============================================================
# NOVO CHAMADO
# ============================================================

def tela_novo_chamado():

    janela = tk.Toplevel(root)
    janela.title("Novo Chamado")
    centralizar_janela(janela, 600, 600)
    janela.resizable(False, False)

    frame = ttk.Frame(janela, padding=20)
    frame.pack(fill="both", expand=True)

    ttk.Label(
        frame,
        text="ABERTURA DE CHAMADO",
        font=("Segoe UI", 16, "bold")
    ).pack(pady=(0, 20))

    ttk.Label(frame, text="Solicitante:").pack(anchor="w")
    entrada_solicitante = ttk.Entry(frame)
    entrada_solicitante.pack(fill="x", pady=(0, 10))

    ttk.Label(frame, text="Setor:").pack(anchor="w")
    combo_setor = ttk.Combobox(
        frame,
        values=SETORES,
        state="readonly"
    )
    combo_setor.pack(fill="x", pady=(0, 10))

    ttk.Label(frame, text="Categoria:").pack(anchor="w")
    combo_categoria = ttk.Combobox(
        frame,
        values=CATEGORIAS,
        state="readonly"
    )
    combo_categoria.pack(fill="x", pady=(0, 10))

    ttk.Label(frame, text="Prioridade:").pack(anchor="w")
    combo_prioridade = ttk.Combobox(
        frame,
        values=PRIORIDADES,
        state="readonly"
    )
    combo_prioridade.pack(fill="x", pady=(0, 10))

    ttk.Label(frame, text="Responsável:").pack(anchor="w")
    entrada_responsavel = ttk.Entry(frame)
    entrada_responsavel.pack(fill="x", pady=(0, 10))

    ttk.Label(frame, text="Descrição:").pack(anchor="w")

    texto_descricao = tk.Text(
        frame,
        height=7,
        font=("Segoe UI", 10)
    )
    texto_descricao.pack(fill="both", expand=True, pady=(0, 15))

    def salvar():

        solicitante = entrada_solicitante.get().strip()
        setor = combo_setor.get().strip()
        categoria = combo_categoria.get().strip()
        prioridade = combo_prioridade.get().strip()
        responsavel = entrada_responsavel.get().strip()
        descricao = texto_descricao.get("1.0", "end").strip()

        if not solicitante:
            messagebox.showwarning(
                "Atenção",
                "Informe o solicitante."
            )
            return

        if not setor:
            messagebox.showwarning(
                "Atenção",
                "Selecione o setor."
            )
            return

        if not categoria:
            messagebox.showwarning(
                "Atenção",
                "Selecione a categoria."
            )
            return

        if not prioridade:
            messagebox.showwarning(
                "Atenção",
                "Selecione a prioridade."
            )
            return

        if not descricao:
            messagebox.showwarning(
                "Atenção",
                "Informe a descrição do chamado."
            )
            return

        numero = cadastrar_chamado(
            solicitante,
            setor,
            categoria,
            descricao,
            prioridade,
            responsavel if responsavel else None
        )

        messagebox.showinfo(
            "Sucesso",
            f"Chamado #{numero} cadastrado com sucesso!"
        )

        atualizar_indicadores()
        janela.destroy()

    ttk.Button(
        frame,
        text="SALVAR CHAMADO",
        command=salvar
    ).pack(fill="x", ipady=5)


# ============================================================
# CONSULTAR CHAMADOS
# ============================================================

def tela_consultar_chamados():

    janela = tk.Toplevel(root)
    janela.title("Consultar Chamados")
    centralizar_janela(janela, 1050, 600)
    janela.minsize(900, 550)

    frame_principal = ttk.Frame(janela, padding=15)
    frame_principal.pack(fill="both", expand=True)

    ttk.Label(
        frame_principal,
        text="CONSULTA DE CHAMADOS",
        font=("Segoe UI", 16, "bold")
    ).pack(pady=(0, 15))

    # --------------------------------------------------------
    # FILTROS
    # --------------------------------------------------------

    frame_filtros = ttk.LabelFrame(
        frame_principal,
        text="Filtros",
        padding=10
    )
    frame_filtros.pack(fill="x", pady=(0, 10))

    ttk.Label(frame_filtros, text="Status:").grid(
        row=0, column=0, padx=5, pady=5
    )

    combo_filtro_status = ttk.Combobox(
        frame_filtros,
        values=["Todos"] + STATUS,
        state="readonly",
        width=18
    )
    combo_filtro_status.set("Todos")
    combo_filtro_status.grid(
        row=0, column=1, padx=5, pady=5
    )

    ttk.Label(frame_filtros, text="Prioridade:").grid(
        row=0, column=2, padx=5, pady=5
    )

    combo_filtro_prioridade = ttk.Combobox(
        frame_filtros,
        values=["Todos"] + PRIORIDADES,
        state="readonly",
        width=15
    )
    combo_filtro_prioridade.set("Todos")
    combo_filtro_prioridade.grid(
        row=0, column=3, padx=5, pady=5
    )

    ttk.Label(frame_filtros, text="Categoria:").grid(
        row=0, column=4, padx=5, pady=5
    )

    combo_filtro_categoria = ttk.Combobox(
        frame_filtros,
        values=["Todos"] + CATEGORIAS,
        state="readonly",
        width=15
    )
    combo_filtro_categoria.set("Todos")
    combo_filtro_categoria.grid(
        row=0, column=5, padx=5, pady=5
    )

    # --------------------------------------------------------
    # TABELA
    # --------------------------------------------------------

    frame_tabela = ttk.Frame(frame_principal)
    frame_tabela.pack(fill="both", expand=True)

    colunas = (
        "id",
        "data",
        "solicitante",
        "setor",
        "categoria",
        "prioridade",
        "responsavel",
        "status"
    )

    tabela = ttk.Treeview(
        frame_tabela,
        columns=colunas,
        show="headings"
    )

    tabela.heading("id", text="ID")
    tabela.heading("data", text="Data")
    tabela.heading("solicitante", text="Solicitante")
    tabela.heading("setor", text="Setor")
    tabela.heading("categoria", text="Categoria")
    tabela.heading("prioridade", text="Prioridade")
    tabela.heading("responsavel", text="Responsável")
    tabela.heading("status", text="Status")

    tabela.column("id", width=50)
    tabela.column("data", width=140)
    tabela.column("solicitante", width=150)
    tabela.column("setor", width=120)
    tabela.column("categoria", width=120)
    tabela.column("prioridade", width=100)
    tabela.column("responsavel", width=150)
    tabela.column("status", width=120)

    scroll = ttk.Scrollbar(
        frame_tabela,
        orient="vertical",
        command=tabela.yview
    )

    tabela.configure(yscrollcommand=scroll.set)

    tabela.pack(
        side="left",
        fill="both",
        expand=True
    )

    scroll.pack(
        side="right",
        fill="y"
    )

    # --------------------------------------------------------
    # CARREGAR DADOS
    # --------------------------------------------------------

    def carregar_chamados():

        for item in tabela.get_children():
            tabela.delete(item)

        chamados = listar_chamados()

        filtro_status = combo_filtro_status.get()
        filtro_prioridade = combo_filtro_prioridade.get()
        filtro_categoria = combo_filtro_categoria.get()

        for chamado in chamados:

            (
                id_chamado,
                data,
                solicitante,
                setor,
                categoria,
                prioridade,
                responsavel,
                status
            ) = chamado

            if (
                filtro_status != "Todos"
                and status != filtro_status
            ):
                continue

            if (
                filtro_prioridade != "Todos"
                and prioridade != filtro_prioridade
            ):
                continue

            if (
                filtro_categoria != "Todos"
                and categoria != filtro_categoria
            ):
                continue

            tabela.insert(
                "",
                "end",
                values=(
                    id_chamado,
                    data,
                    solicitante,
                    setor,
                    categoria,
                    prioridade,
                    responsavel or "",
                    status
                )
            )

    def filtrar():
        carregar_chamados()

    def limpar_filtros():

        combo_filtro_status.set("Todos")
        combo_filtro_prioridade.set("Todos")
        combo_filtro_categoria.set("Todos")

        carregar_chamados()

    frame_botoes = ttk.Frame(frame_principal)
    frame_botoes.pack(fill="x", pady=(10, 0))

    ttk.Button(
        frame_botoes,
        text="FILTRAR",
        command=filtrar
    ).pack(side="left", padx=5)

    ttk.Button(
        frame_botoes,
        text="LIMPAR",
        command=limpar_filtros
    ).pack(side="left", padx=5)

    ttk.Button(
        frame_botoes,
        text="ATUALIZAR",
        command=carregar_chamados
    ).pack(side="right", padx=5)

    carregar_chamados()


# ============================================================
# GERENCIAR CHAMADO
# ============================================================

def tela_gerenciar_chamado():

    janela = tk.Toplevel(root)
    janela.title("Gerenciar Chamado")
    centralizar_janela(janela, 650, 650)
    janela.resizable(False, False)

    frame = ttk.Frame(janela, padding=20)
    frame.pack(fill="both", expand=True)

    ttk.Label(
        frame,
        text="GERENCIAR CHAMADO",
        font=("Segoe UI", 16, "bold")
    ).pack(pady=(0, 15))

    ttk.Label(
        frame,
        text="Informe o número do chamado:"
    ).pack(anchor="w")

    entrada_id = ttk.Entry(frame)
    entrada_id.pack(fill="x", pady=(5, 10))

    frame_info = ttk.LabelFrame(
        frame,
        text="Informações do Chamado",
        padding=10
    )
    frame_info.pack(fill="x", pady=(0, 10))

    texto_info = tk.Text(
        frame_info,
        height=9,
        width=70,
        font=("Segoe UI", 10),
        wrap="word"
    )
    texto_info.pack(fill="x")

    texto_info.config(state="disabled")

    frame_alteracao = ttk.LabelFrame(
        frame,
        text="Alteração",
        padding=10
    )
    frame_alteracao.pack(fill="x", pady=(0, 10))

    ttk.Label(
        frame_alteracao,
        text="Novo status:"
    ).grid(row=0, column=0, padx=5, pady=5, sticky="w")

    combo_status = ttk.Combobox(
        frame_alteracao,
        values=STATUS,
        state="readonly",
        width=25
    )
    combo_status.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(
        frame_alteracao,
        text="Solução:"
    ).grid(row=1, column=0, padx=5, pady=5, sticky="nw")

    texto_solucao = tk.Text(
        frame_alteracao,
        height=5,
        width=50,
        font=("Segoe UI", 10),
        wrap="word"
    )
    texto_solucao.grid(
        row=1,
        column=1,
        padx=5,
        pady=5
    )

    # --------------------------------------------------------
    # BUSCAR CHAMADO
    # --------------------------------------------------------

    def buscar():

        valor = entrada_id.get().strip()

        if not valor.isdigit():
            messagebox.showwarning(
                "Atenção",
                "Informe um número de chamado válido."
            )
            return

        chamado = obter_chamado(int(valor))

        if not chamado:
            messagebox.showerror(
                "Não encontrado",
                "Chamado não encontrado."
            )
            return

        (
            id_chamado,
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
        ) = chamado

        informacoes = (
            f"Chamado: #{id_chamado}\n"
            f"Data de abertura: {data_abertura}\n"
            f"Solicitante: {solicitante}\n"
            f"Setor: {setor}\n"
            f"Categoria: {categoria}\n"
            f"Prioridade: {prioridade}\n"
            f"Responsável: {responsavel or '-'}\n"
            f"Status atual: {status}\n\n"
            f"Descrição:\n{descricao}"
        )

        texto_info.config(state="normal")
        texto_info.delete("1.0", "end")
        texto_info.insert("1.0", informacoes)
        texto_info.config(state="disabled")

        combo_status.set(status)

        texto_solucao.delete("1.0", "end")

        if solucao:
            texto_solucao.insert("1.0", solucao)

    # --------------------------------------------------------
    # SALVAR ALTERAÇÃO
    # --------------------------------------------------------

    def salvar_alteracao():

        valor = entrada_id.get().strip()

        if not valor.isdigit():
            messagebox.showwarning(
                "Atenção",
                "Informe um número de chamado válido."
            )
            return

        status = combo_status.get().strip()

        if not status:
            messagebox.showwarning(
                "Atenção",
                "Selecione o novo status."
            )
            return

        solucao = texto_solucao.get(
            "1.0",
            "end"
        ).strip()

        if status == "Encerrado" and not solucao:
            messagebox.showwarning(
                "Atenção",
                "Informe a solução para encerrar o chamado."
            )
            return

        chamado = obter_chamado(int(valor))

        if not chamado:
            messagebox.showerror(
                "Erro",
                "Chamado não encontrado."
            )
            return

        atualizar_chamado(
            int(valor),
            status,
            solucao if solucao else None
        )

        messagebox.showinfo(
            "Sucesso",
            "Chamado atualizado com sucesso!"
        )

        atualizar_indicadores()

        buscar()

    # --------------------------------------------------------
    # BOTÕES
    # --------------------------------------------------------

    frame_botoes = ttk.Frame(frame)
    frame_botoes.pack(
        fill="x",
        pady=(5, 0)
    )

    ttk.Button(
        frame_botoes,
        text="BUSCAR CHAMADO",
        command=buscar
    ).pack(
        side="left",
        expand=True,
        fill="x",
        padx=(0, 5),
        ipady=5
    )

    ttk.Button(
        frame_botoes,
        text="SALVAR ALTERAÇÃO",
        command=salvar_alteracao
    ).pack(
        side="right",
        expand=True,
        fill="x",
        padx=(5, 0),
        ipady=5
    )


# ============================================================
# RELATÓRIOS
# ============================================================

def tela_relatorios():

    janela = tk.Toplevel(root)
    janela.title("Relatórios")
    centralizar_janela(janela, 700, 600)
    janela.resizable(False, False)

    frame = ttk.Frame(janela, padding=20)
    frame.pack(fill="both", expand=True)

    ttk.Label(
        frame,
        text="RELATÓRIOS",
        font=("Segoe UI", 16, "bold")
    ).pack(pady=(0, 20))

    # --------------------------------------------------------
    # STATUS
    # --------------------------------------------------------

    frame_status = ttk.LabelFrame(
        frame,
        text="Chamados por Status",
        padding=10
    )
    frame_status.pack(fill="x", pady=5)

    for status, quantidade in obter_chamados_por_status():

        ttk.Label(
            frame_status,
            text=f"{status}: {quantidade}"
        ).pack(anchor="w")

    # --------------------------------------------------------
    # PRIORIDADE
    # --------------------------------------------------------

    frame_prioridade = ttk.LabelFrame(
        frame,
        text="Chamados por Prioridade",
        padding=10
    )
    frame_prioridade.pack(fill="x", pady=5)

    for prioridade, quantidade in obter_chamados_por_prioridade():

        ttk.Label(
            frame_prioridade,
            text=f"{prioridade}: {quantidade}"
        ).pack(anchor="w")

    # --------------------------------------------------------
    # CATEGORIA
    # --------------------------------------------------------

    frame_categoria = ttk.LabelFrame(
        frame,
        text="Chamados por Categoria",
        padding=10
    )
    frame_categoria.pack(fill="x", pady=5)

    for categoria, quantidade in obter_chamados_por_categoria():

        ttk.Label(
            frame_categoria,
            text=f"{categoria}: {quantidade}"
        ).pack(anchor="w")

    # --------------------------------------------------------
    # EXPORTAÇÃO
    # --------------------------------------------------------

    def exportar():

        try:
            arquivo = exportar_relatorio_excel()

            messagebox.showinfo(
                "Relatório exportado",
                f"Relatório gerado com sucesso!\n\n{arquivo}"
            )

        except Exception as erro:

            messagebox.showerror(
                "Erro",
                f"Não foi possível gerar o relatório.\n\n{erro}"
            )

    ttk.Button(
        frame,
        text="EXPORTAR RELATÓRIO PARA EXCEL",
        command=exportar
    ).pack(
        fill="x",
        pady=(20, 0),
        ipady=6
    )


# ============================================================
# JANELA PRINCIPAL
# ============================================================

criar_tabela_chamados()

root = tk.Tk()
root.title("Sistema de Controle de Chamados de TI")

root.geometry(f"{LARGURA}x{ALTURA}")
root.minsize(LARGURA, ALTURA)

centralizar_janela(
    root,
    LARGURA,
    ALTURA
)

# ============================================================
# TÍTULO
# ============================================================

frame_titulo = ttk.Frame(root, padding=(20, 15))
frame_titulo.pack(fill="x")

ttk.Label(
    frame_titulo,
    text="SISTEMA DE CONTROLE DE CHAMADOS DE TI",
    font=("Segoe UI", 18, "bold")
).pack()

ttk.Label(
    frame_titulo,
    text="Gestão e acompanhamento de chamados",
    font=("Segoe UI", 10)
).pack(pady=(5, 0))


# ============================================================
# INDICADORES
# ============================================================

frame_indicadores = ttk.Frame(
    root,
    padding=(20, 5)
)
frame_indicadores.pack(fill="x")

frame_indicadores.columnconfigure(
    0,
    weight=1
)

frame_indicadores.columnconfigure(
    1,
    weight=1
)

frame_indicadores.columnconfigure(
    2,
    weight=1
)

frame_indicadores.columnconfigure(
    3,
    weight=1
)


def criar_card(parent, titulo, coluna):

    card = ttk.LabelFrame(
        parent,
        text=titulo,
        padding=10
    )

    card.grid(
        row=0,
        column=coluna,
        padx=5,
        sticky="nsew"
    )

    label = ttk.Label(
        card,
        text="0",
        font=("Segoe UI", 20, "bold"),
        anchor="center"
    )

    label.pack(
        fill="both",
        expand=True
    )

    return label


lbl_total = criar_card(
    frame_indicadores,
    "TOTAL",
    0
)

lbl_abertos = criar_card(
    frame_indicadores,
    "ABERTOS",
    1
)

lbl_atendimento = criar_card(
    frame_indicadores,
    "EM ATENDIMENTO",
    2
)

lbl_encerrados = criar_card(
    frame_indicadores,
    "ENCERRADOS",
    3
)



# ============================================================
# MENU PRINCIPAL
# ============================================================

frame_menu = ttk.Frame(
    root,
    padding=(80, 15, 80, 25)
)

frame_menu.pack(
    fill="both",
    expand=True
)

# Área central do menu
frame_botoes_menu = ttk.Frame(frame_menu)

frame_botoes_menu.pack(
    expand=True
)

# Botões menores e discretos
btn_novo = ttk.Button(
    frame_botoes_menu,
    text="Novo Chamado",
    command=tela_novo_chamado,
    width=24
)

btn_consultar = ttk.Button(
    frame_botoes_menu,
    text="Consultar Chamados",
    command=tela_consultar_chamados,
    width=24
)

btn_gerenciar = ttk.Button(
    frame_botoes_menu,
    text="Gerenciar Chamado",
    command=tela_gerenciar_chamado,
    width=24
)

btn_relatorios = ttk.Button(
    frame_botoes_menu,
    text="Relatórios",
    command=tela_relatorios,
    width=24
)

btn_novo.grid(
    row=0,
    column=0,
    padx=8,
    pady=8,
    ipadx=5,
    ipady=4
)

btn_consultar.grid(
    row=0,
    column=1,
    padx=8,
    pady=8,
    ipadx=5,
    ipady=4
)

btn_gerenciar.grid(
    row=1,
    column=0,
    padx=8,
    pady=8,
    ipadx=5,
    ipady=4
)

btn_relatorios.grid(
    row=1,
    column=1,
    padx=8,
    pady=8,
    ipadx=5,
    ipady=4
)




# ============================================================
# INICIALIZA INDICADORES
# ============================================================

atualizar_indicadores()

root.mainloop()