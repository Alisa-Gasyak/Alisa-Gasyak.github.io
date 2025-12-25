import functools
from itertools import islice


def fib_elem_gen():
    """Генератор, возвращающий элементы ряда Фибоначчи"""
    a = 0
    b = 1

    while True:
        yield a
        res = a + b
        a = b
        b = res


def my_genn():
    """Сопрограмма, возвращающая список элементов ряда Фибоначчи"""
    while True:
        number_of_fib_elem = yield
        
        if number_of_fib_elem <= 0:
            result = []
        else: # Генерируем нужное количество чисел Фибоначчи
            gen = fib_elem_gen()
            result = list(islice(gen, number_of_fib_elem))
        
        yield result


def fib_coroutine(g):
    @functools.wraps(g)
    def inner(*args, **kwargs):
        gen = g(*args, **kwargs)
        gen.send(None)
        return gen
    return inner


def main():
    
    decorated_my_genn = fib_coroutine(my_genn)
    gen = decorated_my_genn()
    
    print(f"gen.send(3) = {gen.send(3)}")
    next(gen)
    
    print(f"gen.send(5) = {gen.send(5)}")
    next(gen)
    
    print(f"gen.send(8) = {gen.send(8)}")
    next(gen)

if __name__ == "__main__":
    main()