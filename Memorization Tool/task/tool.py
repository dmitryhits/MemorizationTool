from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker


Base = declarative_base()


class FlashCardORM(Base):
    __tablename__ = 'flashcard'
    id = Column(Integer, primary_key=True)
    question = Column(String)
    answer = Column(String)
    box = Column(Integer)


class FlashCard:
    def __init__(self):
        self.flashcards = {}
        self.menu()

    def add_flashcard(self):
        question = ''
        answer = ''
        # wait for non-empty input
        while True:
            question = input("Question:\n")
            if question:
                break
        # wait for non-empty input
        while True:
            answer = input("Answer:\n")
            if answer:
                break
        self.flashcards[question] = answer
        new_flashcard = FlashCardORM(question=question, answer=answer, box=0)
        session.add(new_flashcard)
        session.commit()

    def update_flashcard(self, flashcard):
        update_menu = 'press "d" to delete the flashcard:\n'
        update_menu += 'press "e" to edit the flashcard:\n'
        while True:
            print(update_menu)
            user_response = input()
            if user_response == 'd':
                session.delete(flashcard)
                session.commit()
                break
            elif user_response == 'e':
                # wait for non-empty response
                while True:
                    print(f'current question: {flashcard.question}')
                    question = input('please write a new question:\n')
                    if question:
                        break
                # wait for non-empty response
                while True:
                    print(f'current answer: {flashcard.answer}')
                    answer = input('please write a new answer:\n')
                    if answer:
                        break
                # update flashcard
                flashcard.answer = answer
                flashcard.question = question
                session.commit()
                break
            else:
                print(f'{user_response} is not an option')

    def practice_flashcards(self):
        flashcards_list = session.query(FlashCardORM).all()
        if not flashcards_list:
            print("There is no flashcard to practice!\n")
        else:
            for flashcard in flashcards_list:
                print(f"Question: {flashcard.question}")
                print('press "y" to see the answer:')
                print('press "n" to skip:')
                print('press "u" to update:')
                while True:
                    user_response = input()
                    if user_response == 'y':
                        print(f'Answer: {flashcard.answer}')
                        self.learning_menu(flashcard)
                        break
                    elif user_response == 'n':
                        self.learning_menu(flashcard)
                        break
                    elif user_response == 'u':
                        self.update_flashcard(flashcard)
                        break
                    else:
                        print(f'{user_response} is not an option')

    def learning_menu(self, flashcard):
        menu = 'press "y" if your answer is correct:\n'
        menu += 'press "n" if your answer is wrong:\n'
        while True:
            print(menu)
            user_response = input()
            if user_response == 'y':
                if flashcard.box == 2:
                    session.delete(flashcard)
                    session.commit()
                    print('box', flashcard.box)
                else:
                    flashcard.box += 1
                    session.commit()
                break
            elif user_response == 'n':
                break
            else:
                print(f'{user_response} is not an option')

    def menu(self):
        main_menu = "1. Add flashcards\n"
        main_menu += "2. Practice flashcards\n"
        main_menu += "3. Exit"

        while True:
            print(main_menu)
            main_choice = input()
            if main_choice == '1':
                self.add_flashcard_menu()
            elif main_choice == '2':
                self.practice_flashcards()
            elif main_choice == '3':
                print('Bye!')
                exit(0)
            else:
                print(f'\n{main_choice} is not an option\n')

    def add_flashcard_menu(self):
        add_flashcard_prompt = "\n1. Add a new flashcard\n"
        add_flashcard_prompt += "2. Exit"
        # wait for correct input
        while True:
            print(add_flashcard_prompt)
            choice_1 = input()
            if choice_1 == '1':
                self.add_flashcard()
            elif choice_1 == '2':
                # return to main menu
                break
            else:
                print(f'\n{choice_1} is not an option\n')


if __name__ == '__main__':
    engine = create_engine('sqlite:///flashcard.db?check_same_thread=False')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    flashcards = FlashCard()