import sys
from amqplib import client_0_8 as cli

if __name__ == '__main__':
    connection = cli.Connection()

    channel = cli.Channel(connection)
    channel.exchange_declare(exchange='topic_logs',
                             type='topic')

    result = channel.queue_declare(exclusive=True)
    queue_name = result[0]

    binding_keys = sys.argv[1:]
    if not binding_keys:
        print >> sys.stderr, 'Usage: %s [binding_key]' % (sys.argv[0],)
        sys.exit(1)

    for binding_key in binding_keys:
        channel.queue_bind(exchange='topic_logs',
                           queue=queue_name,
                           routing_key=binding_key)

    print ' [*] Waiting for logs. To exit press CTRL+C'

    def callback(msg):
            print " [x] %r" % (msg.body,)

            # with open('rabbitmq.log', 'a') as f:
            #     f.write('%s\n' % msg.body)

    channel.basic_consume(callback=callback,
                          queue=queue_name,
                          no_ack=True)

    while True:
        channel.wait()