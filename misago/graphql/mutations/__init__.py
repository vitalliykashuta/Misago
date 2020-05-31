from .closethread import close_thread_mutation
from .closethreads import close_threads_mutation
from .deletethread import delete_thread_mutation
from .deletethreadreplies import delete_thread_replies_mutation
from .deletethreadreply import delete_thread_reply_mutation
from .deletethreads import delete_threads_mutation
from .editpost import edit_post_mutation
from .editthreadtitle import edit_thread_title_mutation
from .login import login_mutation
from .movethread import move_thread_mutation
from .movethreads import move_threads_mutation
from .postreply import post_reply_mutation
from .postthread import post_thread_mutation
from .register import register_mutation


mutations = [
    close_thread_mutation,
    close_threads_mutation,
    delete_thread_mutation,
    delete_thread_replies_mutation,
    delete_thread_reply_mutation,
    delete_threads_mutation,
    edit_post_mutation,
    edit_thread_title_mutation,
    login_mutation,
    move_thread_mutation,
    move_threads_mutation,
    post_reply_mutation,
    post_thread_mutation,
    register_mutation,
]