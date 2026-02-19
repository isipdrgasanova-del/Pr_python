let expenses = [];

function generateId() {
    return Date.now() + Math.floor(Math.random() * 1000);
}

function validateInput(title, amount, category) {
    if (!title || title.trim() === '') return { valid: false, error: 'Название не может быть пустым' };
    if (!amount || isNaN(amount) || amount <= 0) return { valid: false, error: 'Сумма должна быть положительным числом' };
    if (!category || category.trim() === '') return { valid: false, error: 'Категория не может быть пустой' };
    return { valid: true };
}

function addExpense(title, amount, category) {
    const validation = validateInput(title, amount, category);
    if (!validation.valid) {
        console.error('Ошибка:', validation.error);
        return null;
    }

    const expense = {
        id: generateId(),
        title: title.trim(),
        amount: parseFloat(amount),
        category: category.trim()
    };
    
    expenses.push(expense);
    console.log('Расход добавлен:', expense);
    return expense;
}

function printAllExpenses() {
    console.log('\nВСЕ РАСХОДЫ:');
    if (expenses.length === 0) {
        console.log('Расходов нет');
    } else {
        expenses.forEach(e => console.log(`${e.id} | ${e.title} | ${e.amount}₽ | ${e.category}`));
    }
}

function getTotalAmount() {
    const total = expenses.reduce((sum, e) => sum + e.amount, 0);
    console.log(`Общая сумма: ${total}₽`);
    console.log('Чек:', { 
        дата: new Date().toLocaleString(), 
        сумма: total, 
        количество: expenses.length,
        расходы: expenses.map(e => ({ название: e.title, сумма: e.amount, категория: e.category }))
    });
    return total;
}

function getExpensesByCategory(category) {
    const filtered = expenses.filter(e => e.category.toLowerCase() === category.toLowerCase());
    const total = filtered.reduce((sum, e) => sum + e.amount, 0);
    
    console.log(`\nРАСХОДЫ НА "${category}":`);
    filtered.forEach(e => console.log(`${e.title}: ${e.amount}₽`));
    console.log(`Всего: ${total}₽`);
    
    return { expenses: filtered, total };
}

function findExpenseByTitle(searchString) {
    const found = expenses.find(e => e.title.toLowerCase().includes(searchString.toLowerCase()));
    
    if (found) {
        console.log('Найдено:', found);
        const addExtra = confirm('Добавить комментарий?');
        if (addExtra) {
            const comment = prompt('Введите комментарий:');
            if (comment) {
                found.comment = comment;
                console.log('Комментарий добавлен:', found);
            }
        }
    } else {
        console.log('Ничего не найдено');
    }
    
    return found;
}

const expenseTracker = {
    expenses: expenses,
    currentIndex: 0,
    
    next() {
        if (this.expenses.length === 0) return console.log('Нет расходов');
        this.currentIndex = (this.currentIndex + 1) % this.expenses.length;
        console.log('Текущий:', this.expenses[this.currentIndex]);
    },
    
    previous() {
        if (this.expenses.length === 0) return console.log('Нет расходов');
        this.currentIndex = (this.currentIndex - 1 + this.expenses.length) % this.expenses.length;
        console.log('Текущий:', this.expenses[this.currentIndex]);
    },
    
    addExpense: addExpense,
    getTotalAmount: getTotalAmount,
    getExpensesByCategory: getExpensesByCategory,
    findExpenseByTitle: findExpenseByTitle,
    
    deleteExpenseById(id) {
        const index = this.expenses.findIndex(e => e.id === id);
        if (index === -1) return console.log('ID не найден');
        const deleted = this.expenses.splice(index, 1)[0];
        console.log('Удалено:', deleted);
        return true;
    },
    
    getCategoryStatistics() {
        const stats = {};
        expenses.forEach(e => {
            if (!stats[e.category]) stats[e.category] = { count: 0, total: 0 };
            stats[e.category].count++;
            stats[e.category].total += e.amount;
        });
        
        console.log('\nСТАТИСТИКА:');
        let total = 0;
        for (let cat in stats) {
            console.log(`${cat}: ${stats[cat].count} шт., ${stats[cat].total}₽`);
            total += stats[cat].total;
        }
        console.log(`ИТОГО: ${total}₽`);
        return stats;
    }
};

function runAllExamples() {
    console.clear();
     
    addExpense('Обед', 500, 'Еда');
    addExpense('Тройллебус', 85, 'Транспорт');
    addExpense('Продукты', 1500, 'Еда');
    addExpense('Кино', 400, 'Развлечения');
    
    printAllExpenses();
    getTotalAmount();
    getExpensesByCategory('Еда');
    expenseTracker.getCategoryStatistics();
    
    if (expenses.length > 0) {
        expenseTracker.deleteExpenseById(expenses[0].id);
        printAllExpenses();
    }
    
    console.log('Готово! Используйте функции в консоли.');
}