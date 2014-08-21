# coding: utf-8
import amqplib.client_0_8 as rabbit_cli


if __name__ == '__main__':
    connection = rabbit_cli.Connection()
    channel = connection.channel()
    channel.queue_declare(queue='hello')

    def callback(msg):
            print " [x] Received %r" % (msg.body,)

    channel.basic_consume(callback=callback, queue='hello', no_ack=True)
    print ' [*] Waiting for messages. To exit press CTRL+C'

    while True:
        channel.wait()
