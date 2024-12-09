const fs = require('fs'); // Модуль для работы с файловой системой
const readline = require('readline'); //Для построчного чтения файла


// Хеш-функция (простая, для демонстрации)
function simpleHash(str) {
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    hash = (hash << 5) - hash + str.charCodeAt(i);
    hash |= 0; // Используется для обеспечения 32-битного целого числа
  }
  return Math.abs(hash); // Возвращает абсолютное значение, чтобы избежать отрицательных чисел
}

// Асинхронная функция для чтения файла построчно
const readFile = async (filepath) => {
    const fileStream = fs.createReadStream(filepath);
    const rl = readline.createInterface({ input: fileStream, crlfDelay: Infinity});

    const lines = [];
    for await (const line of rl){
        lines.push(line);
    }
    return lines.join('\n');
};


async function main() {
    try {
        const inputFilePath = process.argv[2]; // путь к входному файлу передается как аргумент командной строки
        if (!inputFilePath) {
            console.error("Укажите путь к входному файлу.");
            return;
        }
        const text = await readFile(inputFilePath); // асинхронное чтение файла
        const words = text.toLowerCase().match(/\b\w+\b/g); // Разделение текста на слова, игнорируя знаки пунктуации и приводя к нижнему регистру
        const tableSize = 100; // Размер хеш-таблицы
        const hashTable = new Array(tableSize).fill(null).map(() => []); // Создание хеш-таблицы с помощью массива массивов (для обработки коллизий методом цепочек)

        if (words) { // проверка, были ли найдены слова в тексте (файл мог быть пустым)
          for (const word of words) {
            const hash = simpleHash(word) % tableSize; // Вычисление хеш-кода и получение индекса в таблице
            hashTable[hash].push(word); // Добавление слова в хеш-таблицу
          }

          const outputFilePath = 'hash_table.txt'; // Путь к выходному файлу
          const tableString = JSON.stringify(hashTable, null, 2); // Преобразование хеш-таблицы в JSON-строку с отступами для читаемости

          fs.writeFileSync(outputFilePath, tableString); // Запись JSON-строки в файл
          console.log(`Хеш-таблица записана в файл: ${outputFilePath}`);
        } else {
          console.log("Файл пустой или не содержит текста.");
        }
    } catch (error) {
        console.error("Ошибка:", error); // Обработка ошибок (например, файл не найден)
    }
}


main();
