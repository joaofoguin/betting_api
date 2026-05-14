def registrar_tentativa(nome_api, rota, ip, autorizado):
    status_texto = "AUTORIZADO" if autorizado else "NEGADO"
    
    # Na Vercel, o print() envia o log direto para o painel de monitoramento da nuvem
    # Evita o erro de "Read-only file system"
    print(f"[AUDITORIA VERCEL] API: {nome_api} | Rota: {rota} | IP: {ip} | Status: {status_texto}")