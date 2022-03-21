import random


class Wordle:
    player_name = ""

    def __init__(self, player_name):
        f = open("C:/Users/docto/PycharmProjects/source/guess.csv", 'r')
        self.words = f.read().replace("\"", "").split(",")
        f = open("C:/Users/docto/PycharmProjects/source/words.csv", 'r')
        self.all_words = f.read().replace("\"", "").split(",") + self.words
        Wordle.player_name = player_name
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

    def update_status(self, user_input: str, guess: list, status: dict):
        for idx, char in enumerate(user_input):
            if guess[idx]:
                if char not in status['in_and_right_spot']:
                    status['in_and_right_spot'].append(char)
                    if char in status['in_but_wrong_spot']:
                        status['in_but_wrong_spot'].remove(char)
            elif guess[idx] is None:
                if char not in status['not_in']:
                    status['not_in'].append(char)
            else:
                if char not in status['in_but_wrong_spot'] and char not in status['in_and_right_spot']:
                    status['in_but_wrong_spot'].append(char)

        for dic in status:
            status[dic] = sorted(status[dic])

    def main(self):
        answer = random.choice(self.words)
        status = {'in_and_right_spot': [], 'in_but_wrong_spot': [], 'not_in': []}
        count = 1

        while count < 7:
            print(f"-----#{count}-----")
            print(status)
            user_input = input("Enter your guess: ")
            guess = self.comparator(user_input, answer)

            if guess == "congratulations!":
                print(guess, Wordle.player_name, "your attempt:", count)
                break
            elif guess == "No such word! Try Again.":
                print(guess)
                continue

            print(guess)
            self.update_status(user_input, guess, status)
            count += 1

        print('The answer is', answer)


play_game = Wordle("Tommy")
