
def gen_bin_tree(height: int, root: int, left_leaf, right_leaf) -> dict:
    roots = [[root]] #Инициализация корней

    for leaf in range(height - 1): #Генерация уровней дерева
        if (len(roots) == 1):
            r = roots[0]  
        else:

            r = [item for s in roots[-1] for item in s]

        leaves = list( 
            map(
                lambda root_value:
                [left_leaf(root_value),
                 right_leaf(root_value)], r)) #Генерация листьев

        roots.append(leaves) #Добавление нового уровня в корни

    roots.reverse()

    roots[-1] = [roots[-1]] #Формирование начального уровня дерева
    roots[0] = list(map(lambda x: [{
        str(x[0]): []
    }, {
        str(x[1]): []
    }], roots[0]))

    for i in range(height - 1): #Заполнение дерева
        sublist = roots[i]
        for j in range(len(sublist)):
            x = sublist.pop()
            roots[i + 1][j // 2][j % 2] = {str(roots[i + 1][j // 2][j % 2]): x}
    tree = roots[-1][0][0]

    return tree


if __name__ == '__main__':
    print(gen_bin_tree(2, 5, lambda x: x + 3, lambda x: x * 2))


