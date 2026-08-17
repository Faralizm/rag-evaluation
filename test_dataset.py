"""
RAG pipeline-ini test etmək üçün 15-20 sual/gözlənilən-cavab cütündən ibarət test dəsti.
Kateqoriyalar: normal (adi suallar) və edge (kənar hallar).
"""

TEST_DATASET = [
    {"id": 1, "category": "normal", "question": "Bu sənəd nə haqqındadır?", "expected_answer": "Sənədin əsas mövzusu"},
    {"id": 2, "category": "normal", "question": "Sənəddəki əsas anlayış nədir?", "expected_answer": "Konkret termin"},
    {"id": 3, "category": "normal", "question": "Sənəddə hansı üsul/metod izah olunur?", "expected_answer": "Konkret metod adı"},
    {"id": 4, "category": "normal", "question": "Sənədin nəticəsi/xülasəsi nədir?", "expected_answer": "Xülasə hissəsi"},
    {"id": 5, "category": "normal", "question": "Sənəddə neçə əsas hissə/bölmə var?", "expected_answer": "Bölmə sayı"},
    {"id": 6, "category": "normal", "question": "Sənəddə qeyd olunan tarix/rəqəm hansıdır?", "expected_answer": "Konkret rəqəm"},
    {"id": 7, "category": "normal", "question": "Sənəddə kim/nə haqqında bəhs olunur?", "expected_answer": "Əsas subyekt"},
    {"id": 8, "category": "normal", "question": "Sənəddəki əsas tövsiyə nədir?", "expected_answer": "Tövsiyə mətni"},
    {"id": 9, "category": "normal", "question": "Sənəddə hansı problem müzakirə olunur?", "expected_answer": "Problem təsviri"},
    {"id": 10, "category": "normal", "question": "Sənədin son bölməsində nə deyilir?", "expected_answer": "Son bölmə məzmunu"},
    {"id": 11, "category": "edge", "question": "Marsda həyat formaları varmı və bu sənəddə bundan bəhs olunurmu?", "expected_answer": "Bu sual sənədlərdə cavablandırılmır"},
    {"id": 12, "category": "edge", "question": "", "expected_answer": "Sistem aydınlaşdırma tələb etməlidir"},
    {"id": 13, "category": "edge", "question": "asdkjaslkdjaslkdj??? nə???", "expected_answer": "Sistem uydurma cavab verməməlidir"},
    {"id": 14, "category": "edge", "question": "Sənəddə A haqqında nə deyilir, sonra bunu B ilə müqayisə et?", "expected_answer": "Hər iki hissəyə cavab verilməlidir"},
    {"id": 15, "category": "edge", "question": "Sənəd deyir ki, X həmişə doğrudur, elə deyilmi?", "expected_answer": "Sistem presuppozisiyanı qəbul etməməlidir"},
    {"id": 16, "category": "edge", "question": "Bu sənədin əksinə olaraq nə deyilir?", "expected_answer": "Sənəddə əks fikir yoxdursa, bunu bildirməlidir"},
    {"id": 17, "category": "edge", "question": "Sənəddəki 100-cü səhifədə nə yazılıb?", "expected_answer": "Sənəddə bu qədər səhifə yoxdursa, bunu bildirməlidir"},
]

if __name__ == "__main__":
    normal_count = sum(1 for item in TEST_DATASET if item["category"] == "normal")
    edge_count = sum(1 for item in TEST_DATASET if item["category"] == "edge")

    print(f"Ümumi sual sayı: {len(TEST_DATASET)}")
    print(f"Normal suallar: {normal_count}")
    print(f"Kənar hallar (edge cases): {edge_count}")

    for item in TEST_DATASET:
        print(f"\n[{item['category']}] #{item['id']}: {item['question']}")
        print(f"  Gözlənilən: {item['expected_answer']}")