"""
Column schema and mapping helpers for EdNet V2.

This file does not read or process data.
It only defines how possible EdNet column names can be mapped into
the project format used by the Adaptive AI Tutor pipeline.
"""

from __future__ import annotations
# from __future__ import annotations satırı, Python'da henüz yazılmamış veya tanımlanmamış sınıfları/tipleri kod içinde rahatça referans gösterebilmenizi sağlar.
# Normalde Python, bir fonksiyonu tanımlarken kullandığınız veri tiplerini (örneğin def bul(x: list[str])) anında çözmeye çalışır. Ancak bu satırı eklediğinizde, tip ipuçları (type hints) birer kod parçası yerine basit birer metin (string) gibi davranır.


PROJECT_COLUMNS = [
    "student_id",
    "question_id",
    "timestamp",
    "tags",
    "elapsed_time",
    "is_correct",
]


OPTIONAL_COLUMNS = [
    "user_answer",
    "correct_answer",
]


COLUMN_ALIASES = {
    "student_id": [
        "student_id",
        "user_id",
        "user",
        "uid",
        "student",
    ],
    "question_id": [
        "question_id",
        "item_id",
        "problem_id",
        "content_id",
        "question",
    ],
    "timestamp": [
        "timestamp",
        "time",
        "created_at",
        "start_time",
        "datetime",
    ],
    "tags": [
        "tags",
        "tag",
        "skill",
        "skill_id",
        "knowledge_component",
        "concept",
        "category",
    ],
    "elapsed_time": [
        "elapsed_time",
        "elapsed_time_ms",
        "duration",
        "time_spent",
        "response_time",
        "solving_time",
    ],
    "is_correct": [
        "is_correct",
        "correct",
        "correctness",
        "answered_correctly",
        "is_answer_correct",
    ],
    "user_answer": [
        "user_answer",
        "answer",
        "student_answer",
        "selected_answer",
    ],
    "correct_answer": [
        "correct_answer",
        "answer_key",
        "correct_option",
        "solution",
    ],
}


# normalize_column_name(column_name): Sütun isimlerindeki boşlukları siler ve harfleri küçülterek isimleri standart bir formata getirir. Böylece büyük/küçük harf veya boşluk farklarından kaynaklanan eşleşme hatalarını önler.
def normalize_column_name(column_name: str) -> str:
    return column_name.lower().strip()


# find_matching_column(columns, target_column): Gelen veri setindeki sütun listesi içinde, projenin aradığı hedef sütunun alternatif bir isminin (alias) olup olmadığını kontrol eder. Eşleşen bir isim bulursa veri setindeki orijinal sütun adını döndürür.
def find_matching_column(columns: list[str], target_column: str) -> str | None:
    normalized_columns = {
        normalize_column_name(column): columns
        for column in columns
    }

    # aliases, aranan sütunun COLUMN_ALIASES içinde tanımlanmış alternatif isimler (takma adlar) listesidir.
    # Örneğin, hedef "student_id" ise, aliases listesi ["user_id", "userID", "student_no"] gibi varyasyonları içerir ve veri setinde bu isimlerden biri var mı diye kontrol edilir.
    aliases = COLUMN_ALIASES.get(target_column, [])

    for alias in aliases:
        normalized_alias = normalize_column_name(alias)

        if normalized_alias in normalized_columns:
            return normalized_columns[normalized_alias]
        
    return None


# build_column_mapping(columns): Projenin ihtiyaç duyduğu tüm zorunlu ve isteğe bağlı sütunlar için yukarıdaki find_matching_column fonksiyonunu çalıştırır. Sonuç olarak hangi proje sütununun veri setindeki hangi sütuna denk geldiğini gösteren bir haritalama (sözlük) oluşturur.
def build_column_mapping(columns: list[str]) -> dict[str, str | None]:
    mapping = {}

    for project_column in PROJECT_COLUMNS + OPTIONAL_COLUMNS:
        mapping[project_column] = find_matching_column(
            columns=columns,
            target_column=project_column
        )

    return mapping



# missing_required_columns(mapping): Hazırlanan haritalamayı kontrol ederek projenin çalışması için mutlaka bulunması gereken zorunlu sütunlardan (PROJECT_COLUMNS) hangilerinin veri setinde eksik olduğunu tespit eder ve bir liste olarak döndürür.
def missing_required_columns(mapping: dict[str, str | None]) -> list[str]:

    return [
        column
        for column in PROJECT_COLUMNS
        if mapping.get(column) is None
    ]


def print_schema_mapping(mapping: dict[str, str | None]) -> None:
    print("EdNet column mapping:")
    print("-" * 60)

    for project_column, real_column in mapping.items():
        if real_column is None:
            print(f"{project_column:20s} -> NOT FOUND")
        else:
            print(f"{project_column:20s} -> {real_column}")


if __name__ == "__main__":
    example_columns = [
        "user_id",
        "question_id",
        "timestamp",
        "skill_id",
        "elapsed_time",
        "correct",
    ]

    example_mapping = build_column_mapping(example_columns)
    print_schema_mapping(example_mapping)

    missing = missing_required_columns(example_mapping)

    if missing:
        print("\nMissing required columns:")
        for column in missing:
            print(f"- {column}")
    else:
        print("\nAll required columns were found.")