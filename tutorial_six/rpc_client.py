import uuid
from amqplib import client_0_8 as cli


class FibonacciRpcClient(object):
    def __init__(self):
        self.connection = cli.Connection()
        self.channel = cli.Channel(self.connection)
        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result[0]
        self.channel.basic_consume(callback=self.on_response,
                                   no_ack=True,
                                   queue=self.callback_queue)

    def on_response(self, msg):
        if self.corr_id == msg.correlation_id:
            self.response = msg.body

    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        message = cli.Message(body=str(n))
        message.properties['reply_to'] = self.callback_queue
        message.properties['correlation_id'] = self.corr_id

        # for k, v in message.__dict__.iteritems():
        #     print '%s: %s' % (k, v)

        self.channel.basic_publish(exchange='',
                                   routing_key='rpc_queue',
                                   msg=message)

        while self.response is None:
            self.channel.wait()
        return int(self.response)

if __name__ == '__main__':
    fibonacci_rpc = FibonacciRpcClient()
    to_find = 9

    print ' [x] Requesting fib(%s)' % to_find
    response = fibonacci_rpc.call(to_find)
    print ' [.] Got %r' % (response,)
