import random


class Wordle:
    def __init__(self, player_name):
        f = open("C:/Users/docto/PycharmProjects/source/guess.csv", 'r')
        self.words = f.read().replace("\"", "").split(",")
        f = open("C:/Users/docto/PycharmProjects/source/words.csv", 'r')
        self.all_words = f.read().replace("\"", "").split(",") + self.words
        self.player_name = player_name
        self.main()

    def comparator(self, guess, answer):
        if guess not in self.all_words:
            return "No such word! Try Again."

        status = []
        for idx, char in enumerate(guess):
            if char in answer:
                if char == answer[idx]:
                    status.append(True)
                else:
                    status.append(False)
            else:
                status.append(None)

        if None not in status and False not in status:
            return "congratulations!"

        return status

    @staticmethod
    def update_status(user_input: str, guess: list, status: dict):
        for idx, char in enumerate(user_input):
            if guess[idx]:
                if char not in status['answer']:
                    status['answer'][idx] = char
                    if char in status['in_but_wrong_spot']:
                        status['in_but_wrong_spot'].remove(char)
            elif guess[idx] is None:
                if char not in status['not_in']:
                    status['not_in'].append(char)
            else:
                if char not in status['in_but_wrong_spot'] and char not in status['answer']:
                    status['in_but_wrong_spot'].append(char)

        status['in_but_wrong_spot'] = sorted(status['in_but_wrong_spot'])
        status['not_in'] = sorted(status['not_in'])

    def main(self):
        answer = random.choice(self.words)
        status = {'answer': [' '] * 5, 'in_but_wrong_spot': [], 'not_in': []}
        count = 1

        while count < 7:
            print(f"-----#{count}-----")
            print(status)
            user_input = input("Enter your guess(if you need any help enter \"help\"): ")

            if user_input == 'help':
                Helper(self.all_words, status)
                continue

            guess = self.comparator(user_input, answer)

            if guess == "congratulations!":
                print(guess, self.player_name, ". your attempt:", count)
                break
            elif guess == "No such word! Try Again.":
                print(guess)
                continue

            print(guess)
            self.update_status(user_input, guess, status)
            count += 1

        print('The answer is', answer)


class Helper:
    def __init__(self, words, status):
        self.words = words
        self.status = status
        self.main()

    @staticmethod
    def exclude_filter(letters, word):
        return False if any([True if letter in word else False for letter in letters]) else True

    @staticmethod
    def include_filter(letters, word):
        return False if any([False if letter in word else True for letter in letters]) else True

    def manual(self, starts_with, ends_with, exclude, include):
        filtered = self.words

        if starts_with:
            filtered = list(filter(lambda x: x.startswith(starts_with), filtered))

        if ends_with:
            filtered = list(filter(lambda x: x.endswith(ends_with), filtered))

        if exclude:
            filtered = list(filter(lambda x: self.exclude_filter(exclude, x), filtered))

        if include:
            filtered = list(filter(lambda x: self.include_filter(include, x), filtered))

        return filtered

    @staticmethod
    def auto_filter(status, word):
        for idx, char in enumerate(status['answer']):
            if char == ' ':
                continue
            if char != word[idx]:
                return False

        return True

    def automatic(self):
        filtered = list(filter(lambda x: self.auto_filter(self.status, x), self.words))
        filtered = list(filter(lambda x: self.include_filter(''.join(self.status['in_but_wrong_spot']), x), filtered))
        filtered = list(filter(lambda x: self.exclude_filter(''.join(self.status['not_in']), x), filtered))

        return filtered

    def main(self):
        while True:
            print('Welcome to wordle helper.')
            user_input = input("Automatic or Manual? ")

            if user_input == 'Automatic':
                possible_words = self.automatic()
            elif user_input == 'Manual':
                print("leave it blank and press enter, if none")
                starts_with = input("Enter the letter(s) start(s) with: ")
                ends_with = input("Enter the letter(s) end(s) with: ")
                exclude = input("Enter the excluded letter(s): ")
                include = input("Enter the included letter(s): ")
                possible_words = self.manual(starts_with, ends_with, exclude, include)
            else:
                print("Please input valid option (Automatic / Manual)")
                continue

            print("Possible words are", possible_words, end='\n\n')
            user_input = input('Enter q for end helper')

            if user_input == 'q':
                break


play_game = Wordle("Tommy")

