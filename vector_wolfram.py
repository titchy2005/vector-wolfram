# import librairies
import wolframalpha
import functools
import threading
import anki_vector
from anki_vector.events import Events

client = wolframalpha.Client('KY6GR9-P6HPW2TQU8')
wake_word_heard = False
repeat = False
    

def main():
    evt = threading.Event()

    def on_wake_word(robot, event_type, event):
        robot.conn.request_control()

        global wake_word_heard
        if not wake_word_heard:
            wake_word_heard = True
            question = input('What is your question?')
            res = client.query(question)
            answer = next(res.results).text
            robot.say_text(answer)
            repeat = True
            evt.set()

    args = anki_vector.util.parse_command_args()
    with anki_vector.Robot(args.serial, requires_behavior_control=False, cache_animation_list=False) as robot:
        on_wake_word = functools.partial(on_wake_word, robot)
        robot.events.subscribe(on_wake_word, Events.wake_word)

        print('------ Vector is waiting to hear "Hey Vector!" Press ctrl+c to exit early ------')

        try:
            if not evt.wait(timeout=60):
                main()
        except KeyboardInterrupt:
            pass

if __name__ == '__main__':
    main()
    while repeat == True:
            main()
            repeat = False



