const fs = require('fs/promises'); // Импорт модуля для асинхронного чтения/записи файлов
const crypto = require('crypto'); // Импорт модуля для криптографических операций (хеширование)

// Класс для узла в связном списке
class Node {
  constructor(word) {
    this.word = word; // Данные узла (слово)
    this.next = null; // Указатель на следующий узел
  }
}

// Класс для связного списка
class LinkedList {
  constructor() {
    this.head = null; // Указатель на первый узел списка
  }

  add(word) { // Добавление нового слова в список
    const newNode = new Node(word);
    if (!this.head) {
      this.head = newNode; // Если список пуст, новый узел становится первым
    } else {
      let current = this.head;
      while (current.next) { // Иначе, идем до конца списка
        current = current.next;
      }
      current.next = newNode; // Добавляем новый узел в конец
    }
  }

  toArray() { // Преобразование списка в массив
    const arr = [];
    let current = this.head;
    while (current) {
      arr.push(current.word);
      current = current.next;
    }
    return arr;
  }
}

async function main() {
    try {
        const inputFilePath = process.argv[2]; // Получение пути к входному файлу из аргументов командной строки
        if (!inputFilePath) {
            console.error("Укажите путь к входному файлу.");
            return;
        }
        const text = await fs.readFile(inputFilePath, 'utf8'); // Асинхронное чтение файла в кодировке UTF8
        const words = text.toLowerCase().match(/\b\w+\b/g); // Разбиение текста на слова с помощью регулярного выражения, приведение к нижнему регистру
        const tableSize = 100; // Размер хеш-таблицы
        const hashTable = new Array(tableSize).fill(null).map(() => new LinkedList()); // Создание хеш-таблицы: массив связных списков

        for (const word of words) { // Цикл по каждому слову
            const hash = crypto.createHash('sha256').update(word).digest('hex'); // Вычисление SHA256 хеша слова
            const index = parseInt(hash, 16) % tableSize; // Вычисление индекса в хеш-таблице (остаток от деления на размер таблицы)
            hashTable[index].add(word); // Добавление слова в соответствующий список в хеш-таблице
        }

        const outputFilePath = 'hash_table.json'; // Путь к выходному JSON файлу
        const tableData = hashTable.map(list => list.toArray()); // Преобразование связных списков в массивы для сериализации в JSON
        await fs.writeFile(outputFilePath, JSON.stringify(tableData, null, 2)); // Асинхронная запись JSON данных в файл
        console.log(`Хеш-таблица записана в файл: ${outputFilePath}`);
    } catch (error) {
        console.error("Ошибка:", error); // Обработка ошибок
    }
}


main(); // Запуск основной функции