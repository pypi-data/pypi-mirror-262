import os
import time
import multiprocessing
from multiprocessing import Queue, Pipe
import codecs


def process_a(queue_ab, pipe_ab):
    while True:
        message = queue_ab.get()
        if message == 'exit':
            break

        processed_message = message.lower()
        pipe_ab.send(processed_message)


def process_b(pipe_ab, queue_ba):
    while True:
        processed_message = pipe_ab.recv()
        if processed_message == 'exit':
            break

        encoded_message = codecs.encode(processed_message, 'rot_13')
        queue_ba.put(encoded_message)


if __name__ == "__main__":
    script_directory = os.path.dirname(os.path.abspath(__file__))
    artifacts_directory = os.path.join(script_directory, "artifacts")
    os.makedirs(artifacts_directory, exist_ok=True)

    with open(os.path.join(artifacts_directory, "integration_results.txt"), "w") as result_file:
        queue_ab = Queue()
        queue_ba = Queue()
        pipe_ab, pipe_ba = Pipe()

        process_a_instance = multiprocessing.Process(target=process_a, args=(queue_ab, pipe_ab))
        process_b_instance = multiprocessing.Process(target=process_b, args=(pipe_ba, queue_ba))

        process_a_instance.start()
        process_b_instance.start()

        for _ in range(5):
            user_input = input("Enter a message (5 times limit): ")
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

            result_file.write(f"{timestamp} - Sent: {user_input}\n")
            queue_ab.put(user_input)

            time.sleep(5)  # Sleep for 5 seconds

            processed_message = queue_ba.get()
            result_file.write(f"{timestamp} - Received: {processed_message}\n")

        queue_ab.put('exit')
        queue_ba.put('exit')

        process_a_instance.join()
        process_b_instance.join()
