def registrar_tentativa(nome_api, rota, ip, autorizado):
    status = "AUTORIZADO" if autorizado else "NEGADO"
    print(f"[LOG ACESSO] API: {nome_api} | Rota: {rota} | IP: {ip} | Status: {status}")
    
    try:
        with open("tentativas_acesso.log", "a", encoding="utf-8") as arquivo:
            arquivo.write(f"API: {nome_api} | Rota: {rota} | IP: {ip} | Status: {status}\n")
    except OSError:
        pass