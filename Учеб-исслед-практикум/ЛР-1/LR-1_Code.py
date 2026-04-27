import re
import os
from collections import Counter
from typing import Dict, List, Tuple

class TextAnalyzer:
    """Main class for text analysis providing various statistical methods."""
    
    def __init__(self, text: str):
        """
        Initialize analyzer with input text.
        
        Args:
            text (str): Raw text to analyze
        """
        self.original_text = text
        self.text = text.strip()
        
    # Базовые методы (анализ, синтез) 
    
    def count_characters(self, include_spaces: bool = True) -> int:
        """
        Count total characters in text.
        
        Args:
            include_spaces (bool): If True, count spaces; if False, exclude them
            
        Returns:
            int: Character count
        """
        if include_spaces:
            return len(self.text)
        else:
            return len(self.text.replace(" ", ""))
    
    def count_words(self) -> int:
        """Count words in text."""
        if not self.text:
            return 0
        words = re.findall(r'\b\w+\b', self.text.lower())
        return len(words)
    
    def count_sentences(self) -> int:
        """
        Count sentences in text.
        Uses punctuation markers: . ! ?
        """
        sentences = re.split(r'[.!?]+', self.text)
        # Filter out empty strings
        sentences = [s for s in sentences if s.strip()]
        return len(sentences)
    
    # Расширенная аналитика (моделирование)
    
    def get_word_frequency(self, top_n: int = None) -> Dict[str, int]:
        """
        Calculate frequency of each word using induction.
        
        Args:
            top_n (int, optional): Return only top N words
            
        Returns:
            Dict[str, int]: Word -> frequency mapping
        """
        words = re.findall(r'\b\w+\b', self.text.lower())
        freq = Counter(words)
        
        if top_n:
            return dict(freq.most_common(top_n))
        return dict(freq)
    
    def get_top_words(self, n: int = 5) -> List[Tuple[str, int]]:
        """Return top N most frequent words."""
        words = re.findall(r'\b\w+\b', self.text.lower())
        return Counter(words).most_common(n)
    
    def avg_word_length(self) -> float:
        """Calculate average length of words."""
        words = re.findall(r'\b\w+\b', self.text)
        if not words:
            return 0.0
        total_length = sum(len(word) for word in words)
        return round(total_length / len(words), 2)
    
    def flesch_kincaid_grade(self) -> float:
        """
        Calculate Flesch-Kincaid Grade Level (readability index).
        Formula: 0.39 * (words/sentences) + 11.8 * (syllables/words) - 15.59
        Simplified: English is complex, using approximate syllable count.
        
        Returns:
            float: Grade level (US school grade)
        """
        word_count = self.count_words()
        sentence_count = self.count_sentences()
        
        if sentence_count == 0:
            return 0.0
            
        words_per_sentence = word_count / sentence_count
        
        # Simple syllable approximation: count vowel groups
        def count_syllables(word: str) -> int:
            word = word.lower()
            vowels = 'aeiou'
            count = 0
            prev_was_vowel = False
            for char in word:
                is_vowel = char in vowels
                if is_vowel and not prev_was_vowel:
                    count += 1
                prev_was_vowel = is_vowel
            return max(1, count)  # Every word has at least 1 syllable
        
        syllables = sum(count_syllables(word) for word in re.findall(r'\b\w+\b', self.text))
        syllables_per_word = syllables / word_count if word_count > 0 else 0
        
        # Flesch-Kincaid Grade Level formula
        grade = 0.39 * words_per_sentence + 11.8 * syllables_per_word - 15.59
        return round(grade, 2)
    
    # Обработка ошибок и вывод  
    
    def full_report(self) -> None:
        """
        Generate complete formatted report using synthesis of all methods.
        """
        print("\n" + "=" * 60)
        print("АНАЛИЗ ТЕКСТА — ПОЛНЫЙ ОТЧЁТ".center(60))
        print("=" * 60)
        
        # Section 1: Basic statistics
        print("\n ОСНОВНЫЕ МЕТРИКИ")
        print("-" * 40)
        print(f"  Символов (с пробелами):      {self.count_characters(include_spaces=True)}")
        print(f"  Символов (без пробелов):     {self.count_characters(include_spaces=False)}")
        print(f"  Слов:                        {self.count_words()}")
        print(f"  Предложений:                 {self.count_sentences()}")
        
        # Section 2: Word analysis
        print("\n АНАЛИЗ СЛОВ")
        print("-" * 40)
        print(f"  Средняя длина слова:         {self.avg_word_length()} симв.")
        print(f"  Топ-5 слов по частоте:")
        top_words = self.get_top_words(5)
        for i, (word, count) in enumerate(top_words, 1):
            print(f"      {i}. '{word}' — {count} раз(а)")
        
        # Section 3: Readability
        print("\n УДОБОЧИТАЕМОСТЬ (Индекс Флеша-Кинкейда)")
        print("-" * 40)
        grade = self.flesch_kincaid_grade()
        print(f"  Уровень образования (US grade): {grade}")
        if grade <= 5:
            print("  Очень легко читать (начальная школа)")
        elif grade <= 8:
            print("  Легко читать (средняя школа)")
        elif grade <= 12:
            print("  Средне (старшая школа)")
        else:
            print("  Сложно (университетский уровень)")
        
        print("\n" + "=" * 60)


def read_text_from_file(filepath: str) -> str:
    """
    Read text from file with error handling (experiment method).
    
    Args:
        filepath (str): Path to file
        
    Returns:
        str: File content or error message
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return f" Ошибка: Файл '{filepath}' не найден."
    except Exception as e:
        return f" Ошибка: {str(e)}"


def main():
    """Main entry point for the console application."""
    print("\n" + " ТЕКСТОВЫЙ АНАЛИЗАТОР v1.0".center(60))
    print("─" * 60)
    print("\nВыберите источник текста:")
    print("  1. Ввести текст вручную")
    print("  2. Загрузить из файла")
    
    choice = input("\nВаш выбор (1 или 2): ").strip()
    
    text = ""
    
    if choice == '1':
        print("\nВведите текст (для завершения нажмите Enter):")
        lines = []
        while True:
            line = input()
            if line == "":
                break
            lines.append(line)
        text = "\n".join(lines)
    
    elif choice == '2':
        filepath = input("Введите путь к файлу: ").strip()
        text = read_text_from_file(filepath)
        if text.startswith(""):
            print(text)
            return
    
    else:
        print("Неверный выбор. Используйте опции 1 или 2.")
        return
    
    if not text or not text.strip():
        print("Текст не может быть пустым.")
        return
    
    # Создаём анализатор и генерируем отчёт
    analyzer = TextAnalyzer(text)
    analyzer.full_report()


if __name__ == "__main__":
    main()