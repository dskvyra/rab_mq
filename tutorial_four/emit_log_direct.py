import sys
from amqplib import client_0_8 as cli

if __name__ == '__main__':
    connection = cli.Connection()
    channel = cli.Channel(connection)

    channel.exchange_declare(exchange='direct_logs',
                             type='direct')

    result = channel.queue_declare(exclusive=True)

    severity = sys.argv[1] if len(sys.argv) > 1 else 'info'
    body = ' '.join(sys.argv[2:]) or 'Hello World!'
    message = cli.Message(body=body)

    channel.basic_publish(msg=message,
                          exchange='direct_logs',
                          routing_key=severity)

    print ' [x] Sent %r' % (message.body,)
    connection.close()