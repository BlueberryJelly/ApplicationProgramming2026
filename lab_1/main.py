from src.get_data import get_data
from src.name_frequency import frequency


def main() -> None:
    text = get_data()

    result = sorted(frequency(text).items(), key=lambda item: item[1], reverse=True)

    if not result:
        print("Среди данных анкетируемых нет имён.")
        return

    max_count = result[0][1]

    for name, count in result:
        if count == max_count:
            print(f"{name}: {count}")
        else:
            break

    return


if __name__ == "__main__":
    main()
