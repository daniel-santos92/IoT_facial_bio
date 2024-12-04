from screeninfo import get_monitors

def centralizar_janela(janela):
    """
    Centraliza uma janela Tkinter na tela principal, mesmo com múltiplos monitores.
    :param janela: Objeto Tkinter (Tk ou Toplevel).
    """
    janela.update_idletasks()  # Garante que as dimensões da janela sejam calculadas corretamente

    # Obter o monitor principal
    monitor_principal = get_monitors()[0]
    largura_tela = monitor_principal.width
    altura_tela = monitor_principal.height

    # Obter dimensões da janela
    largura_janela = janela.winfo_width()
    altura_janela = janela.winfo_height()

    # Calcular coordenadas para centralizar no monitor principal
    x = (largura_tela // 2) - (largura_janela // 2)
    y = (altura_tela // 2) - (altura_janela // 2)

    # Aplicar coordenadas para centralizar
    janela.geometry(f"{largura_janela}x{altura_janela}+{x}+{y}")
