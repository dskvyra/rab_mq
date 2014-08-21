# coding: utf-8
import amqplib.client_0_8 as rabbit_cli

if __name__ == '__main__':
    connection = rabbit_cli.Connection()
    channel = connection.channel()
    message = rabbit_cli.Message(body='Hello World!')

    channel.queue_declare(queue='hello')
    channel.basic_publish(msg=message, exchange='', routing_key='hello')

    print " [x] Sent 'Hello World!'"

    connection.close()
