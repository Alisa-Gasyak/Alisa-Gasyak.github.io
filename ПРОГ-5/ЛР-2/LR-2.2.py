import functools
from itertools import islice

class FibonacchiLst:
    
    
    def __init__(self, lst):
        """
        Инициализация с входным списком
        :param lst: список чисел для фильтрации
        """
        self.lst = lst
        self.index = 0
        
        
        max_val = max(lst) if lst else 0
        self.fib_numbers = set()
        
        a = 0
        b = 1
        while a <= max_val:
            self.fib_numbers.add(a)
            a,b = b, a + b
    
    def __iter__(self):
        """Функция для возвращения итератора"""
        self.index = 0
        return self
    
    def __next__(self):
        """Возвращение следующего числа Фибоначчи из списка"""
        while self.index < len(self.lst):
            current = self.lst[self.index]
            self.index += 1
            if current in self.fib_numbers:
                return current
        raise StopIteration
        
    def get_all_fib_numbers(self):
        """Возвращает все числа Фибоначчи из списка"""
        return [x for x in self.lst if x in self.fib_numbers]


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
    """Сопрограмма"""
    while True:
        number_of_fib_elem = yield
        print(f"Получено: {number_of_fib_elem}")
        
       
        gen = fib_elem_gen()
        fib_list = list(islice(gen, number_of_fib_elem))
        
        fib_filter = FibonacchiLst(fib_list)
        filtered_result = list(fib_filter)
               
        l = [f"{number_of_fib_elem}:"] + filtered_result
        yield l


def fib_coroutine(g):
    @functools.wraps(g)
    def inner(*args, **kwargs):
        gen = g(*args, **kwargs)
        gen.send(None)
        return gen
    return inner



def main():
   
    
    
    lst = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 1]
    fib_filter = FibonacchiLst(lst)
    
    print(f"{lst}")
    print(f"{list(fib_filter)}")
    
if __name__ == "__main__":
    main()