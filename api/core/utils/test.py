from core.utils.redis_queue import RedisQueue

def test_redis_queue():
    q = RedisQueue(name="class_1234")

    q.add_task({"slide": 1, "highlight": "Intro to AI"})
    print(q.peek_all())
    q.add_task({"slide": 2, "highlight": "Neural Networks"})
    print(q.peek_all())
    q.add_priority_task({"slide": 0, "highlight": "Welcome!"})
    print(q.peek_all())
    cur_task = q.get_task()
    print(cur_task)
    print(q.peek_all())
    q.clear_queue()
    print(q.peek_all())

def test_core_utils():
    test_redis_queue()