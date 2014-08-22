import sys
from amqplib import client_0_8 as cli

if __name__ == '__main__':
    connection = cli.Connection()

    channel = cli.Channel(connection)
    channel.exchange_declare(exchange='direct_logs',
                             type='direct')

    result = channel.queue_declare(exclusive=True)
    queue_name = result[0]

    severities = sys.argv[1:]
    if not severities:
        print >> sys.stderr, "Usage: %s [info] [warning] [error]" % \
            (sys.argv[0],)
        sys.exit(1)

    for severity in severities:
        channel.queue_bind(exchange='direct_logs',
                           queue=queue_name,
                           routing_key=severity)

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