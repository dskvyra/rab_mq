import sys
from amqplib import client_0_8 as cli

if __name__ == '__main__':
    connection = cli.Connection()

    channel = cli.Channel(connection)
    channel.exchange_declare(exchange='topic_logs',
                             type='topic')

    routing_key = sys.argv[1] if len(sys.argv) > 1 else 'anonymous.info'

    body = ' '.join(sys.argv[2:]) or 'Hello World!'
    message = cli.Message(body=body)

    channel.basic_publish(msg=message,
                          exchange='topic_logs',
                          routing_key=routing_key)

    print ' [x] Sent %r' % (message.body,)
    connection.close()