# coding: utf-8
import time
import amqplib.client_0_8 as rabbit_cli


if __name__ == '__main__':
    connection = rabbit_cli.Connection()
    channel = connection.channel()
    channel.queue_declare(queue='task_queue', durable=True)

    def callback(msg):
        print ' [x] Received %r' % (msg.body,)
        time.sleep(msg.body.count('.'))
        print '[x] Done'
        channel.basic_ack(msg.delivery_tag)

    # msg = channel.basic_get('task_queue')
    # print msg.body
    # channel.basic_ack(msg.delivery_tag)

    # import ipdb; ipdb.set_trace()

    channel.basic_qos(prefetch_size=0, prefetch_count=1, a_global=False)
    channel.basic_consume(callback=callback, queue='task_queue')

    print ' [*] Waiting for messages. To exit press CTRL+C'

    while True:
        channel.wait()
