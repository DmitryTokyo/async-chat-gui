import tkinter as tk
import asyncio
from tkinter.scrolledtext import ScrolledText
from tkinter import messagebox
from anyio import create_task_group

from src.data_types import ReadConnectionStateChanged, SendingConnectionStateChanged, NicknameReceived
from src.custom_error import InvalidToken, TkAppClosed

from loguru import logger


def process_new_message(input_field, sending_queue):
    text = input_field.get()
    sending_queue.put_nowait(text)
    input_field.delete(0, tk.END)


async def update_tk(root_frame, interval=1 / 120):
    while True:
        try:
            root_frame.update()
        except tk.TclError:
            raise TkAppClosed()
        await asyncio.sleep(interval)


async def update_conversation_history(panel, messages_queue):
    while True:
        msg = await messages_queue.get()
        try:
            panel['state'] = 'normal'
        except tk.TclError:
            raise TkAppClosed()

        if panel.index('end-1c') != '1.0':
            panel.insert('end', '\n')
        panel.insert('end', msg)
        # TODO сделать промотку умной, чтобы не мешала просматривать историю сообщений
        # ScrolledText.frame
        # ScrolledText.vbar
        panel.yview(tk.END)
        panel['state'] = 'disabled'


async def update_status_panel(status_labels, status_updates_queue):
    nickname_label, read_label, write_label = status_labels

    read_label['text'] = f'Reading: no connection'
    write_label['text'] = f'Sending: no connection'
    nickname_label['text'] = f'Username: unknown'

    while True:
        msg = await status_updates_queue.get()
        if isinstance(msg, ReadConnectionStateChanged):
            read_label['text'] = f'Reading: {msg.value}'

        if isinstance(msg, SendingConnectionStateChanged):
            write_label['text'] = f'Sending: {msg.value}'

        if isinstance(msg, NicknameReceived):
            nickname_label['text'] = f'Username: {msg.nickname}'


def create_status_panel(root_frame):
    status_frame = tk.Frame(root_frame)
    status_frame.pack(side="bottom", fill=tk.X)

    connections_frame = tk.Frame(status_frame)
    connections_frame.pack(side="left")

    nickname_label = tk.Label(connections_frame, height=1, fg='grey', font='arial 10', anchor='w')
    nickname_label.pack(side="top", fill=tk.X)

    status_read_label = tk.Label(connections_frame, height=1, fg='grey', font='arial 10', anchor='w')
    status_read_label.pack(side="top", fill=tk.X)

    status_write_label = tk.Label(connections_frame, height=1, fg='grey', font='arial 10', anchor='w')
    status_write_label.pack(side="top", fill=tk.X)

    return nickname_label, status_read_label, status_write_label


async def show_exception_window(exception_queue):
    error_msg = await exception_queue.get()
    if error_msg:
        messagebox.showerror('Error', error_msg)
        raise InvalidToken


async def draw(messages_queue, sending_queue, status_updates_queue, exception_queue):
    root = tk.Tk()

    root.title('Minecraft chat')

    root_frame = tk.Frame()
    root_frame.pack(fill="both", expand=True)

    status_labels = create_status_panel(root_frame)

    input_frame = tk.Frame(root_frame)
    input_frame.pack(side="bottom", fill=tk.X)

    input_field = tk.Entry(input_frame)
    input_field.pack(side="left", fill=tk.X, expand=True)

    input_field.bind("<Return>", lambda event: process_new_message(input_field, sending_queue))

    send_button = tk.Button(input_frame)
    send_button["text"] = "Send"
    send_button["command"] = lambda: process_new_message(input_field, sending_queue)
    send_button.pack(side="left")

    conversation_panel = ScrolledText(root_frame, wrap='none')
    conversation_panel.pack(side="top", fill="both", expand=True)

    try:
        async with create_task_group() as tg:
            tg.start_soon(update_tk, root_frame)
            tg.start_soon(update_conversation_history, conversation_panel, messages_queue)
            tg.start_soon(update_status_panel, status_labels, status_updates_queue)
            tg.start_soon(show_exception_window, exception_queue)
    except TkAppClosed:
        logger.bind(
            module='gui',
            action='drawing_frame',
        ).error('Chat application was closed')
        raise TkAppClosed
