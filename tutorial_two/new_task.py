# coding: utf-8
import sys
import amqplib.client_0_8 as rabbit_cli

if __name__ == '__main__':
    connection = rabbit_cli.Connection()
    channel = connection.channel()
    body = ' '.join(sys.argv[1:]) or 'Hello World!'
    message = rabbit_cli.Message(body=body)

    message.properties['delivery_mode'] = 2

    channel.queue_declare(queue='task_queue', durable=True)
    channel.basic_publish(msg=message,
                          exchange='',
                          routing_key='task_queue',
                          )

    print " [x] Sent %s" % body

    connection.close()
