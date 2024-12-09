class TreeNode {
    constructor(value, left=null, right=null) {
        this.value = value;
        this.left = left;
        this.right = right;
    }
}

function buildTreeFromString(treeStr) {
    if (!treeStr || treeStr === "") {
        return null;
    }

    // Используем стек для хранения узлов и их уровней вложенности
    const stack = [];
    let currentNode = null;

    for (const char of treeStr) {
        if (/^\d$/.test(char)) {
            const val = parseInt(char);
            const node = new TreeNode(val);

            if (currentNode === null) {
                currentNode = node;
            } else {
                if (currentNode.left === null) {
                    currentNode.left = node;
                } else if (currentNode.right === null) {
                    currentNode.right = node;
                }
            }

            stack.push(currentNode);
            currentNode = node;
        } else if (char === '(') {
            continue;
        } else if (char === ',') {
            currentNode = stack[stack.length - 1];
        } else if (char === ')') {
            stack.pop();
            if (stack.length > 0) {
                currentNode = stack[stack.length - 1];
            }
        }
    }

    // Возвращаем корень дерева
    return stack[0];
}

function nonRecursivePreOrderTraversal(root) {
    if (root === null) {
        return ""; // Если переданный корень дерева равен null, значит, дерево пусто, и функция сразу возвращает пустую строку
    }

    const result = []; // Создаётся пустой массив result для хранения значений узлов в порядке обхода
    const stack = [root]; // Создаётся стек, куда изначально кладётся корень дерева

    while (stack.length > 0) {
        const currentNode = stack.pop(); // Извлечение верхнего элемента из стека и сохранение его в переменную currentNode
        result.push(currentNode.value); // Добавление значения текущего узла в массив результатов

        if (currentNode.right !== null) {
            stack.push(currentNode.right); // Если у текущего узла есть правый потомок, он добавляется в стек
        }
        if (currentNode.left !== null) {
            stack.push(currentNode.left); // Проверяется наличие левого потомка, и если он существует, тоже добавляется в стек
        }
    }

    return result.join(' ');
}

// Пример использования
const treeStr = "8(3(1, 6(4, 7)))";
const root = buildTreeFromString(treeStr);
const traversalResult = nonRecursivePreOrderTraversal(root);
console.log(traversalResult);  // Вывод: "8 3 1 6 4 7"