from random import randint as rand

listOfShowsOnNetflix = {
    "1": ["Invincible", "Warrior Nun", "Inside Job", "Super Crooks"],
    "2": ["The Witcher", "The Umbrella Academy", "Outer Banks", "Masters of the Universe: Revelation"],
    "3": ["Sex Education", "Love, Death Robots"],
    "4": ["Stranger Things", "The Crown", "Disenchantment"],
    "5": ["Big Mouth"],
    "6": [],
    "7": [],
    "8": ["Game Of Thrones"],
    "9": [],
    "10": []
}

asked = 5
while asked >= 0:
    seasons = input("How many seasons do you want the show to have? (Enter A Number)"
                    "\n>>>")

    try:
        seasons = int(seasons)
        if 0 >= seasons:
            raise ValueError

        if seasons > 10:
            seasons = 10

        listOfPotentialShows = listOfShowsOnNetflix[str(seasons)]
        total = len(listOfPotentialShows)
        print(total)

        if total > 0:
            displayed = "| "
            for x in listOfPotentialShows:
                displayed += f"{x} | "

            print("The show(s) that fit into the category are:\n"
                  f"{displayed}")
        else:
            print("There are no shows that fit into this category."
                  "\nTry again\n")
            continue

        if total > 1:
            asked = 5
            while asked >= 0:
                randomShow = input("\nDo you want me to choose a random show from this list? (Enter 1 or 2)"
                                   "\n1. Yes"
                                   "\n2. No"
                                   "\n>>>")

                try:
                    randomShow = int(randomShow)
                    if randomShow == 1:
                        randomShow = listOfPotentialShows[rand(0, total)]
                        print("\nThe show I have chosen for you is:", randomShow)

                        asked = 5
                        while asked >= 0:
                            again = input("\nWould you like to try again?"
                                          "\n1. Yes"
                                          "\n2. No"
                                          "\n>>>")

                            try:
                                again = int(again)
                                if again == 1:
                                    randomShow = -1
                                    print()
                                    break

                                elif again == 2:
                                    print("Enjoy")
                                    exit()

                                else:
                                    raise ValueError

                            except ValueError:
                                print("\nSorry, but you are fresh out of tries; Try again later")
                                quit()
                                asked -= 1

                        if randomShow == -1:
                            break

                    elif randomShow == 2:
                        print("Enjoy!")
                        quit()
                    else:
                        raise ValueError

                except ValueError:
                    if asked == 0:
                        print("\nSorry, but you are fresh out of tries; Try again later")
                        exit()

                    asked -= 1
                    pass

        else:
            asked = 5
            while asked >= 0:
                again = input("\nWould you like to try again?"
                              "\n1. Yes"
                              "\n2. No"
                              "\n>>>")

                try:
                    again = int(again)
                    if again == 1:
                        print()
                        break

                    elif again == 2:
                        print("Enjoy")
                        exit()

                    else:
                        raise ValueError

                except ValueError:
                    print("Sorry, but you are fresh out of tries; Try again later")
                    quit()
                    asked -= 1

    except ValueError:
        if asked == 0:
            print("Sorry, but you are fresh out of tries; Try again later")
            exit()

        print("Let me ask that again. Please Enter A Number 1 and Above")
        asked -= 1