import random, string

user_ids = list(range(1, 101))
recipient_ids = list(range(1, 101))

def generate_message(node_topic) -> dict:
    random_user_id = random.choice(user_ids)
    recipient_ids_copy = recipient_ids.copy()
    recipient_ids_copy.remove(random_user_id)
    random_recipient_id = random.choice(recipient_ids_copy)
    message = ''.join(random.choice(string.ascii_letters) for i in range(32))
    return {
        'node': node_topic,
        'user_id': random_user_id,
        'recipient_id': random_recipient_id,
        'message': message
    }
