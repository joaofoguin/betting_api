def registrar_tentativa(nome_api, rota, ip, autorizado):
    status_texto = "AUTORIZADO" if autorizado else "NEGADO"
    print(f"[AUDITORIA] API: {nome_api} | Rota: {rota} | IP: {ip} | Status: {status_texto}")
    
    try:
        with open("tentativas_acesso.log", "a", encoding="utf-8") as arquivo:
            arquivo.write(f"API: {nome_api} | Rota: {rota} | IP: {ip} | Status: {status_texto}\n")
    except Exception as e:
        print(f"Erro local ao escrever no arquivo de log: {e}")