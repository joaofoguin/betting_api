import os
import json
import pika

RABBITMQ_URL = os.getenv("RABBITMQ_URL")


def publicar_evento(nome_evento: str, dados: dict):
    if not RABBITMQ_URL:
        print("[RabbitMQ] RABBITMQ_URL não configurada")
        return

    try:
        params = pika.URLParameters(RABBITMQ_URL)
        connection = pika.BlockingConnection(params)
        channel = connection.channel()

        channel.queue_declare(queue="eventos_lutas", durable=True)

        mensagem = {
            "evento": nome_evento,
            "dados": dados
        }

        channel.basic_publish(
            exchange="",
            routing_key="eventos_lutas",
            body=json.dumps(mensagem),
            properties=pika.BasicProperties(delivery_mode=2)
        )

        connection.close()
        print(f"[RabbitMQ] Evento publicado: {nome_evento}")

    except Exception as erro:
        print(f"[RabbitMQ ERRO] {erro}")