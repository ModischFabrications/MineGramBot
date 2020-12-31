import signal

keep_running = True


# telebot exception handling hides everything, this is a workaround
def exit(sig, frame):
    global keep_running
    keep_running = False
    raise KeyboardInterrupt


signal.signal(signal.SIGINT, exit)
print("Press CTRL+C to stop server")
