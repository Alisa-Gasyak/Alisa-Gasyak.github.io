def test_fib_1():
    gen = my_genn()
    assert gen.send(3) == [0, 1, 1], "Тривиальный случай n = 3, список [0, 1, 1]"

    
def test_fib_2():
    gen = my_genn()
    assert gen.send(5) == [0, 1, 1, 2, 3], "Пять первых членов ряда"

def test_my_genn():
    decorated_my_genn = fib_coroutine(my_genn)
    gen = decorated_my_genn()
    result = gen.send(8)
    print(f"gen.send(8) = {result}")
    assert result == [0, 1, 1, 2, 3, 5, 8, 13], "Восемь первых членов ряда"

def test_my_genn():
    decorated_my_genn = fib_coroutine(my_genn)
    gen = decorated_my_genn()
    result = gen.send(2)
    print(f"gen.send(2) = {result}")
    assert result == [0, 1], "Получение эллементов [0, 1]" 
