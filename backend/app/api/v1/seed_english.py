from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.models.models import Choice, Question, Quiz, User

router = APIRouter()

ENGLISH_QUIZZES = [
    {
        "title": "English Test - Variant 1",
        "description": "English language test questions - Variant 1",
        "duration_minutes": 20,
        "questions": [
            {"text": "This is Lola and her brother, Doniyor. ____ my friends.", "order": 0, "choices": [("They're", True), ("We're", False), ("He's", False), ("She's", False)]},
            {"text": "I ___ a teacher.", "order": 1, "choices": [("am", True), ("is", False), ("are", False), ("be", False)]},
            {"text": "She ___ from Uzbekistan.", "order": 2, "choices": [("is", True), ("am", False), ("are", False), ("be", False)]},
            {"text": "They ___ students.", "order": 3, "choices": [("are", True), ("is", False), ("am", False), ("be", False)]},
            {"text": "My name ___ Ali.", "order": 4, "choices": [("is", True), ("am", False), ("are", False), ("be", False)]},
            {"text": "We ___ in the classroom.", "order": 5, "choices": [("are", True), ("is", False), ("am", False), ("be", False)]},
            {"text": "Tashkent is in ___.", "order": 6, "choices": [("Uzbekistan", True), ("Kazakhstan", False), ("Tajikistan", False), ("Kyrgyzstan", False)]},
            {"text": "Paris is in ___.", "order": 7, "choices": [("France", True), ("Germany", False), ("Italy", False), ("Spain", False)]},
            {"text": "Tokyo is in ___.", "order": 8, "choices": [("Japan", True), ("China", False), ("Korea", False), ("Vietnam", False)]},
            {"text": "25 =", "order": 9, "choices": [("twenty-five", True), ("twenty-four", False), ("twenty-six", False), ("two-five", False)]},
            {"text": "14 =", "order": 10, "choices": [("fourteen", True), ("forty", False), ("four", False), ("forty-one", False)]},
            {"text": "….. are Uzbek and we like plov.", "order": 11, "choices": [("We", True), ("They", False), ("You", False), ("I", False)]},
            {"text": "I'm from Milan. ____ is in Italy.", "order": 12, "choices": [("It", True), ("He", False), ("She", False), ("Milan", False)]},
            {"text": "Excuse me, how ____ your last name?", "order": 13, "choices": [("do you spell", True), ("do you say", False), ("is", False), ("do you write", False)]},
            {"text": "Oh, ____ are my keys!", "order": 14, "choices": [("here", True), ("there", False), ("where", False), ("how", False)]},
            {"text": "I'd like ____ apple, please.", "order": 15, "choices": [("an", True), ("a", False), ("the", False), ("some", False)]},
            {"text": "______ name is Jasur. And my ______ is Aliev.", "order": 16, "choices": [("My / surname", True), ("His / last name", False), ("My / first name", False), ("Your / surname", False)]},
            {"text": "______ name is Anna. ______ Anna Baker.", "order": 17, "choices": [("Her / She's", True), ("His / He's", False), ("My / I'm", False), ("Your / You're", False)]},
            {"text": "Where ______ John from? ______is from the US.", "order": 18, "choices": [("is / He", True), ("are / They", False), ("does / He", False), ("is / She", False)]},
            {"text": "I have ______ brother. ______ name is David.", "order": 19, "choices": [("a / His", True), ("the / Her", False), ("a / Her", False), ("an / Their", False)]},
        ],
    },
    {
        "title": "English Test - Variant 2",
        "description": "English language test questions - Variant 2",
        "duration_minutes": 20,
        "questions": [
            {"text": "Pierre is a French boy. ______ from ______.", "order": 0, "choices": [("He's / France", True), ("She's / France", False), ("They're / France", False), ("He's / Italy", False)]},
            {"text": "Lisa and Max are Americans. ______ from the U.S.A.", "order": 1, "choices": [("They're", True), ("He's", False), ("She's", False), ("We're", False)]},
            {"text": "Hello! My ___ ___ Maria. I ___ ___ from Mexico.", "order": 2, "choices": [("name is / am not", True), ("name is / am", False), ("names are / am not", False), ("name are / am not", False)]},
            {"text": "How many ___ are there in the cupboard?", "order": 3, "choices": [("cups", True), ("cup", False), ("cupper", False), ("cuppes", False)]},
            {"text": "In our garden there is ___ huge pine tree.", "order": 4, "choices": [("a", True), ("an", False), ("the", False), ("some", False)]},
            {"text": "I have got ___ money.", "order": 5, "choices": [("some", True), ("any", False), ("a", False), ("the", False)]},
            {"text": "We have ___ books.", "order": 6, "choices": [("some", True), ("any", False), ("a", False), ("the", False)]},
            {"text": "Do you have ___ car?", "order": 7, "choices": [("a", True), ("an", False), ("some", False), ("any", False)]},
            {"text": "She ___ (read) a book now.", "order": 8, "choices": [("is reading", True), ("reads", False), ("read", False), ("are reading", False)]},
            {"text": "They ___ (play) football in the garden.", "order": 9, "choices": [("are playing", True), ("is playing", False), ("plays", False), ("play", False)]},
            {"text": "I ___ (write) a letter at the moment.", "order": 10, "choices": [("am writing", True), ("is writing", False), ("write", False), ("are writing", False)]},
            {"text": "He ___ (watch) TV now.", "order": 11, "choices": [("is watching", True), ("are watching", False), ("watch", False), ("watches", False)]},
            {"text": "We ___ (listen) to music.", "order": 12, "choices": [("are listening", True), ("is listening", False), ("listen", False), ("listens", False)]},
            {"text": "One box, three ___.", "order": 13, "choices": [("boxes", True), ("boxs", False), ("box", False), ("boxies", False)]},
            {"text": "One baby, five ___.", "order": 14, "choices": [("babies", True), ("babys", False), ("babes", False), ("baby", False)]},
            {"text": "Look! The boys ___ (run) in the park.", "order": 15, "choices": [("are running", True), ("is running", False), ("run", False), ("runs", False)]},
            {"text": "She ___ (cook) dinner now.", "order": 16, "choices": [("is cooking", True), ("are cooking", False), ("cook", False), ("cooks", False)]},
            {"text": "The children ___ (play) with their toys.", "order": 17, "choices": [("are playing", True), ("is playing", False), ("plays", False), ("play", False)]},
            {"text": "How ___ rice do we have left?", "order": 18, "choices": [("much", True), ("many", False), ("more", False), ("few", False)]},
            {"text": "How ___ cars are we buying?", "order": 19, "choices": [("many", True), ("much", False), ("more", False), ("few", False)]},
        ],
    },
    {
        "title": "English Test - Variant 3",
        "description": "English language test questions - Variant 3",
        "duration_minutes": 20,
        "questions": [
            {"text": "How ___ water do I need to run the experiment?", "order": 0, "choices": [("much", True), ("many", False), ("more", False), ("few", False)]},
            {"text": "____ tourists visit Uzbekistan.", "order": 1, "choices": [("Many", True), ("Much", False), ("More", False), ("A lot", False)]},
            {"text": "How ___ times did the phone ring?", "order": 2, "choices": [("many", True), ("much", False), ("more", False), ("few", False)]},
            {"text": "Is that your book? Yes, ___ is.", "order": 3, "choices": [("it", True), ("that", False), ("he", False), ("this", False)]},
            {"text": "He is a ___.", "order": 4, "choices": [("teacher", True), ("teaches", False), ("teaching", False), ("teached", False)]},
            {"text": "She works in a hospital. She is a ___.", "order": 5, "choices": [("nurse", True), ("doctor", False), ("teacher", False), ("driver", False)]},
            {"text": "My father is a ___. He fixes cars.", "order": 6, "choices": [("mechanic", True), ("doctor", False), ("nurse", False), ("teacher", False)]},
            {"text": "I want to be a ___ when I grow up.", "order": 7, "choices": [("doctor", True), ("doctors", False), ("medicine", False), ("medical", False)]},
            {"text": "We have many ___ in our city.", "order": 8, "choices": [("schools", True), ("school", False), ("schooling", False), ("scholar", False)]},
            {"text": "___ is a famous restaurant.", "order": 9, "choices": [("That", True), ("This", False), ("These", False), ("Those", False)]},
            {"text": "___ are beautiful flowers.", "order": 10, "choices": [("These", True), ("That", False), ("This", False), ("Those", False)]},
            {"text": "___ are my friends.", "order": 11, "choices": [("These", True), ("That", False), ("This", False), ("Those", False)]},
            {"text": "___ is my brother.", "order": 12, "choices": [("This", True), ("These", False), ("Those", False), ("That", False)]},
            {"text": "___ are in the classroom now.", "order": 13, "choices": [("We", True), ("They", False), ("I", False), ("He", False)]},
            {"text": "Take… bags into the kitchen.", "order": 14, "choices": [("those", True), ("this", False), ("that", False), ("these", False)]},
            {"text": "Is …. a red flower?", "order": 15, "choices": [("that", True), ("this", False), ("these", False), ("those", False)]},
            {"text": "Is this a television? Yes, …is.", "order": 16, "choices": [("it", True), ("this", False), ("that", False), ("these", False)]},
            {"text": "Look at …. man, over there!", "order": 17, "choices": [("that", True), ("this", False), ("these", False), ("those", False)]},
            {"text": "____ is the place over there where I live.", "order": 18, "choices": [("That", True), ("This", False), ("These", False), ("Those", False)]},
            {"text": "……bottle over there is empty.", "order": 19, "choices": [("That", True), ("This", False), ("These", False), ("Those", False)]},
        ],
    },
    {
        "title": "English Test - Variant 4",
        "description": "English language test questions - Variant 4",
        "duration_minutes": 20,
        "questions": [
            {"text": "……are my parents.", "order": 0, "choices": [("These", True), ("This", False), ("That", False), ("Those", False)]},
            {"text": "My father bought …. toys for me.", "order": 1, "choices": [("those", True), ("this", False), ("that", False), ("these", False)]},
            {"text": "Look at …. birds in the sky.", "order": 2, "choices": [("those", True), ("this", False), ("that", False), ("these", False)]},
            {"text": "Is …hotel nice?", "order": 3, "choices": [("that", True), ("this", False), ("these", False), ("those", False)]},
            {"text": "Who is…. man, over there?", "order": 4, "choices": [("that", True), ("this", False), ("these", False), ("those", False)]},
            {"text": "Why are …. boxes here?", "order": 5, "choices": [("these", True), ("this", False), ("that", False), ("those", False)]},
            {"text": "(Your aunt Rita) … works for a large company.", "order": 6, "choices": [("She", True), ("He", False), ("They", False), ("It", False)]},
            {"text": "My hobby is ___ books.", "order": 7, "choices": [("reading", True), ("read", False), ("reads", False), ("to read", False)]},
            {"text": "I like ___ football on weekends.", "order": 8, "choices": [("playing", True), ("play", False), ("plays", False), ("to play", False)]},
            {"text": "She enjoys ___ music.", "order": 9, "choices": [("listening to", True), ("listen to", False), ("listens to", False), ("to listen", False)]},
            {"text": "Their hobby is ___ photos.", "order": 10, "choices": [("taking", True), ("take", False), ("takes", False), ("to take", False)]},
            {"text": "We love ___ movies at home.", "order": 11, "choices": [("watching", True), ("watch", False), ("watches", False), ("to watch", False)]},
            {"text": "I like my brother. I love ___.", "order": 12, "choices": [("him", True), ("her", False), ("them", False), ("it", False)]},
            {"text": "She is my friend. I can call ___ anytime.", "order": 13, "choices": [("her", True), ("him", False), ("them", False), ("it", False)]},
            {"text": "This is my father. I help ___ every day.", "order": 14, "choices": [("him", True), ("her", False), ("them", False), ("it", False)]},
            {"text": "They are my friends. I often meet ___.", "order": 15, "choices": [("them", True), ("him", False), ("her", False), ("it", False)]},
            {"text": "I have a cat. I feed ___ every morning.", "order": 16, "choices": [("it", True), ("him", False), ("her", False), ("them", False)]},
            {"text": "(John and I) . . . have a favorite restaurant.", "order": 17, "choices": [("We", True), ("They", False), ("You", False), ("I", False)]},
            {"text": "Is this ice-cream for ...... or for you?", "order": 18, "choices": [("me", True), ("I", False), ("my", False), ("mine", False)]},
            {"text": "(Sardor's motorbike) . . . has a very noisy engine.", "order": 19, "choices": [("It", True), ("He", False), ("She", False), ("They", False)]},
        ],
    },
    {
        "title": "English Test - Variant 5",
        "description": "English language test questions - Variant 5",
        "duration_minutes": 20,
        "questions": [
            {"text": "Malik has a dog. . . . . is white.", "order": 0, "choices": [("It", True), ("He", False), ("She", False), ("They", False)]},
            {"text": "(Jim, Aziz, and Harry) . . .. went biking together.", "order": 1, "choices": [("They", True), ("He", False), ("She", False), ("We", False)]},
            {"text": "(Our parents) . . .... live in a sweet home.", "order": 2, "choices": [("They", True), ("He", False), ("She", False), ("We", False)]},
            {"text": "(My friend, Rick) . . .. was honored by the president.", "order": 3, "choices": [("He", True), ("She", False), ("They", False), ("It", False)]},
            {"text": "She took ........", "order": 4, "choices": [("it", True), ("him", False), ("her", False), ("them", False)]},
            {"text": "My cousins are visiting us. . . . . are very nice.", "order": 5, "choices": [("They", True), ("He", False), ("She", False), ("It", False)]},
            {"text": "(The cute girl) . . .. is the youngest student.", "order": 6, "choices": [("She", True), ("He", False), ("They", False), ("It", False)]},
            {"text": "My mother has a car. ........ is a Lacetti.", "order": 7, "choices": [("It", True), ("He", False), ("She", False), ("They", False)]},
            {"text": "(The city - Delhi) . . .. is the capital city of India.", "order": 8, "choices": [("It", True), ("He", False), ("She", False), ("They", False)]},
            {"text": "At ten we go _____ bed.", "order": 9, "choices": [("to", True), ("in", False), ("at", False), ("on", False)]},
            {"text": "He picks up the apples _____ the tree.", "order": 10, "choices": [("from", True), ("of", False), ("in", False), ("at", False)]},
            {"text": "She lives _____ Switzerland.", "order": 11, "choices": [("in", True), ("at", False), ("on", False), ("from", False)]},
            {"text": "There's a letter _____ you.", "order": 12, "choices": [("for", True), ("to", False), ("at", False), ("from", False)]},
            {"text": "Tourists come _____ the boat.", "order": 13, "choices": [("by", True), ("in", False), ("on", False), ("from", False)]},
            {"text": "He speaks to people _____ the radio.", "order": 14, "choices": [("on", True), ("by", False), ("in", False), ("at", False)]},
            {"text": "The books are ___ the table.", "order": 15, "choices": [("on", True), ("in", False), ("at", False), ("under", False)]},
            {"text": "The cat is ___ the chair.", "order": 16, "choices": [("on", True), ("in", False), ("at", False), ("under", False)]},
            {"text": "The picture is ___ the wall.", "order": 17, "choices": [("on", True), ("in", False), ("at", False), ("under", False)]},
            {"text": "The keys are ___ my bag.", "order": 18, "choices": [("in", True), ("on", False), ("at", False), ("under", False)]},
            {"text": "The ball is ___ the box.", "order": 19, "choices": [("in", True), ("on", False), ("at", False), ("under", False)]},
        ],
    },
    {
        "title": "English Test - Variant 6",
        "description": "English language test questions - Variant 6",
        "duration_minutes": 20,
        "questions": [
            {"text": "The lamp is ___ the table.", "order": 0, "choices": [("on", True), ("in", False), ("at", False), ("under", False)]},
            {"text": "There is a garden ___ the house.", "order": 1, "choices": [("behind", True), ("on", False), ("in", False), ("at", False)]},
            {"text": "The shoes are ___ the door.", "order": 2, "choices": [("near", True), ("on", False), ("in", False), ("behind", False)]},
            {"text": "The school is ___ the park.", "order": 3, "choices": [("near", True), ("on", False), ("in", False), ("behind", False)]},
            {"text": "The dog is ___ the sofa.", "order": 4, "choices": [("under", True), ("on", False), ("in", False), ("behind", False)]},
            {"text": "He drives the children _____ school.", "order": 5, "choices": [("to", True), ("at", False), ("in", False), ("from", False)]},
            {"text": "She goes skiing _____ her free time.", "order": 6, "choices": [("in", True), ("at", False), ("on", False), ("during", False)]},
            {"text": "He works _____ an undertaker.", "order": 7, "choices": [("as", True), ("like", False), ("in", False), ("for", False)]},
            {"text": "Does she live in Australia? No, she _____.", "order": 8, "choices": [("doesn't", True), ("don't", False), ("isn't", False), ("aren't", False)]},
            {"text": "We _____ _____ watching television.", "order": 9, "choices": [("don't like", True), ("doesn't like", False), ("aren't like", False), ("isn't like", False)]},
            {"text": "He lives _____ his family.", "order": 10, "choices": [("with", True), ("to", False), ("in", False), ("at", False)]},
            {"text": "We are _____ Uzbekistan.", "order": 11, "choices": [("from", True), ("in", False), ("at", False), ("to", False)]},
            {"text": "Smoking is a _____ habit.", "order": 12, "choices": [("bad", True), ("good", False), ("nice", False), ("great", False)]},
            {"text": "___ your neighbors friendly?", "order": 13, "choices": [("Are", True), ("Is", False), ("Do", False), ("Does", False)]},
            {"text": "___ your neighbor a teacher?", "order": 14, "choices": [("Is", True), ("Are", False), ("Do", False), ("Does", False)]},
            {"text": "Where ___ your neighbors live?", "order": 15, "choices": [("do", True), ("does", False), ("are", False), ("is", False)]},
            {"text": "How ___ your neighbors?", "order": 16, "choices": [("are", True), ("is", False), ("do", False), ("does", False)]},
            {"text": "___ you like your neighbors?", "order": 17, "choices": [("Do", True), ("Does", False), ("Are", False), ("Is", False)]},
            {"text": "They have a ___ dog.", "order": 18, "choices": [("big", True), ("biggest", False), ("bigger", False), ("biger", False)]},
            {"text": "My neighbor has a ___ garden.", "order": 19, "choices": [("beautiful", True), ("beautifull", False), ("beauty", False), ("beautify", False)]},
        ],
    },
    {
        "title": "English Test - Variant 7",
        "description": "English language test questions - Variant 7",
        "duration_minutes": 20,
        "questions": [
            {"text": "I have a ___ car.", "order": 0, "choices": [("new", True), ("news", False), ("newly", False), ("newer", False)]},
            {"text": "Our neighbors live in a ___ house.", "order": 1, "choices": [("big", True), ("biggest", False), ("bigger", False), ("biger", False)]},
            {"text": "She has a ___ cat.", "order": 2, "choices": [("cute", True), ("cutely", False), ("cuter", False), ("cutest", False)]},
            {"text": "The team played _____ and lost the match.", "order": 3, "choices": [("badly", True), ("bad", False), ("worse", False), ("baddly", False)]},
            {"text": "Please listen _____.", "order": 4, "choices": [("carefully", True), ("careful", False), ("careless", False), ("carfully", False)]},
            {"text": "The homework was the _____.", "order": 5, "choices": [("easiest", True), ("easy", False), ("easier", False), ("most easy", False)]},
            {"text": "Peter's very _____ at tennis. He won the game.", "order": 6, "choices": [("good", True), ("well", False), ("best", False), ("better", False)]},
            {"text": "I know the Prime Minister _____.", "order": 7, "choices": [("personally", True), ("personal", False), ("person", False), ("personaly", False)]},
            {"text": "My husband's a _____ cook.", "order": 8, "choices": [("good", True), ("well", False), ("best", False), ("better", False)]},
            {"text": "He is a…. man.", "order": 9, "choices": [("tall", True), ("taller", False), ("tallest", False), ("tally", False)]},
            {"text": "The road is…. It is 400 km.", "order": 10, "choices": [("long", True), ("longer", False), ("longest", False), ("shortly", False)]},
            {"text": "This is a ….girl.", "order": 11, "choices": [("beautiful", True), ("beauty", False), ("beautifully", False), ("beautified", False)]},
            {"text": "In summer we like to drink…. water.", "order": 12, "choices": [("cold", True), ("hot", False), ("colder", False), ("coldly", False)]},
            {"text": "We wear …. clothes in winter.", "order": 13, "choices": [("warm", True), ("cool", False), ("warmer", False), ("warmly", False)]},
            {"text": "I _______ many friends.", "order": 14, "choices": [("have", True), ("has", False), ("am", False), ("is", False)]},
            {"text": "The beggar _______ a stick.", "order": 15, "choices": [("has", True), ("have", False), ("is", False), ("are", False)]},
            {"text": "I _______ no sister.", "order": 16, "choices": [("have", True), ("has", False), ("am", False), ("is", False)]},
            {"text": "My parents _____ a beautiful house.", "order": 17, "choices": [("have", True), ("has", False), ("is", False), ("are", False)]},
            {"text": "My father ___ a new job now.", "order": 18, "choices": [("has", True), ("have", False), ("is", False), ("are", False)]},
            {"text": "My brother ___ a lot of friends now.", "order": 19, "choices": [("has", True), ("have", False), ("is", False), ("are", False)]},
        ],
    },
    {
        "title": "English Test - Variant 8",
        "description": "English language test questions - Variant 8",
        "duration_minutes": 20,
        "questions": [
            {"text": "I ___ a new bike.", "order": 0, "choices": [("have", True), ("has", False), ("am", False), ("is", False)]},
            {"text": "She ___ a cat.", "order": 1, "choices": [("has", True), ("have", False), ("is", False), ("are", False)]},
            {"text": "We ___ two sisters.", "order": 2, "choices": [("have", True), ("has", False), ("is", False), ("are", False)]},
            {"text": "He ___ a big house.", "order": 3, "choices": [("has", True), ("have", False), ("is", False), ("are", False)]},
            {"text": "They ___ a garden.", "order": 4, "choices": [("have", True), ("has", False), ("is", False), ("are", False)]},
            {"text": "This is my bag. ___ bag is red.", "order": 5, "choices": [("My", True), ("His", False), ("Her", False), ("Their", False)]},
            {"text": "He is my friend. ___ name is Tom.", "order": 6, "choices": [("His", True), ("Her", False), ("My", False), ("Their", False)]},
            {"text": "We have a dog. ___ dog is friendly.", "order": 7, "choices": [("Our", True), ("Their", False), ("My", False), ("His", False)]},
            {"text": "She has a pencil. ___ pencil is blue.", "order": 8, "choices": [("Her", True), ("His", False), ("My", False), ("Our", False)]},
            {"text": "I have a brother. ___ brother is tall.", "order": 9, "choices": [("My", True), ("His", False), ("Her", False), ("Our", False)]},
            {"text": "I do not _______ any bad manners.", "order": 10, "choices": [("have", True), ("has", False), ("am", False), ("be", False)]},
            {"text": "My cousin ___ a new girlfriend.", "order": 11, "choices": [("has", True), ("have", False), ("is", False), ("are", False)]},
            {"text": "The pupil ___ an old pencil box.", "order": 12, "choices": [("has", True), ("have", False), ("is", False), ("are", False)]},
            {"text": "You ____ different names.", "order": 13, "choices": [("have", True), ("has", False), ("is", False), ("are", False)]},
            {"text": "Last year, we _______ no difficulty at school.", "order": 14, "choices": [("had", True), ("have", False), ("has", False), ("were", False)]},
            {"text": "He does not _______ any control over his juniors.", "order": 15, "choices": [("have", True), ("has", False), ("had", False), ("be", False)]},
            {"text": "My bicycle too, did not _______ brakes.", "order": 16, "choices": [("have", True), ("has", False), ("had", False), ("be", False)]},
            {"text": "My mother is my ___.", "order": 17, "choices": [("parent", True), ("child", False), ("sibling", False), ("spouse", False)]},
            {"text": "He is my father. I am his ___.", "order": 18, "choices": [("son", True), ("daughter", False), ("child", False), ("sibling", False)]},
            {"text": "This is my sister. She is my ___.", "order": 19, "choices": [("sibling", True), ("parent", False), ("child", False), ("spouse", False)]},
        ],
    },
    {
        "title": "English Test - Variant 9",
        "description": "English language test questions - Variant 9",
        "duration_minutes": 20,
        "questions": [
            {"text": "I am their ___.", "order": 0, "choices": [("child", True), ("parent", False), ("sibling", False), ("spouse", False)]},
            {"text": "My uncle is my father's ___.", "order": 1, "choices": [("brother", True), ("son", False), ("cousin", False), ("nephew", False)]},
            {"text": "My sister is tall. My brother is ___.", "order": 2, "choices": [("short", True), ("tall", False), ("long", False), ("big", False)]},
            {"text": "This book is new. That book is ___.", "order": 3, "choices": [("old", True), ("new", False), ("young", False), ("fresh", False)]},
            {"text": "My house is big. My friend's house is ___.", "order": 4, "choices": [("small", True), ("big", False), ("large", False), ("huge", False)]},
            {"text": "The weather is hot. Yesterday it was ___.", "order": 5, "choices": [("cold", True), ("hot", False), ("warm", False), ("cool", False)]},
            {"text": "The movie was interesting. The book was ___.", "order": 6, "choices": [("boring", True), ("interesting", False), ("exciting", False), ("fun", False)]},
            {"text": "My mother's daughter is my……", "order": 7, "choices": [("sister", True), ("brother", False), ("cousin", False), ("niece", False)]},
            {"text": "My mother's mother is my…….", "order": 8, "choices": [("grandmother", True), ("aunt", False), ("cousin", False), ("mother", False)]},
            {"text": "My father's son is my…….", "order": 9, "choices": [("brother", True), ("sister", False), ("cousin", False), ("nephew", False)]},
            {"text": "My step-mother's son is my……", "order": 10, "choices": [("step-brother", True), ("brother", False), ("cousin", False), ("half-brother", False)]},
            {"text": "My brother's daughter is my……", "order": 11, "choices": [("niece", True), ("nephew", False), ("cousin", False), ("sister", False)]},
            {"text": "My grandpa's father is my…..", "order": 12, "choices": [("great-grandfather", True), ("grandfather", False), ("great-uncle", False), ("grand-uncle", False)]},
            {"text": "My dad's brother is my….", "order": 13, "choices": [("uncle", True), ("cousin", False), ("nephew", False), ("brother", False)]},
            {"text": "My female spouse is my….", "order": 14, "choices": [("wife", True), ("husband", False), ("partner", False), ("girlfriend", False)]},
            {"text": "Antonym: leave", "order": 15, "choices": [("arrive", True), ("go", False), ("depart", False), ("exit", False)]},
            {"text": "Antonym: high", "order": 16, "choices": [("low", True), ("tall", False), ("big", False), ("up", False)]},
            {"text": "Antonym: brave", "order": 17, "choices": [("cowardly", True), ("fearless", False), ("bold", False), ("daring", False)]},
            {"text": "Antonym: Ill", "order": 18, "choices": [("healthy", True), ("sick", False), ("unwell", False), ("tired", False)]},
            {"text": "My grandparents ____________ in Italy.", "order": 19, "choices": [("live", True), ("lives", False), ("living", False), ("lived", False)]},
        ],
    },
    {
        "title": "English Test - Variant 10",
        "description": "English language test questions - Variant 10",
        "duration_minutes": 20,
        "questions": [
            {"text": "We _____________ films on TV every day.", "order": 0, "choices": [("watch", True), ("watches", False), ("watching", False), ("watched", False)]},
            {"text": "Kate and Peter ___________ to the same college.", "order": 1, "choices": [("go", True), ("goes", False), ("going", False), ("went", False)]},
            {"text": "What ________ you ______ at noon?", "order": 2, "choices": [("do / do", True), ("does / does", False), ("are / doing", False), ("did / do", False)]},
            {"text": "To be / they / teachers →", "order": 3, "choices": [("They are teachers", True), ("They is teachers", False), ("They be teachers", False), ("They were teachers", False)]},
            {"text": "she / to be / nurse / a →", "order": 4, "choices": [("She is a nurse", True), ("She are a nurse", False), ("She be a nurse", False), ("She was a nurse", False)]},
            {"text": "My favorite color ___ blue.", "order": 5, "choices": [("is", True), ("am", False), ("are", False), ("be", False)]},
            {"text": "I have ___ brother and sister.", "order": 6, "choices": [("a", True), ("an", False), ("the", False), ("some", False)]},
            {"text": "I go to school ___ bus.", "order": 7, "choices": [("by", True), ("on", False), ("in", False), ("with", False)]},
            {"text": "It ___ raining now.", "order": 8, "choices": [("is", True), ("am", False), ("are", False), ("be", False)]},
            {"text": "The weather ___ cold in winter.", "order": 9, "choices": [("is", True), ("am", False), ("are", False), ("be", False)]},
            {"text": "It ___ windy outside.", "order": 10, "choices": [("is", True), ("am", False), ("are", False), ("be", False)]},
            {"text": "I like it when it ___ warm.", "order": 11, "choices": [("is", True), ("am", False), ("are", False), ("be", False)]},
            {"text": "It ___ cloudy in the morning.", "order": 12, "choices": [("was", True), ("is", False), ("am", False), ("were", False)]},
            {"text": "In summer, it usually ___ hot.", "order": 13, "choices": [("is", True), ("am", False), ("are", False), ("be", False)]},
            {"text": "Sometimes it ___ snow in December.", "order": 14, "choices": [("does", True), ("do", False), ("is", False), ("are", False)]},
            {"text": "Last summer I ___ to Paris.", "order": 15, "choices": [("went", True), ("go", False), ("goes", False), ("gone", False)]},
            {"text": "I ______ playing computer games in my free time.", "order": 16, "choices": [("like", True), ("likes", False), ("liking", False), ("liked", False)]},
            {"text": "I ______ winter.", "order": 17, "choices": [("like", True), ("likes", False), ("liking", False), ("liked", False)]},
            {"text": "Her daughters don't _______ to school.", "order": 18, "choices": [("go", True), ("goes", False), ("going", False), ("gone", False)]},
            {"text": "My father _____ an honest man. He _______ lies.", "order": 19, "choices": [("is / never tells", True), ("is / always tells", False), ("are / never tells", False), ("is / never tell", False)]},
        ],
    },
    {
        "title": "English Test - Variant 11",
        "description": "English language test questions - Variant 11",
        "duration_minutes": 20,
        "questions": [
            {"text": "What _____ your mother _____? — She is a doctor.", "order": 0, "choices": [("does / do", True), ("do / do", False), ("does / does", False), ("is / do", False)]},
            {"text": "We … our teacher a question about the test.", "order": 1, "choices": [("asked", True), ("ask", False), ("asks", False), ("asking", False)]},
            {"text": "Last summer I ___ to Paris.", "order": 2, "choices": [("went", True), ("go", False), ("goes", False), ("gone", False)]},
            {"text": "She ___ a beautiful city last year.", "order": 3, "choices": [("visited", True), ("visit", False), ("visits", False), ("visiting", False)]},
            {"text": "We ___ a museum yesterday.", "order": 4, "choices": [("visited", True), ("visit", False), ("visits", False), ("visiting", False)]},
            {"text": "They ___ their grandparents last weekend.", "order": 5, "choices": [("visited", True), ("visit", False), ("visits", False), ("visiting", False)]},
            {"text": "I ___ many photos during my trip.", "order": 6, "choices": [("took", True), ("take", False), ("takes", False), ("taking", False)]},
            {"text": "I ___ my homework yesterday.", "order": 7, "choices": [("did", True), ("do", False), ("does", False), ("doing", False)]},
            {"text": "She ___ a letter to her friend last night.", "order": 8, "choices": [("wrote", True), ("write", False), ("writes", False), ("writing", False)]},
            {"text": "We ___ in the park last Sunday.", "order": 9, "choices": [("played", True), ("play", False), ("plays", False), ("playing", False)]},
            {"text": "They ___ a cake for the party.", "order": 10, "choices": [("made", True), ("make", False), ("makes", False), ("making", False)]},
            {"text": "He ___ to music in the evening.", "order": 11, "choices": [("listened", True), ("listen", False), ("listens", False), ("listening", False)]},
            {"text": "Gulnoza ..… go to work yesterday but she was sick.", "order": 12, "choices": [("didn't", True), ("don't", False), ("doesn't", False), ("wasn't", False)]},
            {"text": "They … to the park because they were very tired.", "order": 13, "choices": [("didn't go", True), ("don't go", False), ("doesn't go", False), ("not went", False)]},
            {"text": "Did you talk to your boss? — Yes, I ….", "order": 14, "choices": [("did", True), ("do", False), ("does", False), ("was", False)]},
            {"text": "I … twenty minutes for the bus yesterday.", "order": 15, "choices": [("waited", True), ("wait", False), ("waits", False), ("waiting", False)]},
            {"text": "… they fix their bicycles? — Yes, they ….", "order": 16, "choices": [("Did / did", True), ("Do / do", False), ("Does / does", False), ("Were / were", False)]},
            {"text": "Where … you go to school when you were young?", "order": 17, "choices": [("did", True), ("do", False), ("does", False), ("were", False)]},
            {"text": "We … go camping in a park when we were children.", "order": 18, "choices": [("used to", True), ("use to", False), ("uses to", False), ("using to", False)]},
            {"text": "I … dinner last night, so I couldn't watch TV.", "order": 19, "choices": [("cooked", True), ("cook", False), ("cooks", False), ("cooking", False)]},
        ],
    },
    {
        "title": "English Test - Variant 12",
        "description": "English language test questions - Variant 12",
        "duration_minutes": 20,
        "questions": [
            {"text": "Did you … the book? — No, I ….", "order": 0, "choices": [("read / didn't", True), ("read / don't", False), ("read / doesn't", False), ("reads / didn't", False)]},
            {"text": "Why … you wash the dirty dishes last week?", "order": 1, "choices": [("didn't", True), ("don't", False), ("doesn't", False), ("weren't", False)]},
            {"text": "My friend Munisa … see a dentist yesterday.", "order": 2, "choices": [("had to", True), ("has to", False), ("have to", False), ("must", False)]},
            {"text": "I … at work very late last night.", "order": 3, "choices": [("was", True), ("is", False), ("am", False), ("were", False)]},
            {"text": "Zuhra … for help when he fell in the water.", "order": 4, "choices": [("called", True), ("call", False), ("calls", False), ("calling", False)]},
            {"text": "She didn't answer because she … hear it ring.", "order": 5, "choices": [("couldn't", True), ("can't", False), ("wasn't", False), ("didn't", False)]},
            {"text": "I ... tennis yesterday because I don't know how.", "order": 6, "choices": [("didn't play", True), ("don't play", False), ("doesn't play", False), ("wasn't playing", False)]},
            {"text": "Mozart ___________ more than 600 pieces of music.", "order": 7, "choices": [("wrote", True), ("write", False), ("writes", False), ("writing", False)]},
            {"text": "We _______ our classmate in town a few days ago.", "order": 8, "choices": [("saw", True), ("see", False), ("sees", False), ("seeing", False)]},
            {"text": "It was cold, so I _____________ the window.", "order": 9, "choices": [("closed", True), ("close", False), ("closes", False), ("closing", False)]},
            {"text": "I ___________ to the cinema three times last week.", "order": 10, "choices": [("went", True), ("go", False), ("goes", False), ("going", False)]},
            {"text": "Which sentence is in the past simple tense?", "order": 11, "choices": [("I played football yesterday", True), ("I play football", False), ("I am playing football", False), ("I will play football", False)]},
            {"text": "How do you form the past simple of regular verbs?", "order": 12, "choices": [("add -ed", True), ("add -ing", False), ("add -s", False), ("add -er", False)]},
            {"text": "The correct past simple form of go?", "order": 13, "choices": [("went", True), ("goed", False), ("gone", False), ("going", False)]},
            {"text": "Negative sentence in past simple?", "order": 14, "choices": [("I didn't go", True), ("I don't go", False), ("I not go", False), ("I wasn't go", False)]},
            {"text": "Past simple form of eat?", "order": 15, "choices": [("ate", True), ("eated", False), ("eaten", False), ("eating", False)]},
            {"text": "Question in the past simple tense?", "order": 16, "choices": [("Did you see that?", True), ("Do you see that?", False), ("Are you seeing that?", False), ("Have you seen that?", False)]},
            {"text": "Dilobar _____ when she _____ the DVDs.", "order": 17, "choices": [("was shopping / found", True), ("shopped / found", False), ("was shopping / was finding", False), ("shopped / was finding", False)]},
            {"text": "While Aziz _____ a documentary, he _____ asleep.", "order": 18, "choices": [("was watching / fell", True), ("watched / fell", False), ("was watching / was falling", False), ("watched / was falling", False)]},
            {"text": "They _____ when you _____ for remote control.", "order": 19, "choices": [("were sleeping / looked", True), ("slept / looked", False), ("were sleeping / were looking", False), ("slept / were looking", False)]},
        ],
    },
    {
        "title": "English Test - Variant 13",
        "description": "English language test questions - Variant 13",
        "duration_minutes": 15,
        "questions": [
            {"text": "What ________? — I was watching TV.", "order": 0, "choices": [("were you doing", True), ("are you doing", False), ("did you do", False), ("do you do", False)]},
            {"text": "My mother was cooking dinner at 8 p.m. ___.", "order": 1, "choices": [("yesterday", True), ("tomorrow", False), ("today", False), ("now", False)]},
            {"text": "My son ..... ..... television when the lights went out.", "order": 2, "choices": [("was watching", True), ("watched", False), ("is watching", False), ("watches", False)]},
            {"text": "What _____ you _____ when it started hailing?", "order": 3, "choices": [("were / doing", True), ("are / doing", False), ("did / do", False), ("was / doing", False)]},
            {"text": "While the soup was boiling, my brother .... .... sweets.", "order": 4, "choices": [("was eating", True), ("ate", False), ("is eating", False), ("eats", False)]},
            {"text": "Our enemies _____ me when I was lost in the forest.", "order": 5, "choices": [("were following", True), ("followed", False), ("are following", False), ("follow", False)]},
            {"text": "Sardor _____ off the ladder while he _____ the ceiling.", "order": 6, "choices": [("fell / was painting", True), ("was falling / painted", False), ("fell / painted", False), ("was falling / was painting", False)]},
            {"text": "I _____ grammar when I _____ asleep.", "order": 7, "choices": [("was studying / fell", True), ("studied / fell", False), ("was studying / was falling", False), ("studied / was falling", False)]},
            {"text": "The scientists _____ in their lab when they _____ the new drug.", "order": 8, "choices": [("were working / discovered", True), ("worked / discovered", False), ("were working / were discovering", False), ("worked / were discovering", False)]},
            {"text": "My brother _____ on the phone when I ________.", "order": 9, "choices": [("was talking / arrived", True), ("talked / arrived", False), ("was talking / was arriving", False), ("talked / was arriving", False)]},
        ],
    },
]


