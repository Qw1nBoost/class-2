class TreeNode { // Создаем класс узла дерева, который содержит значение и ссылки на левого и правого потомков
    constructor(value, left=null, right=null) {
        this.value = value;
        this.left = left;
        this.right = right;
    }
}

// Парсинг строки и создание дерева
function buildTreeFromString(treeStr) { // функция для парсинга строки в формате линейно-скобочной записи и для построения соответствующего бинарного дерева
    if (!treeStr || treeStr === "") {
        return null;
    }

    // Используем стек для хранения узлов и их уровней вложенности
    const stack = []; //  Создаем пустой стек для отслеживания уровня вложенности и устанавливаем начальный узел равным null
    let currentNode = null;

    for (const char of treeStr) { // Проходим по каждому символу строки
        if (/^\d$/.test(char)) { // Проверяем, является ли текущий символ цифрой
            const val = parseInt(char); // Преобразуем её в целое число
            const node = new TreeNode(val); // Создаем новый узел

            if (currentNode === null) {
                currentNode = node; // Если текущий узел еще не был инициализирован, делаем его корневым узлом
            } else { // Добавляем новый узел либо как левое, либо как правое поддерево текущего узла
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
        } else if (char === ',') { // Запятая указывает на переход к новому дочернему узлу, мы восстанавливаем предыдущий уровень вложенности, извлекая последний узел из стека
            currentNode = stack[stack.length - 1];
        } else if (char === ')') { // Закрывающая скобка означает завершение обработки одного уровня вложенности.
            stack.pop();           // Удаляем верхний элемент из стека и восстанавливаем текущий узел, если стек ещё не пуст.
            if (stack.length > 0) {
                currentNode = stack[stack.length - 1];
            }
        }
    }

    return stack[0]; // возвращается первый элемент стека
}

// Прямой обход
function preOrder(node) {
    if (node !== null) { // Обход выполняется в следующем порядке: корень, левый потомок, правый потомок.
        process.stdout.write(`${node.value} `);
        preOrder(node.left);
        preOrder(node.right);
    }
}

// Центральный обход
function inOrder(node) { // Обход выполняется в следующем порядке: левый потомок, корень, правый потомок
    if (node !== null) {
        inOrder(node.left);
        process.stdout.write(`${node.value} `);
        inOrder(node.right);
    }
}

// Концевой обход
function postOrder(node) { // Обход выполняется в следующем порядке: левый потомок, правый потомок, корень.
    if (node !== null) {
        postOrder(node.left);
        postOrder(node.right);
        process.stdout.write(`${node.value} `);
    }
}

const treeStr = "8(3(1, 6(4, 7)))";
const root = buildTreeFromString(treeStr);

console.log("Прямой обход:");
preOrder(root);
console.log("\nЦентральный обход:");
inOrder(root);
console.log("\nКонцевой обход:");
postOrder(root);