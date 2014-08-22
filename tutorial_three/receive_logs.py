from amqplib import client_0_8 as cli

if __name__ == '__main__':
    connection = cli.Connection()

    channel = cli.Channel(connection)
    channel.exchange_declare(exchange='logs',
                             type='fanout')

    result = channel.queue_declare(exclusive=True)
    queue_name = result[0]
    # import ipdb; ipdb.set_trace()

    channel.queue_bind(exchange='logs',
                       queue=queue_name)

    print ' [*] Waiting for logs. To exit press CTRL+C'

    def callback(msg):
            print " [x] %r" % (msg.body,)

            with open('rabbitmq.log', 'a') as f:
                f.write('%s\n' % msg.body)

    channel.basic_consume(callback=callback,
                          queue=queue_name,
                          no_ack=True)

    while True:
        channel.wait()