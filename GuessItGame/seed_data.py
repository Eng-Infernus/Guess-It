import os
import re
import random
import django

# ── 1.  Django setup ────────────────────────────────────────────────────────────
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GuessIT.settings")  # ← change if needed
django.setup()

from GuessItGame.models import Category, Question, QuestionAnswers

# ── 2.  Author your quiz pool.  Format: (question, correct, [wrong1, wrong2, wrong3]) ──
sample_questions = {
    "Science": [
        ("What planet is closest to the sun? (10pts)",
         "Mercury",
         ["Venus", "Earth", "Mars"]),
        ("What gas do plants absorb from the air? (20pts)",
         "Carbon dioxide",
         ["Oxygen", "Nitrogen", "Hydrogen"]),
        ("What is H₂O commonly called? (30pts)",
         "Water",
         ["Hydrogen peroxide", "Ammonia", "Ethanol"]),
        ("What organ pumps blood in the human body? (40pts)",
         "Heart",
         ["Liver", "Lungs", "Brain"]),
        ("What is the chemical symbol for gold? (50pts)",
         "Au",
         ["Ag", "Go", "Gd"]),
        ("How many bones are in an adult human body? (10pts)",
         "206",
         ["208", "204", "212"]),
        ("What vitamin is produced by the skin when exposed to sunlight? (20pts)",
         "Vitamin D",
         ["Vitamin A", "Vitamin C", "Vitamin B12"]),
        ("What is the hardest natural substance on Earth? (30pts)",
         "Diamond",
         ["Quartz", "Steel", "Titanium"]),
        ("What type of animal is a whale? (40pts)",
         "Mammal",
         ["Fish", "Reptile", "Amphibian"]),
        ("What is the speed of light in a vacuum? (50pts)",
         "299,792,458 meters per second",
         ["300,000,000 meters per second", "250,000,000 meters per second", "350,000,000 meters per second"])
    ],

    "History": [
        ("Who discovered America in 1492? (10pts)",
         "Christopher Columbus",
         ["Ferdinand Magellan", "John Cabot", "Amerigo Vespucci"]),
        ("In which year did World War II end? (20pts)",
         "1945",
         ["1944", "1946", "1943"]),
        ("Who was the first President of the United States? (30pts)",
         "George Washington",
         ["Thomas Jefferson", "John Adams", "Benjamin Franklin"]),
        ("What ancient wonder of the world was located in Alexandria? (40pts)",
         "The Lighthouse of Alexandria",
         ["The Colossus of Rhodes", "The Hanging Gardens", "The Temple of Artemis"]),
        ("Which empire was ruled by Julius Caesar? (50pts)",
         "Roman Empire",
         ["Greek Empire", "Persian Empire", "Byzantine Empire"]),
        ("What year did the Berlin Wall fall? (10pts)",
         "1989",
         ["1991", "1987", "1990"]),
        ("Who was the Egyptian queen who had relationships with Julius Caesar and Mark Antony? (20pts)",
         "Cleopatra",
         ["Nefertiti", "Hatshepsut", "Ankhesenamun"]),
        ("What ship sank in 1912 after hitting an iceberg? (30pts)",
         "Titanic",
         ["Lusitania", "Britannic", "Olympic"]),
        ("Which war was fought between 1861-1865 in America? (40pts)",
         "Civil War",
         ["Revolutionary War", "War of 1812", "Spanish-American War"]),
        ("Who painted the ceiling of the Sistine Chapel? (50pts)",
         "Michelangelo",
         ["Leonardo da Vinci", "Raphael", "Donatello"])
    ],

    "Geography": [
        ("What is the capital of France? (10pts)",
         "Paris",
         ["Lyon", "Marseille", "Nice"]),
        ("Which is the longest river in the world? (20pts)",
         "Nile",
         ["Amazon", "Mississippi", "Yangtze"]),
        ("What is the largest continent by area? (30pts)",
         "Asia",
         ["Africa", "North America", "Europe"]),
        ("Which mountain range contains Mount Everest? (40pts)",
         "Himalayas",
         ["Andes", "Rocky Mountains", "Alps"]),
        ("What is the smallest country in the world? (50pts)",
         "Vatican City",
         ["Monaco", "San Marino", "Liechtenstein"]),
        ("Which desert is the largest in the world? (10pts)",
         "Sahara",
         ["Gobi", "Mojave", "Kalahari"]),
        ("What is the capital of Australia? (20pts)",
         "Canberra",
         ["Sydney", "Melbourne", "Perth"]),
        ("Which country has the most natural lakes? (30pts)",
         "Canada",
         ["Russia", "Finland", "Norway"]),
        ("What is the deepest ocean trench? (40pts)",
         "Mariana Trench",
         ["Puerto Rico Trench", "Java Trench", "Peru-Chile Trench"]),
        ("Which African country is completely surrounded by South Africa? (50pts)",
         "Lesotho",
         ["Swaziland", "Botswana", "Malawi"])
    ],

    "Technology": [
        ("Who co-founded Apple Inc. with Steve Wozniak? (10pts)",
         "Steve Jobs",
         ["Bill Gates", "Michael Dell", "Larry Page"]),
        ("What does 'WWW' stand for? (20pts)",
         "World Wide Web",
         ["World Wide Work", "Web Wide World", "Wide World Web"]),
        ("What does 'CPU' stand for? (30pts)",
         "Central Processing Unit",
         ["Computer Processing Unit", "Central Program Unit", "Computer Program Unit"]),
        ("Which company developed the Android operating system? (40pts)",
         "Google",
         ["Apple", "Microsoft", "Samsung"]),
        ("What does 'AI' stand for? (50pts)",
         "Artificial Intelligence",
         ["Automated Intelligence", "Advanced Intelligence", "Applied Intelligence"]),
        ("What social media platform is known for 280-character messages? (10pts)",
         "Twitter",
         ["Facebook", "Instagram", "LinkedIn"]),
        ("What does 'USB' stand for? (20pts)",
         "Universal Serial Bus",
         ["Universal System Bus", "United Serial Bus", "Universal Service Bus"]),
        ("Which programming language is known for its use in web development and has a coffee-related name? (30pts)",
         "JavaScript",
         ["Java", "Python", "C++"]),
        ("What company was originally called 'BackRub'? (40pts)",
         "Google",
         ["Yahoo", "Bing", "Ask Jeeves"]),
        ("What does 'HTTP' stand for? (50pts)",
         "HyperText Transfer Protocol",
         ["HyperText Transport Protocol", "HyperLink Transfer Protocol", "HyperText Transmission Protocol"])
    ],

    "Sports": [
        ("How many players are on a basketball team on the court at one time? (10pts)",
         "5",
         ["6", "7", "4"]),
        ("What sport is played at Wimbledon? (20pts)",
         "Tennis",
         ["Badminton", "Squash", "Table Tennis"]),
        ("How many holes are on a standard golf course? (30pts)",
         "18",
         ["16", "20", "24"]),
        ("What is the maximum score possible in ten-pin bowling? (40pts)",
         "300",
         ["250", "350", "400"]),
        ("How often are the Summer Olympic Games held? (50pts)",
         "Every 4 years",
         ["Every 2 years", "Every 3 years", "Every 5 years"]),
        ("In what sport would you perform a slam dunk? (10pts)",
         "Basketball",
         ["Volleyball", "Tennis", "Badminton"]),
        ("How many minutes are in a regulation soccer match? (20pts)",
         "90",
         ["80", "100", "120"]),
        ("What is the diameter of a basketball hoop in inches? (30pts)",
         "18",
         ["16", "20", "22"]),
        ("Which sport uses terms like 'spare' and 'strike'? (40pts)",
         "Bowling",
         ["Golf", "Tennis", "Baseball"]),
        ("What is the only sport to have been played on the moon? (50pts)",
         "Golf",
         ["Basketball", "Tennis", "Football"])
    ],

    "Entertainment": [
        ("Who directed the movie 'Titanic'? (10pts)",
         "James Cameron",
         ["Steven Spielberg", "Martin Scorsese", "Christopher Nolan"]),
        ("What is the highest-grossing film of all time? (20pts)",
         "Avatar",
         ["Avengers: Endgame", "Titanic", "Star Wars: The Force Awakens"]),
        ("Which streaming service created 'Stranger Things'? (30pts)",
         "Netflix",
         ["Hulu", "Amazon Prime", "Disney+"]),
        ("Who played Jack Sparrow in 'Pirates of the Caribbean'? (40pts)",
         "Johnny Depp",
         ["Orlando Bloom", "Geoffrey Rush", "Keira Knightley"]),
        ("What is the longest-running animated TV series in US history? (50pts)",
         "The Simpsons",
         ["South Park", "Family Guy", "SpongeBob SquarePants"]),
        ("Which movie features the song 'My Heart Will Go On'? (10pts)",
         "Titanic",
         ["The Bodyguard", "Ghost", "Dirty Dancing"]),
        ("What is the name of the coffee shop in the TV show 'Friends'? (20pts)",
         "Central Perk",
         ["The Grind", "Java Joe's", "Coffee Central"]),
        ("Who composed the music for 'The Lion King'? (30pts)",
         "Hans Zimmer",
         ["John Williams", "Danny Elfman", "Alan Menken"]),
        ("Which actor played the Joker in 'The Dark Knight'? (40pts)",
         "Heath Ledger",
         ["Jack Nicholson", "Joaquin Phoenix", "Jared Leto"]),
        ("What was the first feature-length animated movie ever released? (50pts)",
         "Snow White and the Seven Dwarfs",
         ["Pinocchio", "Fantasia", "Bambi"])
    ],

    "Literature": [
        ("Who wrote 'Romeo and Juliet'? (10pts)",
         "William Shakespeare",
         ["Christopher Marlowe", "Ben Jonson", "John Webster"]),
        ("What is the first book in the Harry Potter series? (20pts)",
         "Harry Potter and the Philosopher's Stone",
         ["Harry Potter and the Chamber of Secrets", "Harry Potter and the Prisoner of Azkaban",
          "Harry Potter and the Goblet of Fire"]),
        ("Who wrote the novel '1984'? (30pts)",
         "George Orwell",
         ["Aldous Huxley", "Ray Bradbury", "Kurt Vonnegut"]),
        ("What is the opening line of Charles Dickens' 'A Tale of Two Cities'? (40pts)",
         "It was the best of times, it was the worst of times",
         ["Call me Ishmael", "It is a truth universally acknowledged", "In a hole in the ground there lived a hobbit"]),
        ("Who wrote 'Pride and Prejudice'? (50pts)",
         "Jane Austen",
         ["Charlotte Brontë", "Emily Brontë", "George Eliot"]),
        ("What creature is Moby Dick? (10pts)",
         "Whale",
         ["Shark", "Octopus", "Sea Serpent"]),
        ("Who wrote 'The Great Gatsby'? (20pts)",
         "F. Scott Fitzgerald",
         ["Ernest Hemingway", "John Steinbeck", "William Faulkner"]),
        ("In which Shakespeare play does the character Hamlet appear? (30pts)",
         "Hamlet",
         ["Macbeth", "Othello", "King Lear"]),
        ("Who wrote 'To Kill a Mockingbird'? (40pts)",
         "Harper Lee",
         ["Toni Morrison", "Maya Angelou", "Flannery O'Connor"]),
        ("What is the first word of Charles Dickens' 'A Christmas Carol'? (50pts)",
         "Marley",
         ["Scrooge", "Christmas", "Bah"])
    ],

    "Art": [
        ("Who painted the 'Mona Lisa'? (10pts)",
         "Leonardo da Vinci",
         ["Michelangelo", "Raphael", "Donatello"]),
        ("Which art movement was Pablo Picasso associated with? (20pts)",
         "Cubism",
         ["Impressionism", "Surrealism", "Expressionism"]),
        ("Which artist is known for cutting off his ear? (30pts)",
         "Vincent van Gogh",
         ["Paul Gauguin", "Henri de Toulouse-Lautrec", "Paul Cézanne"]),
        ("In which museum is the Mona Lisa displayed? (40pts)",
         "Louvre",
         ["Uffizi", "Metropolitan Museum", "British Museum"]),
        ("Who sculpted 'The Thinker'? (50pts)",
         "Auguste Rodin",
         ["Michelangelo", "Donatello", "Bernini"]),
        ("What painting technique did Jackson Pollock become famous for? (10pts)",
         "Drip painting",
         ["Pointillism", "Collage", "Watercolor"]),
        ("Who painted 'The Starry Night'? (20pts)",
         "Vincent van Gogh",
         ["Claude Monet", "Pierre-Auguste Renoir", "Edgar Degas"]),
        ("What does 'Renaissance' mean? (30pts)",
         "Rebirth",
         ["Revolution", "Reformation", "Revival"]),
        ("Who painted 'The Persistence of Memory' featuring melting clocks? (40pts)",
         "Salvador Dalí",
         ["René Magritte", "Max Ernst", "Giorgio de Chirico"]),
        ("Which artist painted the ceiling of the Sistine Chapel? (50pts)",
         "Michelangelo",
         ["Leonardo da Vinci", "Raphael", "Botticelli"])
    ],

    "Music": [
        ("How many strings does a standard guitar have? (10pts)",
         "6",
         ["4", "8", "12"]),
        ("What instrument did Mozart primarily compose for? (20pts)",
         "Piano",
         ["Violin", "Flute", "Harpsichord"]),
        ("Which band released the album 'Abbey Road'? (30pts)",
         "The Beatles",
         ["The Rolling Stones", "Led Zeppelin", "The Who"]),
        ("How many keys are on a standard piano? (40pts)",
         "88",
         ["76", "96", "104"]),
        ("What does 'forte' mean in musical terms? (50pts)",
         "Loud",
         ["Soft", "Fast", "Slow"]),
        ("Which instrument family does the trumpet belong to? (10pts)",
         "Brass",
         ["Woodwind", "Percussion", "String"]),
        ("Who composed 'The Four Seasons'? (20pts)",
         "Antonio Vivaldi",
         ["Johann Sebastian Bach", "Wolfgang Amadeus Mozart", "Ludwig van Beethoven"]),
        ("What is the highest female singing voice type? (30pts)",
         "Soprano",
         ["Alto", "Tenor", "Bass"]),
        ("How many movements are typically in a classical symphony? (40pts)",
         "4",
         ["3", "5", "6"]),
        ("What does 'allegro' mean in music? (50pts)",
         "Fast",
         ["Slow", "Loud", "Soft"])
    ],

    "Mathematics": [
        ("What is 2 + 2? (10pts)",
         "4",
         ["3", "5", "6"]),
        ("What is the value of π (pi) to two decimal places? (20pts)",
         "3.14",
         ["3.16", "3.12", "3.18"]),
        ("What is 7 × 8? (30pts)",
         "56",
         ["54", "58", "64"]),
        ("What is the square root of 64? (40pts)",
         "8",
         ["6", "10", "12"]),
        ("What is 10 to the power of 3? (50pts)",
         "1000",
         ["100", "300", "3000"]),
        ("What is 15% of 200? (10pts)",
         "30",
         ["25", "35", "40"]),
        ("What is the next prime number after 7? (20pts)",
         "11",
         ["9", "13", "15"]),
        ("What is 144 ÷ 12? (30pts)",
         "12",
         ["10", "14", "16"]),
        ("What is the area of a square with side length 5? (40pts)",
         "25",
         ["20", "30", "35"]),
        ("What is the sum of interior angles in a triangle? (50pts)",
         "180 degrees",
         ["90 degrees", "270 degrees", "360 degrees"])
    ],

    "Food & Cooking": [
        ("What spice is derived from the Crocus flower? (10pts)",
         "Saffron",
         ["Turmeric", "Paprika", "Cardamom"]),
        ("What is the main ingredient in guacamole? (20pts)",
         "Avocado",
         ["Tomato", "Onion", "Lime"]),
        ("Which country is famous for inventing pizza? (30pts)",
         "Italy",
         ["Greece", "France", "Spain"]),
        ("What type of pastry is used to make profiteroles? (40pts)",
         "Choux pastry",
         ["Puff pastry", "Filo pastry", "Shortcrust pastry"]),
        ("What is the most consumed beverage in the world after water? (50pts)",
         "Tea",
         ["Coffee", "Beer", "Milk"]),
        ("What gives bread its fluffy texture? (10pts)",
         "Yeast",
         ["Sugar", "Salt", "Oil"]),
        ("Which fruit is known as the 'king of fruits' in Southeast Asia? (20pts)",
         "Durian",
         ["Mango", "Rambutan", "Jackfruit"]),
        ("What is the main ingredient in traditional hummus? (30pts)",
         "Chickpeas",
         ["Lentils", "Black beans", "White beans"]),
        ("Which type of cheese is traditionally used on a Margherita pizza? (40pts)",
         "Mozzarella",
         ["Cheddar", "Parmesan", "Gouda"]),
        ("What cooking method involves cooking food in its own fat? (50pts)",
         "Confit",
         ["Braising", "Poaching", "Steaming"])
    ],

    "Nature & Animals": [
        ("What is the largest mammal in the world? (10pts)",
         "Blue whale",
         ["Elephant", "Giraffe", "Hippopotamus"]),
        ("How many chambers does a human heart have? (20pts)",
         "4",
         ["2", "3", "6"]),
        ("What is the fastest land animal? (30pts)",
         "Cheetah",
         ["Lion", "Leopard", "Gazelle"]),
        ("Which tree produces acorns? (40pts)",
         "Oak",
         ["Maple", "Pine", "Birch"]),
        ("What is the largest species of penguin? (50pts)",
         "Emperor penguin",
         ["King penguin", "Adelie penguin", "Chinstrap penguin"]),
        ("What do pandas primarily eat? (10pts)",
         "Bamboo",
         ["Fish", "Meat", "Fruits"]),
        ("How many legs does a spider have? (20pts)",
         "8",
         ["6", "10", "12"]),
        ("What is the hardest natural substance on Earth? (30pts)",
         "Diamond",
         ["Quartz", "Steel", "Granite"]),
        ("Which planet is known as the Red Planet? (40pts)",
         "Mars",
         ["Venus", "Jupiter", "Saturn"]),
        ("What is the study of earthquakes called? (50pts)",
         "Seismology",
         ["Geology", "Meteorology", "Volcanology"])
    ],

    "Language & Communication": [
        ("What language is spoken in Brazil? (10pts)",
         "Portuguese",
         ["Spanish", "Italian", "French"]),
        ("How do you say 'hello' in Spanish? (20pts)",
         "Hola",
         ["Ciao", "Bonjour", "Guten Tag"]),
        ("What does 'bonjour' mean in English? (30pts)",
         "Hello/Good day",
         ["Goodbye", "Thank you", "Please"]),
        ("Which language has the most native speakers worldwide? (40pts)",
         "Mandarin Chinese",
         ["English", "Spanish", "Hindi"]),
        ("What is the official language of Egypt? (50pts)",
         "Arabic",
         ["Turkish", "Persian", "Hebrew"]),
        ("How do you say 'thank you' in French? (10pts)",
         "Merci",
         ["Gracias", "Danke", "Grazie"]),
        ("What language family does English belong to? (20pts)",
         "Germanic",
         ["Romance", "Slavic", "Celtic"]),
        ("What does 'sayonara' mean in English? (30pts)",
         "Goodbye",
         ["Hello", "Thank you", "Please"]),
        ("Which alphabet is used in Russian? (40pts)",
         "Cyrillic",
         ["Latin", "Greek", "Arabic"]),
        ("What is the most studied foreign language in the world? (50pts)",
         "English",
         ["Spanish", "French", "Mandarin"])
    ],

    "Pop Culture & Social Media": [
        ("Which social media platform is known for its 'Stories' feature? (10pts)",
         "Instagram",
         ["Facebook", "Twitter", "LinkedIn"]),
        ("What does 'going viral' mean on the internet? (20pts)",
         "Content spreading rapidly",
         ["Getting a computer virus", "Being banned", "Losing followers"]),
        ("Which app is famous for short-form dance videos? (30pts)",
         "TikTok",
         ["Snapchat", "Instagram", "YouTube"]),
        ("What does 'LOL' stand for? (40pts)",
         "Laugh Out Loud",
         ["Lots of Love", "Life of Leisure", "League of Legends"]),
        ("Which streaming service has the most global subscribers? (50pts)",
         "Netflix",
         ["Disney+", "Amazon Prime", "Hulu"]),
        ("What is a 'meme'? (10pts)",
         "Viral internet content",
         ["A type of video", "A social media account", "A website"]),
        ("Which platform is owned by Meta (formerly Facebook)? (20pts)",
         "Instagram",
         ["Twitter", "TikTok", "Snapchat"]),
        ("What does 'FOMO' stand for? (30pts)",
         "Fear Of Missing Out",
         ["Fear Of Making Offers", "Friends On My Online", "Fun On My Own"]),
        ("Which platform is primarily used for professional networking? (40pts)",
         "LinkedIn",
         ["Twitter", "Instagram", "TikTok"]),
        ("What does it mean to 'slide into DMs'? (50pts)",
         "Send a private message",
         ["Delete messages", "Share a post", "Block someone"])
    ]
}

