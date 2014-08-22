import sys
from amqplib import client_0_8 as cli

if __name__ == '__main__':
    connection = cli.Connection()
    channel = cli.Channel(connection)

    channel.exchange_declare(exchange='logs',
                             type='fanout')

    result = channel.queue_declare(exclusive=True)

    body = ' '.join(sys.argv[1:]) or 'Hello World!'
    message = cli.Message(body=body)

    channel.basic_publish(msg=message,
                          exchange='logs',
                          routing_key='')

    print ' [x] Sent %r' % (message.body,)
    connection.close()