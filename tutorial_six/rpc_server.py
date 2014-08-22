from amqplib import client_0_8 as cli

if __name__ == '__main__':
    connection = cli.Connection()

    channel = cli.Channel(connection)
    channel.queue_declare(queue='rpc_queue')

    def fib(n):
        if n == 0:
            return 0
        elif n == 1:
            return 1
        else:
            return fib(n-1) + fib(n-2)

    def on_request(msg):
        n = int(msg.body)

        print ' [.] fib(%s)' % (n,)
        response = cli.Message(str(fib(n)))
        response.properties['correlation_id'] = msg.correlation_id
        # import ipdb; ipdb.set_trace()
        msg.channel.basic_publish(exchange='',
                                  routing_key=msg.reply_to,
                                  msg=response)

        msg.channel.basic_ack(delivery_tag=msg.delivery_tag)

    channel.basic_qos(prefetch_size=0, prefetch_count=1, a_global=False)
    channel.basic_consume(callback=on_request, queue='rpc_queue')

    print ' [x] Awaiting RPC requests'

    while True:
        channel.wait()