# ── 3.  Helper – extract the "(xxpts)" value, fallback to 10 / 20 / 30 / 40 / 50 ─
_points_fallback = [10, 20, 30, 40, 50]


def extract_points(question_text: str, idx: int) -> int:
    m = re.search(r"\((\d+)\s*pts?\)", question_text, flags=re.I)
    return int(m.group(1)) if m else _points_fallback[idx % len(_points_fallback)]


# ── 4.  Seed the DB ─────────────────────────────────────────────────────────────
inserted_q = inserted_a = 0

for category_name, q_list in sample_questions.items():
    category, created = Category.objects.get_or_create(category_name=category_name)

    for idx, (text, correct, wrongs) in enumerate(q_list):
        if len(wrongs) != 3:
            raise ValueError(
                f"⛔  \"{text}\" must list **exactly 3 wrong answers**, found {len(wrongs)}."
            )

        # a.  Question row
        q = Question.objects.create(
            text=text,
            correct_answer=correct,
            helper_hint_text=wrongs[0],  # first distractor as hint, tweak if you prefer
            points=extract_points(text, idx),
            category=category
        )
        inserted_q += 1

        # b.  Answer rows (1 correct + 3 wrong = 4 total)
        QuestionAnswers.objects.create(question=q, answer_text=correct)
        for alt in wrongs:
            QuestionAnswers.objects.create(question=q, answer_text=alt)
        inserted_a += 4

print(f"✔  Inserted {inserted_q} questions and {inserted_a} answers (4 per question).")
print("🎉  Database seeding completed successfully!")