@router.post("/seed-english", tags=["seed"])
async def seed_english(db: AsyncSession = Depends(get_db)):
    # Find Asliddin's user ID
    result = await db.execute(select(User).where(User.username == "Asliddin"))
    asliddin = result.scalar_one_or_none()
    if not asliddin:
        raise HTTPException(status_code=404, detail="User 'Asliddin' not found. Run /seed first.")

    # Skip variants already present (idempotent)
    existing = await db.execute(
        select(Quiz.title).where(Quiz.title.like("English Test - Variant %"))
    )
    existing_titles = {row[0] for row in existing.fetchall()}

    created, skipped = [], []

    for quiz_data in ENGLISH_QUIZZES:
        if quiz_data["title"] in existing_titles:
            skipped.append(quiz_data["title"])
            continue

        quiz = Quiz(
            title=quiz_data["title"],
            description=quiz_data["description"],
            duration_minutes=quiz_data["duration_minutes"],
            created_by=asliddin.id,
        )
        db.add(quiz)
        await db.flush()

        for q in quiz_data["questions"]:
            question = Question(quiz_id=quiz.id, text=q["text"], order=q["order"])
            db.add(question)
            await db.flush()
            for text, is_correct in q["choices"]:
                db.add(Choice(question_id=question.id, text=text, is_correct=is_correct))

        created.append(quiz_data["title"])

    await db.commit()

    total_questions = sum(
        len(q["questions"])
        for q in ENGLISH_QUIZZES
        if q["title"] in set(created)
    )

    return {
        "created": len(created),
        "skipped_already_exist": len(skipped),
        "total_questions_added": total_questions,
        "variants": created,
    }
