import logging

def setup_logging(debug=False):
    """
    Configura o sistema de logs.
    :param debug: Ativa logs detalhados se True.
    """
    log_level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - [%(levelname)s] - %(message)s",
        handlers=[logging.StreamHandler()]
    )

    if debug:
        logging.debug("Modo debug ativado. Logs detalhados estão sendo exibidos.")
    else:
        logging.info("Modo padrão ativado. Logs básicos estão sendo exibidos.")
