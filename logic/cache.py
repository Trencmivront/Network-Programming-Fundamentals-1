frame_list = []

# Here I decided to implement pop-push operations of queue
# being performed at the end of list instead of head

def pop():
    length = len(frame_list)
    if(length > 0):
        frame_list.pop(length - 1)

def push(value):
    frame_list.append(value)

def get_last_frame():
    """ 
    Returns the last frame from list.

    Pop the last used frame before using this function. """
    length = len(frame_list)
    if(length > 0):
        return frame_list[length - 1]
