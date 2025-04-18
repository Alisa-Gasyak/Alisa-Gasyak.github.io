def gen_bin_tree_nonerec(height: int, root: int, left_leaf, right_leaf) -> dict:
    if height < 1:
        return {}

    
    tree = {str(root): []}
    queue = [(tree, root)]  # Список для хранения узлов и их значений для обработки в очереди

    current_height = 1

    while current_height < height:
        # Обрабатываем текущий уровень
        next_level = []
        
        for node, value in queue:
            # Генерируем значения для левого и правого ответвления
            left_value = left_leaf(value)
            right_value = right_leaf(value)

            # Создаем левого и правого ответвления и добавляем их в узел
            left_node = {str(left_value): []}
            right_node = {str(right_value): []}
            node[str(value)].append(left_node)
            node[str(value)].append(right_node)

            # Добавляем потомков в очередь для дальнейшей обработки
            next_level.append((left_node, left_value))
            next_level.append((right_node, right_value))

        # Обновляем очередь на следующий уровень
        queue = next_level
        current_height += 1

    return tree


if __name__ == '__main__':
    result = gen_bin_tree_nonerec(2, 5, lambda x: x + 3, lambda x: x * 2)
    print(result)